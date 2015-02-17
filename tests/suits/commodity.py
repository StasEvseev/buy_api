#coding: utf-8
from tests.suits import BaseSuite


class CommodityTestSuite(BaseSuite):
    def _get_commodity_all(self):
        return self._get_records("/api/commodity")

    def _get_commodity(self, id):
        return self._get_record("/api/commodity/", id)

    def _create_commodity(self, name, numeric, thematic):
        return self.client.put("/api/commodity",
                            data=self._serialize({'data': {'name': name, 'numeric': numeric, 'thematic': thematic}}),
                            headers=self._get_headers())

    def create_commodity(self, *args, **kwargs):
        return self._deserialize(self._create_commodity(*args, **kwargs).data)

    def _update_commodity(self, id, name, numeric, thematic):
        return self.client.post("/api/commodity/" + str(id),
                             data=self._serialize({'data': {'name': name, 'numeric': numeric, 'thematic': thematic}}),
                             headers=self._get_headers())

    def _delete_commodity(self, id):
        return self._delete_record("/api/commodity/", id)