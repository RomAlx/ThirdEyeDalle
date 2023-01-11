FROM python:3.11

WORKDIR /usr/src/dalle-bot/

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

