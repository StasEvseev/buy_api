#coding: utf-8
from flask import json
from flask.ext.fixtures import Fixtures

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Command

from app import app
from models import db

from models.pointsale import PointSale
from models.seller import Seller
from models.receiver import Receiver
from models.waybill import WayBill
from models.waybillitem import WayBillItems
from models.commodity import Commodity
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from models.order import Order
from models.orderitem import OrderItem
from models.provider import Provider
from mails.model import Mail
from models.price import Price, PriceParish
from models.retailinvoice import RetailInvoice
from models.retailinvoiceitem import RetailInvoiceItem
from models.good import Good
from models.acceptance import Acceptance
from models.warehouse import WareHouse
from models.pointsaleitem import PointSaleItem
from security.model import User#,# Role
from models.sync import Sync

class MyMan(Manager):

    def run(self, commands=None, default_command=None):
        import sys
        """
        Prepares manager to receive command line input. Usually run
        inside "if __name__ == "__main__" block in a Python script.

        :param commands: optional dict of commands. Appended to any commands
                         added using add_command().

        :param default_command: name of default command to run if no
                                arguments passed.
        """

        if commands:
            self._commands.update(commands)

        if default_command is not None and len(sys.argv) == 1:
            sys.argv.append(default_command)

        try:
            result = self.handle(sys.argv[0], sys.argv[1:])
        except SystemExit as e:
            result = e.code
            sys.exit(result or 0)


man = MyMan(app)
man.add_command('db', MigrateCommand)

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