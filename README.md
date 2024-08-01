## exitosa-core

Create core to exitosa store

## How to setup

## Requirements

    1. Docker version 26.00 or greter
    2. Python version 3.12

## Local Development

1. Rename `.env.dev.template` to `.env.

2. Build development container (run on terminal):

    ```
       $ docker-compose -f docker-compose.yml up -d --build
    ```

3. Run migrations from container exitosa-core execute:

    ```
       $ python manage.py migrate
    ```

The project is running on http://127.0.0.1:1337

## Dev Guide

User default:
    email: 'admin@exitosa.com'
    password: 'Exitosa1234'

### Migrations

1. Crete new migration detecting change in models

    ```
        $ python manage.py makemigrations
    ```

2. Create empty migrations.

    ```
        $ python manage.py makemigrations --empty <yourappname>
    ```
