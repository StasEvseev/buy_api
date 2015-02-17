#coding: utf-8
from collections import namedtuple
import os
from sqlalchemy import asc, desc
from excel.output import PrintInvoice, PATH_TEMPLATE
from models import db
from models.waybill import WayBill, TYPE, RETAIL
from models.waybillitem import WayBillItems
from services import ModelService


WayBillItem = namedtuple('WayBillItem', ['good_id', 'count', 'fullname', 'is_approve'])

class WayBillServiceException(Exception):
    pass


class WayBillService(object):

    @classmethod
    def check_exists(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Проверяем есть ли уже сформированная итоговая накладная по приходной определенной точке или получателю.
        """
        count = 0
        if invoice_id:
            count = cls.count_exists(invoice_id, receiver_id, pointsale_id, type)
        return True if count else False

    @classmethod
    def get_by_id(cls, id):
        return WayBill.query.get(id)

    @classmethod
    def get_items(cls, id):
        return cls.get_by_id(id).items

    #TODO deprecated
    @classmethod
    def get_by_attr(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Извлекаем накладную из БД по приходной, получателю и типу.
        """
        if not receiver_id or not pointsale_id:
            raise WayBillServiceException(u"No receiver or point sale")
        if invoice_id:
            if ModelService.check_id(receiver_id):
                waybill = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).one()
            else:
                waybill = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).one()
            # return count
        else:
            if ModelService.check_id(receiver_id):
                waybill = WayBill.query.filter(
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).one()
            else:
                waybill = WayBill.query.filter(
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).one()
        return waybill

    @classmethod
    def count_exists(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Возвращаем количество накладных по приходной накладной, получателю и типу.
        """

        if not receiver_id or not pointsale_id:
            raise WayBillServiceException(u"No receiver or point sale")

        if invoice_id:
            if ModelService.check_id(receiver_id):
                count = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    # WayBill.date == date,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).count()
            else:
                count = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    # WayBill.date == date,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).count()
            return count
        else:
            if ModelService.check_id(receiver_id):
                count = WayBill.query.filter(
                    # WayBill.date == date,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).count()
            else:
                count = WayBill.query.filter(
                    # WayBill.date == date,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).count()
            return count

    @classmethod
    def generate_number(cls, date, type):
        """
        Генерация номера для накладной.
        Маска - [порядкой номер для дня] - [тип(1,2)] - [дата полная].
        Пример - 001-1-20122014 - означает первая розничная накладная на дату 20 декабря 2014 года.
        """
        waybill = WayBill.query.filter(
            WayBill.date==date).order_by(desc(WayBill.id)).first()
        if waybill is None:
            return "001-" + str(type) + "-" + date.strftime("%d%m%Y")
        else:
            number = waybill.number
            numbers = number.split("-")
            number = int(numbers[0])
            return "-".join(['%03d' % (number + 1), str(type), numbers[2]])

    #TODO изменить сигнатуру метода
    @classmethod
    def create(cls, pointsale_from_id, invoice_id, date, receiver_id, pointsale_id, type, forse=False):
        """
        Создаем или получаем итоговую накладную.
        Сначала проверяем, есть ли уже накладная по параметрам уникальности(приходная накладная, получатели
        (точки или получатель) и тип).
        Если накладной нет, то создаем.
        Если накладная уже есть, генерим исключение. Но если нам передали флаг forse, то извлекаем из БД и возвращаем.
        """
        if not ModelService.check_id(receiver_id) and not ModelService.check_id(pointsale_id):
            raise WayBillServiceException(u"No receiver or point sale")

        if ModelService.check_id(receiver_id) and ModelService.check_id(pointsale_id):
            raise WayBillServiceException(u"Ambiguity: receiver_id OR pointsale_id")

        if pointsale_from_id and ModelService.check_id(pointsale_id) and pointsale_id == pointsale_from_id:
            raise WayBillServiceException(u"Нельзя делать накладную прихода циклической.")

        if type not in TYPE.keys():
            raise WayBillServiceException(u"Value type = %s invalid." % type)

        # check_exist = cls.check_exists(invoice_id, receiver_id, pointsale_id, type)

        # if check_exist:
        #     if forse:
        #         waybill = WayBillService.get_by_attr(invoice_id, receiver_id, pointsale_id, type)
        #     else:
        #         raise WayBillServiceException(u"Invoice has document.")
        # else:
        waybill = WayBill()
        waybill.invoice_id = invoice_id
        waybill.pointsale_from_id = pointsale_from_id
        waybill.date = date
        waybill.receiver_id = receiver_id if receiver_id != -1 else None
        waybill.pointsale_id = pointsale_id if pointsale_id != -1 else None
        waybill.type = type
        waybill.number = cls.generate_number(date, type)
        db.session.add(waybill)
        return waybill

    @classmethod
    def build_retail_items(cls, items):
        """
        Собираем объекты для более удобной обработки из списка словарей.
        """
        return [WayBillItem(good_id=it['good_id'],
                            count=it['count_invoice'] if "count_invoice" in it else None,
                            fullname=it['full_name'] if 'full_name' in it else None,
                            is_approve=it['is_approve'] if 'is_approve' in it else False) for it in items]

    @classmethod
    def upgrade_items(cls, waybill, items, path_target, path):
        from priceserv import PriceService
        from services import GoodService
        from pointsale import PointSaleService

        # for waybl_item in waybill.items:
        #     pointsaleitem = PointSaleService.get_item_to_pointsale_good(
        #         waybill.pointsale_from_id, waybl_item.good_id)
        #     if waybl_item.count:
        #         pointsaleitem.count += waybl_item.count
        #         db.session.add(pointsaleitem)

        waybill.items.delete()
        #
        db.session.add(waybill)

        items = filter(lambda x: x.is_approve, items)

        for it in items:
            good = GoodService.get_good(it.good_id)
            if waybill.type == RETAIL:
                if not good.price_id or not PriceService.get_price(good.price_id).price_retail:
                    raise WayBillServiceException(
                        u"Товар без розничной цены. %s" % good.full_name)
            else:
                if not good.price_id or not PriceService.get_price(good.price_id).price_gross:
                    raise WayBillServiceException(
                        u"Товар без оптовой цены. %s" % good.full_name)

            retail_item = WayBillItems(
                good_id=good.id, waybill=waybill, count=it.count if it.count else None)
            # if it.count:
            #     count = int(it.count)
                # pointsaleitem = PointSaleService.get_item_to_pointsale_good(
                # waybill.pointsale_from_id, good.id)
                # pointsaleitem.count -= count
                # db.session.add(pointsaleitem)
            db.session.add(retail_item)

        pi = PrintInvoice(
            path=os.path.join(PATH_TEMPLATE, 'print_invoice.xls'),
            destination=path_target)
        pi.set_cells(0, 0, ['a', 'b', 'c', 'date'])
        pi.set_cells(0, 2, ['name', 'count', 'price_pay', 'mul'])
        pi.write(0, 0, [{'a': u'', 'b': u'', 'c': u'', 'date': waybill.date.strftime('%d.%m.%Y')}, ])

        if waybill.type == RETAIL:
            pi.write(0, 2, [
                {'name': it.fullname, 'count': it.count or "",
                 'price_pay': GoodService.get_price(it.good_id).price_retail, 'mul': ''} for it in items])
        else:
            pi.write(0, 2, [
                {'name': it.fullname, 'count': it.count or "",
                 'price_pay': GoodService.get_price(it.good_id).price_gross, 'mul': ''} for it in items])


        waybill.file = path