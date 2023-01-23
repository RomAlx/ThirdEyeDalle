from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_BOT

storage = MemoryStorage()

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


