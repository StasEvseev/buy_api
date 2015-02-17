#coding: utf-8
import base64
from flask import json
from werkzeug.datastructures import Headers


class BaseSuite(object):

    def __init__(self, client, application):
        self.client = client
        self.application = application

    def _delete_record(self, url, id):
        return self.client.delete(url + str(id), headers=self._get_headers())

    def _get_record(self, url, id):
        return self.client.get(url + str(id), headers=self._get_headers())

    def _get_records(self, url):
        return self.client.get(url + "?count=10&page=1&filter_field=filter_field&filter_text=", headers=self._get_headers(is_json=False))

    def _serialize(self, dict):
        return json.dumps(dict)

    def _deserialize(self, data):
        return json.loads(data)

    def _get_headers(self, is_json=True):
        from security.model import User

        with self.application.app_context():
            user = User.query.get(1)
            token = user.generate_auth_token()

        par = {"Authorization": "Basic " + base64.b64encode(token + ":unused")}
        if is_json:
            par['Content-Type'] = 'application/json'

        return Headers(par)