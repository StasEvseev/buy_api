#coding: utf-8
from flask import request
from flask import json
from flask.ext import restful


class RetailResource(restful.Resource):
    """
    Ресурс сохраняет накладную с ее позициями и возвращает ссылку на файл.
    """
    def post(self):
        retailinvoice = request.json['data']
        invoice_id = retailinvoice['invoice_id']
        items = retailinvoice['items']

        for it in items:

            pass

        print retailinvoice
