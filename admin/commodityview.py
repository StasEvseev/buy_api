#coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from admin.baseview import BaseViewAuth
from models.commodity import Commodity
from flask.ext import login


class CommodityView(BaseViewAuth):

    form_columns = ('name', 'thematic')
    column_labels = dict(name=u'Наименование', thematic=u'Тематика')
    can_delete = False

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CommodityView, self).__init__(Commodity, session, **kwargs)