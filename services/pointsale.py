#coding: utf-8

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from models import db
from models.pointsale import PointSale
from models.pointsaleitem import PointSaleItem


class PointSaleService(object):

    @classmethod
    def get_all(cls):
        return PointSale.query.all()

    @classmethod
    def get_all_exclude(cls, exclude_id):
        return PointSale.query.filter(PointSale.id != exclude_id)

    @classmethod
    def get_by_id(cls, id):
        return PointSale.query.get(id)

    @classmethod
    def get_or_create(cls, point_id, good_id):
        try:
            pointitem = PointSaleItem.query.filter(
                PointSaleItem.pointsale_id==point_id,
                PointSaleItem.good_id==good_id).one()
        except NoResultFound:
            pointitem = PointSaleItem()
            pointitem.pointsale_id = point_id
            pointitem.good_id = good_id
        db.session.add(pointitem)

        return pointitem

    # @classmethod
    # def update_count(cls, pointitem, count):
    #     if count:
    #         pointitem.count+= int(count) - pointitem.count
    #         db.session.add(pointitem)

    @classmethod
    def down_update_count(cls, poinitem, count):
        if count:
            poinitem.count += poinitem.count + int(count)
            db.session.add(poinitem)

    @classmethod
    def get_item_to_pointsale_good(cls, pointsale_id, good_id):
        try:
            return PointSaleItem.query.filter(
                PointSaleItem.pointsale_id==pointsale_id,
                PointSaleItem.good_id==good_id).one()
        except NoResultFound:
            pass

    @classmethod
    def get_item_to_pointsale(cls, point_id, excl_items=None):
        if excl_items:
            return PointSaleItem.query.filter(
                and_(PointSaleItem.pointsale_id==point_id, PointSaleItem.good_id.notin_(excl_items)))
        else:
            return PointSaleItem.query.filter(
                PointSaleItem.pointsale_id==point_id)