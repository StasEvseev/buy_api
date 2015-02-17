#coding: utf-8

from flask.ext.admin import Admin

from admin.acc import AcceptanceView
from admin.commodityview import CommodityView
from admin.goodview import GoodView, GoodViewPoint, GoodView2
from admin.pointsaleview import PointSaleView
from admin.providerview import ProviderView
from admin.mailview import MailView
from admin.loginview import MyAdminIndexView
from admin.receiverview import ReceiverView
from admin.sellerview import SellerView
from admin.syncview import SyncView
from admin.waybillview import WayBillView, WayBillCustomView


admin = Admin(name=u"Личный кабинет",
              index_view=MyAdminIndexView(name=u"Главная"),
              base_template='my_master.html')

admin.add_view(MailView(name=u'Прием почты', menu_icon_type='glyph', menu_icon_value='fa fa-envelope'))
admin.add_view(AcceptanceView(name=u"Приемки", menu_icon_type='glyph', menu_icon_value='fa fa-cube'))
admin.add_view(WayBillCustomView(name=u"Накладные", menu_icon_type='glyph', menu_icon_value='fa fa-table'))
admin.add_view(GoodViewPoint(name=u"Продукты", menu_icon_type='glyph', menu_icon_value='fa fa-cubes'))