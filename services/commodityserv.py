#coding: utf-8
from collections import namedtuple

from models.commodity import Commodity


from sqlalchemy.orm.exc import NoResultFound


CommodityStub = namedtuple('CommodityStub', ['name', 'price_retail', 'id_commodity', 'id_price'])


class CommodityService(object):

    @classmethod
    def get_all_commodity_with_price(cls):
        from services import PriceService
        commodity_all = Commodity.query.all()

        res = []

        for commodity in commodity_all:
            price = PriceService.get_price_to_commodity(commodity.id)
            if price.id:

                res.append(CommodityStub(id_commodity=commodity.id, id_price=price.id,
                                         name=commodity.name, price_retail=price.price_retail))

        return res

    @classmethod
    def get_or_create_commodity(cls, name, thematic=None):
        try:
            commodity = Commodity.query.filter(Commodity.name==name).one()
        except NoResultFound as err:
            return False, Commodity(name=name, thematic=thematic)
        else:
            return True, commodity

    @classmethod
    def get_commodity(cls, name):
        return Commodity.query.filter(Commodity.name==name).one()