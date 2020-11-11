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
