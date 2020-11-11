from api.ddb_actions import reset
from django.test import TestCase, Client
from django.test.utils import override_settings
import json

import logging

log = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
log.setLevel(logging.DEBUG)


@override_settings(DEBUG=True)
class ViewTest(TestCase):
    def tearDown(self):
        reset()

    def test_get_route(self):
        client = Client()
        response = client.generic(method="GET", path='/api/getRoute', data=json.dumps({'route': 0}))
        self.assertEqual(response.status_code, 200)

