#coding: utf-8

from tests import BaseTestCase
from tests.suits.commodity import CommodityTestSuite


class CommodityTest(BaseTestCase):

    def set_up(self):
        self.commodity_suite = CommodityTestSuite(self.client, self.application)

    def test_commodity(self):
        """
        Проверяем CRUD номенклатуры
        """
        self.commodity()

    def commodity(self):
        """
        Тестируем создание/редактирование/получение/удаление номенклатуры.
        """
        from models.commodity import Commodity

        COMS = (
            ((u"ЛТД", True, ""), (u"ЛТД2", True, u"1Т")),
            ((u"Вечерние челны", True, ""), (u"Веч. Челны", False, "")),
            ((u"Машинка", False, ""), (u"Машинка", False, u"25ИГР"))
        )

        with self.application.app_context():

            for com in COMS:
                #Тестируем создание
                name, numeric, thematic = com[0]
                name_new, numeric_new, thematic_new = com[1]
                data = self.commodity_suite._create_commodity(name, numeric, thematic)
                assert data.status_code, 200

                com = Commodity.query.filter(Commodity.name==name).one()
                self.assertEqual(com.numeric, numeric)
                self.assertEqual(com.thematic, thematic)

                #Тестируем получение
                data = self.commodity_suite._get_commodity(com.id)
                self.assertEqual(data.status_code, 200)
                js = self.commodity_suite._deserialize(data.data)
                self.assertEqual(js["id"], com.id)
                self.assertEqual(js['name'], com.name)
                self.assertEqual(js['numeric'], com.numeric)
                self.assertEqual(js['thematic'], com.thematic)
                #Тестируем редактирование
                data = self.commodity_suite._update_commodity(com.id, name_new, numeric_new, thematic_new)
                com = Commodity.query.get(com.id)
                self.assertEqual(data.status_code, 200)
                self.assertEqual(com.name, name_new)
                self.assertEqual(com.numeric, numeric_new)
                self.assertEqual(com.thematic, thematic_new)

                data = self.commodity_suite._get_commodity_all()
                self.assertEqual(data.status_code, 200)

                #Тестируем удаление
                data = self.commodity_suite._delete_commodity(com.id)
                self.assertEqual(data.status_code, 200)
                self.assertIsNone(Commodity.query.get(com.id))