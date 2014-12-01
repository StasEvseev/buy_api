#coding: utf-8

from flask.ext import restful
from flask.ext.restful import marshal_with, fields
from resources.core import TokenResource, BaseTokeniseResource


class CommodityResource(BaseTokeniseResource):

    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'category': fields.String(attribute='thematic')
    }))})
    def get(self):
        from services import CommodityService

        comm_all = CommodityService.get_all_commodity_with_price()

        return {'items': comm_all}