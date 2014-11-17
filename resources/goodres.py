#coding: utf-8
from flask import request
from flask.ext.restful import marshal_with, fields, abort
from resources.core import BaseTokeniseResource
from services.goodservice import GoodService, GoodServiceException


class GoodResource(BaseTokeniseResource):

    def post(self, id):
        try:
            data = request.json['data']
            print "=" * 80
            print data
            print "=" * 80
            barcode = data['barcode']
            count = data['count']
        except KeyError:
            abort(402, message="Bad args")
        try:
            GoodService.update_good(id, count, barcode)
        except GoodServiceException as err:
            abort(404, message=unicode(err))
        return "ok"

    @marshal_with({
        'id': fields.Integer,
        'full_name': fields.String,
        'commodity_id': fields.Integer,
        'price_id': fields.Integer,
        'barcode': fields.Integer,
        'count': fields.Integer,
        'is_confirm': fields.Boolean
    })
    def get(self, id):
        try:
            good = GoodService.get_good(id)
        except GoodServiceException as err:
            abort(404, message=unicode(err))
        return good