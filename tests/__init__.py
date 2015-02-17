#coding: utf-8
import base64
import os
import unittest
import sys
from flask import json
import app
from manage import man
from werkzeug.datastructures import Headers

CURRENT_DIR = os.path.dirname(__file__)
PATH_DB = os.path.join(CURRENT_DIR, "app.db")

class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)

        self.module = app
        self.application = self.module.app

    def setUp(self):
        try:
            os.remove(PATH_DB)
        except OSError:
            pass
        self.application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+PATH_DB #(COMMON_URL % (USER, PASSWORD, "test"))
        self.application.config['TESTING'] = True
        self.client = self.module.app.test_client()

        old_argv = sys.argv
        sys.argv = []
        sys.argv.append("manage.py")
        sys.argv.append("db")
        sys.argv.append("upgrade")

        man.run()

        sys.argv = old_argv

        self.__initialize()

        self.set_up()

    def __initialize(self):
        """
        Инициализация БД. Нужен как минимум один пользователь.
        """
        data = self.application.test_client().post("/admin/register/", data={
                    'login': 'I',
                    'email': 'a@a2.ru',
                    'password': 'I'
                }, follow_redirects=True)
        assert data.status_code, 200
        assert "Добро пожаловать!" in data.data

    def tearDown(self):
        os.remove(PATH_DB)
        self.tear_down()

    def _serialize(self, dict):
        return json.dumps(dict)

    def _deserialize(self, data):
        return json.loads(data)

    def set_up(self):
        pass

    def tear_down(self):
        pass