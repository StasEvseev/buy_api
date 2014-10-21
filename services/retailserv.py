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


RetailStub = namedtuple('RetailStub', ['id_price', 'id_commodity', 'full_name', 'price_retail', 'count'])


class RetailServiceException(Exception):
    pass


class RetailDuplicateItemsException(RetailServiceException):
    pass


class RetailService(object):

    @classmethod
    def get_retail_items(cls, invoice_id):

        res = []

        invoice = MailInvoiceService.get_invoice(invoice_id)

        products = invoice.items

        for prod in products:
            commodity = CommodityService.get_commodity(prod.name)
            price = PriceService.get_price_to_commodity(commodity.id)

            res.append(RetailStub(
                id_price=price.id, id_commodity=commodity.id,
                full_name=prod.full_name, price_retail=price.price_retail, count=prod.count))

        return res

    @classmethod
    def build_retail_items(cls, items):
        return [RetailStub(id_price=it['id_price'], id_commodity=it['id_commodity'],
                           full_name=it['full_name'], price_retail='', count='') for it in items]

    @classmethod
    def get_retail_invoice(cls, invoice_id):
        count = RetailInvoice.query.filter(RetailInvoice.invoice_id==invoice_id).count()
        if count:
            return RetailInvoice.query.filter(RetailInvoice.invoice_id==invoice_id).one()

    @classmethod
    def create_retail_invoice(cls, invoice_id):
        invoice = MailInvoiceService.get_invoice(invoice_id)
        db.session.add(RetailInvoice(date=invoice.date, number=invoice.number, invoice=invoice))
        db.session.commit()

    @classmethod
    def save_retail_invoice(cls, retail, items):
        # if retail.retailinvoiceitems:
        retail.retailinvoiceitems.delete()

        import uuid

        pi = PrintInvoice(
            path=os.path.join(path_template, 'print_invoice.xls'),
            destination=os.path.join(PATH_TO_GENERATE_INVOICE, str(uuid.uuid4()) + ".xls"))
        pi.set_cells(0, 0, ['a', 'b', 'c', 'date'])
        # pi.set_cells(0, 2, ['name', 'count', 'price_pay', 'mul'])
        pi.write(0, 0, [{'a': u'', 'b': u'', 'c': u'', 'date': retail.date.strftime('%d.%m.%Y')}, ])
        # pi.write(0, 0, [])

        db.session.add(retail)

        for it in items:

            retailitem_q = RetailInvoiceItem.query.filter(
                RetailInvoiceItem.retailinvoice==retail,
                RetailInvoiceItem.commodity_id==it.id_commodity)

            if retailitem_q.count() > 0:
                retail_item = retailitem_q.one()
                raise RetailDuplicateItemsException(u"В накладной не может быть двух одинаковых позиций. %s" % retail_item.full_name)

            retail_item = RetailInvoiceItem(
                full_name=it.full_name, price_id=it.id_price, commodity_id=it.id_commodity, retailinvoice=retail)
            db.session.add(retail_item)
        db.session.commit()