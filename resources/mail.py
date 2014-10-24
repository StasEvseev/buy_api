#coding: utf-8

from flask.ext import restful
from flask.ext.restful import abort, marshal_with, fields, reqparse

from mails.model import Mail
from resources.core import TokenResource

from services.mailinvoice import MailInvoiceService, MailInvoiceException
from sqlalchemy import desc


parser = reqparse.RequestParser()
parser.add_argument('length', type=int)
parser.add_argument('start', type=int)


class MailCheck(TokenResource):
    """
    Ресурс для работы с почтой.
    """



    def post(self):
        """
        Запрос на обработку почтового ящика(проверка новых писем и сохранение их в БД).
        """
        try:
            MailInvoiceService.handle_mail()
        except MailInvoiceException as err:
            abort(404, message=unicode(err))
        return 'ok'

    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'date': fields.String,
        'title': fields.String,
        'from': fields.String(attribute='from_'),
        'is_handling': fields.Boolean,
        'invoice_id': fields.Integer
    }))})
    def get(self, **kwargs):
        """
        Получим все почтовые письма.
        """
        args = parser.parse_args()

        mails = Mail.query.order_by(desc(Mail.date)).offset(args['start']).limit(args['length']).all()

        return {'items': mails}