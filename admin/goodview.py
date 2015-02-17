#coding: utf-8
from flask.ext import login

from admin.baseview import BaseViewAuth
from admin.core import ProjectAngularView

from models.good import Good

from resources import GoodsResource


class GoodView(BaseViewAuth):

    form_columns = ('full_name', 'barcode', )
    column_labels = {
        'full_name': u'Полное наименование',
        'barcode': u"Штрих код",
        'is_confirm': u'Товар получен',
        'invoiceitem.invoice.number': u'Накладная',
        'invoiceitem.invoice.provider.name': u'Поставщик',
        'invoiceitem.invoice.acceptance.date': u'Дата приема'}
    column_list = ('full_name', 'barcode', 'is_confirm', 'invoiceitem.invoice.acceptance.date',
                   'invoiceitem.invoice.number', 'invoiceitem.invoice.provider.name')
    can_delete = False
    can_create = False
    can_edit = False
    column_filters = ('full_name', 'barcode')

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GoodView, self).__init__(Good, session, **kwargs)


class ResGood(object):

    def __init__(self, res, url):
        self.res = res
        self.url = url

    @property
    def name(self):
        return self.res.__class__.__name__

    @property
    def full_path(self):
        return "/api" + self.url

res = ResGood(GoodsResource, '/good')


class GoodView2(ProjectAngularView):
    model = Good

    columns = (
        (u'Полное наименование', 'full_name'),
        (u'Номер локальный', 'number_local'),
        (u'Номер глобальный', 'number_global')
    )

    is_selected = True

    res_table = res

    resource = (res, )

    def __init__(self, session, **kwargs):
        self.session = session
        super(GoodView2, self).__init__(**kwargs)

    def index_view(self):

        return self.render(self.page(),
                           list_columns=self.columns,
                           res_table=self.res_table,
                           list_res=self.resource,
                           is_selected=self.is_selected,
                           token=login.current_user.generate_auth_token())

    def page(self):
        return 'test/main.html'




class GoodViewPoint(ProjectAngularView):
    def index_view(self):
        return self.render('good/good.html',
                           token=login.current_user.generate_auth_token())