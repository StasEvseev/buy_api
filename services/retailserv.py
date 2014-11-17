#coding: utf-8
from collections import namedtuple
from config import PATH_TO_GENERATE_INVOICE
import os
from excel.output import PrintInvoice, path_template
from models import db
from models.invoice import Invoice
from models.retailinvoice import RetailInvoice
from models.retailinvoiceitem import RetailInvoiceItem
from services import MailInvoiceService, CommodityService, PriceService
from sqlalchemy import exists


RetailStub = namedtuple('RetailStub', ['full_name', 'price_retail', 'count', 'id_good'])


class RetailServiceException(Exception):
    pass


class RetailDuplicateItemsException(RetailServiceException):
    """
    Возникает при дубляже одинаковых позиций в одной накладной.
    """
    pass


class RetailNotPriceException(RetailServiceException):
    """
    Возникает при отсутствии цены.
    """
    pass


class RetailService(object):
    """
    Сервис для работы с розничной накладной.
    """

    @classmethod
    def get_retail_items(cls, invoice_id):
        """
        Получаем все позиции накладной с проставленными ценами.
        """
        from services.goodservice import GoodService
        res = []

        invoice = MailInvoiceService.get_invoice(invoice_id)

        products = invoice.items

        for prod in products:
            good = GoodService.get_good(prod.good_id)
            commodity = CommodityService.get_commodity(prod.name)
            price = PriceService.get_price_to_commodity(commodity.id, date_from=invoice.date)

            res.append(RetailStub(
                id_good=good.id,
                full_name=prod.full_name, price_retail=price.price_retail, count=prod.count))

        return res

    @classmethod
    def build_retail_items(cls, items):
        return [RetailStub(full_name=it['full_name'], id_good=it['id_good'], price_retail='', count='') for it in items]

    @classmethod
    def get_retail_invoice(cls, invoice_id):
        """
        Получаем розничную накладную по приходной накладной.
        При отсутсвии таковой - ничего не возвращаем.
        """
        count = RetailInvoice.query.filter(RetailInvoice.invoice_id==invoice_id).count()
        if count:
            return RetailInvoice.query.filter(RetailInvoice.invoice_id==invoice_id).one()

    @classmethod
    def create_retail_invoice(cls, invoice_id):
        """
        Создаем розничную накладную.
        """
        invoice = MailInvoiceService.get_invoice(invoice_id)
        retail = RetailInvoice(date=invoice.date, number=invoice.number, invoice=invoice)
        db.session.add(retail)
        db.session.commit()
        return retail

    @classmethod
    def save_retail_invoice(cls, retail, items, path_target):
        """
        Сохраняем позиции розничной накладной и формируем бланк.
        """
        from services.goodservice import GoodService
        retail.retailinvoiceitems.delete()

        db.session.add(retail)

        for it in items:
            #Проверяем проставлена ли цена розницу.
            print it.id_good
            good = GoodService.get_good(it.id_good)
            if not PriceService.get_price(good.price_id).price_retail:
                raise RetailNotPriceException(
                    u"У товара должна быть указана розничная цена. %s" % it.full_name)

            retailitem_q = RetailInvoiceItem.query.filter(
                RetailInvoiceItem.retailinvoice==retail,
                RetailInvoiceItem.good_id==good.id)

            if retailitem_q.count() > 0:
                retail_item = retailitem_q.one()
                raise RetailDuplicateItemsException(
                    u"В накладной не может быть двух одинаковых позиций. %s" % retail_item.full_name)

            retail_item = RetailInvoiceItem(
                good_id=good.id, retailinvoice=retail)
            db.session.add(retail_item)

        pi = PrintInvoice(
            path=os.path.join(path_template, 'print_invoice.xls'),
            destination=path_target)
        pi.set_cells(0, 0, ['a', 'b', 'c', 'date'])
        pi.set_cells(0, 2, ['name', 'count', 'price_pay', 'mul'])
        pi.write(0, 0, [{'a': u'', 'b': u'', 'c': u'', 'date': retail.date.strftime('%d.%m.%Y')}, ])

        pi.write(0, 2, [
            {'name': it.full_name, 'count': '',
             'price_pay': GoodService.get_price(it.id_good).price_retail, 'mul': ''} for it in items])

        retail.file = path_target
        db.session.commit()