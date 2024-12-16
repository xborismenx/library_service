# Library service
A comprehensive library management system that enables users to borrow books and calculate payments based on borrowing duration.
## Technological stack
- Python3.12
- Django Rest Framework
- Aiogram 
- Django-Q 
- Postgres
- drf-spectacular 
## Features
### Admin features
- CRUD books
- Receiving notifications in TG when creating new borrowings or overdue older
- Manage borrowing records
### User features
- Browse available books
- Borrow books with a simple checkout process
- Calculate payments based on borrowing duration

## Installing using github
1. git clone https://github.com/xborismenx/library_service.git
2. cd library_service
3. python -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. set all variables in env.sample for work with postgres and rename to .env 
7. Create scheduled task to check overdue borrowings (borrowings.tasks.overdue_borrowings)
8. python manage.py migrate
9. python manage.py runserver

## Run with docker
1. Docker should be installed
2. Create .env file based in .env.sample and fill it with necessary data
3. docker compose build
4. docker compose up

## Features
Admin can create, update