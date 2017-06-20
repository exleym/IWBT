import json
import unittest
import requests
from sqlalchemy import create_engine
from iwbt import create_app
from iwbt.models.rivers import Base


class TestRiverResourceAPI(unittest.TestCase):
    API_BASE = 'http://localhost:5000/api/v1.0/'
    con = create_engine('sqlite://')

    def create_resource(self, resource_name, data):
        url = '/api/v1.0/' + resource_name
        r = self.client.post(url, data=json.dumps(data),
                             content_type='application/json')
        return r

    def get_resource(self, resource_name, resource_id):
        url = '/api/v1.0/{}/{}'.format(resource_name, resource_id)
        return self.client.get(url, content_type='application/json')

    def get_resources(self, resource_name):
        url = '/api/v1.0/{}/'.format(resource_name)
        return self.client.get(url, content_type='application/json')

    def setUp(self):
        Base.metadata.create_all(bind=self.con)
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        Base.metadata.drop_all(bind=self.con)

    def test_create_area(self):
        with self.app.test_request_context():
            rv = self.create_resource('area', {'name': 'Test Area 01'})
            data = json.loads(rv.data)
            self.assertEqual(data["name"], "Test Area 01")

    def test_get_area(self):
        with self.app.test_request_context():
            self.create_resource('area', {'name': 'Test Area 01'})
            resp = self.get_resource('area', 1)
            data = json.loads(resp.data)
            self.assertEqual(data["name"], 'Test Area 01')

    def test_get_multiple_areas(self):
        with self.app.test_request_context():
            self.create_resource('area', {'name': 'Test Area 01'})
            self.create_resource('area', {'name': 'Test Area 02'})
            self.create_resource('area', {'name': 'Test Area 03'})
            resp = self.get_resources('areas')
            data = json.loads(resp.data)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[1]['name'], 'Test Area 02')

    def test_create_river(self):
        with self.app.test_request_context():
            a = self.create_resource('area', {'name': 'Test Area 01'})
            river = self.create_resource('river', {'name': 'Test River 01',
                                                   'area_id': 1})
            area = json.loads(a.data)
            river = json.loads(river.data)
            self.assertEqual(area['name'], river['area']['name'])

    def test_missing_area(self):
        with self.app.test_request_context():
            river = self.create_resource('river',
                                         {'name': 'Test River 01',
                                          'area_id': 4})
            river = json.loads(river.data)
            self.assertEqual(river['area'], None)

    def test_river_with_sections(self):
        with self.app.test_request_context():
            a = self.create_resource('area', {'name': 'Test Area 01'})
            river = self.create_resource('river', {'name': 'Test River 01',
                                                   'area_id': 1})
            section1 = self.create_resource('section')




    # def test_create_river(self):
    #     a_resp = self.create_resource('area', {'name': 'Test Area 01'})
    #     area_id = a_resp.json()['id']
    #     r = self.create_resource('river', {'name': 'Test River 01',
    #                                        'area_id': area_id})
    #     self.assertEquals(r.json()['name'], 'Test River 01')