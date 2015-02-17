#coding: utf-8
from flask.ext import login
from admin.core import ProjectAngularView


class MailView(ProjectAngularView):
    def index_view(self):
        # from app import app
        # app.logger.error("Солнышко! Как дела?")
        return self.render('mail/mail.html', token=login.current_user.generate_auth_token())