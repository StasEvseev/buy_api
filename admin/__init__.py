#coding: utf-8

from flask.ext.admin import Admin

from admin.myview import MyView, InvoiceView


admin = Admin(name="Home Proj")
admin.add_view(MyView(name=u'Проверка почты'))
# admin.add_view(InvoiceView(name=u'накладная'))