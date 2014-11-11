#coding: utf-8
from flask import g, jsonify

from flask.ext import restful
from security import auth


# def run(f):
#     a = 1
#     b = 2
#     return f

class BaseTokeniseResource(restful.Resource):
    decorators = [auth.login_required]

class TokenResource(BaseTokeniseResource):

    def get(self):
        token = g.user.generate_auth_token()
        print token
        return jsonify({ 'token': token.decode('ascii') })


