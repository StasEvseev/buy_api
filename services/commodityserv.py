#coding: utf-8

from models.commodity import Commodity
from sqlalchemy.orm.exc import NoResultFound


class CommodityService(object):

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