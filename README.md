# api
backend-api for Lenz API 

# Setup Instructions

## Technologies and Installations
- Database
    - Postgres SQL 
    - PG Admin 4
- Django Version 4.2.4
- Python Version 3.11

## Instructions

### Install Python Version 3.11

### Git Clone project

### Setup Python Virtual Environment
-  python -m venv ./env
    - this will create a virtual environment within the API directory called <b>env</b>
    - to enact virtual environment run <b>"./env/Scripts/activate"</b> from main API directory
    - note you must be in virtual environment in order to execute/run python and django commands.

### pip install requirements.txt
- this will install any dependencies
- if you are adding more dependencies to the project, please update requirements.txt by running the command <b>pip freeze > requirements.txt</b>
- NEW UPDATE:
    - update requirements.txt with the command <b>pipreqs . --force</b>

### Create A Database
- assuming postgres is installed correctly, on the command line run <b>createdb <db_name></b> to create a database within postgres, we will use this database name in the next steps

### Create A ".env" Configuration file

- in the main API Directory, create a file called ".env"
- we will use this as configuration for your API
    
- add the following lines to the file:
    - POSTGRES_DB=<db_name>
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=<db_password>
    - POSTGRES_HOST=127.0.0.1

### Run Migrations
- The application will always have migrations to run from previous updates etc, to run migrations run the following command:
    - python manage.py migrate
        - this will update your database and tables, it is very important we do not delete migration files and try to push a single migration per pull request
- to update migrations or add new ones to the application, run the following command:
    - python manage.py makemigrations
- to make migrations for a specific app to your database, run the following command:
    - python manage.py <app_name> makemigrations
- to perform migrations on a specific database, run the following command:
    - python manage.py makemigrations DATABASE=<db_name>

### Create A Super User
- a super user acts as an admin for the application as well as for django-admin, to create a super user run the following command:
    - python manage.py createsuperuser
        - follow the prompts to create the super user
        - remember your password! django automatically hashes passwords in the database making it quite difficult to retrieve

### Collect Static Files
= command:
    - python manage.py collectstatic
- what it does:
    - collects all the static files to run some of the various interfaces such as the admin interface

### Running Tests

- python manage.py test apps.<app-name>.tests
- this will run the tests located in the <b>tests</b> directory of the app
- all tests must start with the word <b>test</b> in order for Django to discover it
- write tests in this file and in actions we will target them to run

### Heroku Commands
- heroku container:push web --app savvygrocer
- heroku container:release web --app savvygrocer