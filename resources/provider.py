#coding: utf-8

from flask.ext.restful import fields

from resources.core import BaseCanoniseResource

from models.provider import Provider


class ProviderCanon(BaseCanoniseResource):

    model = Provider
    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'emails': fields.String
    }

    multif = {'filter_field': ('name', 'address')}