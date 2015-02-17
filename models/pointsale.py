#coding: utf-8
from models import db


class PointSale(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # fname = db.Column(db.String(250))
    # lname = db.Column(db.String(250))
    name = db.Column(db.String(250))

    address = db.Column(db.String(250))



    # passport = db.Column(db.String(250))


    pass