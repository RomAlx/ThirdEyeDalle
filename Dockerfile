FROM python:latest

WORKDIR /usr/src/dalle-bot/

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app

COPY . .

