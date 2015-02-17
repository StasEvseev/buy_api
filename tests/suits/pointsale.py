#coding: utf-8
from tests.suits import BaseSuite

from models.pointsale import PointSale
from models import db

class PointSaleSuite(BaseSuite):

    def create_test_pointsale(self, name, address):
        # with self.application.app_context():
        pointsale = PointSale(name=name, address=address)
        db.session.add(pointsale)
        db.session.commit()
        return pointsale