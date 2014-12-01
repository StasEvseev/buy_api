#coding: utf-8
from models.acceptance import Acceptance


class AcceptanceService(object):
    @classmethod
    def get_all(cls):
        return Acceptance.query.all()