#coding: utf-8

from flask.ext.admin import Admin

from admin.mailview import MailView, InvoiceView


admin = Admin(name="Home Proj", template_mode='bootstrap3')
admin.add_view(MailView(name=u'Прием почты'))