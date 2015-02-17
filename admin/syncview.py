#coding: utf-8
from admin.baseview import BaseViewAuth
from models.sync import Sync


class SyncView(BaseViewAuth):
    # form_columns = ('date_start', 'date', 'emails')
    column_labels = dict(date_start=u'Дата и время начала', date_end=u'Дата и время окончания', status_string=u"Статус")
    column_list = ('date_start', 'date_end', 'status_string')
    can_edit = False
    can_delete = False
    can_create = False
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SyncView, self).__init__(Sync, session, **kwargs)