#coding: utf-8

from flask.ext.restful.fields import Raw

class Date(Raw):
    def format(self, value):
        return value.isoformat()

from flask.ext import restful


from resources.acceptance import (
    AcceptanceResource, AcceptanceSaleInvoiceResource, AcceptanceInvoiceItemsResource,
    AcceptanceItemsResource, AcceptanceRemainItemsResource, AcceptanceIdResource, AcceptanceHelperResource,
    AcceptanceCanon)
from resources.commodity import CommodityResource, CommoditysResource, CommodityCanonResource
from resources.core import TokenResource
from resources.goodres import GoodResource, GoodsResource, GoodResourceCanon
from resources.invoice import (
    InvoiceResource, InvoicePriceItemsResource, InvoiceItemResource, InvoiceItemCountResource, InvoiceIdResource)
from resources.mail import MailCheck, MailInvoiceItem
from resources.pointsale import PointSaleResource, PointSaleItemResource, PointSaleCanon
from resources.price import PriceBulkResource, PriceResource, PriceHelperResource, PriceParishByGood
from resources.provider import ProviderCanon
from resources.receiver import ReceiverResource
from resources.sync import SyncResource, SyncResourceError, SyncResourceCreate
from resources.waybill import WayBillItemItemsResource, WayBillHelperResource, \
    WayBillCanon


class MyApi(restful.Api):
    def register_canon(self, canon_res, url):
        res1, res2 = canon_res._register_into_rest()
        self.add_resource(res1, url)
        self.add_resource(res2, url + "/<int:id>")


api = MyApi(prefix='/api')

api.add_resource(TokenResource, '/token')

api.add_resource(MailCheck, '/mail')
api.add_resource(MailInvoiceItem, '/mail/<int:id>/items')

api.add_resource(InvoiceItemResource, '/invoice/<int:invoice_id>/items')
api.add_resource(InvoiceItemCountResource, '/invoice/<int:invoice_id>/count')

api.register_canon(GoodResourceCanon, "/good")
api.add_resource(PriceParishByGood, '/good/<int:id>/priceparish')

api.register_canon(PointSaleCanon, '/pointsale')
api.add_resource(PointSaleItemResource, '/pointsale/<int:point_id>/items')

api.add_resource(ReceiverResource, '/receiver')

# api.add_resource(WayBillResource, '/waybill')
# api.add_resource(WayBillItemResource, '/waybill/<int:id>')
api.register_canon(WayBillCanon, "/waybill")

api.add_resource(WayBillHelperResource, '/waybill/check_exists')
api.add_resource(WayBillItemItemsResource, '/waybill/<int:id>/items')

api.add_resource(PriceBulkResource, '/pricebulk')
api.add_resource(InvoicePriceItemsResource, '/invoicepriceitems/<int:invoice_id>')

api.add_resource(SyncResourceCreate, '/sync/new')
api.add_resource(SyncResource, '/sync/<int:invoice_id>/stop')
api.add_resource(SyncResourceError, '/sync/<int:invoice_id>/status/<int:status>')

api.register_canon(CommodityCanonResource, '/commodity')
api.add_resource(InvoiceResource, '/invoice')
api.add_resource(InvoiceIdResource, '/invoice/<int:id>')
# api.add_resource(AcceptanceResource, '/acceptance')
api.register_canon(AcceptanceCanon, '/acceptance')

api.add_resource(AcceptanceHelperResource, '/acceptance/<int:id>/check')
api.add_resource(AcceptanceItemsResource, '/acceptance/<int:id>/items')
api.add_resource(AcceptanceRemainItemsResource, '/acceptance/remain/<int:id>/items')
api.add_resource(AcceptanceIdResource, '/acceptance/<int:id>')

api.add_resource(AcceptanceSaleInvoiceResource, '/acceptance/pointsale/<int:point_id>/invoice/<int:invoice_id>')
# api.add_resource(AcceptanceSaleWaybillResource, '/acceptance/pointsale/<int:point_id>/waybill/<int:waybill_id>')

api.add_resource(AcceptanceInvoiceItemsResource, '/acceptance/<int:acc_id>/invoice/<int:invoice_id>/items')

# api.add_resource(AcceptanceMailResource, '/acceptance/mail/<int:id>')

# api.add_resource(ProviderResource, '/provider')

api.register_canon(ProviderCanon, '/provider')

api.add_resource(PriceResource, '/price')
api.add_resource(PriceHelperResource, '/price/getprice')