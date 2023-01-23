import logging

from aiogram import executor

import create_bot

from handlers import client

# Configure logging
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('Бот вышел в онлайн')
    client.register_handlers_client(create_bot.dp)

if __name__ == '__main__':
    executor.start_polling(create_bot.dp, skip_updates=True, on_startup=on_startup)