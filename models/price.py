#coding: utf-8
from models import db


class Price(db.Model):
    """
    Единица товара
    """
    id = db.Column(db.Integer, primary_key=True)

    # commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    # commodity = db.relationship('Commodity', backref=db.backref('prices', lazy='dynamic'))
    #
    # number_local = db.Column(db.String(250))
    # number_global = db.Column(db.String(250))
    #
    # date_from = db.Column(db.Date)

    # NDS = db.Column(db.DECIMAL)
    # #Пред цена
    # price_prev = db.Column(db.DECIMAL)
    # #Пост цена
    # price_post = db.Column(db.DECIMAL)

    #Розничная цена
    price_retail = db.Column(db.DECIMAL)
    #Оптовая цена
    price_gross = db.Column(db.DECIMAL)

    #name = db.Column(db.String(250))
    #thematic = db.Column(db.String(250))


    def __repr__(self):
        return '<Price to %r from %s (%s, %s)>' % (self.commodity.name, self.date_from, self.price_retail or "", self.price_gross or "")


class PriceParish(db.Model):
    """
    Цена прихода
    """
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'), nullable=False)
    commodity = db.relationship('Commodity', backref=db.backref('priceparish', lazy='dynamic'))

    number_local_from = db.Column(db.String(250))
    number_global_from = db.Column(db.String(250))

    date_from = db.Column(db.Date)

    NDS = db.Column(db.DECIMAL)
    #Пред цена
    price_prev = db.Column(db.DECIMAL)
    #Пост цена
    price_post = db.Column(db.DECIMAL, nullable=False)

    price_id = db.Column(db.Integer, db.ForeignKey('price.id'), nullable=False)
    price = db.relationship('Price', backref=db.backref('priceparish', lazy='dynamic'))
    #Накладная основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    invoice = db.relationship('Invoice', backref=db.backref('priceparish', lazy='dynamic'))