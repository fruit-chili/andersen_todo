FROM python:3.10.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code/andersen_todo

RUN pip install --upgrade pip
COPY requirements.txt /code/andersen_todo
RUN pip install -r requirements.txt

COPY . /code/
