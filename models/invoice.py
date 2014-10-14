#coding: utf-8
from models import db
from provider import Provider


class Invoice(db.Model):
    """
    Приходная накладная.
    """
    id = db.Column(db.Integer, primary_key=True)
    #Номер
    number = db.Column(db.String(250))
    #Дата накладной
    date = db.Column(db.Date)
    #Поставщик
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(Provider,
        backref=db.backref('invoices', lazy='dynamic'))

    mail_id = db.Column(db.Integer, db.ForeignKey('mails.id'))
    mail = db.relationship('Mail', backref=db.backref('mails', lazy='dynamic'))

    #Сумма без НДС, руб.
    sum_without_NDS = db.Column(db.DECIMAL)
    #Сумма с учетом НДС, руб.
    sum_with_NDS = db.Column(db.DECIMAL)
    #Сумма НДС, руб.
    sum_NDS = db.Column(db.DECIMAL)

    #Вес товара
    weight = db.Column(db.DECIMAL)
    #Отпустил
    responsible = db.Column(db.String(250))

    def __repr__(self):
        return '<Invoice %r>' % self.number