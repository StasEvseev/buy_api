#coding: utf-8
from flask.ext.restful import marshal_with, fields
from resources.core import BaseTokeniseResource
from services.acceptnceserv import AcceptanceService


class AcceptanceResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'date': fields.String,
        'invoice_id': fields.Integer
    }))})
    def get(self):
        return {'items': AcceptanceService.get_all()}