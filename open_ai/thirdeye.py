import openai
import requests
import os
from aiogram import types, Dispatcher



import create_bot
from data_base import mysql_db

from keyboards import KEYBOARD_WORK, SPECIAL_MENU, MAIN_MENU
from texts import WORK_MESSAGE, ABOUT_MESSAGE, CONTACTS_MESSAGE, GENERATE_MESSAGE, EXCEPTION_MESSAGE, UPGRADE_MESSAGE1, \
    UPGRADE_MESSAGE2
from texts import ABOUT_BTN, CONTACTS_BTN, GENERATE_BTN

from config import SECRET_OPENAI

openai.api_key = SECRET_OPENAI

main_media_group = {}

async def generate_img(message, prompt):
    try:
        main = main_media_group.get(message.chat.id)
        if message.text == ABOUT_BTN:
            await create_bot.bot.send_message(message.from_user.id, ABOUT_MESSAGE, reply_markup=MAIN_MENU, parse_mode='MarkdownV2',
                             disable_web_page_preview=True)
        elif message.text == CONTACTS_BTN:
            await create_bot.bot.send_message(message.from_user.id, CONTACTS_MESSAGE, reply_markup=MAIN_MENU)
        else:
            if main is None:
                await mysql_db.db_write_data(message)
                await create_bot.bot.send_message(message.from_user.id, WORK_MESSAGE, reply_markup=SPECIAL_MENU)
                response = openai.Image.create(
                    prompt=prompt,
                    n=2,
                    size="1024x1024"
                )
                media = types.MediaGroup()
                media.attach_photo(response['data'][0]['url'])
                media.attach_photo(response['data'][1]['url'])
                main_media_group[message.chat.id] = [prompt, response['data'][0]['url'], response['data'][1]['url']]
                await create_bot.bot.send_media_group(message.chat.id, media=media)
                await create_bot.bot.send_message(message.from_user.id,
                                 text=f'👁 {prompt}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                 parse_mode='MarkdownV2', disable_web_page_preview=True, reply_markup=KEYBOARD_WORK)
    except Exception as ex:
        await create_bot.bot.send_message(message.from_user.id, EXCEPTION_MESSAGE)


async def upgrade_img(call, photo_num, id):
    try:
        await call.answer()
        if photo_num == 1:
            await create_bot.bot.send_message(id, UPGRADE_MESSAGE1, reply_markup=SPECIAL_MENU)
        if photo_num == 2:
            await create_bot.bot.send_message(id, UPGRADE_MESSAGE2, reply_markup=SPECIAL_MENU)
        print("Request")
        r = requests.get(main_media_group[id][photo_num])
        print("save pic")
        with open(f'img/{id}.png', 'wb') as f:
            f.write(r.content)
        print("clear info")
        prompt = main_media_group[id][0]
        main_media_group[id] = None
        print("Request to open ai")
        response = openai.Image.create_variation(
            image=open(f'img/{id}.png', 'rb'),
            n=1,
            size="1024x1024"
        )
        print("Delete pic")
        os.remove(f'img/{id}.png')
        print("Save url")
        image_url = response['data'][0]['url']
        print(image_url)
        await create_bot.bot.send_photo(chat_id=id, photo=image_url,
                       caption=f'👁 {prompt}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                       parse_mode='MarkdownV2', reply_markup=MAIN_MENU)
    except Exception as ex:
        await create_bot.bot.send_message(call.message.from_user.id, EXCEPTION_MESSAGE)
