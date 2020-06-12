# Setup
FROM python:3.8-alpine
ENV PYTHONBUFFERED 1

# Set working directory
WORKDIR home/django/django_shiroe

# Install image dependencies
RUN apk add --update --no-cache postgresql-client git less openssh
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev jpeg-dev zlib-dev
RUN apk update && apk add bash

# Install python dependencies
COPY requirements/local.txt ./
COPY requirements/requirements.txt ./
RUN pip3 install -r local.txt

# Copy files into container
COPY ./ ./

# Create static & media file folders
RUN mkdir -p ./media
RUN mkdir -p ./static

# Create user and group
RUN addgroup -S djangogroup
RUN adduser -S -D -h ./ django djangogroup

# Set permissions
RUN chown -R django:djangogroup .
RUN chmod -R a+rwx ./

USER django

# Yaay!
CMD ./docker/commands/test.sh