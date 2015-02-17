#coding: utf-8

from models import db
from models.commodity import Commodity
from models.invoice import Invoice
from models.price import Price


class Good(db.Model):
    """
    Товар
    """
    id = db.Column(db.Integer, primary_key=True)
    #количество
    # count = db.Column(db.Integer)
    #штрих код
    barcode = db.Column(db.BigInteger)

    #Полное наименование
    full_name = db.Column(db.String(250))
    #Продукция
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship(Commodity, backref=db.backref('goods', lazy='dynamic'))

    number_local = db.Column(db.String(250))
    number_global = db.Column(db.String(250))
    #Цена на продукцию
    price_id = db.Column(db.Integer, db.ForeignKey('price.id'))
    price = db.relationship(Price, backref=db.backref('goods', lazy='dynamic'))

    #подтвержден товар
    # is_confirm = db.Column(db.BOOLEAN, default=False)


    # def invoice(self):
    #     return Invoice.query.filter(Invoice.id==self.invoiceitem.invoice_id).one()