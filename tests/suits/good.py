#coding: utf-8
from tests.suits import BaseSuite


class GoodTestSuite(BaseSuite):
    def _get_good_all(self):
        return self._get_records("/api/good")

    def _get_good(self, id):
        return self._get_record("/api/good/", id)

    def _create_good(self, id_comm, number_l, number_g, price_ret, price_gr):
        return self.client.put("/api/good",
                            data=self._serialize({'data': {
                                'commodity_id': id_comm,
                                'number_global': number_g,
                                'number_local': number_l,
                                'price.price_gross': price_gr,
                                'price.price_retail': price_ret}}),
                            headers=self._get_headers())

    def create_good(self, *args, **kwargs):
        return self._deserialize(self._create_good(*args, **kwargs).data)

    def _update_good(self, id, id_comm, number_l, number_g, price_ret, price_gr):
        return self.client.post("/api/good/" + str(id), data=self._serialize({'data': {
                                'commodity_id': id_comm,
                                'number_global': number_g,
                                'number_local': number_l,
                                'price.price_gross': price_gr,
                                'price.price_retail': price_ret}}),
                             headers=self._get_headers())

    def _delete_good(self, id):
        return self._delete_record("/api/good/", id)