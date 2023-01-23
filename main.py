import sys
from flask import Flask
from flask import request
from flask import jsonify
#from flask_sslify import SSLify

from aiogram import Bot

from config import TOKEN_BOT

import handlers

print(sys.prefix)

bot = Bot(token=TOKEN_BOT)

app = Flask(__name__)
#sslify = SSLify(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        handlers.message_handler(r)
        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


