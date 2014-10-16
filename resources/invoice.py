#coding: utf-8

from flask.ext import restful
from services.retailserv import RetailService


class InvoiceResource(restful.Resource):

    def get(self):
        pass

class InvoiceRetailResource(restful.Resource):

    def get(self, invoice_id):
        return {'a': 1, 'b': 2}


class InvoiceRetailItemsResource(restful.Resource):

    def get(self, invoice_id):
        print RetailService.get_retail_items(invoice_id)
        print "GET"
        return {'items': []}
        pass