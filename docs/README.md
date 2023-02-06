Directory Structure

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