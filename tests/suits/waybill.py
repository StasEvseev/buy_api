#coding: utf-8

from . import BaseSuite


class WayBillTestSuite(BaseSuite):

    def get_waybills(self):
        return self._get_records("/api/waybill")

    def get_waybill(self, id):
        return self._get_record("/api/waybill/", id)

    def create_waybill(self, date, type, invoice_id, pointsale_from_id, items, receiver_id=None, pointsale_id=None):
        return self.client.put('/api/waybill', data=self._serialize({'data':{
            'invoice_id': invoice_id,
            'items': items,
            'type': type,
            'receiver_id': receiver_id or -1,
            'pointsale_id': pointsale_id or -1,
            'pointsale_from_id': pointsale_from_id,
            'date': date
        }}), headers=self._get_headers(True))

    def update_waybill(self, id, date, items):
        return self.client.post('/api/waybill/' + str(id), data=self._serialize({'data': {
            'items': items,
            'date': date
        }}), headers=self._get_headers(True))