#coding: utf-8

from flask.ext import restful
from resources.mail import MailCheck
from resources.price import PriceBulkResource

api = restful.Api(prefix='/api')
# api.add_resource(MailCheck, '/mail')

api.add_resource(MailCheck, '/mail')

api.add_resource(PriceBulkResource, '/pricebulk')