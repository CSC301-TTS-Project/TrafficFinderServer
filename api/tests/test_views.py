from api.ddb_actions import reset
from django.test import TestCase, Client
from django.test.utils import override_settings
import json


class ViewTest(TestCase):

    def tearDown(self):
        reset()

    def test_get_route(self):
        client = Client()
        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['Route'], [])

    def test_insert_node(self):
        client = Client()
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json")
        self.assertEqual(response_1.status_code, 200)

        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75126,
            'lng': -79.6347,
            'index': 1
        }), content_type="application/json")
        self.assertEqual(response_2.status_code, 200)

        # Should correspond to this segment https://tinyurl.com/y5ymsllm
        self.assertEqual(json.loads(response_2.content)['1'], [{"id": 1033, "lat": 43.75079, "lng": -79.63473},
                                                               {"id": 1034, "lat": 43.75126, "lng": -79.6347}])

        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content)['Route'], [[{'id': 30326191, 'lat': 43.75079, 'lng': -79.63473}],
                                                                 [{'id': 1033, 'lat': 43.75079, 'lng': -79.63473},
                                                                  {'id': 1034, 'lat': 43.75126, 'lng': -79.6347}]])

    def test_delete_node(self):
        client = Client()
        response_1 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75079,
            'lng': -79.63473,
            'index': 0
        }), content_type="application/json")
        self.assertEqual(response_1.status_code, 200)

        response_2 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75126,
            'lng': -79.6347,
            'index': 1
        }), content_type="application/json")
        self.assertEqual(response_2.status_code, 200)

        response_3 = client.delete('/api/deleteNode', json.dumps({
            'route': 0,
            'index': 1
        }), content_type="application/json")

        self.assertEqual(response_3.status_code, 200)
        # should be empty
        self.assertEqual(json.loads(response_3.content), {})

        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['Route'], [[{'id': 30326191, 'lat': 43.75079, 'lng': -79.63473}]])
