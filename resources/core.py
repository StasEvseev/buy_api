#coding: utf-8
from functools import partial
from flask import g, jsonify, request

from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with, fields, abort
from sqlalchemy import desc, asc, or_
from log import error, debug
from models import db
from security import auth


parser = reqparse.RequestParser()
parser.add_argument('filter_field', type=str)
parser.add_argument('filter_text', type=unicode)
parser.add_argument('sort_field', type=str)
parser.add_argument('sort_course', type=str)
parser.add_argument('count', type=int)
parser.add_argument('page', type=int)


class BaseCanoniseResource(object):
    model = None
    attr_json = {}

    attr_response_post = {}
    attr_response_put = {}

    multif = {"filter_field": ()}

    class CanonException(Exception):
        pass

    @classmethod
    def _register_into_rest(cls):
        """
        Регистрация ресурсов в РЕСТе.
        """
        self = cls()
        cls.attr_response_post = cls.attr_response_post or cls.attr_json
        cls.attr_response_put = cls.attr_response_put or cls.attr_json
        type1 = type(
            cls.__name__ + "Item",
            (BaseTokeniseResource, ),
            {
                "get": marshal_with({'items': fields.List(fields.Nested(cls.attr_json)),
                                     'count': fields.Integer,
                                     'max': fields.Integer})(self.get_items.__func__).__get__(self, cls),
                "put": marshal_with(cls.attr_response_put)(self.put.__func__).__get__(self, cls),
                "parent": self
            }
        )

        type2 = type(
            cls.__name__ + "Items",
            (BaseTokeniseResource, ),
            {
                "get": marshal_with(cls.attr_json)(self.get.__func__).__get__(self, cls),
                "post": marshal_with(cls.attr_response_post)(self.post.__func__).__get__(self, cls),
                "delete": self.delete,
                "parent": self
            }
        )

        return type1, type2

    def filter_query(self, query, filter_field, filter_text, sort_field, sort_course, page, count):
        """
        Метод для дополнительной фильтрации.
        """
        if filter_field and filter_text:
            if filter_field in self.multif.keys():
                flds = self.multif[filter_field]
                subq = []
                for fld in flds:
                    subq.append(self.model.__table__.columns[fld].ilike("%"+filter_text+"%"))
                query = query.filter(or_(*subq))
            else:
                query = query.filter(
                    self.model.__table__.columns[filter_field].ilike("%"+filter_text+"%")
                )
        if sort_field and sort_course:
            query = query.order_by(
                {'desc': desc, 'asc': asc}[sort_course](self.model.__table__.columns[sort_field])
            )
        max_ = query.count()

        if page and count:
            query = query.offset((page - 1) * count).limit(count)
        records = query.all()
        count_ = query.count()
        return records, max_, count_

    def _get_attr_relation(self):
        return filter(lambda value: hasattr(value[1], "attribute")
                                                 and getattr(value[1], "attribute") != None
                                                 and "." in getattr(value[1], "attribute"),
                                   self.attr_json.iteritems())

    #===================================================================================================================
    #BASE CRUD - вынести в отдельный объект
    def get_by_id(self, id):
        return self.model.query.get(id)

    def save_model(self, obj):
        db.session.add(obj)
        return obj

    def pre_save(self, obj, data):
        return obj

    def post_save(self, obj, data, create_new=False):
        if data:
            attr_relation = self._get_attr_relation()
            list_created_obj = []
            for key, attr in attr_relation:
                objnest = obj
                chain_models, _, at = attr.attribute.rpartition(".")
                for chain_model in chain_models.split("."):
                    try:
                        value = getattr(objnest, chain_model)
                        if not value and key in data:
                            relation_model = objnest._sa_class_manager[chain_model].property.argument
                            setattr(objnest, chain_model, relation_model())
                            # instance = relation_model()
                            # setattr(instance, )
                            # setattr(objnest, ch, instance)
                            objnest = getattr(objnest, chain_model)
                        else:
                            objnest = value
                    except AttributeError:
                        break
                else:
                    try:
                        setattr(objnest, at, data[key])
                    except KeyError:
                        pass
                    else:
                        if objnest not in list_created_obj:
                            list_created_obj.append(objnest)
            for objs in list_created_obj:
                db.session.add(objs)

    #===================================================================================================================

    def fill_obj(self, data, obj=None):
        """
        заполнение объекта данными с json
        """
        if 'id' in data:
            obj = self.get_by_id(data['id'])
        elif not obj:
            obj = self.model()
        for key in self.attr_json.keys():
            if key not in data:
                continue
            setattr(obj, key, data.get(key))
        return obj

    #===================================================================================================================
    #REST

    def get_items(self):
        """
        Работа с большим количество записей по модели.
        """
        args = parser.parse_args()

        filter_field = args['filter_field']
        filter_text = args['filter_text']
        sort_field = args['sort_field']
        sort_course = args['sort_course']
        page = args['page']
        count = args['count']

        query = self.model.query

        records, max_, count_ = self.filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page, count)

        return {'items': records, 'count': count_, 'max': max_}

    def put(self):
        """
        Сохранение новой записи.
        """
        try:
            # db.session = db.session.begin_nested()
            data = request.json['data']
            good_stub = self.fill_obj(data)
            obj = self.pre_save(good_stub, data)
            del good_stub
            obj = self.save_model(obj)
            db.session.flush()
            self.post_save(obj, data, create_new=True)
            db.session.commit()
        except BaseCanoniseResource.CanonException as exc:
            debug(unicode(exc))
            db.session.rollback()
            abort(400, message=unicode(exc))
        except Exception as exc:
            error("Ошибка при создании записи модели %s. %s", self.model.__class__.__name__, unicode(exc))
            db.session.rollback()
            raise
        else:
            pass
            # db.session.commit()
        return obj

    def get(self, id):
        """
        Получение объекта в форме JSON.
        """
        return self.model.query.get(id)

    def post(self, id):
        """
        Редактирование записи.
        """
        try:
            # db.session.begin_nested()
            data = request.json['data']
            good_stub = self.fill_obj(data, self.get_by_id(id))
            obj = self.pre_save(good_stub, data)
            obj = self.save_model(obj)
            self.post_save(good_stub, data)
            db.session.commit()
        except BaseCanoniseResource.CanonException as exc:
            debug(unicode(exc))
            db.session.rollback()
            abort(400, message=unicode(exc))
        except Exception as exc:
            error("Ошибка при редактировании записи %d модели %s. %s", id, self.model.__class__.__name__, unicode(exc))
            db.session.rollback()
            raise
        else:
            pass
            # db.session.commit()
        return obj

    def delete(self, id):
        """
        Удаление записи.
        """
        db.session.delete(self.get_by_id(id))
        db.session.commit()


class BaseTokenMixinResource(object):
    decorators = [auth.login_required]


class BaseTokeniseResource(restful.Resource):
    decorators = [auth.login_required]


class BaseModelPackResource(restful.Resource):
    model = None

    def get(self):
        args = parser.parse_args()

        filter_field = args['filter_field']
        filter_text = args['filter_text']
        sort_field = args['sort_field']
        sort_course = args['sort_course']
        page = args['page']
        count = args['count']

        query = self.model.query

        if filter_field and filter_text:
            query = query.filter(
                self.model.__table__.columns[filter_field].like("%"+filter_text+"%")
            )
        if sort_field and sort_course:
            query = query.order_by(
                {'desc': desc, 'asc': asc}[sort_course](self.model.__table__.columns[sort_field])
            )
        max_ = query.count()

        if page and count:
            query = query.offset((page - 1) * count).limit(count)
        mails = query.all()
        count_ = query.count()

        return {'items': mails, 'count': count_, 'max': max_}


class TokenResource(BaseTokeniseResource):

    def get(self):
        # user = getattr(g, 'user', None)
        # if user is None:
        #     user = fetch_current_user_from_database()
        #     g.user = user
        #     token = user.generate_auth_token()
        token = g.user.generate_auth_token()
        # print token
        return jsonify({
            'token': token.decode('ascii')
        })