# Follow steps from the website below
# https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
FROM python:3.8.1-slim-buster

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]