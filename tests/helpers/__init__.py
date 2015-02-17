#coding: utf-8
import random
import string
from datetime import datetime, date, timedelta
from flask.ext.restful.fields import String, DateTime, Integer, Boolean
from resources import Date


class Generator(object):

    @classmethod
    def generate_string(cls, length=12):
        return unicode(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length)))

    @classmethod
    def generate_date(cls, from_=date(2008, 1, 1), to_=date.today()):
        delta = to_ - from_
        # int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_days = random.randrange(delta.days)

        return from_ + timedelta(days=random_days)

    @classmethod
    def generate_datetime(cls, from_=datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p'), to_=datetime.now()):
        delta = to_ - from_
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return from_ + timedelta(seconds=random_second)

    @classmethod
    def generate_int(cls, min=0, max=2048):
        return random.randrange(min, max)

    @classmethod
    def generate_boolean(cls):
        return {0: False, 1: True}[random.randrange(0, 2)]

    @classmethod
    def generate_data(cls, attrs, relation=False):
        data = {}

        for name, type in attrs.iteritems():

            if hasattr(attrs[name], 'attribute'):
                attribute = getattr(attrs[name], 'attribute')
                attributes = attribute.split(".")
                if len(attributes) > 1:
                    pass
            elif name.endswith("_id"):
                pass
            else:

                if type == String:
                    value = cls.generate_string()
                elif type == DateTime:
                    value = cls.generate_datetime()
                elif type == Date:
                    value = cls.generate_date().isoformat()
                elif type == Integer:
                    value = cls.generate_int()
                elif type == Boolean:
                    value = cls.generate_boolean()
                else:
                    value = ""
                data[name] = value
        return data