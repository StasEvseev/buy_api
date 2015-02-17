#coding: utf-8

from tests import BaseTestCase
from tests.helpers import Generator
from tests.suits.application import ApplicationSuite
from tests.suits.canon import BaseCanonSuite
from tests.suits.commodity import CommodityTestSuite
from tests.suits.good import GoodTestSuite
from tests.suits.pointsale import PointSaleSuite
from tests.suits.receiver import ReceiverSuite
from tests.suits.waybill import WayBillTestSuite

from models.waybill import WayBill, TYPE, RETAIL, GROSS


class WayBillTest(BaseTestCase):

    def test_(self):
        with self.application.app_context():
            self.init_relation_models()
            self.method_to_test()

    def method_to_test(self):
        self.waybill_crud()

    def init_relation_models(self):
        self.receiver = self.receiver_suite.create_test_receiver()
        self.receiver_id = self.receiver.id
        self.point_1 = self.pointsale_suite.create_test_pointsale(name=u"ШШК", address=u"наб. Челны")
        self.point_1_id = self.point_1.id
        self.point_2 = self.pointsale_suite.create_test_pointsale(name=u"Одиссей", address=u"Наб. Челны, ул. Беляева, 75")
        self.point_2_id = self.point_2.id

        self.application_suite = ApplicationSuite(self.client, self.application)
        self.good_id = self.application_suite.good(u"XXL", 77, 114, 105.0, 86.0)
        self.good_2_id = self.application_suite.good(u"Машинка", None, None, 24.0, 21.0)
        self.good_3_id = self.application_suite.good(u"ЗОЖ", 4, 105, None, 9.5)
        self.good_4_id = self.application_suite.good(u"Мельница", None, None, 15.0, None)

    def crush(self):
        count = WayBill.query.count()
        #TEST CRASH
        #Тут создаем накладную и получателю и точке
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=self.receiver_id,
            type=RETAIL, invoice_id=None, pointsale_from_id=self.point_1_id, items=[], pointsale_id=self.point_2_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную без получателя и точки
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=None, pointsale_id=None, type=RETAIL, invoice_id=None,
            pointsale_from_id=None, items=[]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную неизвестного типа
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=self.receiver_id, type=3, invoice_id=None,
            pointsale_from_id=self.point_1_id, items=[]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную с циклической ссылкой(откуда уходит товар, туда и приходит)
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=RETAIL, invoice_id=None,
            pointsale_from_id=self.point_1_id, items=[]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создание розничной накладной с товаром в котором только оптовая цена
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=RETAIL, invoice_id=None,
            pointsale_from_id=self.point_2_id, items=[{
                'good_id': self.good_3_id,
                'count': 15,
                'is_approve': True
            }])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создание оптовой накладной с товаром в котором только розничная цена
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=GROSS, invoice_id=None,
            pointsale_from_id=self.point_2_id, items=[{
                'good_id': self.good_4_id,
                'count': 15,
                'is_approve': True
            }]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

    def waybill_crud(self):

        self.date = Generator.generate_date()
        self.date_2 = Generator.generate_date()
        self.items = [{'good_id': self.good_id, 'count': 10, 'is_approve': True},
                      {'good_id': self.good_4_id, 'count': 5, 'is_approve': True}]
        self.items_2 = [{'good_id': self.good_2_id, 'count': 7, 'is_approve': True}]
        self.crush()

        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_2_id, type=RETAIL,
            invoice_id=None, pointsale_from_id=self.point_1_id, items=self.items)

        self.assertEqual(response.status_code, 200)
        data = self._deserialize(response.data)

        self.assertEqual(WayBill.query.count(), 1)
        waybill = WayBill.query.first()

        self.assertEqual(waybill.pointsale_id, self.point_2_id)
        self.assertEqual(waybill.pointsale_from_id, self.point_1_id)
        self.assertEqual(waybill.type, RETAIL)
        self.assertEqual(waybill.date, self.date)
        self.assertEqual(waybill.items.count(), len(self.items))

        response = self.waybill_suite.get_waybill(waybill.id)
        self.assertEqual(response.status_code, 200)

        response = self.waybill_suite.update_waybill(waybill.id, date=unicode(self.date_2), items=self.items_2)
        self.assertEqual(response.status_code, 200)

        waybill = WayBill.query.get(waybill.id)
        self.assertEqual(waybill.date, self.date_2)
        self.assertEqual(waybill.items.count(), len(self.items_2))

    # def waybill_create_from_acceptance(self):
    #     pass
    #
    # def waybill_create_from_mail(self):
    #     pass
    #
    # def waybill_create_custom(self):
    #     pass

    def set_up(self):
        self.receiver_suite = ReceiverSuite(self.client, self.application)
        self.pointsale_suite = PointSaleSuite(self.client, self.application)
        self.waybill_suite = WayBillTestSuite(self.client, self.application)

        self.commodity_suite = CommodityTestSuite(self.client, self.application)
        self.good_suite = GoodTestSuite(self.client, self.application)

    def tear_down(self):
        pass



class WayBillCreateFromAcceptance(WayBillTest):

    def method_to_test(self):
        self.waybill()

    def waybill(self):

        pass
