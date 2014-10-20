#coding: utf-8
from collections import namedtuple
from services import MailInvoiceService, CommodityService, PriceService


RetailStub = namedtuple('RetailStub', ['id_price', 'id_commodity', 'full_name', 'price_retail', 'count'])


class RetailService(object):

    @classmethod
    def get_retail_items(self, invoice_id):

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

    pass