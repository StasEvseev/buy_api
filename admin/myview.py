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
        url_invoice_retail = url_for('.invoice_retail', invoice_id=invoice_id)
        url_invoice_gross = url_for('.invoice_gross', invoice_id=invoice_id)
        invoice = MailInvoiceService.get_invoice(invoice_id)

        items = PriceService.generate_price_stub(invoice.items)

        return self.render('prices.html',
                           date=invoice.date,
                           attention=any([it.is_change for it in items]),
                           url_back=url_back,
                           url_retail=url_invoice_retail,
                           url_gross=url_invoice_gross,
                           invoice_items=items)

    @expose('/invoice-retail/<string:invoice_id>')
    def invoice_retail(self, invoice_id):
        url_prices = url_for('.prices', invoice_id=invoice_id)
        return self.render('invoice_retail.html', invoice_id=invoice_id, url_prices=url_prices)

    @expose('/invoice-gross/<string:invoice_id>')
    def invoice_gross(self, invoice_id):
        return self.render('invoice_gross.html')

    @expose('/bla/bla')
    def bla(self):
        pass


class InvoiceView(BaseView):

    @expose('/')
    def index(self):
        return self.render('invoice.html')