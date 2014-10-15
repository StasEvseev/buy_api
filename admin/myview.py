#coding: utf-8
from flask import request, url_for
from flask.ext.admin import BaseView, expose
from models.invoice import Invoice


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

    @expose('/invoice/<string:invoice_id>')
    def invoice(self, invoice_id):
        url = url_for('.index')
        invoice = Invoice.query.get(invoice_id)
        return self.render('invoice.html', url=url)

    @expose('/bla/bla')
    def bla(self):
        pass


class InvoiceView(BaseView):

    @expose('/')
    def index(self):
        return self.render('invoice.html')