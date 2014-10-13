#coding: utf-8
from models import db


class Order(db.Model):
    """
    Модель заказа
    """
    id = db.Column(db.Integer, primary_key=True)
    #Заказ с
    date_start = db.Column(db.Date)
    #Заказ по
    date_end = db.Column(db.Date)
    #Поставщик
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider',
        backref=db.backref('orders', lazy='dynamic'))

    def __repr__(self):
        return '<Order from %r>' % self.provider.name