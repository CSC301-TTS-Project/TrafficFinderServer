from django.test import TestCase

# Create your tests here.
class DummyTestCase(TestCase):
    def setUp(self):
        pass

    def test_hello_world(self):
        self.assertEqual(True, True)