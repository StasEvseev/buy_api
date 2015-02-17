#coding: utf-8

from flask import request
from flask.ext.restful import abort, marshal_with, fields
from resources.core import BaseTokeniseResource

from services import GoodService, MailInvoiceService, PriceService, PriceServiceException, NotFindPriceParishExc

ATTR = {
    'id': fields.Integer,
    'commodity_id': fields.Integer,
    'NDS': fields.Float,
    'price_prev': fields.Price,
    'price_post': fields.Price,
    'number_local': fields.String,
    'number_global': fields.String,
    'price_gross': fields.Price,
    'price_retail': fields.Price,
    'date_from': fields.String
}

ATTR_FULL = ATTR.copy()
ATTR_FULL["provider_id"] = fields.Integer(attribute="invoice.provider_id")
ATTR_FULL["provider_name"] = fields.String(attribute="invoice.provider.name")
ATTR_FULL["invoice_number"] = fields.String(attribute="invoice.number")

ITEMS_ATTR = {'items': fields.List(fields.Nested(ATTR))}
ITEMS_ATTR_FULL = {"items": fields.List(fields.Nested(ATTR_FULL))}


class PriceResource(BaseTokeniseResource):
    @marshal_with(ITEMS_ATTR)
    def get(self):
        return {'items': PriceService.get_all()}

    def post(self):
        pass


class PriceParishByGood(BaseTokeniseResource):
    """
    Ресурс для получения цен прихода по товару.
    """
    @marshal_with(ITEMS_ATTR_FULL)
    def get(self, id):
        good = GoodService.get_good(id)
        commodity = good.commodity

        try:
            items = PriceService.get_priceparish(
                commodity_id=commodity.id,
                number_global=good.number_global,
                number_local=good.number_local)
        except NotFindPriceParishExc:
            items = []
        return {'items': items}


class PriceHelperResource(BaseTokeniseResource):
    """
    Получаем цены-рекомендации по товару и "цене с НДС"
    """

    @marshal_with({'items': fields.List(fields.Nested({
        'invoice_id': fields.Integer,
        'invoice_str': fields.String,
        'provider_id': fields.Integer,
        'provider_str': fields.String,
        'number_local_from': fields.String,
        'number_global_from': fields.String,
        'date_from': fields.String,
        'price_post': fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String
    }))})
    def get(self):
        args = request.args
        good_id = args['good_id']
        price_post = args['price_post']

        good = GoodService.get_good(good_id)
        commodity = good.commodity
        try:
            prices = PriceService.prices_parish_to_commodity_price(
                commodity, float(price_post))
        #TODO - кажется тут не вылетит никогда исключение PriceServiceException
        except PriceServiceException as exc:
            abort(404, message=unicode(exc), code=1)
        else:
            return {'items': [{
                'invoice_id': x.invoice_id,
                'invoice_str': unicode(x.invoice),
                'provider_id': x.invoice.provider_id,
                'provider_str': x.invoice.provider.name,
                'number_local_from': x.number_local_from,
                'number_global_from': x.number_global_from,
                'date_from': x.date_from,
                'price_post': x.price_post,
                'price_retail': x.price.price_retail,
                'price_gross': x.price.price_gross
            } for x in prices]}


class PriceBulkResource(BaseTokeniseResource):
    """
    Массовое сохранение цен.
    """
    def post(self):
        data = request.json['data']

        prices = data['items']
        invoice_id = data['invoice_id']
        invoice = MailInvoiceService.get_invoice(invoice_id)
        try:
            PriceService.create_or_update_prices(invoice, prices)
        except PriceServiceException as err:
            abort(404, message=unicode(err))
        return "ok"
