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
        url_back = url_for('.index')
        url_next = url_for('.invoice_retail', invoice_id=invoice_id)
        invoice = MailInvoiceService.get_invoice(invoice_id)

        items = PriceService.generate_price_stub(invoice.items)

        return self.render('prices.html',
                           date=invoice.date,
                           url_back=url_back,
                           url_next=url_next,
                           invoice_items=items)

    @expose('/invoice-retail/<string:invoice_id>')
    def invoice_retail(self, invoice_id):
        return self.render('invoice_retail.html')
        pass

    @expose('/bla/bla')
    def bla(self):
        pass


class InvoiceView(BaseView):

    @expose('/')
    def index(self):
        return self.render('invoice.html')