### Setup

Setup a Postgres instance via Docker:

```
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres
```

Restore database after you have retrieved a recent dump:

```
export PGPASSWORD=postgres && pg_restore -h localhost -d postgres <dump-file-name>.tar -c -U postgres
```