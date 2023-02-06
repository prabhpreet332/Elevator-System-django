## DB Model
<i>Please see the file db_schema.png</i>

## Directory Structure
### Different django-apps and directories
Apps:
1. `elevator`<br>Contains the code for Elevator and Floor entities.
1. `elevator_admin`<br>Contains the code for Elevator System Admin and Elevator Request Handler entities.

Directories:
1. `utils`<br>Contains the misc code utilized by the apps. Eg: `utils.elevator_manager.ElevatorManager` class has the `accept_request()` and `process_request()` methods that drive the elevator system operations.

### Directory Tree

```
├── docker-compose.yaml
├── Dockerfile
├── docs
│   └── Elevator Problem Statement.pdf
├── elevator_system
│   ├── manage.py
│   ├── elevator
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   └── views.py
│   ├── elevator_admin
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests
│   │   └── views.py
│   ├── elevator_system
│   │   ├── asgi.py
│   │   ├── config
│   │   ├── db.sqlite3
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── utils
│       ├── __init__.py
│       ├── elevator_manager.py
│       └── utils.py
├── README.md
├── requirements-ci.txt
├── requirements.txt
├── scripts
│   ├── ci-lint.sh
│   ├── entrypoint.sh
│   └── start_script.sh
└── setup.cfg


```

## Packages installed
1. requirements.txt
    1. `Django` - Django base package
    1. `django-cors-headers` - To have the CORS middleware to prevent CORS sharing vulnerability
    1. `djangorestframework` - For building REST APIs
    1. `django-model-utils` - For having SoftDeletable Models
    1. `django-extensions` - For having Timestamped Models (for elevator requests)
    1. `psycopg2-binary` - Postgres Driver for using with ORM
    1. `gunicorn` - for having WSGI server (used with production settings)
    1. `django-filter` - for adding query params support

1. requirements-ci.txt
    1. `black` - for formatting
    1. `flake8` - for linting
    1. `isort` - for formatting imports
    1. `coverage` - for coverage reports
