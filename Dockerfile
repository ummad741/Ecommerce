FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /djangoapp
COPY requirements.txt /djangoapp/requirements.txt
RUN pip install -r requirements.txt
COPY . /djangoapp/

EXPOSE 8000
