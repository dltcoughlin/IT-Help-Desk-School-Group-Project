FROM python:3.10.0 as base

ARG DB_URL

ENV DB_URL=$DB_URL

RUN pip3 install django

RUN pip3 install psycopg2-binary django-dotenv tzdata

FROM base as development

RUN mkdir app/

COPY . app/

WORKDIR app

RUN python3 manage.py makemigrations src

RUN python3 manage.py sqlmigrate src 0001

RUN python3 manage.py migrate

FROM development as test

CMD ["python3", "manage.py", "test"]

FROM test as build

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
