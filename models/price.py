#coding: utf-8
from models import db


class Price(db.Model):
    """
    Единица товара
    """
    id = db.Column(db.Integer, primary_key=True)

    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship('Commodity', backref=db.backref('prices', lazy='dynamic'))

    number_from = db.Column(db.String(250))

    NDS = db.Column(db.DECIMAL)
    #Пред цена
    price_prev = db.Column(db.DECIMAL)
    #Пост цена
    price_post = db.Column(db.DECIMAL)

    #name = db.Column(db.String(250))
    #thematic = db.Column(db.String(250))


    def __repr__(self):
        return '<Price %r>' % self.name