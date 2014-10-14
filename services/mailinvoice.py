#coding: utf-8
from excel import InvoiceModel
from mails.action import get_count_mails, NotConnect, get_mails
from mails.model import Mail
from models import db
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem


class MailInvoiceException(Exception):
    pass


class MailInvoiceService(object):

    @classmethod
    def get_new_mails(cls):
        pass

    @classmethod
    def handle_mail(cls):
        """
        Метод обрабатывает почтовый ящик
        """
        count = cls.get_count_new_mails()
        if count > 0:
            mails = get_mails()
            for mail in mails:
                ml = Mail(title=mail.title, date=mail.date_, from_=mail.from_, to=mail.to_, file=mail.file_)

                invoice = InvoiceModel(ml.file)

                invmodel = Invoice(
                    number=invoice.number, date=invoice.date, mail=ml,
                    sum_without_NDS=invoice.sum_without_NDS, sum_with_NDS=invoice.sum_with_NDS,
                    sum_NDS=invoice.sum_NDS, weight=invoice.weight, responsible=invoice.responsible)

                products = invoice.get_products()
                db.session.add(ml)
                db.session.add(invmodel)

                for product in products:
                    invitem = InvoiceItem(
                        full_name=product.full_name, name=product.name, number=product.number,
                        count_order=product.count_order, count_postorder=product.count_postorder,
                        count=product.count, price_without_NDS=product.price_without_NDS,
                        price_with_NDS=product.price_with_NDS, sum_without_NDS=product.sum_without_NDS,
                        sum_NDS=product.sum_NDS, rate_NDS=product.rate_NDS, sum_with_NDS=product.sum_with_NDS,
                        thematic=product.thematic, count_whole_pack=product.count_whole_pack,
                        placer=product.placer, invoice=invmodel)
                    db.session.add(invitem)

                db.session.commit()

    @classmethod
    def get_count_new_mails(cls):
        try:
            return get_count_mails()
        except NotConnect as err:
            raise MailInvoiceException(err)