#coding: utf-8
from collections import namedtuple

from models.commodity import Commodity


from sqlalchemy.orm.exc import NoResultFound


CommodityStub = namedtuple('CommodityStub', ['id', 'name', 'category'])


class CommodityService(object):

    @classmethod
    def get_all_commodity_with_price(cls):
        commodity_all = Commodity.query.all()
        return commodity_all

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