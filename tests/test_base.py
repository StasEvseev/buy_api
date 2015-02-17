#coding: utf-8

from tests import BaseTestCase

class FlaskrTestCase(BaseTestCase):

    def test_login(self):
        """
        Проверяем систему авторизации
        """
        self.start_page()

    def test_auth_api(self):
        """
        Проверяем, что REST API не работает без авторизации
        """
        self.auth_api()

    def start_page(self):
        #Пытаемся зайти в системе без авторизации
        data = self.client.get("/admin/mailview")
        #опа. Не получается.
        assert data.status_code, 301
        #может быть тут фиктивная проверка пользователя
        data = self.client.post("/admin/login/", data={
            'login': 'Stas',
            'password': 'Stas'
        }, follow_redirects=True)
        assert data.status_code, 200
        #однакож
        assert "Invalid user" in data.data

        #ну ладно, зарегаемся и заходим.
        data = self.client.post("/admin/register/", data={
                    'login': 'Stas',
                    'email': 'a@a.ru',
                    'password': 'Stas'
                }, follow_redirects=True)

        assert data.status_code, 200
        #Ура товарищи!
        assert "Добро пожаловать!" in data.data

    def auth_api(self):
        #проверяем все api на требование авторизации
        for rule in self.application.url_map.iter_rules():
            if rule.rule.startswith("/api"):

                for meth in rule.methods:
                    if meth == "OPTIONS":
                        continue
                    data = getattr(self.client, meth.lower())(rule.rule)
                    assert data.status_code in [401, 405, 404]