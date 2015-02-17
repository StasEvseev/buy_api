#coding: utf-8

from flask.ext.restful import abort, marshal_with, fields
from log import warning, debug

from mails.model import Mail

from resources import InvoiceItemResource
from resources.core import BaseTokeniseResource, BaseTokenMixinResource, BaseModelPackResource

from services import MailInvoiceService, MailInvoiceException


class MailInvoiceItem(BaseTokeniseResource):
    def get(self, id):
        mail = MailInvoiceService.get_mail(id)
        return InvoiceItemResource().get(mail.invoice_id)



class MailCheck(BaseTokenMixinResource, BaseModelPackResource):
    """
    Ресурс для работы с почтой.
    """

    model = Mail

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
        'invoice_id': fields.Integer,
        'provider_id': fields.Integer(attribute='invoice.provider_id'),
        'provider': fields.String(attribute='invoice.provider.name')
    })), 'count': fields.Integer})
    def get(self, **kwargs):
        """
        Получим все почтовые письма.
        """
        result = super(MailCheck, self).get()

        return {'items': result['items'], 'count': result['count']}