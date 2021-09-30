# pull official base image
FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
# set work directory

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# install dependencies

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /cars-rest-api

WORKDIR /cars-rest-api
COPY ./cars-rest-api/ /cars-rest-api

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput
RUN mkdir -p /vol/web/static
# add and run as non-root user
RUN adduser -D myuser

RUN chown -R myuser:myuser /vol/
RUN chmod -R 755 /vol/web
USER myuser

CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
