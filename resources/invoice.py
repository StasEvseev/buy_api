#coding: utf-8

from flask import request
from flask.ext import restful
from flask.ext.restful import marshal_with, fields, reqparse


# parser = reqparse.RequestParser()
# parser.add_argument('approve', type=bool)
# parser.add_argument('start', type=int)
from resources.core import TokenResource, BaseTokeniseResource
from security import auth
from services.mailinvoice import InvoiceService


#class InvoiceResource(restful.Resource):

#    def get(self):
#        pass

class InvoiceRetailResource(restful.Resource):

    def get(self, invoice_id):
        return {'a': 1, 'b': 2}


class InvoiceResource(BaseTokeniseResource):
    """
    Ресурс для получения всех накладных.
    """

    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'number': fields.String,
        'date': fields.String
    }))})
    def get(self):
        return {'items': InvoiceService.get_all()}


class InvoiceItemResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'name': fields.String,
        'number_local': fields.String,
        'number_global': fields.String,
        'count_order': fields.Integer,
        'count_postorder': fields.Integer,
        'count': fields.Integer,
        'price_without_NDS': fields.Price,
        'price_with_NDS': fields.Price,
        'sum_without_NDS': fields.Price,
        'sum_NDS': fields.Price,
        'rate_NDS': fields.Price,
        'sum_with_NDS': fields.Price,
        'thematic': fields.String,
        'count_whole_pack': fields.Integer,
        'placer': fields.Integer,
    }))})
    def get(self, invoice_id):
        return {'items': InvoiceService.get_items(invoice_id)}


class InvoicePriceItemsResource(BaseTokeniseResource):
    """
    ресурс для получения товаров, цен, и их рекомендуемую стоимость на товары из накладной
    """

    @marshal_with({'items': fields.List(fields.Nested({
        'id_commodity': fields.Integer,
        'full_name': fields.String,
        'number_local': fields.String,
        'number_global': fields.String,
        'NDS': fields.String,
        'price_prev': fields.String,
        'price_post': fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'price_retail_recommendation': fields.String,
        'price_gross_recommendation': fields.String,
        'is_change': fields.Boolean
    }))})
    def get(self, invoice_id):
        from services.mailinvoice import MailInvoiceService
        from services.priceserv import PriceService

        invoice = MailInvoiceService.get_invoice(invoice_id)

        items = PriceService.generate_price_stub(invoice.items, invoice)

        return {'items': [{
            'id_commodity': it.id_commodity,
            'full_name': it.full_name,
            'number_local': it.number_local,
            'number_global': it.number_global,
            'NDS': it.NDS,
            'price_prev': it.price_prev,
            'price_post': it.price_post,
            'price_retail': it.price_retail,
            'price_gross': it.price_gross,
            'price_retail_recommendation': it.price_retail_recommendation,
            'price_gross_recommendation': it.price_gross_recommendation,
            'is_change': it.is_change
        } for it in items]}


class InvoiceRetailItemsResource(BaseTokeniseResource):
    """
    Ресурс
    """
    
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
