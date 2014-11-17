#coding: utf-8
from models import db
from models.good import Good


class InvoiceItem(db.Model):
    """
    Элемент приходной накладной
    """
    id = db.Column(db.Integer, primary_key=True)

    #Полное наименование издания
    full_name = db.Column(db.String(250))
    #Название издания
    name = db.Column(db.String(250))
    #Номер издания
    number_local = db.Column(db.String(250))

    number_global = db.Column(db.String(250))

    #Заказ
    count_order = db.Column(db.Integer)
    #Дозак
    count_postorder = db.Column(db.Integer)
    #Количество
    count = db.Column(db.Integer)

    #"Цена Без НДС, руб."
    price_without_NDS = db.Column(db.DECIMAL)
    #"Цена с НДС, руб."
    price_with_NDS = db.Column(db.DECIMAL)
    #Сумма без НДС, руб.
    sum_without_NDS = db.Column(db.DECIMAL)
    #Сумма НДС, руб.
    sum_NDS = db.Column(db.DECIMAL)
    #Ставка НДС
    rate_NDS = db.Column(db.DECIMAL)
    #Сумма с учетом НДС, руб.
    sum_with_NDS = db.Column(db.DECIMAL)

    #Тематика изд.
    thematic = db.Column(db.String(250))
    #Целых пачек
    count_whole_pack = db.Column(db.Integer)
    #Россыпь (экз.)
    placer = db.Column(db.Integer)

    #Накладная
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship('Invoice',
        backref=db.backref('items', lazy='dynamic'))

    #Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(Good, backref=db.backref('invoiceitems', lazy='dynamic'))

    def __repr__(self):
        return '<InvoiceItem %r>' % self.name