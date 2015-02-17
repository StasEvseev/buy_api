#coding: utf-8

from flask.ext.restful import marshal_with, fields

from resources.core import BaseTokeniseResource, BaseCanoniseResource

from models.receiver import Receiver

from services import ReceiverService


class ReceiverResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'fullname': fields.String,
        'fname': fields.String,
        'lname': fields.String,
        'pname': fields.String,
        'address': fields.String,
        'passport': fields.String
    }))})
    def get(self):
        return {'items': ReceiverService.get_all()}


class ReceiverCanonResource(BaseCanoniseResource):
    model = Receiver

    attr_json = {
        'id': fields.Integer,
        'fullname': fields.String,
        'fname': fields.String,
        'lname': fields.String,
        'pname': fields.String,
        'address': fields.String,
        'passport': fields.String
    }
    pass