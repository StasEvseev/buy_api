#coding: utf-8
from datetime import datetime
from flask import url_for
from sqlalchemy import asc
from models import db
from invoice import Invoice
from models.pointsale import PointSale
from models.receiver import Receiver


class WayBill(db.Model):
    """
    накладная.
    """
    id = db.Column(db.Integer, primary_key=True)
    #Номер
    number = db.Column(db.String(250))
    #Дата накладной
    date = db.Column(db.Date)

    #Торговая точка - откуда пересылают товар
    pointsale_from_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale_from = db.relationship(PointSale, foreign_keys='WayBill.pointsale_from_id', backref=db.backref('from_waybills', lazy='dynamic'))

    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'))
    receiver = db.relationship(Receiver, backref=db.backref('waybills', lazy='dynamic'))

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(PointSale, foreign_keys='WayBill.pointsale_id', backref=db.backref('waybills', lazy='dynamic'))

    type = db.Column(db.Integer)
    #Основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(Invoice, backref=db.backref('waybills', lazy='dynamic'))

    #Файл накладной
    file = db.Column(db.String)

    @property
    def rec(self):
        if self.receiver:
            return self.receiver.fullname
        elif self.pointsale:
            return self.pointsale.name
        else:
            return "Накладная не имеет получателя"

    @property
    def typeS(self):
        return TYPE[self.type]

    @property
    def filepath(self):
        return url_for('static', filename='files/' + self.file.split("/")[-1])

    def __repr__(self):
        return '<WayBill %r>' % self.number

RETAIL = 1
GROSS = 2
TYPE = {RETAIL: u"Розничная", GROSS: u"Оптовая"}
