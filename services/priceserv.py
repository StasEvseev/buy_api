#coding: utf-8
from collections import namedtuple
from models import db
from models.price import Price

from services import CommodityService
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound


PriceStub = namedtuple('PriceStub', ['id', 'id_commodity', 'full_name', 'number_local', 'number_global', 'NDS',
                                     'price_prev',
                                     'price_post', 'price_retail', 'price_gross', 'is_change',
                                     'price_retail_recommendation', 'price_gross_recommendation'])


class PriceServiceException(Exception):
    pass


class PriceService(object):

    @classmethod
    def create_or_update_prices(cls, datas):
        try:
            for data in datas:
                id_commodity = int(data['id'])
                price_retail = float(data['price_retail']) if data['price_retail'] else None
                price_gross = float(data['price_gross']) if data['price_gross'] else None
                NDS = float(data['NDS'])
                price_prev = float(data['price_prev'])
                price_post = float(data['price_post'])

                if not price_retail and not price_gross:
                    continue
                try:
                    price = Price.query.filter(
                        Price.commodity_id==id_commodity,
                        Price.price_prev==price_prev,
                        Price.price_post==price_post).one()
                except NoResultFound as err:
                    price = Price(commodity_id=id_commodity, number_local=data['number_local'],
                                  number_global=data['number_global'], NDS=NDS,
                                  price_prev=price_prev, price_post=price_post, price_retail=price_retail,
                                  price_gross=price_gross)
                    db.session.add(price)
                else:
                    price.NDS = NDS
                    price.price_retail = price_retail
                    price.price_gross = price_gross
                    db.session.add(price)
        except Exception as err:
            raise PriceServiceException(err)
        else:
            db.session.commit()

    @classmethod
    def get_price_to_commodity(cls, id_commodity):
        price = Price.query.filter(
            Price.commodity_id==id_commodity,
        ).order_by(desc(Price.number_local), desc(Price.number_global)).first()
        if price is None:
            price = PriceStub(
            id='',
            id_commodity=id_commodity,
            full_name='',
            number_local='',
            number_global='',
            NDS='',
            price_prev='',
            price_post='',
            price_retail='',
            price_gross='',
            price_retail_recommendation='',
            price_gross_recommendation='',
            is_change=''
        )
        return price

    @classmethod
    def generate_price_stub(cls, products):

        res = []

        for prod in products:
            commodity = CommodityService.get_commodity(prod.name)
            price = PriceService.get_price_to_commodity(commodity.id)

            pricestub = PriceStub(
                id='',
                id_commodity=commodity.id,
                full_name=prod.full_name,
                number_local=prod.number_local,
                number_global=prod.number_global,
                NDS=prod.rate_NDS,
                price_prev=prod.price_without_NDS,
                price_post=prod.price_with_NDS,
                price_retail=price.price_retail or '',
                price_gross=price.price_gross or '',
                price_retail_recommendation=float(prod.price_with_NDS) * 1.6,
                price_gross_recommendation=float(prod.price_with_NDS) * 1.4,
                is_change=((price.price_prev and prod.price_without_NDS != price.price_prev) or (price.price_post and prod.price_with_NDS != price.price_post)))

            res.append(pricestub)

        return res