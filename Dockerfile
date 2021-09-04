FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /box-backend
WORKDIR /box-backend
COPY . /box-backend

ADD  requirements.txt  /box-backend
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



CMD ["gunicorn", "--chdir", "chamedoon", "--workers", "3", "--bind", ":8000", "chamedoon.wsgi:application"]



