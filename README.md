# Library service

## Installing using github
1. git clone https://github.com/xborismenx/library_service.git
2. cd library_service
3. python -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. set all variables in env.sample for work with postgres 
7. python manage.py migrate
8. python manage.py runserver


## Run with docker
1. Docker should be installed
2. Create .env file based in .env.sample and fill it with necessary data
3. docker compose build
4. docker compose up