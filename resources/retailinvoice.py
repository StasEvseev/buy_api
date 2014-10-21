#coding: utf-8
from flask import request
from flask import json
from flask.ext import restful
from flask.ext.restful import abort
from services.retailserv import RetailService, RetailServiceException


class RetailResource(restful.Resource):
    """
    Ресурс сохраняет накладную с ее позициями и возвращает ссылку на файл.
    """
    def post(self):

        forse = False

        if request.args:
            forse = request.args['confirm'] in ['true']

        retailinvoice = request.json['data']
        invoice_id = retailinvoice['invoice_id']
        items = retailinvoice['items']

        retail = RetailService.get_retail_invoice(invoice_id)
        if retail and not forse:
            res = {"status": "confirm"}
        else:
            try:
                retail_items = RetailService.build_retail_items(items)
                RetailService.save_retail_invoice(retail, retail_items)
                res = {"status": "ok", "path": "/static/files/1.xlsx"}
            except RetailServiceException as retailexc:
                abort(404, message=unicode(retailexc))

        return res