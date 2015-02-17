#coding: utf-8

from tests.suits import BaseSuite
from models.provider import Provider
from models import db


class ProviderTestSuite(BaseSuite):
    EMAIL = "stas@mail.ru"

    def create_test_provider(self):
        with self.application.app_context():
            provider = Provider(name='name', address='address', emails=self.EMAIL)
            db.session.add(provider)
            db.session.commit()
            return provider.id, provider.name, provider.address, provider.emails