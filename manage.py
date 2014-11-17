#coding: utf-8
from flask import json
from flask.ext.fixtures import Fixtures

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Command

from app import app
from models import db

from models.commodity import Commodity
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from models.order import Order
from models.orderitem import OrderItem
from models.provider import Provider
from mails.model import Mail
from models.price import Price
from models.retailinvoice import RetailInvoice
from models.retailinvoiceitem import RetailInvoiceItem
from models.good import Good
from models.acceptance import Acceptance
from models.warehouse import WareHouse
from security.model import User#,# Role

migrate = Migrate(app, db)
manager = Manager(app)

class TestConfig(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True
    FIXTURES_DIRS = ['datas/fixtures']

app.config.from_object(TestConfig)
fixtures = Fixtures(app, db)


class FixtureCommand(Command):
    "фикстуры"

    def run(self):

        datas = []
        with open("datas/init.json") as f:
            datas = json.loads(f.read())

        fixtures.load_fixtures(datas)

manager.add_command('db', MigrateCommand)
manager.add_command('fixture', FixtureCommand())

if __name__ == "__main__":
    manager.run()