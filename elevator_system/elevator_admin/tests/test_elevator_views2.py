from django.conf import settings  # noqa
from rest_framework import status  # noqa
from rest_framework.test import APIClient, APITestCase  # noqa


class TestElevator2(APITestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_dummy2(self):
        self.assertEqual(1, 1)
