#coding: utf-8
from models import db


class OrderItem(db.Model):
    """
    Позиция в заказе.
    """
    id = db.Column(db.Integer, primary_key=True)
    #Название издания
    name = db.Column(db.String(250))
    #Ориент. дата выхода
    date = db.Column(db.Date)
    #Рем%
    remission = db.Column(db.DECIMAL)
    #НДС%
    NDS = db.Column(db.DECIMAL)
    #Заказ клиента
    count = db.Column(db.Integer)

    #Пред цена
    price_prev = db.Column(db.Float)
    #Пост цена
    price_post = db.Column(db.Float)

    #Заказ
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order',
        backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<OrderItem %r>' % self.name