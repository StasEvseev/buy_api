#coding: utf-8
from models import db


class Provider(db.Model):
    """
    Поставщик
    """
    id = db.Column(db.Integer, primary_key=True)
    #Наименование
    name = db.Column(db.String(250))

    address = db.Column(db.String(250))

    emails = db.Column(db.String(250))

    def __repr__(self):
        return '<Provider %r>' % self.name

    def get_emails(self):
        if self.emails:
            return self.emails.split(",")
        return []