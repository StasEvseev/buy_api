#coding: utf-8
from collections import namedtuple
from models import db
from models.good import Good
from services import PriceService


GoodStub = namedtuple('GoodStub', ['id_price', 'id_commodity', 'full_name', 'count', 'barcode'])

class GoodServiceException(Exception):
    pass

class GoodNotPriceException(GoodServiceException):
    pass

class GoodNotFountException(GoodServiceException):
    pass

class GoodService(object):

    @classmethod
    def get_good(cls, id):
        good = Good.query.get(id)
        if not good:
            raise GoodNotFountException(u"Не найдено записи в БД")
        return good

    @classmethod
    def get_price(cls, good_id):
        from services.priceserv import PriceService
        good = cls.get_good(good_id)
        return PriceService.get_price(good.price_id)

    @classmethod
    def update_good(cls, id, count, barcode):
        good = cls.get_good(id)
        good.barcode = barcode

        if good.count:
            good.count = count
            good.is_confirm = True

        db.session.add(good)

        db.session.commit()


        # return
        # pass

    # @classmethod
    # def save_items(self, items):
    #     goods = [
    #         GoodStub(id_price=it['id_price'], id_commodity=it['id_commodity'], full_name=it['full_name'],
    #                  price_retail=it['id_price'], price_gross=it['id_price'], count=it['id_price'])
    #         for it in items
    #     ]
    #
    #     for it in goods:
    #         #Проверяем проставлена ли цена розницу.
    #         if not PriceService.get_price(it.id_price):
    #             raise GoodNotPriceException(
    #                 u"У товара должна быть указана розничная цена. %s" % it.full_name)
    #
    #         # retailitem_q = RetailInvoiceItem.query.filter(
    #         #     RetailInvoiceItem.retailinvoice==retail,
    #         #     RetailInvoiceItem.commodity_id==it.id_commodity)
    #         #
    #         # if retailitem_q.count() > 0:
    #         #     retail_item = retailitem_q.one()
    #         #     raise RetailDuplicateItemsException(
    #         #         u"В накладной не может быть двух одинаковых позиций. %s" % retail_item.full_name)
    #
    #         good_item = Good(
    #             full_name=it.full_name, price_id=it.id_price, commodity_id=it.id_commodity, count=it.count,
    #             barcode=it.barcode)
    #         db.session.add(good_item)
    #
    #     return goods
    #     # RetailStub = namedtuple('RetailStub', ['id_price', 'id_commodity', 'full_name', 'price_retail', 'count'])
    #     # pass
    #
    # # @classmethod
    # # def build_retail_items(cls, items):
    # #     return [RetailStub(id_price=it['id_price'], id_commodity=it['id_commodity'],
    # #                        full_name=it['full_name'], price_retail='', count='') for it in items]
    # #
    # # pass