from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from django.conf import settings

class TestElevator(APITestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_dummy(self):
        self.assertEqual(1,1)
