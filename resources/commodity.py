#coding: utf-8

from flask.ext import restful
from flask.ext.restful import marshal_with, fields
from resources.core import TokenResource, BaseTokeniseResource


class CommodityResource(BaseTokeniseResource):

    @marshal_with({'items': fields.List(fields.Nested({
        'name': fields.String,
        'price_retail': fields.String,
        'id_price': fields.Integer,
        'id_commodity': fields.Integer
    }))})
    def get(self):
        from services import CommodityService

        comm_all = CommodityService.get_all_commodity_with_price()

        return {'items': [
            {'name': comm_stub.name, 'price_retail': comm_stub.price_retail,
             'id_price': comm_stub.id_price, 'id_commodity': comm_stub.id_commodity} for comm_stub in comm_all
        ]}