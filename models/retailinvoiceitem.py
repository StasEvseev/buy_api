#coding: utf-8
from models import db
from models.commodity import Commodity
from models.good import Good
from models.price import Price
from models.retailinvoice import RetailInvoice


class RetailInvoiceItem(db.Model):
    """
    Позиция в розничной накладной.
    """
    id = db.Column(db.Integer, primary_key=True)

    #Розничная накладная
    retailinvoice_id = db.Column(db.Integer, db.ForeignKey('retail_invoice.id'))
    retailinvoice = db.relationship(RetailInvoice, backref=db.backref('retailinvoiceitems', lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(Good, backref=db.backref('retailinvoiceitems', lazy='dynamic'))

    def __repr__(self):
        return '<RetailInvoiceItem %r>' % self.good.full_name or ''