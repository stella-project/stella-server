# stella-server

#### Setup:
```
docker-compose up -d
```

#### API endpoints

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
