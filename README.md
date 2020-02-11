# stella-server

The STELLA server provides the following services:

1. User administration (administration of admins, participants and sites)
2. Dashboard service
3. Automated generation of the STELLA app &rarr; `docker-compose.yml`  
4. ~~Benchmark service: Comparison of experimental systems against baseline (production system)~~
5. Data storage (user feedback) for data analysis, training, etc.

#### Setup:
```
docker-compose up -d
```

#### API endpoints

Use `util/fill-db.py` to fill database with dummy data.

---

`/stella/api/v1/sessions` 

`GET` Get all sessions in database.

`POST` Post new session.

---

`/stella/api/v1/sessions/<int:id>` 

`GET` Get session by id `<int:id>`.

---

`/stella/api/v1/sessions/<int:id>/rankings` `GET` `POST`

`GET` Get rankings of session by id `<int:id>`.

`POST` Post new ranking to session with id `<int:id>`.

---

`/stella/api/v1/rankings` 

`GET` Get all rankings.

---

`/stella/api/v1/rankings/<int:id>`

`GET` Get ranking by id `<int:id>`.

#### Run server without container for dev purposes:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```