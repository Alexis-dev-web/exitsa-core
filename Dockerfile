FROM python:3.12

ENV TZ=America/Mexico_City

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    tzdata \
    && pip install psycopg2

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD ["gunicorn", "exitosa_core.wsgi:application", "--bind", "0.0.0.0:8000"]
