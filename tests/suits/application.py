#coding: utf-8
from tests.suits import BaseSuite
from tests.suits.commodity import CommodityTestSuite
from tests.suits.good import GoodTestSuite


class ApplicationSuite(object):

    def __init__(self, client, application):
        self.client = client
        self.application = application

        self.commodity_suite = CommodityTestSuite(self.client, self.application)
        self.good_suite = GoodTestSuite(self.client, self.application)

    def good(self, name, number_l, number_g, price_retail, price_gross):
        # if number_l is None and number_g is None:
        #     numeric = False
        numeric = False if number_l is None and number_g is None else True
        com_id = self.commodity_suite.create_commodity(name, numeric, "")["id"]
        good_id = self.good_suite.create_good(com_id, number_l, number_g, price_retail, price_gross)["id"]

        return good_id

    def acceptance_mail(self, file_name, pointsale_id, date):

        pass