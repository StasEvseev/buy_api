#coding: utf-8
from models import db


class Price(db.Model):
    """
    Единица товара
    """
    id = db.Column(db.Integer, primary_key=True)

    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship('Commodity', backref=db.backref('prices', lazy='dynamic'))

    number_local = db.Column(db.String(250))
    number_global = db.Column(db.String(250))

    date_from = db.Column(db.Date)

    NDS = db.Column(db.DECIMAL)
    #Пред цена
    price_prev = db.Column(db.DECIMAL)
    #Пост цена
    price_post = db.Column(db.DECIMAL)

    #Розничная цена
    price_retail = db.Column(db.DECIMAL)
    #Оптовая цена
    price_gross = db.Column(db.DECIMAL)

    #name = db.Column(db.String(250))
    #thematic = db.Column(db.String(250))


    def __repr__(self):
        return '<Price %r>' % self.name