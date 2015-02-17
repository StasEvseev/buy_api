#coding: utf-8
from models import db
from models.good import Good
from models.waybill import WayBill


class WayBillItems(db.Model):
    """
    Позиция в накладной.
    """
    id = db.Column(db.Integer, primary_key=True)

    #накладная
    waybill_id = db.Column(db.Integer, db.ForeignKey('way_bill.id'))
    waybill = db.relationship(WayBill, backref=db.backref('items', lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(Good, backref=db.backref('waybillitems', lazy='dynamic'))

    count = db.Column(db.Integer)

    def __repr__(self):
        return '<WayBillItems %r>' % self.good.full_name or ''