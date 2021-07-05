FROM python:3.7

RUN apt-get update && apt-get install -y libpq-dev gcc
# need gcc to compile psycopg2

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .

#CMD python manage.py db init &&\
#    python manage.py db migrate &&\
#    python manage.py db upgrade
