#coding: utf-8
from collections import defaultdict

import re
from tests import BaseTestCase
from resources import AcceptanceCanon, CommodityCanonResource, PointSaleCanon, ProviderCanon
from resources.receiver import ReceiverCanonResource
from tests.helpers import Generator
from tests.suits.canon import BaseCanonSuite


class BaseCanonTest(BaseTestCase):

    RESOURCES = [
        AcceptanceCanon, CommodityCanonResource, PointSaleCanon, ProviderCanon, ReceiverCanonResource
    ]

    def test_(self):
        with self.application.app_context():
            self.base_canon()

    def base_canon_item(self, url, resource):
        COUNT = 5
        attrs = resource.attr_json
        model = resource.model

        attr_relation = resource._get_attr_relation()

        ids = []

        for i in xrange(COUNT):
            data_json = Generator.generate_data(attrs)
            del data_json['id']

            response = self.base_canon_suite.put(url, data_json)
            self.assertEqual(response.status_code, 200)
            data = self._deserialize(response.data)
            ids.append(data['id'])

            instance = model.query.get(data['id'])

            for attr_n, att in attr_relation:
                attribute = att.attribute
                chain_models, _, at = attribute.rpartition(".")
                for chain_model in chain_models.split("."):
                    nest = getattr(instance, chain_model)
                    self.assertIsNone(nest)
                    break

            response = self.base_canon_suite.get(url, data['id'])
            self.assertEqual(response.status_code, 200)

            data = self._deserialize(response.data)

            for key, value in data_json.iteritems():
                self.assertEqual(data[key], value)

        self.assertEqual(model.query.count(), COUNT)
        response = self.base_canon_suite.get(url)

        self.assertEqual(response.status_code, 200)
        data = self._deserialize(response.data)
        self.assertEqual(data['count'], COUNT)

        for id in ids:
            data_json_update = Generator.generate_data(attrs)
            del data_json_update['id']

            response = self.base_canon_suite.post(url, id, data_json_update)
            self.assertEqual(response.status_code, 200)

            response = self.base_canon_suite.get(url, id)
            self.assertEqual(response.status_code, 200)
            data = self._deserialize(response.data)

            for key, value in data_json_update.iteritems():
                self.assertEqual(data[key], value)

        for id in ids:
            response = self.base_canon_suite.delete(url, id)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(model.query.get(id))

    def base_canon(self):
        for resource, data in self.test_url.iteritems():
            url = data['data']['url']

            self.base_canon_item(url, resource)


    def set_up(self):
        api = self.application.api
        prefix = api.prefix

        self.test_url = defaultdict(dict)

        for res, url, _ in api.resources:
            if hasattr(res, 'parent') and type(getattr(res, 'parent')) in self.RESOURCES:
                
                self.test_url[res.parent][url[0]] = res
                # self.test_url[res.parent][1].append(res)

        def main_url(urls):
            for url in urls:
                reg = re.search("(<.+>)", url)
                if not reg:
                    return url

        for resource, url_res in self.test_url.iteritems():
            url = main_url(url_res.keys())
            values = url_res.values()
            del self.test_url[resource]
            self.test_url[resource]['data'] = {"url": prefix + url, "items": values}

        self.base_canon_suite = BaseCanonSuite(self.client, self.application)

    def tear_down(self):
        pass
