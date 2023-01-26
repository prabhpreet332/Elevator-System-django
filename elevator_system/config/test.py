from .local import LocalConfig
class TestConfig(LocalConfig):
    TEST_RUNNER="django.test.runner.DiscoverRunner"