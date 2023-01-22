FROM python:3.9

WORKDIR /ThirdEyeDalle

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 main:app

COPY . .

