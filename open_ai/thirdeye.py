import openai
import requests
import os
import time
from aiogram import types

import create_bot
from data_base import mysql_db

from keyboards import KEYBOARD_WORK, SPECIAL_MENU, MAIN_MENU
from texts import WORK_MESSAGE, WAIT_MESSAGE, ABOUT_MESSAGE, CONTACTS_MESSAGE, EXCEPTION_MESSAGE, UPGRADE_MESSAGE1, \
    UPGRADE_MESSAGE2
from texts import ABOUT_BTN, CONTACTS_BTN

from config import SECRET_OPENAI

openai.api_key = SECRET_OPENAI

main_media_group = {}

counter_gen = 0
counter_upd = 0
counter_all = 0
start_time = time.time_ns()
queue_gen = []
queue_upd = []


async def generate_img(chat_id, prompt):
    try:
        if prompt == ABOUT_BTN:
            await create_bot.bot.send_message(chat_id, ABOUT_MESSAGE, reply_markup=MAIN_MENU, parse_mode='MarkdownV2',
                             disable_web_page_preview=True)
        elif prompt == CONTACTS_BTN:
            await create_bot.bot.send_message(chat_id, CONTACTS_MESSAGE, reply_markup=MAIN_MENU)
        else:
            if main_media_group.get(chat_id) is None:
                global counter_gen
                global counter_upd
                global counter_all
                global start_time
                await create_bot.bot.send_message(chat_id, WORK_MESSAGE, reply_markup=SPECIAL_MENU)
                await create_bot.bot.send_message(chat_id,
                                                  WAIT_MESSAGE + str(counter_all//50+1) + ' мин',
                                                  reply_markup=SPECIAL_MENU)
                counter_gen = counter_gen + 1
                counter_all = counter_gen + counter_upd
                count = counter_gen
                queue_gen.append([chat_id, prompt])
                await mysql_db.db_write_data(chat_id, prompt)
                for i in range(count):
                    if counter_all > 50 and time.time() - start_time < 60:
                        start_time = time.time()
                        await create_bot.bot.send_message(chat_id, WORK_MESSAGE,
                                                          reply_markup=SPECIAL_MENU)
                        break
                    else:
                        counter_gen = counter_gen - 1
                        counter_all = counter_all - 1
                        gen = queue_gen.pop(0)
                        response = openai.Image.create(
                            prompt=gen[1],
                            n=2,
                            size="1024x1024"
                        )
                        media = types.MediaGroup()
                        media.attach_photo(response['data'][0]['url'])
                        media.attach_photo(response['data'][1]['url'])
                        main_media_group[gen[0]] = [gen[1], response['data'][0]['url'], response['data'][1]['url']]
                        await create_bot.bot.send_media_group(gen[0], media=media)
                        await create_bot.bot.send_message(gen[0],
                                         text=f'👁 {gen[1]}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                         parse_mode='MarkdownV2', disable_web_page_preview=True, reply_markup=KEYBOARD_WORK)
    except Exception as ex:
        await create_bot.bot.send_message(chat_id, EXCEPTION_MESSAGE)


async def upgrade_img(photo_num, chat_id):
    try:
        if photo_num == 1:
            await create_bot.bot.send_message(chat_id, UPGRADE_MESSAGE1, reply_markup=SPECIAL_MENU)
        if photo_num == 2:
            await create_bot.bot.send_message(chat_id, UPGRADE_MESSAGE2, reply_markup=SPECIAL_MENU)
        global counter_gen
        global counter_upd
        global counter_all
        global start_time
        counter_upd = counter_upd + 1
        counter_all = counter_gen + counter_upd
        count = counter_upd
        queue_upd.append([photo_num, chat_id])
        for i in range(count):
            if counter_all > 50 and time.time() - start_time < 60:
                start_time = time.time()
                break
            else:
                await create_bot.bot.send_message(chat_id,
                                                  WAIT_MESSAGE + str(counter_all//50+1) + ' мин',
                                                  reply_markup=SPECIAL_MENU)
                counter_gen = counter_gen - 1
                counter_all = counter_all - 1
                upd = queue_upd.pop(0)
                r = requests.get(main_media_group[upd[1]][photo_num])
                with open(f'img/{upd[1]}.png', 'wb') as f:
                    f.write(r.content)
                prompt = main_media_group[upd[1]][0]
                main_media_group[upd[1]] = None
                response = openai.Image.create_variation(
                    image=open(f'img/{upd[1]}.png', 'rb'),
                    n=1,
                    size="1024x1024"
                )
                os.remove(f'img/{upd[1]}.png')
                image_url = response['data'][0]['url']
                await create_bot.bot.send_photo(chat_id=upd[1], photo=image_url,
                               caption=f'👁 {prompt}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                               parse_mode='MarkdownV2', reply_markup=MAIN_MENU)
    except Exception as ex:
        await create_bot.bot.send_message(chat_id, EXCEPTION_MESSAGE)
