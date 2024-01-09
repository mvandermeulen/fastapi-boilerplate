# FastAPI REST API boilerplate

## Description <!-- omit in toc -->

FastAPI REST API boilerplate is a comprehensive starting point for developing robust web applications. It provides a structured foundation equipped with essential features and configurations.

<img src=".github/preview.png" alt="Swagger preview" />

## Table of Contents <!-- omit in toc -->

- [Features](#features)
- [Project structure](#project-structure)
- [Environmnent variables](#environmnent-variables)
- [Quick run](#quick-run)
- [Comfortable development](#comfortable-development)
- [Links](#links)
- [Database utils](#database-utils)
<!-- - [Tests](#tests)
- [Tests in Docker](#tests-in-docker)
- [Test benchmarking](#test-benchmarking) -->

## Features

- [x] Precommit ([Pre-commit](https://pre-commit.com/))
- [x] Config Service ([Pydantic](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)).
- [x] Database ([Sqlalchemy](https://www.sqlalchemy.org)).
- [x] Database migration ([Alembic](https://alembic.sqlalchemy.org))
- [x] Swagger.
- [x] Redoc.
- [x] Sign in and sign up via email.
- [x] Social sign in (apple, facebook, google, linkedin, microsoft)
- [x] Seeding ([sqlalchemyseed](https://sqlalchemyseed.readthedocs.io/en/stable/)).
- [x] Mailing
- [x] Realtime notification using [messaging queue](https://www.rabbitmq.com/) and [python-socketio](https://python-socketio.readthedocs.io/en/latest/server.html)
- [x] File uploads (aws s3, cloudinary, google cloud storage)
- [x] Redis
- [x] Admin and User roles using RBAC ([Casbin](https://casbin.org/fr/docs/rbac)).
- [x] Elasticseach (using [pgsync](https://pgsync.com/), [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html))
- [x] Docker.
- [ ] Admin dashboard using ([sqladmin](https://aminalaee.dev/sqladmin/))
- [ ] I18N
- [ ] E2E and units tests.
- [ ] Monitoring using grafana and prometheus ([Grafana](https://grafana.com/))
- [ ] CI ([Gitlab](https://docs.gitlab.com/ee/ci/)).

## Project Structure

```
seeder           # Configurtion for database seeding
migrations       # Alembic migration files
app              # Rest api files
app.core         # General components like config, security, types, role, etc...
app.db           # Database connection specific
app.crud         # CRUD for types from models
app.models       # Sqlalchemy models
app.schemas      # Pydantic models that used in crud or handlers
app.templates    # Html files for mails
app.endpoints    # Restapi endpoints files
```

```
├── app
|   |
│   ├── core
│   ├── crud
│   ├── db
│   ├── endpoints
│   │   ├── api.py
│   │   └── v1
│   │   └── v2
│   │   └── ...
│   ├── main.py
│   ├── models
│   ├── schemas
|   |
│   └── templates
|
├── migrations
├── seeder
|── .vscode
|── .github
|──...

```

## Environmnent variables
To correctly run the project, you will need some environment variables. Expose & import them in core/config.py

befor starting you need to generate RSA key pairs, both public and private keys.
You can use [this website](https://travistidwell.com/jsencrypt/demo/) or any other method you prefer to generate these keys.
Keep a note of the file paths where you save these keys on your project folder (like `private_key.pem` and `public_key.pem`) or local machine.


- `ENV` : Running Environment can be dev, staging, preprod
- `API_BASE_URL`: The pathname of the api version url
- `API_URL`: api base url
- `DB_HOST`: Postgres database host
- `DB_PORT`: Postgres database port
- `DB_NAME`: Postgres database name
- `DB_USER_NAME`: Postgres user
- `DB_PASSWORD`: Postgres password
- `SECRET_KEY`: Postgres password
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token duration
- `PRIVATE_KEY_PATH`: Specify the absolute file paths to the RSA private key you generated earlier (`private_key.pem` if you saved it in your project root folder)
- `PUBLIC_KEY_PATH`: Specify the absolute file paths to the RSA public key you generated earlier (`public_key.pem` if you saved it in your project root folder)
- `SMTP_TLS`: Indicates whether to use TLS (true or false) for SMTP email communication.
- `SMTP_PORT`: The port number for SMTP email communication.
- `SMTP_HOST`: The hostname or IP address of the SMTP server for sending emails.
- `SMTP_USER`: The username for authenticating with the SMTP server.
- `SMTP_PASSWORD`: The password for authenticating with the SMTP server.
- `RABBIT_MQ_HOST`: RabbitMQ host (localhost in this case)
- `RABBIT_MQ_PORT`: RabbitMQ port (5672 in this case)
- `RABBIT_MQ_PASSWORD`: RabbitMQ password (password123 in this case)
- `RABBIT_MQ_USER`: RabbitMQ user (root in this case)
- `APPLE_CLIENT_ID`: Apple OAuth client ID
- `APPLE_SECRET_KEY`: Apple OAuth secret key
- `APPLE_WEBHOOK_OAUTH_REDIRECT_URI`: Redirect URI for Apple OAuth callbacks
- `FACEBOOK_CLIENT_ID`: Facebook OAuth client ID
- `FACEBOOK_SECRET_KEY`: Facebook OAuth secret key
- `FACEBOOK_WEBHOOK_OAUTH_REDIRECT_URI`: Redirect URI for Facebook OAuth callbacks
- `GOOGLE_CLIENT_ID`: Google OAuth client ID
- `GOOGLE_SECRET_KEY`: Google OAuth secret key
- `GOOGLE_WEBHOOK_OAUTH_REDIRECT_URI`: Redirect URI for Google OAuth callbacks
- `LINKEDIN_CLIENT_ID`: LinkedIn OAuth client ID
- `LINKEDIN_SECRET_KEY`: LinkedIn OAuth secret key
- `LINKEDIN_WEBHOOK_OAUTH_REDIRECT_URI`: Redirect URI for LinkedIn OAuth callbacks
- `MSAL_CLIENT_ID`: Microsoft MSAL client ID
- `MSAL_CLIENT_SECRET`: Microsoft MSAL client secret
- `MSAL_WEBHOOK_OAUTH_REDIRECT_URI`: Redirect URI for Microsoft MSAL OAuth callbacks
- `CLOUDINARY_CLOUD_NAME`: The name of your Cloudinary cloud.
- `CLOUDINARY_API_KEY`: Your Cloudinary API key.
- `CLOUDINARY_API_SECRET`: Your Cloudinary API secret.
- `AWS_BUCKET_NAME`: The name of the AWS S3 bucket you want to access.
- `AWS_KEY_ID`: AWS access key ID for accessing the S3 bucket.
- `AWS_SECRET_KEY`: AWS secret key for accessing the S3 bucket.
- `AWS_REGION`: The AWS region where the S3 bucket is located.
- `GCS_BUCKET_NAME`: The name of the Google Cloud Storage (GCS) bucket you want to access.
- `REDIS_HOST`:
- `REDIS_PORT`:
- `REDIS_DB`:
- `ELASTIC_HOST`: Elasticsearch host, for exemple `http://elasticsearch:9200`
- `ELASTIC_CLUSTER_NAME`: Elasticsearch cluster name for exemple `elastic`, you can find it in docker-compose file
- `ELASTIC_PASSWORD`: Elasticsearch password for exemple `password123` you can find it in docker-compose file

## Quick run

```bash
git clone --depth 1 https://github.com/kaanari-tech/fastapi-boilerplate.git my-app
cd my-app/
docker-compose up -d --build
```

For check status run

```bash
docker-compose logs
```

## Comfortable development

```bash
git clone --depth 1 https://github.com/kaanari-tech/fastapi-boilerplate.git my-app
cd my-app/
cp .env.example .env
```

Change `DB_HOST=postgres` to `DB_HOST=localhost`,
`DB_PORT=5432` to `DB_PORT=6001`
`RABBIT_MQ_HOST=rabbitmq` to `RABBIT_MQ_HOST=localhost`
`REDIS_HOST=redis-cache` to `REDIS_HOST=localhost`
`ELASTIC_HOST=http://elasticsearch:9200` to `ELASTIC_HOST=http://localhost:9200`
make sure you have [poetry](https://python-poetry.org) install
Run additional container:

```bash
docker-compose up -d postgres-db redis-cache rabbitmq adminer elasticsearch
poetry install
poe migrate
docker-compose up -d pgsync
poe run
```

## Links

- Swagger: <http://localhost:8001/docs>
- Redoc: <http://localhost:8001/redoc>
- Openapi json: <http://localhost:8001/api/v1/openapi.json>
- Adminer (client for DB): <http://localhost:8080>

## Database utils

Generate migration

```bash
poe makemigrations
```

Run migration

```bash
poe migrate
```

Revert migration

```bash
poe dwngrade
```

Drop all tables in database

```bash
poe drop-tables
```
