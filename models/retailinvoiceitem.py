#coding: utf-8
from models import db
from models.commodity import Commodity
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

    #Полное наименование
    full_name = db.Column(db.String(250))
    #Продукция
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship(Commodity, backref=db.backref('retailinvoiceitems', lazy='dynamic'))
    #Цена на продукцию
    price_id = db.Column(db.Integer, db.ForeignKey('price.id'))
    price = db.relationship(Price, backref=db.backref('retailinvoiceitems', lazy='dynamic'))

    def __repr__(self):
        return '<RetailInvoiceItem %r>' % self.full_name