#coding: utf-8
from datetime import datetime


class HelperService(object):

    @classmethod
    def convert_to_pydate(cls, str_date):
        if str_date.find('T') not in [-1]:
            return datetime.strptime(str_date[:str_date.find('T')], '%Y-%m-%d')
        else:
            return datetime.strptime(str_date, '%Y-%m-%d')