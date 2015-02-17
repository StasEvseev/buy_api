#coding: utf-8
from datetime import datetime
import os

from flask import request, url_for
from flask.ext.restful import abort, marshal_with, fields, reqparse

from config import PATH_TO_GENERATE_INVOICE

from models import db
from models.waybill import WayBill

from resources.core import BaseTokeniseResource, BaseTokenMixinResource, BaseModelPackResource, BaseCanoniseResource

from services import GoodService, HelperService, PointSaleService, WayBillService, WayBillServiceException


item = {'id': fields.Integer,
        'date': fields.String,
        'number': fields.String,
        'pointsale_from_id': fields.Integer,
        'pointsale_from': fields.String,
        'receiver_id': fields.Integer,
        'receiver': fields.String,
        'pointsale_id': fields.Integer,
        'pointsale': fields.String,
        'point': fields.String,
        'type': fields.Integer,
        'type_str': fields.String,
        'invoice_id': fields.Integer,
        'invoice': fields.String,
        'filepath': fields.String}

item_items = {
    'id': fields.Integer,
    'full_name': fields.String,
    'good_id': fields.Integer,
    'count_invoice': fields.Integer(default=""),
    'count': fields.Integer(default=""),
    'price': fields.String,
    'price_gross': fields.String,
    'price_retail': fields.String,
    'is_approve': fields.Boolean
}


def convert_itemitems_to_json(item, type):
    price = GoodService.get_price(item.good_id)
    # WayBillService.get_items()
    # PointSaleService
    # pointitem = PointSaleService.get_item_to_pointsale_good(item.pointsale_from_id, item.good_id)
    return {
        'id': item.id,
        'full_name': item.good.full_name,
        'good_id': item.good_id,
        'count_invoice': item.count,
        # 'count': pointitem.count if pointitem else 0,
        'price': price.price_retail if type == 1 else price.price_gross,
        'price_gross': price.price_gross,
        'price_retail': price.price_retail,
        'is_approve': True
    }


def convert_item_to_json(item_waybill):
    return {
        'id': item_waybill.id,
        'date': item_waybill.date,
        'number': item_waybill.number,
        'pointsale_from_id': item_waybill.pointsale_from_id,
        'pointsale_from': item_waybill.pointsale_from.name if item_waybill.pointsale_from else None,
        'receiver_id': item_waybill.receiver_id or None,
        'receiver': item_waybill.receiver.fullname if item_waybill.receiver else None,
        'pointsale_id': item_waybill.pointsale_id or None,
        'pointsale': item_waybill.pointsale.name if item_waybill.pointsale else None,
        'point': item_waybill.rec,
        'type': item_waybill.type,
        'type_str': item_waybill.typeS,
        'invoice_id': item_waybill.invoice_id or None,
        'invoice': item_waybill.invoice,
        'filepath': item_waybill.filepath
    }


parser = reqparse.RequestParser()
parser.add_argument('invoice_id', type=int)
parser.add_argument('receiver_id', type=int)
parser.add_argument('pointsale_id', type=int)
parser.add_argument('type', type=int)


class WayBillHelperResource(BaseTokeniseResource):
    @marshal_with({'data': fields.Nested(item),
                   'status': fields.Boolean,
                   'extra': fields.String})
    def get(self):
        args = parser.parse_args()
        invoice_id = args['invoice_id']
        receiver_id = args['receiver_id']
        pointsale_id = args['pointsale_id']
        type = args['type']

        count = WayBillService.count_exists(invoice_id, receiver_id, pointsale_id, type)
        if count:
            if count > 1:
                return {'status': True, 'extra': 'multi'}
            else:
                waybill = WayBillService.get_by_attr(invoice_id, receiver_id, pointsale_id, type)
                return {'status': True, 'data': waybill, 'extra': 'single'}
        else:
            return {'status': False}


class WayBillCanon(BaseCanoniseResource):
    model = WayBill

    attr_json = {
        'id': fields.Integer,
        'date': fields.String,
        'number': fields.String,
        'pointsale_from_id': fields.Integer,
        'pointsale_from': fields.String(attribute="pointsale_from.name"),
        'receiver_id': fields.Integer,
        'receiver': fields.String(attribute="receiver.fullname"),
        'pointsale_id': fields.Integer,
        'pointsale': fields.String(attribute="pointsale.name"),
        'point': fields.String,
        'type': fields.Integer,
        'type_str': fields.String(attribute="typeS"),
        'invoice_id': fields.Integer,
        'invoice': fields.String,
        'filepath': fields.String
    }

    attr_response_put = {
        'data': fields.Nested(item),
        'status': fields.String,
        'path': fields.String
    }

    attr_response_post = {
        'status': fields.String,
        'path': fields.String
    }

    class WayBillCanonException(BaseCanoniseResource.CanonException):
        pass

    def pre_save(self, obj, data):
        obj.date = HelperService.convert_to_pydate(data['date'])
        obj.waybill_items = data['items']
        return super(WayBillCanon, self).pre_save(obj, data)

    def post(self, id):
        obj = super(WayBillCanon, self).post(id)
        return {"status": "ok", "path": obj.file_load, "data": obj}

    def save_model(self, obj):
        import uuid
        file_name = str(uuid.uuid4()) + ".xls"
        path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
        try:
            # items = obj.waybill_items
            if not obj.id:
                waybill = WayBillService.create(
                    obj.pointsale_from_id, obj.invoice_id, obj.date, obj.receiver_id, obj.pointsale_id, obj.type,
                    forse=True)
                # obj = waybill
            else:
                super(WayBillCanon, self).save_model(obj)
                waybill = obj
            items = WayBillService.build_retail_items(obj.waybill_items)
            path = url_for('static', filename='files/' + file_name)
            WayBillService.upgrade_items(waybill, items, path_to_target, path)
            waybill.file_load = path
        except WayBillServiceException as exc:
            raise WayBillCanon.WayBillCanonException(unicode(exc))
        return waybill

    def put(self):
        obj = super(WayBillCanon, self).put()
        return {"status": "ok", "path": obj.file_load, "data": obj}


# #TODO
# class WayBillResource(BaseTokenMixinResource, BaseModelPackResouce):
#
#     model = WayBill
#
#     @marshal_with({'data': fields.Nested(item),
#                    'status': fields.String,
#                    'path': fields.String})
#     def put(self):
#         data = request.json['data']
#         invoice_id = data['invoice_id']
#         items = data['items']
#         type = data['type']
#         receiver_id = data['receiver_id']
#         pointsale_id = data['pointsale_id']
#         pointsale_from_id = data['pointsale_from_id']
#         date = data['date']
#         date = HelperService.convert_to_pydate(date)
#
#         import uuid
#         file_name = str(uuid.uuid4()) + ".xls"
#         path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
#
#         try:
#             waybill = WayBillService.create(
#                 pointsale_from_id, invoice_id, date, receiver_id, pointsale_id, type, forse=True)
#             items = WayBillService.build_retail_items(items)
#             path = url_for('static', filename='files/' + file_name)
#             WayBillService.upgrade_items(waybill, items, path_to_target, path)
#             db.session.commit()
#
#             return {"status": "ok", "path": path, "data": waybill}
#         except WayBillServiceException as retailexc:
#             db.session.rollback()
#             abort(404, message=unicode(retailexc))
#
#         # return res
#
#     @marshal_with({'items': fields.List(fields.Nested(item)), 'count': fields.Integer})
#     def get(self):
#
#         result = super(WayBillResource, self).get()
#
#         return {'items': [convert_item_to_json(x) for x in result['items']], 'count': result['count']}
#
# #TODO
# class WayBillItemResource(BaseTokeniseResource):
#
#     def post(self, id):
#         data = request.json['data']
#
#         date = data['date']
#         items = data['items']
#         date = HelperService.convert_to_pydate(date)
#
#         import uuid
#         file_name = str(uuid.uuid4()) + ".xls"
#         path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
#
#         waybill = WayBillService.get_by_id(id)
#         waybill.date = date
#         db.session.add(waybill)
#
#         try:
#             path = url_for('static', filename='files/' + file_name)
#             items = WayBillService.build_retail_items(items)
#             WayBillService.upgrade_items(waybill, items, path_to_target, path)
#             db.session.commit()
#             return {"status": "ok", "path": path}
#         except WayBillServiceException as retailexc:
#             db.session.rollback()
#             abort(404, message=unicode(retailexc))
#
#     @marshal_with(item)
#     def get(self, id):
#         return convert_item_to_json(WayBillService.get_by_id(id))


class WayBillItemItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested(item_items))})
    def get(self, id):
        waybill = WayBillService.get_by_id(id)
        return {'items': [convert_itemitems_to_json(x, waybill.type) for x in waybill.items]}