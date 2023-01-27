from .common import CommonConfig


class TestConfig(CommonConfig):
    DEBUG = False
    TEST_RUNNER = "django.test.runner.DiscoverRunner"
    ROOT_URLCONF = "elevator_system.elevator_system.urls"
