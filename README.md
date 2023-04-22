# techlog-article-service

## Introduction
- This is the repository of the APIs that my TechLog blog will use in order to do the CRUD operations on the article data

## History
- Initially this project was planned to be implemented in [Express.js](https://expressjs.com/) backend
- However, due to my personal reasons, I am now required to learn and use [FastAPI](https://fastapi.tiangolo.com/)
- Hence this project from now on will be migrated from the previous TS codebase into Python codebase using FastAPI

## Roadmap
- Techstacks are the followings(to be added)
  - Backend Framework: FastAPI with [Python typing system](https://docs.python.org/3/library/typing.html), and with [Python](https://www.python.org/) version 3.9

  - Database: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
    - for the driver adapter, I'll use  [asyncpg]((https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg))
    - for database migration, we'll use [alembic 1.10.3](https://alembic.sqlalchemy.org/en/latest/)
    - why choose alembic over other ORM-agonostic tools such as flyway or liquibase?: see [this link on how we usually organize a microservice and its DB](https://www.prisma.io/dataguide/managing-databases/microservices-vs-monoliths#how-do-microservices-affect-database-architecture)

  - Python related tools
    - package managing tool: [poetry](https://python-poetry.org/)
    - code formatter: [black](https://black.readthedocs.io/en/stable/)
    - linter: [ruff](https://beta.ruff.rs/docs/)
    - unit testing: [pytest](https://pytest.org/)

  - CI/CD tools
    - [Github Actions](https://docs.github.com/en/actions)
    - [Docker](https://www.docker.com/)
    - [Terraform](https://www.terraform.io/)
    - test coverage tool

1. Migrate into FastAPI

2. Separate the main server from this microservice

3. Integration/E2E Testing and Deploy

4. Add Features(TBA)
- Redis Cache
- Kafka

## File Structure
- check [this stackoverflow page](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application)
- many ideas have been around, and there is no "correct" answer, but I think we would better off following the corrent trend dealing with pyproject.toml
- so this project's file structure is largely based upon:
  - the official tutorial of [how to package a Python project](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
  - [pypa's sample project](https://github.com/pypa/sampleproject)

## TBA
