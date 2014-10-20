#coding: utf-8

from flask import request
from flask.ext import restful
from flask.ext.restful import marshal_with, fields, reqparse


# parser = reqparse.RequestParser()
# parser.add_argument('approve', type=bool)
# parser.add_argument('start', type=int)



class InvoiceResource(restful.Resource):

    def get(self):
        pass

class InvoiceRetailResource(restful.Resource):

    def get(self, invoice_id):
        return {'a': 1, 'b': 2}


class InvoiceRetailItemsResource(restful.Resource):

    @marshal_with({'items': fields.List(fields.Nested({
        'id_commodity': fields.Integer,
        'id_price': fields.String,
        'full_name': fields.String,
        'price_retail': fields.String,
        'count': fields.String,
        'is_approve': fields.Boolean
    }))})
    def get(self, invoice_id):
        from services import RetailService
        args = request.args

        items = RetailService.get_retail_items(invoice_id)

        if 'approve' in args:
            if args['approve'] in ['true']:
                items = filter(lambda x: x.price_retail, items)
            elif args['approve'] in ['false']:
                items = filter(lambda x: x.price_retail == '', items)

        return {'items': [
            {'full_name': item.full_name,
             'price_retail': item.price_retail,
             'count': item.count,
             'id_commodity': item.id_commodity,
             'id_price': item.id_price,
             'is_approve': item.price_retail != ''} for item in items]}