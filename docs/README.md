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