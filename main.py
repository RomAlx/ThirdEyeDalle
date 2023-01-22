import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

from aiogram import Bot


from data_base import mysql_db

from config import TOKEN_BOT

import handlers

print(sys.prefix)

bot = Bot(token=TOKEN_BOT)

application = Flask(__name__)
sslify = SSLify(application)


@application.route(('/'+TOKEN_BOT), methods=['POST', 'GET'])
async def index():
    if request.method == 'POST':
        r = request.get_json()
        await handlers.message_handler(r)
        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    mysql_db.db_start()
    application.run(host='0.0.0.0')