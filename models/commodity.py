#coding: utf-8
from models import db


class Commodity(db.Model):
    """
    Единица товара
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    thematic = db.Column(db.String(250))


    def __repr__(self):
        return '<Commodity %r>' % self.name