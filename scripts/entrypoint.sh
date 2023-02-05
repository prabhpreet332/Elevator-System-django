#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${DJANGO_POSTGRES_DATABASE}",
        user="${DJANGO_POSTGRES_USER}",
        password="${DJANGO_POSTGRES_PASSWORD}",
        host="${DJANGO_POSTGRES_HOST}",
        port="${DJANGO_POSTGRES_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

redis_ready() {
    python << END
import sys

from redis import Redis
from redis import RedisError


try:
    redis = Redis.from_url("${CELERY_BROKER_URL}", db=0)
    redis.ping()
except RedisError:
    sys.exit(-1)
END
}

until postgres_ready; do
    >&2 echo "Waiting for PostgreSQL to become available..."
    sleep 5
done
    >&2 echo "PostgreSQL is available"


python elevator_system/manage.py makemigrations --settings=elevator_system.config.local
python elevator_system/manage.py migrate --settings=elevator_system.config.local

exec "$@"