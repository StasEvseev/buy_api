#coding: utf-8

from flask import request

from flask.ext.restful import marshal_with, fields, abort
from sqlalchemy import asc

from models import db
from models.invoiceitem import InvoiceItem

from resources.core import  BaseTokeniseResource

from services import HelperService, InvoiceService


class InvoiceIdResource(BaseTokeniseResource):
    def post(self, id):
        from services import AcceptanceService
        invoice = InvoiceService.get_by_id(id)
        data = request.json['data']

        items = data['items']
        pointsale_id = data['pointsale_id']
        date = data['date']
        date = HelperService.convert_to_pydate(date)

        try:
            invoice = InvoiceService.save_from_json(date, items, invoice=invoice)
            is_new, acceptance = AcceptanceService.get_or_create_by_invoice_pointsale(invoice.id, pointsale_id)
            acceptance.date = date
            # if is_new:
            db.session.commit()

            AcceptanceService.update_fact_count_items(acceptance.id, date, [{'id': x.id,
                                                                             'fact_count': x.count,
                                                                             'good_id': x.good_id} for x in invoice.items])
            db.session.add(acceptance)
            db.session.commit()
        except Exception:
            abort(400, message=u"Ошибка!!!!")
        return "ok"

class InvoiceResource(BaseTokeniseResource):
    """
    Ресурс для получения всех накладных.
    """

    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'number': fields.String,
        'date': fields.String,
        'provider_id': fields.Integer,
        'provider_name': fields.String(attribute='provider.name'),
        'is_acceptance': fields.Boolean,
        'acceptance_id': fields.Integer
    }))})
    def get(self):
        args = request.args

        if 'from' in args:
            invoices = InvoiceService.get_from(args['from'])
        else:
            invoices = InvoiceService.get_all()

        return {'items': invoices}

    @marshal_with({'data': fields.Nested({
        'id': fields.Integer,
        'number': fields.String,
        'date': fields.String,
        'provider_id': fields.Integer,
        'provider_name': fields.String(attribute='provider.name'),
        'is_acceptance': fields.Boolean,
        'acceptance_id': fields.Integer
    })})
    def put(self):
        from services import AcceptanceService
        data = request.json['data']

        items_json = data['items']
        provider_id = data['provider_id']
        pointsale_id = data['pointsale_id']
        date = data['date']
        date = HelperService.convert_to_pydate(date)

        try:
            # db.session.begin_nested()
            invoice = InvoiceService.save_from_json(date, items_json, provider_id)
            is_new, acceptance = AcceptanceService.get_or_create_by_invoice_pointsale(invoice.id, pointsale_id)

            # if is_new:
            acceptance.date = date
            db.session.flush()
            # db.session.commit()

            AcceptanceService.update_fact_count_items(acceptance.id, date, [{'id': x.id,
                                                                             'fact_count': x.count,
                                                                             'good_id': x.good_id} for x in invoice.items])
            db.session.add(acceptance)
        except Exception as exc:
            db.session.rollback()
            abort(400, message=u"Ошибка!!!!")
        else:
            db.session.commit()

        return {'data': invoice}


class InvoiceItemResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'name': fields.String,
        'number_local': fields.String,
        'number_global': fields.String,
        'count_order': fields.Integer,
        'count_postorder': fields.Integer,
        'count': fields.Integer,
        'price_without_NDS': fields.String,
        'price_with_NDS': fields.String,
        'sum_without_NDS': fields.String,
        'sum_NDS': fields.String,
        'rate_NDS': fields.String,
        'sum_with_NDS': fields.String,
        'thematic': fields.String,
        'count_whole_pack': fields.Integer,
        'placer': fields.Integer,
        'good_id': fields.Integer,
        'commodity_id': fields.Integer(attribute='good.commodity_id'),
        'price_id': fields.Integer(attribute='good.price_id'),
        'price_retail': fields.Integer(attribute='good.price.price_retail', default=''),
        'price_gross': fields.Integer(attribute='good.price.price_gross', default=''),
        'fact_count': fields.Integer(default='')
    }))})
    def get(self, invoice_id):
        return {'items': InvoiceService.get_items(invoice_id)}


class InvoiceItemCountResource(BaseTokeniseResource):
    @marshal_with({'result': fields.Nested({'count': fields.Integer})})
    def get(self, invoice_id):
        count = InvoiceService.get_count_items(invoice_id)
        return {'result': {'count': count}}


class InvoicePriceItemsResource(BaseTokeniseResource):
    """
    ресурс для получения товаров, цен, и их рекомендуемую стоимость на товары из накладной
    """

    @marshal_with({'items': fields.List(fields.Nested({
        'id_commodity': fields.Integer,
        'full_name': fields.String,
        'number_local': fields.String,
        'number_global': fields.String,
        'NDS': fields.String,
        'price_prev': fields.String,
        'price_post': fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'price_retail_recommendation': fields.String,
        'price_gross_recommendation': fields.String,
        'is_change': fields.Boolean,
        'id_good': fields.Integer
    }))})
    def get(self, invoice_id):
        from services import MailInvoiceService, PriceService

        invoice = MailInvoiceService.get_invoice(invoice_id)

        items = PriceService.generate_price_stub(invoice.items.order_by(asc(InvoiceItem.id)))

        return {'items': [{
            'id_commodity': it.id_commodity,
            'id_good': it.id_good,
            'full_name': it.full_name,
            'number_local': it.number_local,
            'number_global': it.number_global,
            'NDS': it.NDS,
            'price_prev': it.price_prev,
            'price_post': it.price_post,
            'price_retail': it.price_retail,
            'price_gross': it.price_gross,
            'price_retail_recommendation': it.price_retail_recommendation,
            'price_gross_recommendation': it.price_gross_recommendation,
            'is_change': it.is_change
        } for it in items]}


# class InvoiceRetailItemsResource(BaseTokeniseResource):
#     """
#     Ресурс
#     """
#
#     @marshal_with({'items': fields.List(fields.Nested({
#         'id_good': fields.Integer,
#         'full_name': fields.String,
#         'price_retail': fields.String,
#         'count': fields.String,
#         'is_approve': fields.Boolean
#     }))})
#     def get(self, invoice_id):
#         from services import RetailService
#         args = request.args
#
#         items = RetailService.get_retail_items(invoice_id)
#
#         if 'approve' in args:
#             if args['approve'] in ['true']:
#                 items = filter(lambda x: x.price_retail, items)
#             elif args['approve'] in ['false']:
#                 items = filter(lambda x: x.price_retail == '', items)
#
#         return {'items': [
#             {'full_name': item.full_name,
#              'price_retail': item.price_retail,
#              'count': item.count,
#              'id_good': item.id_good,
#              # 'id_commodity': item.id_commodity,
#              # 'id_price': item.id_price,
#              'is_approve': item.price_retail != ''} for item in items]}
