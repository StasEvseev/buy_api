#coding: utf-8
from admin.baseview import BaseViewAuth
from models.pointsale import PointSale


class PointSaleView(BaseViewAuth):
    # Disable model creation
    #can_create = False
    # form_excluded_columns = ['invoices', ]
    form_columns = ('name', 'address')
    column_labels = dict(name=u'Наименование точки', address=u'Адрес')
    # Override displayed fields
    column_list = ('name', 'address')#, 'email')
    can_delete = False

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    # def action_view(self):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PointSaleView, self).__init__(PointSale, session, **kwargs)