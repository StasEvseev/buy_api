#coding: utf-8
from flask import request

from flask.ext import restful
from flask.ext.restful import marshal_with, fields, abort
from models import db
from models.commodity import Commodity
from resources.core import TokenResource, BaseTokeniseResource, BaseCanoniseResource
from services import CommodityService


# ATTR_ITEM = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'category': fields.String(attribute='thematic'),
#     'numeric': fields.Boolean
# }


class CommodityCanonResource(BaseCanoniseResource):
    model = Commodity

    multif = {'filter_field': ('name', 'thematic')}

    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'thematic': fields.String,
        'numeric': fields.Boolean
    }


class CommoditysResource(BaseTokeniseResource):
    pass
    # @marshal_with(ATTR_ITEM)
    # def get(self, id):
    #     commodity = CommodityService.get_by_id(id)
    #     return commodity


class CommodityResource(BaseTokeniseResource):
    pass

    # @marshal_with({'items': fields.List(fields.Nested(ATTR_ITEM))})
    # def get(self):
    #     comm_all = CommodityService.get_all_commodity_with_price()
    #     return {'items': comm_all}
    #
    # @marshal_with({'data': fields.Nested({
    #     'id': fields.Integer,
    #     'name': fields.String,
    #     'category': fields.String(attribute='thematic'),
    #     'numeric': fields.Boolean
    # })})
    # def put(self):
    #     data = request.json['data']
    #
    #     name = data['name']
    #     thematic = data['thematic']
    #     numeric = data['numeric']
    #
    #     res, commodity = CommodityService.get_or_create_commodity(name, thematic, numeric)
    #     if res is False:
    #         db.session.add(commodity)
    #         db.session.commit()
    #     if res is True:
    #         abort(400, message=u"В системе есть номенклатура с таким именем.")
    #     return {'data': commodity}