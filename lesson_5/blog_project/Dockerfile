FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /lesson_5

COPY requirements.txt /lesson_5/

RUN pip install -r requirements.txt

COPY . /lesson_5/

ENV PYTHONPATH /lesson_5

EXPOSE 5000