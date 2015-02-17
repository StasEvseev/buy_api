#coding: utf-8
from models import db


class Sync(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #Дата начала
    date_start = db.Column(db.DateTime)
    #Дата накладной
    date_end = db.Column(db.DateTime)
    #Статус енам
    status = db.Column(db.Integer)

    @property
    def status_string(self):
        return ENUM_STATUS[self.status]

IN_PROGRESS = 1
COMPLETE = 2
CANCEL = 3
TIMEOUT = 4
NO_CONN = 5
IOERROR = 6
BATCH_ERROR = 7
AUTH_ERROR = 8

ENUM_STATUS = {
    IN_PROGRESS: u"В процессе",
    COMPLETE: u"Закончен",
    CANCEL: u"Отменен",
    TIMEOUT: u"Долгий отклик",
    NO_CONN: u"Нет соединения",
    IOERROR: u"Проблемы с вводом/выводом",
    BATCH_ERROR: u"Ошибка массового сохранения",
    AUTH_ERROR: u"Проблемы авторизации в приложении",
}