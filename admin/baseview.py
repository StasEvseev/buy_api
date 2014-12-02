#coding: utf-8
from flask import url_for
from flask.ext.admin import expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext import login
from flask.ext.security import url_for_security
from werkzeug.utils import redirect


class BaseViewAuth(ModelView):

    @expose('/')
    def index_view(self):
        if login.current_user.is_authenticated():
            return super(BaseViewAuth, self).index_view()
        else:
            return redirect('/')

    def inaccessible_callback(self, name, **kwargs):
        return

    def is_accessible(self):
        return login.current_user.is_authenticated()