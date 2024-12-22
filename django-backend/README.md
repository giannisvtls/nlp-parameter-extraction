# Intelligencia Django Backend Assessment

A Django application to serve as RESTful API backend. 

## Requirements

In order to run the project locally the following requirements should be already installed:

* Python >=3.12
* Pipenv
* PostgreSQL

## Running the project

### Configuration

Create a `.env` file in the root folder of the project \
Copy the environment variables from the `.env.sample` to the `.env` file \
Fill the Database configuration


### Run Locally

#### If you haven't already, create the database:

```sql
CREATE DATABASE efo_db;
```

#### Install dependencies

To activate this project's virtualenv, run the following command:
```shell
pipenv shell
```
To install all project dependencies you can run the following command:
```shell
pipenv install
```

#### Apply migrations

To apply any pending database migrations you can run the following command:

```shell
pipenv run python manage.py migrate
```

#### Serve API

The easiest way to run the project is to execute the following command:

```shell
pipenv run python manage.py runserver
```

## Documentation

After running the project, you can access the OpenApi documentation and interact with the API using the built-in
[swagger interface](http://127.0.0.1:8000/api/docs).