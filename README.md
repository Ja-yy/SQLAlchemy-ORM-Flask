# SQLAlchemy-ORM-Flask
This repository accompanies the SQLAlchemy ORM structure for Flask

The APIs related to bookmarks were implemented for better understanding

## Setup

### Tools

This is the list of tools that you'll require for this project

* `pip` and `pipenv` for python dependency management.
* `migrate` for database migrations.
* `docker` for docker image creation.
* `docker-compose` for testing locally.

### Configuration

You'll have to perform the following configuration:

## Deploying localy

If you are on linux based system
```sh
make
```
If on windows based system

```
docker-compose up -d --build
```
## Flask Port

http://0.0.0.0:8000

## Routes

* register user-`post` -> http://0.0.0.0:8000/api/v1/auth/register
* to login-`post` -> http://0.0.0.0:8000/api/v1/auth/login 
* to get refresh token-`post` -> http://0.0.0.0:8000/api/v1/auth/token/refresh
* get all bookmarks-`get` -> http://0.0.0.0:8000/api/v1/bookmarks/
* add bookmarks-`post` -> http://0.0.0.0:8000/api/v1/bookmarks/
* get bookmark by id -`get` -> http://0.0.0.0:8000/api/v1/bookmarks/<id>
* update bookmark by id -`put` -> http://0.0.0.0:8000/api/v1/bookmarks/<id>
* delete bookmark by id - `delete` ->http://0.0.0.0:8000/api/v1/bookmarks/<id>
* redirect to bookmark link eith short link - `get` ->http://0.0.0.0:8000/api/v1/bookmarks/<short_url>
* bookmark stats - `get` -> http://0.0.0.0:8000/api/v1/bookmarks/stats
