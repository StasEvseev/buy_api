#coding: utf-8


from flask.ext import restful
from flask import request
from flask import json
from flask.ext.restful import abort, marshal_with, fields, reqparse
from resources.core import TokenResource
from services.mailinvoice import MailInvoiceService
from services.priceserv import PriceService, PriceServiceException


class PriceResource(TokenResource):
    def get(self):
        pass

    def post(self):
        pass


class PriceBulkResource(TokenResource):
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