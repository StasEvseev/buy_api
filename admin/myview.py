#coding: utf-8
from flask.ext.admin import BaseView, expose


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')