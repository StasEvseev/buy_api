#coding: utf-8

from flask.ext import restful
from resources.commodity import CommodityResource
from resources.core import TokenResource
from resources.invoice import InvoiceRetailResource, InvoiceRetailItemsResource, InvoicePriceItemsResource
from resources.mail import MailCheck
from resources.price import PriceBulkResource
from resources.retailinvoice import RetailResource


api = restful.Api(prefix='/api')
# api.add_resource(MailCheck, '/mail')

api.add_resource(TokenResource, '/token')

api.add_resource(MailCheck, '/mail')

api.add_resource(PriceBulkResource, '/pricebulk')

# api.add_resource(InvoiceRetailResource, '/retailitems/<int:invoice_id>')
api.add_resource(InvoiceRetailItemsResource, '/retailitems/<int:invoice_id>')
api.add_resource(InvoicePriceItemsResource, '/invoicepriceitems/<int:invoice_id>')

api.add_resource(CommodityResource, '/commodity')

api.add_resource(RetailResource, '/retail-invoice')