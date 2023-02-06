# Elevator-System-django
A challenge to implement the business logic for a simplified elevator model in Python. It decides whether the elevator should go up, go down, or stop. An elevator system, which can be initialised with N elevators and maintains the elevator states as well.

### Documentation in `docs/`

## Run Project:
1. Pre-requisites:
    1. Make sure to have the docker installed.
    1. Make sure to have port `8000` (for Django Application), `5432` (for PostgreSQL) open on the system.
1. Run Application:
    1. ```docker compose build```
    1. ```docker compose run --detach```
1. Get logs
    1. ```docker compose logs --follow [django|postgres]```
1. Shutdown:
    1. ```docker compose down```
