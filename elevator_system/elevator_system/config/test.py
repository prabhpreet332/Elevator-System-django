from pathlib import Path

from .local import *  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
TEST_RUNNER = "django.test.runner.DiscoverRunner"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
