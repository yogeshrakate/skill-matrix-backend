# skill-matrix-backend

## Install dependencies

```bash
 pip install requirements.txt
```

### Note :- Make Sure to check the DB name and credentials

1) [src/script.py.mako]() :- (Variable Name) "sqlalchemy.url"

2) [src/api/database.py]() :- (Variable Name) "SQLALCHEMY_DATABASE_URL"


### Create a new migration
```
alembic revision --autogenerate -m "<migration_name>"
```


## Migrate Database

```
alembic upgrade head
```

## Run Server

```
uvicorn main:app --host 0.0.0.0 --port 8000
```
