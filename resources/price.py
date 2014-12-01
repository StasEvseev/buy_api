#coding: utf-8


from flask.ext import restful
from flask import request
from flask import json
from flask.ext.restful import abort, marshal_with, fields, reqparse
from resources.core import TokenResource, BaseTokeniseResource
from services.mailinvoice import MailInvoiceService
from services.priceserv import PriceService, PriceServiceException


class PriceResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
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
    }))})
    def get(self):
        return {'items': PriceService.get_all()}

    def post(self):
        pass


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
            PriceService.create_or_update_prices(prices, invoice.date)
        except PriceServiceException as err:
            abort(404, message=unicode(err))
        return "ok"
