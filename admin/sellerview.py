#coding: utf-8

from admin.baseview import BaseViewAuth
# from models.pointsale import PointSale
from models.seller import Seller


class SellerView(BaseViewAuth):
    # Disable model creation
    #can_create = False
    # form_excluded_columns = ['invoices', ]
    form_columns = ('lname', 'fname', 'pname', 'address', 'passport')
    column_labels = dict(fullname=u'Полное имя', address=u'Адрес', fname=u'Имя', lname=u'Фамилия', pname=u'Отчество',
                         passport=u'Паспортные данные')
    # Override displayed fields
    column_list = ('fullname', 'address', )#, 'email')
    can_delete = False
    # can_delete = False

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    # def action_view(self):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SellerView, self).__init__(Seller, session, **kwargs)