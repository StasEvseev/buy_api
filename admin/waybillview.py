#coding: utf-8
from flask.ext.admin import expose
from admin.baseview import BaseViewAuth
from admin.core import AngularView, ProjectAngularView
from models.waybill import WayBill
from flask.ext import login


class WayBillView(BaseViewAuth):
    column_labels = dict(number=u'Номер', date=u'Дата', rec=u"Получатель", typeS=u"Тип")
    column_list = ('number', 'date', 'rec', 'typeS')#, 'email')
    can_delete = False
    can_create = False

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(WayBillView, self).__init__(WayBill, session, **kwargs)


class WayBillCustomView(ProjectAngularView):
    def index_view(self):
        return self.render('waybill/waybill.html',
            token=login.current_user.generate_auth_token())