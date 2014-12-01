#coding: utf-8
from admin.acceptance import AcceptanceView
from admin.commodityview import CommodityView
from admin.providerview import ProviderView

from flask.ext.admin import Admin

from admin.mailview import MailView
from admin.loginview import MyAdminIndexView

from models import db


admin = Admin(name=u"Личный кабинет", template_mode='bootstrap3', index_view=MyAdminIndexView(),
              base_template='my_master.html')
admin.add_view(MailView(name=u'Прием почты'))
admin.add_view(ProviderView(db.session, name=u'Поставщики'))
admin.add_view(CommodityView(db.session, name=u'Товары'))
admin.add_view(AcceptanceView(db.session, name=u"Приемки"))