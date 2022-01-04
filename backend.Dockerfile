FROM node:14-alpine AS node

WORKDIR /app

# Install frontend dependencies
COPY ./package.json .
COPY ./package-lock.json .
RUN npm ci

# Build them
COPY ./tsconfig.json .
COPY ./webpack.config.js .
COPY ./static ./static
RUN npm run build

FROM python:3.8-alpine

WORKDIR /app

# Install native dependencies
RUN apk update && \
    apk add build-base jpeg-dev libpng-dev linux-headers gettext postgresql-dev libxml2-dev libxslt-dev libffi-dev bash

# Install gunicorn
RUN pip install gunicorn

# Install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

# Copy static files
COPY --from=node /app/webpack-stats.json .
COPY --from=node /app/static/dist ./static/dist
RUN rm -rf ./static/ts ./static/scss

VOLUME ["/app/staticfiles", "/app/media"]

# Set up
EXPOSE 8000

ENV WORKERS=4
ENTRYPOINT [ "/app/docker/django-entrypoint.sh" ]
CMD gunicorn -b 0.0.0.0:8000 -w $WORKERS --forwarded-allow-ips="*" main.wsgi:application
