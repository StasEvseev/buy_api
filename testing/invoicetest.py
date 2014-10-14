#coding: utf-8
from flask import current_app
from app import app
from models import db
from mails.model import Mail
from excel import InvoiceModel
import re

with app.app_context():
    invoice = InvoiceModel(Mail.query.first().file)
    
    print "Номер накладной - ", invoice.number
    print "Дата накладной - ", invoice.date
    print "Сумма без НДС - ", invoice.sum_without_NDS
    print "Сумма с НДС - ", invoice.sum_with_NDS
    print "Сумма НДС - ", invoice.sum_NDS
    print "Вес товара - ", invoice.weight
    print "Отпустил - ", invoice.responsible