#coding: utf-8

from . import BaseSuite

class AcceptanceSuite(BaseSuite):

    def acceptance_from_mail(self, invoice_id, pointsale_id, date, items):
        """
        /acceptance/pointsale/<int:point_id>/invoice/<int:invoice_id>
        """
        data = {
            'data': {'items': items, 'date': unicode(date)},
        }
        return self.client.post("/api/acceptance/pointsale/" + str(pointsale_id) + "/invoice/" + str(invoice_id),
                                data=self._serialize(data), headers=self._get_headers(True))

    def acceptance_custom(self, pointsale_id, provider_id, date, items):
        """
        date: 2015-02-12T10:20:45.518Z
        items: [,…]
        pointsale_id: 2
        provider_id: 1
        """
        data = {
            "data": {
                "date": unicode(date),
                "pointsale_id": pointsale_id,
                "provider_id": provider_id,
                "items": items
            }
        }
        return self.client.put("/api/invoice", data=self._serialize(data), headers=self._get_headers(True))

    def invoice_items(self, invoice_id):
        return self.client.get("/api/invoice/" + str(invoice_id) + "/items", headers=self._get_headers())