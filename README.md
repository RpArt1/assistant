# FastAPI Application


This project is a FastAPI-based application designed to manage "memories" using a RESTful API. It allows users to create, read, update, and delete memories stored in a MariaDB database. The application is structured to use asynchronous database operations, ensuring high performance and scalability.

## Application Design and Architecture

### Framework & Language

- **Framework**: FastAPI
- **Programming Language**: Python 3.9

### Application Structure

- `main.py`: The entry point of the FastAPI application.
- `dependencies.py`: Contains dependency injection utilities, such as database session management.
- `models/`: Contains SQLAlchemy ORM models for MariaDB (`mariadb_models.py`) and schemas/models for Qdrant if used (`qdrant_models.py`).
- `schemas/`: Includes Pydantic models for request validation and response serialization for MariaDB (`mariadb_schemas.py`) and Qdrant (`qdrant_schemas.py`).
- `crud/`: Defines CRUD operations for interacting with MariaDB (`mariadb_crud.py`) and Qdrant (`qdrant_crud.py`).
- `routers/`: Organizes API routes into separate modules for MariaDB (`mariadb_router.py`) and Qdrant (`qdrant_router.py`).

### Infrastructure and Technologies

- **Databases**: MariaDB for relational data and Qdrant for vector search (optional).
- **Containerization**: Docker for containerizing the application and databases.
- **Orchestration**: Docker Compose for defining and running multi-container Docker applications.


## Setup and run application 
docker-compose build
docker-compose run

## tet running 

go to http://localhost:8000 and try test endpoint 