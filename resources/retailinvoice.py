#coding: utf-8

import os

from flask import request, url_for
from flask.ext.restful import abort

from config import PATH_TO_GENERATE_INVOICE
from resources.core import TokenResource, BaseTokeniseResource
from services.retailserv import RetailService, RetailServiceException


class RetailResource(BaseTokeniseResource):
    """
    Ресурс сохраняет накладную с ее позициями и возвращает ссылку на файл.
    """
    def post(self):

        #TODO: отрефакторить.

        import uuid
        file_name = str(uuid.uuid4()) + ".xls"
        path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)

        forse = False

        if request.args:
            forse = request.args['confirm'] in ['true']

        retailinvoice = request.json['data']
        invoice_id = retailinvoice['invoice_id']
        items = retailinvoice['items']

        retail = RetailService.get_retail_invoice(invoice_id)
        if retail:
            if not forse:
                return {"status": "confirm"}

        else:
            retail = RetailService.create_retail_invoice(invoice_id)
        try:
            retail_items = RetailService.build_retail_items(items)
            RetailService.save_retail_invoice(retail, retail_items, path_to_target)
            path = url_for('static', filename='files/' + file_name)
            res = {"status": "ok", "path": path}
        except RetailServiceException as retailexc:
            abort(404, message=unicode(retailexc))

        return res