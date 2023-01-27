from .common import CommonConfig


class LocalConfig(CommonConfig):
    DEBUG = True
    ROOT_URLCONF = "elevator_system.urls"
