#coding: utf-8
from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.acceptance import Acceptance


class AcceptanceService(object):

    @classmethod
    def get_by_invoice_id(cls, invoice_id):
        try:
            return Acceptance.query.filter(
                Acceptance.invoice_id==invoice_id
            ).one()
        except NoResultFound:
            pass

    @classmethod
    def get_all(cls):
        return Acceptance.query.all()

    @classmethod
    def get_by_id(cls, id):
        return Acceptance.query.get(id)

    @classmethod
    def update_fact_count_items(cls, acceptance_id, date, items, created=False):
        """
        Обновляет фактическое количество у прихода
        """
        from mailinvoice import InvoiceService
        from pointsale import PointSaleService
        acceptance = AcceptanceService.get_by_id(acceptance_id)
        acceptance.date = date

        if acceptance.invoice_id:
            # invoice = acceptance.invoice
            for it in items:
                item_id = it['id']
                count = it['fact_count']
                good_id = it['good_id']
                old_cnt = InvoiceService.get_item_by_id(item_id).fact_count
                InvoiceService.update_fact_count_items(item_id, count)
                if count:
                    pointitem = PointSaleService.get_or_create(acceptance.pointsale_id, good_id)
                    if old_cnt:
                        if created:
                            pointitem.count += count
                        else:
                            pointitem.count += int(count) - old_cnt
                    else:
                        pointitem.count = count
                    db.session.add(pointitem)
        db.session.add(acceptance)

    @classmethod
    def get_or_create_by_invoice_pointsale(cls, invoice_id, pointsale_id):
        """
        Получаем либо создаем приемку товара.
        """
        try:
            acceptance = Acceptance.query.filter(
                Acceptance.invoice_id==invoice_id,
                Acceptance.pointsale_id==pointsale_id).one()
            is_new = False
        except NoResultFound:
            acceptance = Acceptance()
            acceptance.invoice_id = invoice_id
            acceptance.pointsale_id = pointsale_id
            db.session.add(acceptance)
            is_new = True

        return is_new, acceptance