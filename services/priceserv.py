#coding: utf-8
from collections import namedtuple
from log import debug, error
from models import db
from models.price import Price, PriceParish

from services import CommodityService

from sqlalchemy import desc, and_
from sqlalchemy.orm.exc import NoResultFound


PriceStub = namedtuple('PriceStub', ['id', 'id_commodity', 'full_name', 'number_local', 'number_global', 'NDS',
                                     'id_good',
                                     'price_prev',
                                     'price_post', 'price_retail', 'price_gross', 'is_change',
                                     'price_retail_recommendation', 'price_gross_recommendation'])

# Данные для обновления цены
#   params:
#       id_commodity - id номенклатурный
#       price_retail - цена розницы
#       price_gross - цена опта
#       prive_prev - цена без НДС
#       price_post - цена с НДС
#       NDS - размер НДС
#       number_local - номер локальный(в пределах года)
#       number_global - номер глобальный(в пределах всего выпуска издания)
#       date - дата, с которой действует цена
#
DataToUpdatePrice = namedtuple('DataToUpdatePrice', ['id_commodity', 'price_retail', 'price_gross', 'price_prev',
                                                     'price_post', 'NDS', 'number_local', 'number_global', 'invoice'])


class PriceServiceException(Exception):
    """
    Базовый класс исключений для сервисного слоя цен.
    """
    pass
    # def __init__(self, message, code=None):
    #     self.code = code
    #     self.message = message


class NotPriceException(PriceServiceException):
    """
    Исключение о том, что отсутсвует цена на розницу и опт
    """
    pass


class NotFindPriceExc(PriceServiceException):
    """
    Ислючение говорящее о том, что цена в системе не найдена
    """
    pass


class NotFindPriceParishExc(PriceServiceException):
    """
    Иключение о том, что не найдена PriceParish с указанной ценой с НДС.
    """
    pass


class PriceArgumentExc(PriceServiceException):
    pass


class PriceService(object):
    """
    Сервисный слой цен.
    """

    RATE_RETAIL = 1.6
    RATE_GROSS = 1.4

    RANGE_PRICE = 1.15

    @classmethod
    def price_retail(cls, price_post):
        return price_post * cls.RATE_RETAIL

    @classmethod
    def price_gross(cls, price_post):
        return price_post * cls.RATE_GROSS

    @classmethod
    def get_price(cls, id):
        """
        Получим модель цены.
        """
        return Price.query.filter(Price.id==id).one()

    @classmethod
    def get_all(cls):
        """
        Получим все цены в системе.
        """
        return Price.query.all()

    @classmethod
    def prices_parish_to_commodity_price(cls, commodity_model, price_post):
        """
        Выбираем цены прихода под критерий:
        "Цена с НДС" варьируется в пределах 10% вверх и вниз.
        """
        return PriceParish.query.filter(
            PriceParish.commodity_id==commodity_model.id,
            and_(PriceParish.price_post>=price_post / cls.RANGE_PRICE,
                PriceParish.price_post<=price_post * cls.RANGE_PRICE)
        )

    @classmethod
    def create_or_update_prices(cls, invoice_model, data_items):
        """
        Создаем или изменяем цены позиций переданной накладной.
        """
        invoice_id = invoice_model.id
        debug("Начало сохранения цен в позициях накладной %d", invoice_id)
        from services import GoodService
        try:
            for data in data_items:
                commodity_id = int(data['id_commodity'])
                price_retail = float(data['price_retail']) if data['price_retail'] else None
                price_gross = float(data['price_gross']) if data['price_gross'] else None
                NDS = float(data['NDS'])
                price_prev = float(data['price_prev'])
                price_post = float(data['price_post'])
                good = GoodService.get_good(data['id_good'])
                number_local = data['number_local']
                number_global = data['number_global']

                cls.create_or_update(good, DataToUpdatePrice(
                    id_commodity=commodity_id, price_retail=price_retail, price_gross=price_gross, price_prev=price_prev,
                    price_post=price_post, NDS=NDS, number_local=number_local, number_global=number_global,
                    invoice=invoice_model))
        except Exception as err:
            error("Ошибка сохранения цен в позициях накладной %d. %s", invoice_id, unicode(err))
            db.session.rollback()
            raise PriceServiceException(err)
        else:
            db.session.commit()
        debug("Конец сохранения цен в позициях накладной %d", invoice_id)

    @classmethod
    def get_priceparish(cls, commodity_id, number_local=None, number_global=None, date=None):
        """
        Получаем цену по номенклатуре, номерам и дате.
        """
        commodity = CommodityService.get_by_id(commodity_id)
        if commodity.numeric:
            #ОБРАБОТКА НОМЕРНОЙ НОМЕНКЛАТУРЫ
            if not number_local and not number_global:
                raise PriceArgumentExc(u"Для номерной номенклатуры нужно указать общий год и номер в пределах года")

            priceparish = PriceParish.query.filter(
                PriceParish.commodity_id==commodity_id,
                PriceParish.number_local_from<=number_local,
                PriceParish.number_global_from<=number_global
            ).order_by(desc(PriceParish.number_local_from),
                       desc(PriceParish.number_global_from))
            count = priceparish.count()

            if count == 0:
                raise NotFindPriceParishExc(u"Не найдено цен для номенклатуры %s и номеров %s и %s" % (
                    commodity.name, number_local, number_global))

            return  priceparish
        else:
            #ОБРАБОТКА БЕЗНОМЕРНОЙ НОМЕНКЛАТУРЫ
            if number_local or number_global:
                raise PriceArgumentExc(u"Для безномерной номенклатуры номера должны быть пустыми.")
            priceparish = PriceParish.query.filter(
                PriceParish.commodity_id==commodity_id
            ).order_by(desc(PriceParish.date_from))
            if date:
                priceparish = priceparish.filter(PriceParish.date_from<=date)
            count = priceparish.count()
            if count == 0:
                raise NotFindPriceParishExc(u"Не найдено цен для номенклатуры %s" % commodity.name)
            else:
                return priceparish

    @classmethod
    def get_price_priceparish(cls, commodity_id, price_post, number_local=None, number_global=None, date=None):
        """
        Ищем цену и цену прихода по номенклатуре, цене с НДС, номерам и дате.

        Генерирует NotFindPriceExc, PriceArgumentExc, NotFindPriceParishExc.
        """
        try:
            priceparish = cls.get_priceparish(commodity_id, number_local, number_global, date)
        except NotFindPriceParishExc as exc:
            """
            Если сработало исключение, то и цены значит нет на данный товар. Поэтому генерируем соответствующее исключение.
            """
            raise NotFindPriceExc(unicode(exc))
        commodity = CommodityService.get_by_id(commodity_id)
        try:
            priceparish = priceparish.filter(
                PriceParish.price_post==price_post).one()
        except NoResultFound:
            raise NotFindPriceParishExc(u"Не найдено цены прихода для товара %s и ценой %s" % (
                commodity.name, price_post))
        return priceparish.price, priceparish

    @classmethod
    def get_final_price_to_commodity_numbers_date(cls, commodity_id, price_retail, price_gross, number_local=None,
                                                  number_global=None, date=None):
        priceparish = cls.get_priceparish(commodity_id, number_local, number_global, date)

        priceparish = priceparish.join(Price).filter(
            Price.price_retail==price_retail, Price.price_gross==price_gross)

        if priceparish.count() > 0:
            return priceparish.first().price
        return None

    @classmethod
    def has_final_price_to_commodity_numbers_date(cls, commodity_id, price_retail, price_gross, number_local=None,
                                                  number_global=None, date=None):
        res = cls.get_final_price_to_commodity_numbers_date(commodity_id, price_retail, price_gross, number_local,
                                                      number_global, date)
        # priceparish = cls.priceparish_commodity_numbers_date(commodity_id, number_local, number_global, date)
        #
        # priceparish = priceparish.join(Price).filter(
        #     Price.price_retail==price_retail, Price.price_gross==price_gross)
        #
        # if priceparish.count() > 0:
        if res:
            return True
        return False

    @classmethod
    def create_or_update(cls, good_model, data):
        """
        Создаем либо обновляем цену в товаре.

        Для начала нам нужно найти цену в системе по номенклатуре и цене с НДС(по сути из цены с НДС и складывается
        конечная стоимость продажи).

        Есть момент, что цен прихода может быть несколько. А вот цена продажи у них все равно единая.

        В случае отсутствия цены по условию выше, создаем новую цену со всеми переданными параметрами.

        Если находим, то корректируем у цены НДС, цены розницы и опта и дату действия цены.

        :argument good_model - инстанс Good
        :argument data - инстанс DataToUpdatePrice.

        :return инстанс Price

        """
        invoice = data.invoice
        if not data.price_retail and not data.price_gross:
            raise PriceArgumentExc(u"Нету розничной и оптовой цены")
        try:
            price, _ = cls.get_price_priceparish(
                commodity_id=data.id_commodity, price_post=data.price_post, number_local=data.number_local,
                number_global=data.number_global, date=invoice.date)
        except NotFindPriceExc:
            """
            Если не найдено цен вообще на номенклатуру, то создаем и цену прихода, и цену продажи.
            """
            price = Price(price_retail=data.price_retail, price_gross=data.price_gross)
            priceparish = PriceParish(commodity_id=data.id_commodity, number_local_from=data.number_local,
                                      number_global_from=data.number_global, NDS=data.NDS, price_prev=data.price_prev,
                                      price_post=data.price_post, date_from=invoice.date)
            priceparish.invoice = invoice
            priceparish.price = price
            db.session.add(price)
            db.session.add(priceparish)
            good_model.price = price
            db.session.add(good_model)

        except NotFindPriceParishExc as exc:
            """
            Если не найдена цена прихода с "ценой с НДС", надо найти в системе, есть ли цены продажи с указанными
            розничными и оптовыми ценами, и если такое есть, надо добавить новую цену прихода
            """
            price = cls.get_final_price_to_commodity_numbers_date(
                data.id_commodity, data.price_retail, data.price_gross, data.number_local, data.number_global,
                invoice.date)

            if not price:
                price = Price(price_retail=data.price_retail, price_gross=data.price_gross)
                db.session.add(price)

            priceparish = PriceParish(
                commodity_id=data.id_commodity, number_local_from=data.number_local,
                number_global_from=data.number_global, NDS=data.NDS, price_prev=data.price_prev,
                price_post=data.price_post, date_from=invoice.date)
            priceparish.invoice = invoice
            priceparish.price = price
            db.session.add(priceparish)
            good_model.price = price
            db.session.add(good_model)
        else:
            """
            иначе нашли цену и изменим ее
            """
            good_model.price = price
            price.price_retail = data.price_retail
            price.price_gross = data.price_gross

            db.session.add(good_model)
            db.session.add(price)
        return price

    @classmethod
    def get_price_invoiceitem(cls, item):
        """
        Ищет цену для позиции накладной.
        """
        commodity = item.good.commodity

        try:
            price, _ = cls.get_price_priceparish(
                commodity.id, item.price_with_NDS, item.number_local, item.number_global, item.invoice.date)

        except NotFindPriceParishExc as exc:
            return PriceStub(
                id='',
                id_good='',
                id_commodity=commodity.id,
                full_name='',
                number_local='',
                number_global='',
                NDS='',
                price_prev='',
                price_post='',
                price_retail='',
                price_gross='',
                price_retail_recommendation='',
                price_gross_recommendation='',
                is_change=True
            )

        except PriceServiceException:
            return PriceStub(
                id='',
                id_good='',
                id_commodity=commodity.id,
                full_name='',
                number_local='',
                number_global='',
                NDS='',
                price_prev='',
                price_post='',
                price_retail='',
                price_gross='',
                price_retail_recommendation='',
                price_gross_recommendation='',
                is_change=False
            )
        else:
            price.is_change = False
            return price

    @classmethod
    def generate_price_stub_item(cls, invoiceitem):
        """
        Выдераем все данные из позиции накладной,
        чтобы выдать рекомендации по ценам, изменяемость цен.
        """
        commodity = CommodityService.get_commodity(invoiceitem.name)
        price = PriceService.get_price_invoiceitem(invoiceitem)

        pricestub = PriceStub(
            id='',
            id_commodity=commodity.id,
            id_good=invoiceitem.good_id,
            full_name=invoiceitem.full_name,
            number_local=invoiceitem.number_local,
            number_global=invoiceitem.number_global,
            NDS=invoiceitem.rate_NDS,
            price_prev=invoiceitem.price_without_NDS,
            price_post=invoiceitem.price_with_NDS,
            price_retail=price.price_retail or '',
            price_gross=price.price_gross or '',
            price_retail_recommendation=cls.price_retail(float(invoiceitem.price_with_NDS)),
            price_gross_recommendation=cls.price_gross(float(invoiceitem.price_with_NDS)),
            is_change=price.is_change)
        return pricestub

    @classmethod
    def generate_price_stub(cls, invoiceitems):
        """
        По продуктам и накладной формируем цены.
        """
        res = []
        for invoiceitem in invoiceitems:
            pricestub = cls.generate_price_stub_item(invoiceitem)
            res.append(pricestub)
        return res

    #TODO deprecated
    @classmethod
    def get_price_to_commodity(cls, id_commodity, date_from=None):
        """
        Получаем цену по номенклатуре.

        Если передана дата, то используем ее для поиска промежуточных цен.
        """
        if date_from:

            price_query = Price.query.filter(
                and_(
                    Price.commodity_id == id_commodity,
                    Price.date_from <= date_from
                )
            )
        else:
            price_query = Price.query.filter(
                Price.commodity_id==id_commodity,
            )
        price = price_query.order_by(desc(Price.date_from)).first()
        if price is None:
            price = PriceStub(
            id='',
            id_good='',
            id_commodity=id_commodity,
            full_name='',
            number_local='',
            number_global='',
            NDS='',
            price_prev='',
            price_post='',
            price_retail='',
            price_gross='',
            price_retail_recommendation='',
            price_gross_recommendation='',
            is_change=''
        )
        return price

    #TODO deprecated
    @classmethod
    def price_commodity_numbers(cls, commodity_id, number_local=None, number_global=None):
        commodity = CommodityService.get_by_id(commodity_id)
        if commodity.numeric:
            if not number_local and not number_global:
                raise PriceArgumentExc(u"Для номерной номенклатуры нужно указать общий год и номер в пределах года")

            price = Price.query.filter(
                Price.commodity_id==commodity_id,
                Price.number_local<=number_local,
                Price.number_global<=number_global,
            ).order_by(desc(Price.number_local), desc(Price.number_global)).first()
            if price is None:
                raise NotFindPriceExc(u"Не найдена цена для номенклатуры %s и номеров %s и %s" % (commodity.name, number_local, number_global))
            return price
        else:
            try:
                price = Price.query.filter(
                    Price.commodity_id==commodity_id
                ).one()
            except NoResultFound:
                raise NotFindPriceExc(u"Не найдена цена для номенклатуры %s" % commodity.name)
            else:
                return price

    #TODO deprecated
    @classmethod
    def price_to_commodity_pricepost_numbers(cls, commodity_id, pricepost, number_local=None, number_global=None):

        price = cls.price_commodity_numbers(commodity_id, number_local, number_global)

        if float(price.price_post) == float(pricepost):
            return price
        else:
            commodity = CommodityService.get_by_id(commodity_id)
            raise NotFindPriceExc(u"Не найдена цена для номенклатуры %s и цены с НДС %s" % (commodity.name, pricepost))

        # commodity = CommodityService.get_by_id(commodity_id)
        # if commodity.numeric:
        #     if not number_local and not number_global:
        #         raise PriceArgumentExc(u"Для номерной номенклатуры нужно указать общий год и номер в пределах года")
        #
        #     price = Price.query.filter(
        #         Price.commodity_id==commodity_id,
        #         Price.number_local<=number_local,
        #         Price.number_global<=number_global,
        #     ).order_by(desc(Price.number_local, Price.number_global)).first()
        #     if price is None:
        #         raise NotFindPriceExc(u"Не найдена цена для номенклатуры %s и номеров %s и %s" % (commodity.name, number_local, number_global))
        #
        # else:
        #
        #     pass
        # pass

    #TODO deprecated
    @classmethod
    def get_price_to_commodity_and_price_post(cls, commodity_id, price_post):
        """
        Находим цену в системе по номенклатуре и цене с НДС(по сути из цены с НДС и складывается
        конечная стоимость продажи).
        """
        try:
            price = Price.query.filter(
                Price.commodity_id==commodity_id,
                Price.price_post==price_post).one()
        except NoResultFound as err:
            raise NotFindPriceExc(u"Не найдена цена для номенклатуры %s и цены с НДС %s" % (commodity_id, price_post))
        return price