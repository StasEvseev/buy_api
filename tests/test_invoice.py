#coding: utf-8
import os
import datetime
from tests import BaseTestCase
from tests.suits.invoice import MailInvoiceTestSuite

from tests.suits.provider import ProviderTestSuite

from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from mails.model import Mail
from models.price import PriceParish, Price
from models.good import Good
from models.commodity import Commodity
from excel import InvoiceModel


class InvoiceTestCase(BaseTestCase):

    def set_up(self):
        self.FILE_NAME = "20141020_2IAEW4.xlsx"
        test_date = datetime.datetime.strptime("Fri, 19 Dec 2014 20:20:57", '%a, %d %b %Y %H:%M:%S')
        self.provider_suite = ProviderTestSuite(self.client, self.application)

        self.mailinvoice_provider = MailInvoiceTestSuite(self.client, self.application)
        self.mail_stub = self.mailinvoice_provider.get_stub(test_date, self.FILE_NAME)

        self.test_provider = self.provider_suite.create_test_provider()
        self.test_date = test_date.date()

    def test_incoming_invoice(self):
        with self.application.app_context():
            self.incoming_invoice()
            self.price_invoice()

    def price_invoice(self):

        ITEMS = (
            (u"Men's Health №11(196)", 106.0, 125.0),
            (u"Men's Health/мини формата/№11(117)", 85.0, 105.0),
            (u"Святые №29(12)Лука Войно-Ясенецкий", 15.0, 18.0),
            (u"Ума палата.Спецвыпуск.Календарь Озорные котята б/н 2015", 34.0, 42.0),
            (u"Советский спорт-понедельник №20.10(20141020)", 46.0, 50.0),
        )

        self.assertEqual(Price.query.count(), 0)
        self.assertEqual(PriceParish.query.count(), 0)

        #сохраняем цены
        resp = self.mailinvoice_provider.price_invoice(self.invoice.id, datas=ITEMS)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Price.query.count(), len(ITEMS))
        self.assertEqual(PriceParish.query.count(), len(ITEMS))

        for item in ITEMS:
            name, gross, retail = item
            attrs = self.mailinvoice_provider._get_item(self.invoice.id, name, gross, retail)
            good = self.mailinvoice_provider._get_good(self.invoice.id, name)
            commodity = good.commodity
            price = good.price
            if commodity.numeric:
                price_parish = PriceParish.query.filter(
                    PriceParish.commodity_id==good.commodity_id,
                    PriceParish.number_local_from==attrs['number_local'],
                    PriceParish.number_global_from==attrs['number_global']
                ).one()
            else:
                price_parish = PriceParish.query.filter(
                    PriceParish.commodity_id==good.commodity_id,
                    PriceParish.date_from==self.invoice.date
                ).one()

            self.assertEqual(float(price.price_gross), gross)
            self.assertEqual(float(price.price_retail), retail)
            self.assertEqual(price_parish.number_local_from, attrs['number_local'])
            self.assertEqual(price_parish.number_global_from, attrs['number_global'])
            self.assertEqual(price_parish.date_from, self.invoice.date)
            self.assertEqual(float(price_parish.NDS), attrs['NDS'])
            self.assertEqual(float(price_parish.price_prev), attrs['price_prev'])
            self.assertEqual(float(price_parish.price_post), attrs['price_post'])
            self.assertEqual(price_parish.price_id, price.id)

    def incoming_invoice(self):
        ITEMS = (
            (u"Men's Health №11(196)", 3, 0, 3, 58.00, 63.8000, 174.00, 10, 17.40, 191.40, u"1МЖ", 0, 3),
            (u"Men's Health/мини формата/№11(117)",	2,	0,	2,	48.72,	53.5900,	97.44,	10,	9.74,	107.18,	u"1МЖ", 0, 2),
            (u"Грамотейка №11(61)",	4,	0,	4,	11.48,	12.6300,	45.92,	10,	4.59,	50.51,	u"2ДЛ", 0, 4),
            (u"Губка Боб и его друзья №21(108)",	2,	0,	2,	75.29,	82.8200,	150.58,	10,	15.06,	165.64,	u"2ДЛ", 0, 2),
            (u"Советский спорт-понедельник №20.10(20141020)", 11, 0,	11,	14.74, 16.2100, 162.14,	10, 16.21,	178.35, u"1СП", 11, 0),
            (u"Ума палата.Спецвыпуск.Календарь Озорные котята б/н 2015",	5, 0, 5, 29.00, 31.9000, 145.00, 10, 14.50, 159.50, u"1ОБ", 0, 5)
        )
        self.assertEqual(InvoiceItem.query.count(), 0)
        self.assertEqual(Good.query.count(), 0)
        self.assertEqual(Mail.query.count(), 0)
        self.assertEqual(Invoice.query.count(), 0)
        self.mailinvoice_provider.handle_invoice(self.mail_stub.date_, self.FILE_NAME)
        self.assertEqual(Mail.query.count(), 1)
        self.assertEqual(Invoice.query.count(), 1)
        invoice = Invoice.query.first()
        self.invoice = invoice

        resp = self.mailinvoice_provider._mails()
        self.assertEqual(resp.status_code, 200)
        data = self._deserialize(resp.data)
        self.assertEqual(data['count'], 1)

        resp = self.mailinvoice_provider._invoice_items(self.invoice.id)
        self.assertEqual(resp.status_code, 200)
        data = self._deserialize(resp.data)
        self.assertEqual(len(data['items']), 41)

        self.assertEqual(invoice.number, u'О-00064184')
        self.assertEqual(invoice.date, self.test_date)
        self.assertEqual(invoice.provider_id, self.test_provider[0])
        self.assertEqual(float(invoice.sum_without_NDS), float(9153.12))
        self.assertEqual(float(invoice.sum_with_NDS), float(10076.83))
        self.assertEqual(float(invoice.sum_NDS), float(923.71))
        self.assertEqual(float(invoice.weight), float(71.408))
        self.assertEqual(invoice.responsible, u"Зарипов Б. Р.")

        mail = Mail.query.first()
        self.assertEqual(mail.title, self.mail_stub.title)
        self.assertEqual(mail.date, self.mail_stub.date_)
        self.assertEqual(mail.from_, self.mail_stub.from_)
        self.assertEqual(mail.to, self.mail_stub.to_)
        self.assertEqual(mail.file, self.mail_stub.file_)
        self.assertEqual(mail.is_handling, False)
        self.assertEqual(mail.invoice_id, invoice.id)

        self.assertEqual(InvoiceItem.query.count(), 41)
        self.assertEqual(Good.query.count(), 41)

        for it in ITEMS:
            name, ord_cnt, reord_cnt, cnt, pr_wo_N, pr_w_N, s_wo_N, r_N, s_N, s_w_N, th, cnt_pk, plc = it
            n, l, g = InvoiceModel.get_name_number(name)
            item = InvoiceItem.query.filter(
                InvoiceItem.name==n,
                InvoiceItem.invoice_id==self.invoice.id
            ).one()

            self.assertEqual(item.full_name, name)
            self.assertEqual(item.number_local, l)
            self.assertEqual(item.number_global, g)
            self.assertEqual(item.count_order, ord_cnt)
            self.assertEqual(item.count_postorder, reord_cnt)
            self.assertEqual(item.count, cnt)
            self.assertEqual(float(item.price_without_NDS), pr_wo_N)
            self.assertEqual(float(item.price_with_NDS), pr_w_N)
            self.assertEqual(float(item.sum_without_NDS), s_wo_N)
            self.assertEqual(float(item.sum_NDS), s_N)
            self.assertEqual(float(item.rate_NDS), r_N)
            self.assertEqual(float(item.sum_with_NDS), s_w_N)
            self.assertEqual(item.thematic, th)
            self.assertEqual(item.count_whole_pack, cnt_pk)
            self.assertEqual(item.placer, plc)
            self.assertIsNotNone(item.good_id)

            comm = Commodity.query.filter(Commodity.name==n).one()
            self.assertEqual(comm.thematic, th)
            self.assertEqual(comm.numeric, bool(l) and bool(g))

            good = Good.query.get(item.good_id)
            self.assertEqual(good.commodity_id, comm.id)
            self.assertEqual(good.full_name, name)
            self.assertEqual(good.number_local, l)
            self.assertEqual(good.number_global, g)
            self.assertIsNone(good.price)