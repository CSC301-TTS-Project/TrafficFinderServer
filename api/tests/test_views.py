from boto3 import client
from api.ddb_actions import reset
from django.test import TestCase, Client
import json
from django.conf import settings
import geojson


class ViewTest(TestCase):

    def setUp(self) -> None:
        client = Client()
        response = client.post('/api/signup_user',
                               {'username': "TestUser",
                                'password': "qwerty",
                                'email': "test@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        reset()

    def test_login(self):
        client = Client()
        response = client.post('/api/login_user',
                               {'username': "TestUser",
                                'password': "qwerty"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.content))

    def test_get_route(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response = client.post('/api/getRoute', json.dumps({'route': 0}), content_type="application/json",
                               HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_insert_node(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_1.status_code, 200)

        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75126,
            'lng': -79.6347,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_2.status_code, 200)

        # Should correspond to this segment https://tinyurl.com/y5ymsllm
        self.assertEqual(json.loads(response_2.content)['1'], {
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326192, 'lat': 43.75126, 'lng': -79.6347},
            'coordinates': [[-79.63473, 43.75079], [-79.6347, 43.75094], [-79.6347, 43.75126]]
        })

        response = client.post(
            '/api/getRoute', json.dumps({'route': 0}), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

        # Corresponds to https://jsfiddle.net/176tzbq8/2/
        self.assertEqual(json.loads(response.content), [{
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473}, 'coordinates': []
        }, {
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326192, 'lat': 43.75126, 'lng': -79.6347},
            'coordinates': [[-79.63473, 43.75079], [-79.6347, 43.75094], [-79.6347, 43.75126]]
        }])

    def test_delete_node(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_1.status_code, 200)

        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75126,
            'lng': -79.6347,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_2.status_code, 200)

        response_3 = client.post('/api/deleteNode', json.dumps({
            'route': 0,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)

        self.assertEqual(response_3.status_code, 200)
        # should be empty
        self.assertEqual(json.loads(response_3.content), {})

        response = client.post('/api/getRoute', json.dumps(
            {'route': 0}), content_type="application/json", HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [{
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473}, 'coordinates': []
        }])

    def test_get_traffic_data(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_1.status_code, 200)
        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.744883,
            'lng': -79.610741,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_2.status_code, 200)

        response = client.post(
            '/api/getTrafficData',
            json.dumps(
                {
                    'selections': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    'route': 0,
                    'date_range': [
                        "2018-09-01",
                        "2018-09-07"],
                    'days_of_week': [
                        0,
                        3,
                        5],
                    'hour_range': [
                        7,
                        13]}),
            content_type="application/json",
            HTTP_AUTHORIZATION=token)

        # Corresponds to traffic data for route
        # https://jsfiddle.net/dh4w9ez2/12/

        assert response.status_code == 200
        assert response._headers['content-type'] == (
            'Content-Type', 'text/csv')
        assert response.content.startswith(
            b'route_num,num_days,link_obs,min_speed,mean_speed,max_speed,pct_50_speed,pct_85_speed,pct_95_speed,'
            b'std_dev_speed,min_tt,mean_tt,max_tt,std_dev_tt,total_length\n')

    def test_get_api_keys(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response = client.get('/api/getKeys', HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(json.loads(response.content))

    def test_modify_route(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_1.status_code, 200)

        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.749309,
            'lng': -79.635237,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_2.status_code, 200)

        response_3 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.747832,
            'lng': -79.632544,
            'index': 2
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_3.status_code, 200)

        response_4 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.747521,
            'lng': -79.633854,
            'index': 3
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_3.status_code, 200)

        response_modify = client.patch('/api/modifyNode', json.dumps({
            'route': 0,
            'index': 3,
            'lat': 43.747965,
            'lng': -79.631314,
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_modify.status_code, 200)

        assert json.loads(response_modify.content) == {
            "new_node": {"id": 1182083962, "lat": 43.74801, "lng": -79.63134},
            "segment_updates": {
                "3": {
                    "start_node": {"id": 30326160, "lat": 43.74774, "lng": -79.63243},
                    "end_node": {"id": 1182083962, "lat": 43.74801, "lng": -79.63134},
                    "coordinates": [
                      [-79.63243, 43.74774],
                      [-79.63183, 43.74789],
                      [-79.63147, 43.74798],
                      [-79.63134, 43.74801]
                    ]
                }
            }
        }

    def test_get_geo_json(self):
        client = Client()
        response = client.post('/api/login_user',
                               json.dumps({'username': "TestUser",
                                           'password': "qwerty"}),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        token = "Token " + json.loads(response.content)["token"]
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_1.status_code, 200)
        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.744883,
            'lng': -79.610741,
            'index': 1
        }), content_type="application/json", HTTP_AUTHORIZATION=token)
        self.assertEqual(response_2.status_code, 200)

        response3 = client.post('/api/getGeoJson',
                                json.dumps({'route': 0}),
                                content_type="application/json", HTTP_AUTHORIZATION=token)
        assert geojson.loads(response3.content).is_valid
