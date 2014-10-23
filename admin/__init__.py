#coding: utf-8
# from admin.providerview import ProviderView

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from admin.mailview import MailView
from admin.loginview import MyAdminIndexView
from models import db
from models.provider import Provider


admin = Admin(name=u"Личный кабинет", template_mode='bootstrap3', index_view=MyAdminIndexView(),
              base_template='my_master.html')
admin.add_view(MailView(name=u'Прием почты'))
admin.add_view(ModelView(Provider, db.session))