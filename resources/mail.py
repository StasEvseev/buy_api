#coding: utf-8

from flask.ext import restful
from flask.ext.restful import abort, marshal_with, fields

from mails.action import get_count_mails, NotConnect, get_mails
from mails.model import Mail
from models import db
class MailCheck(restful.Resource):
    @marshal_with({'date_': fields.DateTime, 'title': fields.String,
                   'from_': fields.String, 'to_': fields.String, 'file_': fields.String})
    def get(self):
        result = []
        try:
           count = get_count_mails()
        except NotConnect as err:
            abort(404, unicode(err))
        else:
            if count > 0:
                mails = get_mails()

                for mail in mails:
                    ml = Mail(title=mail.title, date=mail.date_, from_=mail.from_, to=mail.to_, file=mail.file_)
                    db.session.add(ml)
                    db.session.commit()
                result = [{'title': m.title, 'date_': m.date_,
                           'from_': m.date_, 'to_': m.to_,
                           'file_': m.file_} for m in mails]
                # print u'Внимание', u'В почтовом ящике обнаружено %s новых письма. Обработать?' % count
        return result