#coding: utf-8
from sqlalchemy import UniqueConstraint

from models import db
from models.invoice import Invoice
from models.pointsale import PointSale
from models.waybill import WayBill


class Acceptance(db.Model):
    """
    Приемка товара
    """
    id = db.Column(db.Integer, primary_key=True)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(PointSale, backref=db.backref('acceptances', lazy=True))
    #Накладная основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), unique=True)
    invoice = db.relationship(Invoice,
        backref=db.backref('acceptance', uselist=False))
    waybill_id = db.Column(db.Integer, db.ForeignKey('way_bill.id'), unique=True)
    waybill = db.relationship(WayBill, backref=db.backref('acceptance', uselist=False))
    #Дата приема товара
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Acceptance %r>' % self.name