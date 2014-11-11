#coding: utf-8

from flask.ext import restful
from flask.ext.restful import abort, marshal_with, fields, reqparse

from mails.model import Mail
from resources.core import TokenResource, BaseTokeniseResource

from services.mailinvoice import MailInvoiceService, MailInvoiceException
from sqlalchemy import desc, asc


parser = reqparse.RequestParser()
parser.add_argument('filter_field', type=str)
parser.add_argument('filter_text', type=unicode)
parser.add_argument('sort_field', type=str)
parser.add_argument('sort_course', type=str)
parser.add_argument('count', type=int)
parser.add_argument('page', type=int)


class MailCheck(BaseTokeniseResource):
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
    })), 'count': fields.Integer})
    def get(self, **kwargs):
        """
        Получим все почтовые письма.
        """
        args = parser.parse_args()

        filter_field = args['filter_field']
        filter_text = args['filter_text']
        sort_field = args['sort_field']
        sort_course = args['sort_course']
        page = args['page']
        count = args['count']

        query = Mail.query

        if filter_field and filter_text:
            query = query.filter(
                Mail.__table__.columns[filter_field].like("%"+filter_text+"%")
            )
        if sort_field and sort_course:
            query = query.order_by(
                {'desc': desc, 'asc': asc}[sort_course](Mail.__table__.columns[sort_field])
            )
        # query =
        query = query.offset((page - 1) * count).limit(count)
        mails = query.all()
        count_ = query.count()

        return {'items': mails, 'count': count_}