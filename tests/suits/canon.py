#coding: utf-8

from . import BaseSuite

class BaseCanonSuite(BaseSuite):

    def get(self, url, id=None):
        if id:
            url = url + "/"
            response = self._get_record(url, id)
        else:
            response = self._get_records(url)
        return response

    def put(self, url, data):
        return self.client.put(url,
                            data=self._serialize({'data': data}),
                            headers=self._get_headers())

    def post(self, url, id, data):
        return self.client.post(url + "/" + str(id),
                             data=self._serialize({'data': data}),
                             headers=self._get_headers())

    def delete(self, url, id):
        return self._delete_record(url + "/", id)