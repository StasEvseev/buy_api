#coding: utf-8

from models import db
from models.invoice import Invoice


class Acceptance(db.Model):
    """
    Приемка товара
    """
    id = db.Column(db.Integer, primary_key=True)

    #Накладная основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(Invoice,
        backref=db.backref('acceptances', lazy='dynamic'))
    #Дата приема товара
    date = db.Column(db.Date)

    def __repr__(self):
        return '<Acceptance %r>' % self.name