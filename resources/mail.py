#coding: utf-8

from flask.ext import restful
from flask.ext.restful import abort, marshal_with, fields, reqparse

# from mails.action import get_count_mails, NotConnect, get_mails
from mails.model import Mail
from services.mailinvoice import MailInvoiceService, MailInvoiceException
# from models import db
from sqlalchemy import desc


parser = reqparse.RequestParser()
parser.add_argument('length', type=int)
parser.add_argument('start', type=int)


class MailCheck(restful.Resource):

    @marshal_with({'data': fields.List(fields.Nested({
        'date': fields.DateTime,
        'title': fields.String,
        'from': fields.String(attribute='from_'),
        'is_handling': fields.Boolean
    }))})
    def get(self, **kwargs):
        args = parser.parse_args()

        try:
            MailInvoiceService.handle_mail()
            # pass
        except MailInvoiceException as err:
            abort(404, message=unicode(err))

        mails = Mail.query.order_by(desc(Mail.date)).offset(args['start']).limit(args['length']).all()

        return {'data': mails}