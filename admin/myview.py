#coding: utf-8
from flask import request, url_for
from flask.ext.admin import BaseView, expose
from services.mailinvoice import MailInvoiceService
from services.priceserv import PriceService


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

    @expose('/prices/<string:invoice_id>')
    def prices(self, invoice_id):
        url = url_for('.index')
        invoice = MailInvoiceService.get_invoice(invoice_id)

        items = PriceService.generate_price_stub(invoice.items)

        return self.render('prices.html',
                           date=invoice.date,
                           url=url, invoice_items=items)

    @expose('/bla/bla')
    def bla(self):
        pass


class InvoiceView(BaseView):

    @expose('/')
    def index(self):
        return self.render('invoice.html')