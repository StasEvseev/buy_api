#coding: utf-8
from models import db
# from invoice import Invoice


class Receiver(db.Model):
    """
    Получатель.
    """
    id = db.Column(db.Integer, primary_key=True)
    #Номер
    fname = db.Column(db.String(250))
    lname = db.Column(db.String(250))
    pname = db.Column(db.String(250))

    address = db.Column(db.String(250))

    passport = db.Column(db.String(250))

    @property
    def fullname(self):
        return " ".join([self.lname or "", self.fname or "", self.pname or ""])



    #Основание
    # invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    # invoice = db.relationship(Invoice, backref=db.backref('retailinvoices', lazy='dynamic'))

    #Файл накладной
    # file = db.Column(db.String)

    # def __repr__(self):
    #     return '<RetailInvoice %r>' % self.number