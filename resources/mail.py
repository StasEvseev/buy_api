#coding: utf-8
from flask import jsonify

from flask.ext import restful
from flask.ext.restful import abort, marshal_with, fields, reqparse

from mails.action import get_count_mails, NotConnect, get_mails
from mails.model import Mail
from models import db


parser = reqparse.RequestParser()
parser.add_argument('length', type=int)
parser.add_argument('start', type=int)

class MailCheck(restful.Resource):
    # @marshal_with({'date_': fields.DateTime, 'title': fields.String,
    #                'from_': fields.String, 'to_': fields.String, 'file_': fields.String})
    # def get(self):
    #     result = []
    #     try:
    #        count = get_count_mails()
    #     except NotConnect as err:
    #         abort(404, message=unicode(err))
    #     else:
    #         if count > 0:
    #             mails = get_mails()
    #
    #             for mail in mails:
    #                 ml = Mail(title=mail.title, date=mail.date_, from_=mail.from_, to=mail.to_, file=mail.file_)
    #                 db.session.add(ml)
    #                 db.session.commit()
    #             result = [{'title': m.title, 'date_': m.date_,
    #                        'from_': m.date_, 'to_': m.to_,
    #                        'file_': m.file_} for m in mails]
    #             # print u'Внимание', u'В почтовом ящике обнаружено %s новых письма. Обработать?' % count
    #     return result

    # @marshal_with({'date_': fields.DateTime, 'title': fields.String,
    #                'from_': fields.String, 'to_': fields.String, 'file_': fields.String})
    # @marshal_with({'data': res})
    def get(self, **kwargs):
        args = parser.parse_args()
        # print kwargs
        res = []

        mails = Mail.query.offset(args['start']).limit(args['length']).all()

        print mails

        # import flask.ext.restful.inputs

        for mail in mails:
            res.append(jsonify({
                'date': mail.date,
                'title': mail.title ,
                'from': mail.from_
            }))

        return {'data': res}