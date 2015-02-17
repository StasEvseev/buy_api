#coding: utf-8

from flask import request

from flask.ext.restful import marshal_with, fields, abort

from sqlalchemy.exc import IntegrityError
from resources import Date

from resources.core import BaseTokeniseResource, BaseCanoniseResource

from services import AcceptanceService, HelperService, InvoiceService

from models import db
from models.acceptance import Acceptance


class AcceptanceCanon(BaseCanoniseResource):
    model = Acceptance

    attr_json = {
        'id': fields.Integer,
        'date': Date,
        'invoice_id': fields.Integer,
        'invoice_str': fields.String(attribute='invoice'),
        'provider_id': fields.String(attribute='invoice.provider_id'),
        'provider_name': fields.String(attribute='invoice.provider.name'),
        'pointsale_id': fields.Integer,
        'pointsale_name': fields.String(attribute='pointsale.name')
    }

    def pre_save(self, obj, data):
        obj = super(AcceptanceCanon, self).pre_save(obj, data)

        obj.date = HelperService.convert_to_pydate(data['date'])

        return obj


    def post_save(self, obj, data, create_new=False):
        super(AcceptanceCanon, self).post_save(obj, data, create_new)

        items = data['items'] if 'items' in data else []

        AcceptanceService.update_fact_count_items(obj.id, obj.date, items)


class AcceptanceResource(BaseTokeniseResource):
    pass

class AcceptanceRemainItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'good_id': fields.Integer,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'count': fields.String
    }))})
    def get(self, id):
        return {'items': InvoiceService.get_items_acceptance(id)}


class AcceptanceHelperResource(BaseTokeniseResource):
    pass


class AcceptanceItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'good_id': fields.Integer,
        "price_without_NDS": fields.String,
        "price_with_NDS": fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'count': fields.String,
        'fact_count': fields.String
    }))})
    def get(self, id):

        return {'items': InvoiceService.get_items_acceptance(id, remain=False)}

class AcceptanceIdResource(BaseTokeniseResource):
    """
    Ресурс для работы с единицей приемки.
    """
    def post(self, id):
        data = request.json['data']

        date = data['date']
        items = data['items']

        AcceptanceService.update_fact_count_items(id, HelperService.convert_to_pydate(date), items)

        try:
            db.session.commit()
        except Exception as exc:
            abort(400, message=unicode(exc))

        return "ok"



class AcceptanceInvoiceItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'good_id': fields.Integer,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'count': fields.String
    }))})
    def get(self, acc_id, invoice_id):

        return {'items': InvoiceService.get_item_to_acceptance(invoice_id, acc_id)}



class AcceptanceSaleInvoiceResource(BaseTokeniseResource):
    """
    Приход товара на точку по выбранной накладной.
    """
    def post(self, point_id, invoice_id):
        """
        Сохраняем(обновляем) количество пришедшего товара у накладной.

        Параметры:

        point_id - точка-приемник.
        invoice_id - накладная в системе.
        """
        data = request.json['data']

        date = data['date']
        date = HelperService.convert_to_pydate(date)
        items = data['items']

        is_new, acceptance = AcceptanceService.get_or_create_by_invoice_pointsale(invoice_id, point_id)
        acceptance.date = date

        if is_new:
            db.session.flush()
            # db.session.commit()

        AcceptanceService.update_fact_count_items(acceptance.id, date, items)
        db.session.add(acceptance)
        try:
            db.session.commit()
        except IntegrityError:
            abort(400, message=u"Нельзя делать приход одной накладной в две разные точки.")
            # return "error"

        return "ok"