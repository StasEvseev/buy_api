#coding: utf-8

from models import db


class WareHouse(db.Model):
    """
    Склад товара
    """
    id = db.Column(db.Integer, primary_key=True)

    #Наименование склада
    name = db.Column(db.String(250))
    #адрес склада
    address = db.Column(db.String(250))