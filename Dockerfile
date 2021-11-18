FROM reg.utabib.ir/devops/python:3.8.5-slim-buster

RUN apt-get update --fix-missing && apt-get install -qq -y \
    build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /utabib
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Ashkan Hadadi <hadadi.ashkan@gmail.com>>"
CMD gunicorn -w 10 --threads 2000 --log-level debug --timeout 200 -b 0.0.0.0:8081 --access-logfile - "application.app:create_app('application.config.DevelopmentConfig')"