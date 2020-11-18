from api.ddb_actions import reset
from django.test import TestCase, Client
import json


class ViewTest(TestCase):

    def tearDown(self):
        reset()

    def test_get_route(self):
        client = Client()
        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

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
        self.assertEqual(json.loads(response_2.content)['1'], {
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326192, 'lat': 43.75126, 'lng': -79.6347},
            'coordinates': [[-79.63473, 43.75079], [-79.6347, 43.75094], [-79.6347, 43.75126]]
        })

        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(json.loads(response.content), [{
            'start_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473},
            'end_node': {'id': 30326191, 'lat': 43.75079, 'lng': -79.63473}, 'coordinates': []
        }])

    def test_get_traffic_data(self):
        # TODO: Verify return vals after creating a route
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

        response = client.generic(method="GET", path='/api/getTrafficData', data=json.dumps({
            'route': 0,
            'date_range': ["2018-09-01", "2018-09-07"],
            'days_of_week': [0, 3, 5],
            'hour_range': [7, 13]
        }))

        assert response.status_code == 200
        assert response._headers['content-type'] == ('Content-Type', 'text/csv')
        assert response.content == b"hour,link_dir,length,hourly_mean_tt,link_obs\n" \
                                b"08:00:00,29492876F,52,41.0,1\n" \
                                b"10:00:00,29492876F,52,11.5,1\n"

    def test_modify_route(self):
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

        response_3 = client.post('/api/insertNode', json.dumps({
            'route': 0,
            'lat': 43.75126,
            'lng': -79.6347,
            'index': 2
        }), content_type="application/json")
        self.assertEqual(response_2.status_code, 200)

        response_4 = client.patch('/api/modifyNode', json.dumps({
            'route': 0,
            'index': 1,
            'lat': 43.75126,
            'lng': -79.6347,
        }), content_type="application/json")

        self.assertEqual(response_3.status_code, 200)