#coding: utf-8

from flask.ext.admin import Admin

from admin.myview import MyView, InvoiceView


admin = Admin(name="Home Proj", template_mode='bootstrap3')
admin.add_view(MyView(name=u'Прием почты'))
# admin.add_view(InvoiceView(name=u'накладная'))