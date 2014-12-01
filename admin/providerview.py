#coding: utf-8


from flask.ext.admin.contrib.sqla import ModelView
from models.provider import Provider
from flask.ext import login


class ProviderView(ModelView):
    # Disable model creation
    #can_create = False
    # form_excluded_columns = ['invoices', ]
    form_columns = ('name', 'address', 'emails')
    column_labels = dict(name=u'Наименование', address=u'Адрес', emails=u"Почтовые ящики")
    # Override displayed fields
    column_list = ('name', )#, 'email')
    can_delete = False

    def is_accessible(self):
        return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProviderView, self).__init__(Provider, session, **kwargs)