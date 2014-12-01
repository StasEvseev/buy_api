#coding: utf-8

from flask.ext import restful
from resources.acceptance import AcceptanceResource
from resources.commodity import CommodityResource
from resources.core import TokenResource
from resources.goodres import GoodResource
from resources.invoice import InvoiceResource, InvoiceRetailItemsResource, InvoicePriceItemsResource, \
    InvoiceItemResource, InvoiceItemCountResource
from resources.mail import MailCheck
from resources.price import PriceBulkResource, PriceResource
from resources.provider import ProviderResource
from resources.retailinvoice import RetailResource


api = restful.Api(prefix='/api')
# api.add_resource(MailCheck, '/mail')

api.add_resource(TokenResource, '/token')

api.add_resource(MailCheck, '/mail')



api.add_resource(InvoiceItemResource, '/invoice/<int:invoice_id>/items')

api.add_resource(InvoiceItemCountResource, '/invoice/<int:invoice_id>/count')

api.add_resource(GoodResource, '/good/<int:id>')

api.add_resource(PriceBulkResource, '/pricebulk')
api.add_resource(RetailResource, '/retail-invoice')
# api.add_resource(InvoiceRetailResource, '/retailitems/<int:invoice_id>')
api.add_resource(InvoiceRetailItemsResource, '/retailitems/<int:invoice_id>')
api.add_resource(InvoicePriceItemsResource, '/invoicepriceitems/<int:invoice_id>')

api.add_resource(CommodityResource, '/commodity')
api.add_resource(InvoiceResource, '/invoice')
api.add_resource(AcceptanceResource, '/acceptance')
api.add_resource(ProviderResource, '/provider')
api.add_resource(PriceResource, '/price')