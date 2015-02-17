#coding: utf-8

from flask import request, json

from flask.ext.restful import marshal_with, fields
from models.pointsale import PointSale
from resources.core import BaseTokeniseResource, BaseCanoniseResource

from services import PointSaleService


class PointSaleCanon(BaseCanoniseResource):
    model = PointSale

    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String
    }

    multif = {'filter_field': ("name", "address")}

    def filter_query(self, query, filter_field, filter_text, sort_field, sort_course, page, count):
        try:
            exclude_points = request.args['exclude_point_id']
        except KeyError:
            pass
        else:
            query = query.filter(
                self.model.id != exclude_points
            )
        return super(PointSaleCanon, self).filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page, count)


class PointSaleResource(BaseTokeniseResource):
    pass
#     @marshal_with({'items': fields.List(fields.Nested({
#         'id': fields.Integer,
#         'name': fields.String,
#         'address': fields.String,
#         # 'price_prev': fields.Price,
#         # 'price_post': fields.Price,
#         # 'number_local': fields.String,
#         # 'number_global': fields.String,
#         # 'price_gross': fields.Price,
#         # 'price_retail': fields.Price,
#         # 'date_from': fields.String
#     }))})
#     def get(self):
#         try:
#             exclude_points = request.args['exclude_point_id']
#         except KeyError:
#             return {'items': PointSaleService.get_all()}
#         else:
#             return {'items': PointSaleService.get_all_exclude(exclude_id=exclude_points)}


class PointSaleItemResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'count': fields.Integer(attribute='count'),
        'good_id': fields.Integer(attribute='good.id'),
        'full_name': fields.String(attribute='good.full_name'),
        'price_retail': fields.String(attribute='good.price.price_retail'),
        'price_gross': fields.String(attribute='good.price.price_gross'),
        # 'is_handling': fields.Boolean,
        # 'invoice_id': fields.Integer,
        # 'provider_id': fields.Integer(attribute='invoice.provider_id'),
        # 'provider': fields.String(attribute='invoice.provider.name')
    }))})
    def get(self, point_id):
        try:
            exclude_items = request.args['exclude_items']
            exclude_items = json.loads(exclude_items)['array']
        except KeyError:
            exclude_items = []

        return {'items': PointSaleService.get_item_to_pointsale(point_id, exclude_items)}