# tradecore-test
Tradecore interview test project.

## Running the application locally

To run the application locally, follow the following steps

+ Install docker and docker-compose
+ Copy the contents of the `.env_template` to `.env` and update the
relevant environment variables
+ Run the command `docker-compose up` and you should be all set. 

## Tech stack 

### DjangoRestFramework
source - [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
Used to write restful API endpoints

### simple JWT
source - [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
A JWT authentication backend for Django rest framework. 

### Celery
source - (https://docs.celeryproject.org/en/stable/)[https://docs.celeryproject.org/en/stable/]
Used to run tasks asynchronously. 

### requests
source - [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
Used to make http requests in python. 

### Factory Boy 
source - [https://factoryboy.readthedocs.io/en/stable/](https://factoryboy.readthedocs.io/en/stable/)
Used to create database fixtures which are then used in testing.

### Coverage
source - [https://coverage.readthedocs.io/en/coverage-5.5/](https://coverage.readthedocs.io/en/coverage-5.5/)
Tool to measure code coverage.

## Running tests

Tests use DjangoRestFramework's inbuilt `APITestCase` and `APIRequestFactory`. In order to run 
the tests use the following command. 
Each Django app has it's own tests written inside a `tests.py` file.

```
python manage.py test
```

Tests coverage can be check by running the following commands in sequence. 

```
coverage run --source='.' manage.py test
```
```
coverage report
```

Github actions have been used to setup a CI pipeline and so every time the code is pushed 
to github, the tests are ran automatically. 

