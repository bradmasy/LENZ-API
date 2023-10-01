# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

ENV SECRET_KEY='django-insecure-q7atufjzx2=&a^btpq0n1n^k)pwl)z*%8idzje=390g*3iz#bh'
# ENV POSTGRES_DB=SavvyGrocerMain
# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=password
# ENV POSTGRES_HOST=127.0.0.1

# run gunicorn
CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT