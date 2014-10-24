#coding: utf-8

from flask import url_for, g
from flask.ext.admin import BaseView, expose
from flask.ext import login

from services.mailinvoice import MailInvoiceService



class MailView(BaseView):
    """
    View в админку для работы с почтой.
    """

    def is_accessible(self):
        return login.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render('index.html',
                           token=login.current_user.generate_auth_token())

    @expose('/prices/<string:invoice_id>')
    def prices(self, invoice_id):
        url_back = url_for('.index')
        url_invoice_retail = url_for('.invoice_retail', invoice_id=invoice_id)
        url_invoice_gross = url_for('.invoice_gross', invoice_id=invoice_id)
        invoice = MailInvoiceService.get_invoice(invoice_id)

        return self.render('prices.html',
                           date=invoice.date,
                           url_back=url_back,
                           url_retail=url_invoice_retail,
                           url_gross=url_invoice_gross,
                           invoice_id=invoice_id, token=login.current_user.generate_auth_token())

    @expose('/invoice-retail/<string:invoice_id>')
    def invoice_retail(self, invoice_id):
        url_prices = url_for('.prices', invoice_id=invoice_id)
        return self.render('invoice_retail.html',
                           invoice_id=invoice_id,
                           url_prices=url_prices,
                           token=login.current_user.generate_auth_token())

    @expose('/invoice-gross/<string:invoice_id>')
    def invoice_gross(self, invoice_id):
        return self.render('invoice_gross.html')