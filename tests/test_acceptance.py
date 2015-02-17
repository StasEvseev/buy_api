#coding: utf-8
from datetime import datetime
from datetime import date
from models.invoice import Invoice
from models.pointsaleitem import PointSaleItem
from models.invoiceitem import InvoiceItem
from models.price import Price, PriceParish
from models.good import Good

from tests import BaseTestCase
from tests.suits.acceptance import AcceptanceSuite
from tests.suits.application import ApplicationSuite
from tests.suits.invoice import MailInvoiceTestSuite
from tests.suits.pointsale import PointSaleSuite
from tests.suits.provider import ProviderTestSuite


class AcceptanceTest(BaseTestCase):
    def set_up(self):
        self.FILE_NAME = "20141020_2IAEW4.xlsx"

        self.acceptance_suite = AcceptanceSuite(self.client, self.application)

        self.pointsale_suite = PointSaleSuite(self.client, self.application)

        self.application_suite = ApplicationSuite(self.client, self.application)

        self.provider_suite = ProviderTestSuite(self.client, self.application)
        self.test_provider_id, _, _, _ = self.provider_suite.create_test_provider()

        self.invoice_suite = MailInvoiceTestSuite(self.client, self.application)
        with self.application.app_context():
            pointsale = self.pointsale_suite.create_test_pointsale(name=u"ШШК", address=u"Наб. Челны")
            self.pointsale_id = pointsale.id

    def invoice_(self):
        # with self.application.app_context():
        self.invoice_suite.handle_invoice(datetime=datetime.now(), file_name=self.FILE_NAME)
        self.invoice_id = Invoice.query.first().id


class AcceptanceCrud(AcceptanceTest):

    pass



class AcceptanceTestFromMail(AcceptanceTest):
    """
    item = {
        fact_count: 1
        good_id: 96
        id: 44
    }
    """

    def test_from_mail(self):
        with self.application.app_context():
            self.invoice_()
            response = self.acceptance_suite.invoice_items(self.invoice_id)
            self.assertEqual(response.status_code, 200)

            items = self._deserialize(response.data)
            self.assertEqual(len(items['items']), 41)

            items = [{'good_id': x['good_id'], 'id': x['id'], 'fact_count': num} for num, x in enumerate(items['items'][:10])]
            count_pointitems = len(filter(lambda x: x['fact_count'], items))

            for item in InvoiceItem.query.filter(InvoiceItem.invoice_id==self.invoice_id):
                self.assertIsNone(item.fact_count)

            self.assertEqual(PointSaleItem.query.filter(PointSaleItem.pointsale_id==self.pointsale_id).count(), 0)
            self.assertEqual(PointSaleItem.query.count(), 0)

            response = self.acceptance_suite.acceptance_from_mail(
                self.invoice_id, self.pointsale_id, date=date.today(), items=items)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(PointSaleItem.query.filter(PointSaleItem.pointsale_id==self.pointsale_id).count(), count_pointitems)
            self.assertEqual(PointSaleItem.query.count(), count_pointitems)

            for item in items:
                self.assertEqual(InvoiceItem.query.get(item['id']).fact_count, item['fact_count'] if item['fact_count'] else None)


class AcceptanceTestCustom(AcceptanceTest):
    """
    item = {
        good_id: 48
        price_gross: "21"
        price_post: "15"
        price_retail: "24"
    }
    """

    def test_(self):
        with self.application.app_context():
            PRICE_GROSS_1 = 5.5
            PRICE_RETAIL_1 = 8.0
            COUNT_1 = 5

            PRICE_GROSS_2 = 7.9
            PRICE_RETAIL_2 = 12.0
            COUNT_2 = 15

            PRICE_CHANGE_GROSS_2 = PRICE_GROSS_2 + 1
            PRICE_CHANGE_RETAIL_2 = PRICE_RETAIL_2 + 1.5

            PRICE_POST_1 = 3.8
            PRICE_POST_2 = 7.0

            self.good_id = self.application_suite.good(u"ЛТД", 5, 105, PRICE_RETAIL_1, PRICE_GROSS_1)
            self.good_2_id = self.application_suite.good(u"Вечерние Челны", 22, 607, PRICE_RETAIL_2, PRICE_GROSS_2)
            self.assertEqual(Price.query.count(), 2)
            items = [
                {"good_id": self.good_id, "price_gross": PRICE_GROSS_1, "price_retail": PRICE_RETAIL_1, "price_post": PRICE_POST_1, "count_invoice": COUNT_1},
                {"good_id": self.good_2_id, "price_gross": PRICE_CHANGE_GROSS_2, "price_retail": PRICE_CHANGE_RETAIL_2, "price_post": PRICE_POST_2, "count_invoice": COUNT_2}
            ]
            response = self.acceptance_suite.acceptance_custom(
                self.pointsale_id, self.test_provider_id, date.today(), items)
            data = self._deserialize(response.data)
            invoice_id = data['data']['id']

            self.assertEqual(response.status_code, 200)

            good_1 = Good.query.get(self.good_id)
            good_2 = Good.query.get(self.good_2_id)
            invoice = Invoice.query.get(invoice_id)

            self.assertEqual(Price.query.count(), 4)

            self.assertEqual(PriceParish.query.filter(
                PriceParish.commodity_id==good_1.commodity_id,
            ).count(), 1)

            self.assertEqual(PriceParish.query.filter(
                PriceParish.commodity_id==good_2.commodity_id,
            ).count(), 1)

            self.assertEqual(float(good_1.price.price_gross), PRICE_GROSS_1)
            self.assertEqual(float(good_1.price.price_retail), PRICE_RETAIL_1)
            self.assertEqual(float(good_2.price.price_gross), PRICE_CHANGE_GROSS_2)
            self.assertEqual(float(good_2.price.price_retail), PRICE_CHANGE_RETAIL_2)

            invitem_1 = InvoiceItem.query.filter(
                InvoiceItem.invoice_id==invoice_id, InvoiceItem.good_id==self.good_id
            ).first()
            invitem_2 = InvoiceItem.query.filter(
                InvoiceItem.invoice_id==invoice_id, InvoiceItem.good_id==self.good_2_id
            ).first()
            self.assertEqual(invitem_1.fact_count, COUNT_1)
            self.assertEqual(invitem_2.fact_count, COUNT_2)
            self.assertEqual(float(invitem_1.price_with_NDS), PRICE_POST_1)
            self.assertEqual(float(invitem_2.price_with_NDS), PRICE_POST_2)

            pointsaleitem_1 = PointSaleItem.query.filter(
                PointSaleItem.good_id==self.good_id
            ).first()
            pointsaleitem_2 = PointSaleItem.query.filter(
                PointSaleItem.good_id==self.good_2_id
            ).first()

            self.assertEqual(pointsaleitem_1.count, COUNT_1)
            self.assertEqual(pointsaleitem_2.count, COUNT_2)