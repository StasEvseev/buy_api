#coding: utf-8
from flask.ext.admin.base import AdminViewMeta, expose, BaseView
from flask.ext import login
from werkzeug.utils import redirect


class AngularMeta(AdminViewMeta):
    def __init__(cls, classname, bases, fields):
        super(AngularMeta, cls).__init__(classname, bases, fields)

        for p in dir(cls):
            if p == 'index':
                @expose('/<path:path>')
                def ind(self, *args, **kwargs):
                    return self.index()
                cls.ind = ind

class AngularView(BaseView):
    """
    Базовый класс для выюшек ангуляра.
    Всего один метод view - index - ловит все субурлы и передает ему.
    """
    __metaclass__ = AngularMeta

    @expose('/')
    def index(self):
        pass


class ProjectAngularView(AngularView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect('/')
        return self.index_view()

    def index_view(self):
        pass