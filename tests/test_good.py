#coding: utf-8

from tests import BaseTestCase
from tests.suits.commodity import CommodityTestSuite
from tests.suits.good import GoodTestSuite


class GoodTest(BaseTestCase):

    def set_up(self):
        self.commodity_suite = CommodityTestSuite(self.client, self.application)
        self.good_suite = GoodTestSuite(self.client, self.application)

    def test_good(self):
        """
        Проверяем CRUB товара.
        """
        self.good()

    def good(self):
        """
        Тестируем создание/редактирование/получение/удаление товаров.
        """
        COMS = (
            (u"ЛТД", True, ""),
            (u"Вечерние челны", True, ""),
            (u"Машинка", False, "")
        )

        GOODS = (
            #товары
            #id номенклатуры, номер локальный, номера глобальный, цена розницы, цена опта
            (
                (1, u"1", u"1", 1, 1, True), #SUCCESS
                (1, u"1", u"1", 1, 3, True) #меняем только цену
            ),
            (
                (1, u"1", u"123123", 145, 120, True), #SUCCESS
                (2, u"1", u"123123", 120, 100, True) #меняем цену и номенклатуру
            ),
            (
                (2, u"234", u"674", 90, 100, True), #SUCCESS
                (3, u"234", u"674", 90, 100, False) #попытка поменять номенклатуру на безномерную, но с номерами
            ),
            (
                (3, u"12", u"15", 4, 5, False), #пытаемся создать для безномерной номенклатуры товар с номером
                ()
            ),
            (
                (1, None, None, 1, 1, False), #пытаемся создать для номерной номенклатуры товар без номера
                ()
            ),
            (
                (1, u"1", u"1", 2, 1, False), #пытаемся создать товар с уже существующими номерами
                ()
            ),
            (
                (3, None, None, 66, 77, True),#SUCCESS
                (2, None, None, 66, 77, False)#попытка изменить тип номенклатуры на номерную и сохранить без номера
            )
        )

        with self.application.app_context():
            from models.good import Good
            from models.price import Price
            from models.commodity import Commodity

            for com in COMS:
                name, numeric, thematic = com
                self.commodity_suite._create_commodity(name, numeric, thematic)

            good_count = 0
            price_count = 0
            commodity_count = len(COMS)
            for good in GOODS:
                id_comm, number_l, number_g, price_ret, price_gr, res = good[0]

                resp = self.good_suite._create_good(id_comm, number_l, number_g, price_ret, price_gr)
                if res:
                    self.assertEqual(resp.status_code, 200)
                    good_count += 1
                    price_count += 1
                    data = self._deserialize(resp.data)
                    id = data['id']
                    good = Good.query.get(id)
                    self.assertEqual(good.commodity_id, id_comm)
                    # self.assertEqual(good.commodity.name + u" №" + number_l + u"(" + number_g + u")", good.full_name)
                    self.assertEqual(good.number_local, number_l)
                    self.assertEqual(good.number_global, number_g)
                    self.assertEqual(float(good.price.price_retail), float(price_ret))
                    self.assertEqual(float(good.price.price_gross), float(price_gr))
                else:
                    self.assertEqual(resp.status_code, 400)

                self.assertEqual(Good.query.count(), good_count)
                self.assertEqual(Price.query.count(), price_count)
                self.assertEqual(Commodity.query.count(), commodity_count)

            for good in GOODS:
                id_comm_old, number_l_old, number_g_old, price_ret_old, price_gr_old, res_old = good[0]
                try:
                    id_comm, number_l, number_g, price_ret, price_gr, res = good[1]
                except ValueError:
                    continue
                good = Good.query.filter(Good.commodity_id==id_comm_old)
                if number_l_old and number_g_old:
                    good = good.filter(
                        Good.number_local==number_l_old,
                        Good.number_global==number_g_old)
                good = good.one()
                price = good.price
                resp = self.good_suite._get_good(good.id)
                self.assertEqual(resp.status_code, 200)
                data = self._deserialize(resp.data)
                #тестируем получение
                self.assertEqual(data['id'], good.id)
                self.assertEqual(data['commodity_id'], good.commodity_id)
                self.assertEqual(data['full_name'], good.full_name)
                self.assertEqual(data['number_global'], good.number_global)
                self.assertEqual(data['number_local'], good.number_local)
                self.assertEqual(float(data['price.price_gross']), float(good.price.price_gross))
                self.assertEqual(float(data['price.price_retail']), float(good.price.price_retail))
                self.assertEqual(data['price_id'], good.price_id)

                #тестируем обновление
                resp = self.good_suite._update_good(good.id, id_comm, number_l, number_g, price_ret, price_gr)
                if res:
                    good = Good.query.get(good.id)
                    self.assertEqual(resp.status_code, 200)
                    self.assertEqual(good.commodity_id, id_comm)
                    self.assertEqual(good.number_global, number_g)
                    self.assertEqual(good.number_local, number_l)
                    self.assertEqual(float(good.price.price_gross), float(price_gr))
                    self.assertEqual(float(good.price.price_retail), float(price_ret))
                else:
                    self.assertEqual(resp.status_code, 400)
                    good_new = Good.query.get(good.id)
                    self.assertEqual(good_new.commodity_id, good.commodity_id)
                    self.assertEqual(good_new.number_local, good.number_local)
                    self.assertEqual(good_new.number_global, good.number_global)
                    self.assertEqual(float(good_new.price.price_gross), float(price.price_gross))
                    self.assertEqual(float(good_new.price.price_retail), float(price.price_retail))
                    self.assertEqual(good_new.price_id, good.price_id)

                self.assertEqual(Good.query.count(), good_count)
                self.assertEqual(Price.query.count(), price_count)
                self.assertEqual(Commodity.query.count(), commodity_count)

            for good in Good.query.all():
                good_count -= 1
                self.good_suite._delete_good(good.id)

                self.assertEqual(Good.query.count(), good_count)
                self.assertEqual(Price.query.count(), price_count)
                self.assertEqual(Commodity.query.count(), commodity_count)