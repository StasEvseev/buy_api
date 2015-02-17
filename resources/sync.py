#coding: utf-8
import datetime
from models import db

from models.sync import Sync, IN_PROGRESS, COMPLETE

from resources.core import BaseTokeniseResource


class SyncResourceCreate(BaseTokeniseResource):
    def get(self):
        print "SYNC"
        sync = Sync()
        sync.date_start = datetime.datetime.now()
        sync.status = IN_PROGRESS
        db.session.add(sync)
        db.session.commit()

        return {"id": sync.id}


class SyncResource(BaseTokeniseResource):
    def post(self, invoice_id):
        print "POST SYNC"
        sync = Sync.query.get(invoice_id)
        sync.date_end = datetime.datetime.now()
        sync.status = COMPLETE
        db.session.add(sync)
        db.session.commit()
        return "ok"


class SyncResourceError(BaseTokeniseResource):
    def post(self, invoice_id, status):
        sync = Sync.query.get(id)
        sync.date_end = datetime.datetime.now()
        sync.status = status
        db.session.add(sync)
        db.session.commit()
        return "ok"