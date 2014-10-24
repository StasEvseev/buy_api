#coding: utf-8

from flask.ext import restful
from security import auth


# def run(f):
#     a = 1
#     b = 2
#     return f

class TokenResource(restful.Resource):
    decorators = [auth.login_required]