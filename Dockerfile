# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /app

# set environment variables
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2

# install Celery dependencies
RUN apk add --no-cache libffi-dev

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

ENV SECRET_KEY=${DJANGO_SECRET_KEY}

# Make new migrations
RUN python manage.py makemigrations

# Migrate
RUN python manage.py migrate

# ENV POSTGRES_DB=LENZ-API
# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=password
# ENV POSTGRES_HOST=127.0.0.1

# run gunicorn
CMD celery -A project worker -l info & celery -A project beat --loglevel=info & gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
