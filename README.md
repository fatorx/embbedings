# FastAPI / Langchain / OpenAI / Gemini

This repository is a scaffold to create applications .

------

## Functionalities

- Receives a text input and checks if the input is valid.
- If the input is in Portuguese, it translates it to English.
- With the input processed, the Vanna AI service is used to generate a SQL query.

------

## Requirements

Todo

------
## Technologies

- Python 3.12 with FastAPI
- MySQL 8.0.32

------

## Quickstart - Docker and Tests

### First time

Create a build/mysql folder, to hold a volume for the database.
```bash
$ mkdir -t build/mysql
$ chmod -R 777 build/mysql
```

Create a copy of .env.example and fill the variables with the values of your choice (i.e. your database credentials, etc)
```bash
$ cp .env.example .env 
```

Execute docker compose

```bash
$ docker compose up -d --build 
```

### Running after build 

```bash
$ docker compose up -d
```

### Access documentation

In the browser, access http://0.0.0.0:8003/docs, for access to API methods in OpenAPI format.

------

### Running tests

```bash
$ docker exec -it api pytest
```