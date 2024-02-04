# techlog-article-service

## Introduction
- This is the repository of the APIs that my TechLog blog will use in order to do the CRUD operations on the article data


## History
- Initially this project was planned to be implemented as an [Express.js](https://expressjs.com/) backend service.
- However, having decided to be a Python/ML expert, I have decided to use [FastAPI](https://fastapi.tiangolo.com/).
- Hence this project has been migrated from the previous TS codebase into the Python codebase using FastAPI, which you currently see as of now.


## Tech Stack
- This project uses the following list of technologies
  - Backend Framework: FastAPI with [Python](https://www.python.org/) version 3.11
  - Database: we use Google's [Firestore](https://cloud.google.com/firestore)
    - since AWS RDS or GCP Cloud SQL have relatively high costs for running the DB servers, we switched to other options, and one of them was Firestore
    - originally, it was [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
      - for the driver adapter, I use [asyncpg]((https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.asyncpg)); this is because I wanted to implement the I/O operations as asynchrous ones as much as possible
      - for database migration, I use [alembic 1.10.3](https://alembic.sqlalchemy.org/en/latest/)
      - why choose alembic over other ORM-agonostic tools such as flyway or liquibase?: see [this link on how we usually organize a microservice and its DB](https://www.prisma.io/dataguide/managing-databases/microservices-vs-monoliths#how-do-microservices-affect-database-architecture)

  - Python related tools
    - package managing tool: [poetry](https://python-poetry.org/)
    - code formatter: [black](https://black.readthedocs.io/en/stable/)
    - linter: [ruff](https://beta.ruff.rs/docs/)
    - unit testing: [pytest](https://pytest.org/)
    - I wrote an [article on these tools](https://dev.to/uponthesky/python-how-to-begin-your-new-python-project-4607)

  - CI/CD tools
    - [Github Actions](https://docs.github.com/en/actions)(cloud vendor specific deployment workflows are to be added in the production code)
    - [Terraform](https://www.terraform.io/) is used for managing the overall infrastructure

- These are the tools that I will adopt in the near future
  - Cache layer: [Redis](https://redis.io/)
  - Monitoring tool: [Sentry](https://sentry.io/welcome/)
  - test coverage tool


## Project Design

### Architecture
This project tries to adopt what is called [Hexagonal pattern](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)). This may be a little bit of overkill for this small project. However, this pattern allows us to follow the SOLID principle easier, and the code becomes more readable and testable.

Above of all, I am very happy with this pattern since it forces the developer to think the business logic(the "domain" layer) first, so that we can quickly adjust to any frequent changes in the codebase.

### Serverless
This project is based on the serverless technologies, such as AWS Lambda and serverless database services.
