#coding: utf-8
import datetime
from services import PriceService
from tests import BaseTestCase
from tests.suits.invoice import MailInvoiceTestSuite
from tests.suits.provider import ProviderTestSuite
from models.invoice import Invoice
from models.price import Price, PriceParish


class ChangePriceTestCase(BaseTestCase):

    def set_up(self):
        self.FILE_NAME = "20141020_2IAEW4.xlsx"
        test_date = datetime.datetime.strptime("Fri, 19 Dec 2014 20:20:57", '%a, %d %b %Y %H:%M:%S')

        self.FILE_NAME2 = "20141021_2IAEW4.xlsx"
        test_date2 = datetime.datetime.strptime("Fri, 25 Dec 2014 19:15:13", '%a, %d %b %Y %H:%M:%S')

        self.mailinvoice_provider = MailInvoiceTestSuite(self.client, self.application)
        self.provider_suite = ProviderTestSuite(self.client, self.application)
        self.provider_suite.create_test_provider()

        self.mail_stub = self.mailinvoice_provider.get_stub(test_date, self.FILE_NAME)
        self.mail_stub2 = self.mailinvoice_provider.get_stub(test_date2, self.FILE_NAME2)

    def test_change_price(self):
        with self.application.app_context():
            self.invoice_change_price()

    def invoice_change_price(self):
        """
        Меняется ли цена у товара при приходе накладной с измененными ценами.
        """
        ITEMS = (
            (u"Men's Health №11(196)", 95.0, 120.0),
            (u"Men's Health/мини формата/№11(117)", 86.0, 105.0),
            (u"Ума палата.Спецвыпуск.Календарь Год козы б/н 2015", 24.0, 30.0),
            (u"Ума палата.Спецвыпуск.Календарь Гороскоп б/н 2015", 23.0, 29.0),
            (u'Цифровые сканворды №42(680)', 14.0, 17.0),
            (u'Числовые сканворды №42(466)', 11.0, 14.0),
            (u"Моя семья №41(735)", 22.0, 26.0)
        )

        CIP_SCAN = u'Цифровые сканворды №42(680)'
        CH_SCAN = u'Числовые сканворды №42(466)'
        MN = u"Men's Health №12(197)"
        MN_MINI = u"Men's Health/мини формата/№12(118)"
        MIND_PAL = u"Ума палата.Спецвыпуск.Календарь Год козы б/н 2015"
        MIND_GOR = u"Ума палата.Спецвыпуск.Календарь Гороскоп б/н 2015"

        # ITEMS2 = (
        #     # (u'Цифровые сканворды №42(680)'), #неизменный номер, цена не менялась
        #     # (u'Числовые сканворды №42(466)'), #неизменный номер, но менялась цена
        #     # (u"Men's Health №12(197)"), #изменилась цена но цена продажи не поменялась
        #     (MN_MINI, 90.0, 110.0), #изменилась цена и поменяли цену продажи
        #     (MIND_PAL, 25.0, 32.0), #безномерная но поменяла цену, поменяем цену продажи
        #     # (MIND_GOR, ) #безномерная, цену поменяла, но мы оставляем продажу такой же
        # )

        PRICE_CH = {
            MN_MINI: (90.0, 110.0),
            MIND_PAL: (25.0, 32.0)
        }

        #проверка вычисления изменения цены товара
        ITEM_CHANGE_PRICE = (
            (CIP_SCAN, False),
            (CH_SCAN, True),
            (MN, True),
            (MN_MINI, True),
            (MIND_PAL, True),
            (MIND_GOR, True)
        )

        #проверка создания новой цены
        ITEM_NEW_PRICE = (
            (CIP_SCAN, False),
            (CH_SCAN, False),
            (MN, False),
            (MN_MINI, True),
            (MIND_PAL, True),
            (MIND_GOR, False)
        )

        #принимаем накладную исходную
        self.mailinvoice_provider.handle_invoice(self.mail_stub.date_, self.FILE_NAME)
        invoice = Invoice.query.first()

        for item in ITEMS:
            name, _, _ = item
            inv_item = self.mailinvoice_provider._get_invoiceitem(invoice.id, name)
            price = PriceService.generate_price_stub_item(inv_item)
            self.assertEqual(price.is_change, False)
        #раставляем цены на некоторые товары
        self.mailinvoice_provider.price_invoice(invoice.id, datas=ITEMS)

        #принимает накладную с измененными ценами
        self.mailinvoice_provider.handle_invoice(self.mail_stub2.date_, self.FILE_NAME2)
        invoice2 = Invoice.query.filter(
            Invoice.id!=invoice.id
        ).one()
        #проверяем, оповещает ли система об измененных ценах
        for item in ITEM_CHANGE_PRICE:
            name, is_ch = item
            inv_item = self.mailinvoice_provider._get_invoiceitem(invoice2.id, name)
            price = PriceService.generate_price_stub_item(inv_item)
            self.assertEqual(price.is_change, is_ch)
        #сохраняем новые цены

        self.mailinvoice_provider.price_invoice(invoice2.id, datas=[(x, PRICE_CH[x][0], PRICE_CH[x][1]) for x in PRICE_CH])

        for item in ITEM_NEW_PRICE:
            name, new_pr = item
            inv_item = self.mailinvoice_provider._get_invoiceitem(invoice2.id, name)
            good = self.mailinvoice_provider._get_good(invoice2.id, name)
            prices_parish = PriceParish.query.filter(
                PriceParish.commodity_id==good.commodity.id,
            )
            self.assertEqual(prices_parish.count(), 2 if new_pr else 1)
            if new_pr and name in PRICE_CH:
                prices_gross, price_retail = PRICE_CH[name]
                self.assertEqual(float(good.price.price_retail), price_retail)
                self.assertEqual(float(good.price.price_gross), prices_gross)