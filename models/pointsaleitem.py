#coding: utf-8
from models import db
from models.good import Good
from models.pointsale import PointSale


class PointSaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(PointSale, backref=db.backref('items', lazy=True))

    #Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(Good, backref=db.backref('pointsaleitems', uselist=False))

    count = db.Column(db.Integer)