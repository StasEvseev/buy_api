#coding: utf-8

from flask.ext import restful
from resources.mail import MailCheck

api = restful.Api(prefix='/api')
api.add_resource(MailCheck, '/mail')