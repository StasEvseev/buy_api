#coding: utf-8
from flask import request, url_for
from flask.ext.admin import BaseView, expose
from services.mailinvoice import MailInvoiceService


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

    @expose('/prices/<string:invoice_id>')
    def prices(self, invoice_id):
        url = url_for('.index')
        invoice = MailInvoiceService.get_invoice(invoice_id)

        return self.render('prices.html',
                           date=invoice.date,
                           url=url, invoice_items=list(invoice.items))

    @expose('/bla/bla')
    def bla(self):
        pass


class InvoiceView(BaseView):

    @expose('/')
    def index(self):
        return self.render('invoice.html')