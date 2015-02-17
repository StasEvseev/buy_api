#coding: utf-8
import os

from excel import InvoiceModel

from tests.suits import BaseSuite

from mock import Mock

from services import MailInvoiceService

from mails.action import MailHepls
from mails.action import MailObject

from tests.suits.provider import ProviderTestSuite

from models.invoiceitem import InvoiceItem



class MailInvoiceTestSuite(BaseSuite):

    def _mails(self):
        return self._get_records("/api/mail")

    def _invoice_items(self, id):
        return self._get_record("/api/invoicepriceitems/", id)

    def _price_invoice(self, id, list_items):
        return self.client.post("/api/pricebulk",
                         data=self._serialize({'data': {'invoice_id': id, 'items': list_items}}),
                         headers=self._get_headers())

    def _get_invoiceitem(self, invoice_id, full_name):
        n, l, g = InvoiceModel.get_name_number(full_name)
        return InvoiceItem.query.filter(
            InvoiceItem.name==n,
            InvoiceItem.invoice_id==invoice_id
        ).one()

    def _get_good(self, invoice_id, fullname):
        item = self._get_invoiceitem(invoice_id, fullname)
        return item.good

    def _get_item(self, invoice_id, name, price_gross, price_retail):
        item = self._get_invoiceitem(invoice_id, name)
        good = item.good
        return {
            'id_commodity': good.commodity_id,
            'id_good': good.id,
            'price_gross': price_gross,
            'price_retail': price_retail,
            'price_post': float(item.price_with_NDS),
            'price_prev': float(item.price_without_NDS),
            'number_local': item.number_local,
            'number_global': item.number_global,
            'NDS': float(item.rate_NDS)
        }

    def get_stub(self, datetime, file_name):
        def date_stub():
            return datetime
        def file_stub():
            return os.path.join(os.getcwd(), "tests", "stubs", file_name)
        return MailObject(
            title="NEW", date_=date_stub(),
            from_=ProviderTestSuite.EMAIL, to_="a@a.ru", file_=file_stub())

    def handle_invoice(self, datetime, file_name):
        mail_stub = self.get_stub(datetime, file_name)

        MailHepls.get_mails = Mock(return_value=(ProviderTestSuite.EMAIL, {ProviderTestSuite.EMAIL: [mail_stub]}))
        MailInvoiceService.get_count_new_mails = Mock(return_value=1)
        MailInvoiceService.handle_mail()

    def price_invoice(self, invoice_id, datas):
        prices = []

        for item in datas:
            name, gross, retail = item
            prices.append(self._get_item(invoice_id, name, gross, retail))

        return self._price_invoice(invoice_id, prices)