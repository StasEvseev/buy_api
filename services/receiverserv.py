#coding: utf-8
from models.receiver import Receiver


class ReceiverService(object):

    @classmethod
    def get_all(cls):
        return Receiver.query.all()