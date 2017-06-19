import json
import unittest
import requests
from iwbt import create_app, get_db, get_session
from iwbt.models.rivers import Area


class TestRiverResourceAPI(unittest.TestCase):
    API_BASE = 'http://localhost:5000/api/v1.0/'

    def create_resource(self, resource_name, data):
        url = '/api/v1.0/' + resource_name
        r = self.client.post(url, data=json.dumps(data),
                             content_type='application/json')
        return r

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_area(self):
        rv = self.create_resource('area', {'name': 'Test Area 01'})
        data = json.loads(rv.data)
        self.assertEqual(data["name"], "Test Area 01")
        session = get_session(self.app)
        print session.query(Area).all()
        #print self.client.get('/api/v1.0/areas/').data

    # def test_create_river(self):
    #     a_resp = self.create_resource('area', {'name': 'Test Area 01'})
    #     area_id = a_resp.json()['id']
    #     r = self.create_resource('river', {'name': 'Test River 01',
    #                                        'area_id': area_id})
    #     self.assertEquals(r.json()['name'], 'Test River 01')