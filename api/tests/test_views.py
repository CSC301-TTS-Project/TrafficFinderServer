from django.test import TestCase
from api.ddb_actions import reset

import logging
logger = logging.getLogger(__name__)
logging.disable(logging.NOTSET)
logger.setLevel(logging.DEBUG)


class ViewTest(TestCase):
    def tearDown(self):
        reset()

    def test_get_route(self):
        logger.log("TEST")
        response = self.client.get('/getRoute', {'route': 0})
        assert response.status_code == 200
