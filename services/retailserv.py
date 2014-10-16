#coding: utf-8
from collections import namedtuple
from services.commodityserv import CommodityService
from services.mailinvoice import MailInvoiceService
from services.priceserv import PriceService


RetailStub = namedtuple('RetailStub', ['full_name', 'price_retail'])


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
                full_name=prod.full_name, price_retail=price.price_retail))

        return res

    pass