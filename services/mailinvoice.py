#coding: utf-8
from excel import InvoiceModel
from mails.action import get_count_mails, NotConnect, get_mails
from mails.model import Mail
from models import db
from models.invoice import Invoice


class MailInvoiceException(Exception):
    pass


class MailInvoiceService(object):

    @classmethod
    def get_new_mails(cls):
        pass

    @classmethod
    def handle_mail(cls):
        count = cls.get_count_new_mails()
        if count > 0:
            mails = get_mails()
            for mail in mails:
                ml = Mail(title=mail.title, date=mail.date_, from_=mail.from_, to=mail.to_, file=mail.file_)

                invoice = InvoiceModel(ml.file)

                db.session.add(ml)
                db.session.commit()

    @classmethod
    def get_count_new_mails(cls):
        try:
            return get_count_mails()
        except NotConnect as err:
            raise MailInvoiceException(err)