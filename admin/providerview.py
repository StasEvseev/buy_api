#coding: utf-8


from flask.ext.admin.contrib.sqla import ModelView
from models.provider import Provider


class ProviderView(ModelView):
    # Disable model creation
    can_create = False

    # Override displayed fields
    column_list = ('login', 'email')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(ProviderView, self).__init__(Provider, session, **kwargs)