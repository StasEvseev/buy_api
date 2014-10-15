#coding: utf-8
from collections import namedtuple
from services.commodityserv import CommodityService


PriceStub = namedtuple('PriceStub', ['id_commodity', 'number_local', 'number_global', 'NDS', 'price_prev',
                                     'prive_post', 'price_retail', 'price_gross'])


class PriceService(object):

    @classmethod
    def generate_price_stub(cls, products):

        return [
            PriceStub(
                id_commodity=CommodityService.get_commodity(prod.name),
                number_local=prod.number_local,
                number_global=prod.number_global,
                NDS=prod.rate_NDS,
                price_prev='',
                prive_post='',
                price_retail='',
                price_gross='') for prod in products
        ]

        pass
    pass