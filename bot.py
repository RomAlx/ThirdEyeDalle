import logging

from aiogram import executor

import create_bot
from create_bot import dp
from data_base import mysql_db

from handlers import client, admin, other

# Configure logging
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот вышел в онлайн')
    mysql_db.db_start()
    client.register_handlers_client(create_bot.dp)

if __name__ == '__main__':
    executor.start_polling(create_bot.dp, skip_updates=True, on_startup=on_startup)