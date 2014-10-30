#coding: utf-8


from flask import url_for
from flask.ext.admin import expose
from flask.ext import admin, login
from flask import redirect, request
from flask.ext.admin import helpers
from security import User
from security.form import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash

from models import db


class MyAdminIndexView(admin.AdminIndexView):
    """
    Базовая вьюха админки
    """

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
            from flask import session
            session.permanent = True

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))
        # link = u'<p>Не имеете аккаунта? <a href="' + url_for('.register_view') + u'">Нажмите для регистрации.</a></p>'
        self._template_args['form'] = form
        # self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    # @expose('/register/', methods=('GET', 'POST'))
    # def register_view(self):
    #     form = RegistrationForm(request.form)
    #     if helpers.validate_form_on_submit(form):
    #         user = User()
    #
    #         form.populate_obj(user)
    #         # we hash the users password to avoid saving it as plaintext in the db,
    #         # remove to use plain text:
    #         user.password = generate_password_hash(form.password.data)
    #
    #         db.session.add(user)
    #         db.session.commit()
    #
    #         login.login_user(user)
    #         return redirect(url_for('.index'))
    #     link = u'<p>Уже имеете аккаунт? <a href="' + url_for('.login_view') + u'">Нажмите для входа.</a></p>'
    #     self._template_args['form'] = form
    #     self._template_args['link'] = link
    #     return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))