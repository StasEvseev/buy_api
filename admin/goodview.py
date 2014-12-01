#coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login
from flask.ext.admin.model import InlineFormAdmin
from models.good import Good


class GoodView(ModelView):

    form_columns = ('full_name', 'count', 'barcode', )
    column_labels = {
        'full_name': u'Полное наименование',
        'count': u'Количество',
        'barcode': u"Штрих код",
        'is_confirm': u'Товар получен',
        'invoiceitem.invoice': u'Накладная',
        'invoiceitem.invoice.provider.name': u'Поставщик',
        'invoiceitem.invoice.acceptance.date': u'Дата приема'}
    column_list = ('full_name', 'count', 'barcode', 'is_confirm', 'invoiceitem.invoice.acceptance.date',
                   'invoiceitem.invoice', 'invoiceitem.invoice.provider.name')
    can_delete = False
    can_create = False
    can_edit = False
    column_filters = ('full_name', 'barcode')

    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GoodView, self).__init__(Good, session, **kwargs)