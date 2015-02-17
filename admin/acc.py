#coding: utf-8
from flask.ext import login

from admin.core import ProjectAngularView


class AcceptanceView(ProjectAngularView):
    def index_view(self):
        return self.render('acceptance/acceptance.html', token=login.current_user.generate_auth_token())