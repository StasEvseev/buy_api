#coding: utf-8

from flask.ext import restful
from flask.ext.restful import marshal_with, fields
from services.retailserv import RetailService


class InvoiceResource(restful.Resource):

    def get(self):
        pass

class InvoiceRetailResource(restful.Resource):

    def get(self, invoice_id):
        return {'a': 1, 'b': 2}


class InvoiceRetailItemsResource(restful.Resource):

    @marshal_with({'items': fields.List(fields.Nested({
        'full_name': fields.String,
        'price_retail': fields.String,
        'count': fields.String
        # 'from': fields.String(attribute='from_'),
        # 'is_handling': fields.Boolean,
        # 'invoice_id': fields.Integer
    }))})
    def get(self, invoice_id):
        items = RetailService.get_retail_items(invoice_id)
        return {'items': [
            {'full_name': item.full_name, 'price_retail': item.price_retail, 'count': item.count} for item in items]}