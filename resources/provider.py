#coding: utf-8
from flask.ext.restful import marshal_with, fields
from resources.core import BaseTokeniseResource
from services.providerserv import ProviderService


class ProviderResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'emails': fields.String
    }))})
    def get(self):
        return {'items': ProviderService.get_all()}