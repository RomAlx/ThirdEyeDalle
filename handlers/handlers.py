import requests

import json

import main
from open_ai import thirdeye

from texts import WELCOME_MESSAGE, MAIN_MESSAGE, EXCEPTION_MESSAGE, HELP_MESSAGE, EMPTY_MESSAGE, ABOUT_MESSAGE, \
    CONTACTS_MESSAGE, CHECK_MESSAGE, AUTH_NO_MESSAGE, GENERATE_MESSAGE, THANKS_MESSAGE, UPGRADE_MESSAGE1, \
    UPGRADE_MESSAGE2
from texts import GENERATE_BTN, ABOUT_BTN, CONTACTS_BTN, CANCEL_BTN, UP1_BTN, UP2_BTN
from keyboards import KEYBOARD_WELCOME, MAIN_MENU, KEYBOARD_CORRECT_AUTH

check = {}


async def auth_check(chat_id, r):
    try:
        user_status = await main.bot.get_chat_member(-1001534006781, chat_id)
        if user_status.status == 'left':
            await main.bot.send_message(chat_id, CHECK_MESSAGE, reply_markup=KEYBOARD_CORRECT_AUTH)
            await main.bot.send_message(chat_id, AUTH_NO_MESSAGE, reply_markup=MAIN_MENU)
        else:
            global check
            check = r
            await main.bot.send_message(chat_id, GENERATE_MESSAGE)
    except Exception as ex:
        print(ex)
        await main.bot.send_message(chat_id, EXCEPTION_MESSAGE)


async def message_handler(r):

    if 'message' in r:
        global check
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        message_id = r['message']['message_id']
        try:
            if message == '/start':
                await main.bot.send_message(chat_id, text=WELCOME_MESSAGE, reply_markup=KEYBOARD_WELCOME,
                                            disable_web_page_preview=True)
            elif message == '/help':
                await main.bot.send_message(chat_id, text=HELP_MESSAGE, reply_markup=MAIN_MENU,
                                            disable_web_page_preview=True)
            elif message == GENERATE_BTN:
                await auth_check(chat_id, r)
            elif message == CANCEL_BTN:
                await auth_check(chat_id, r)
            elif message == ABOUT_BTN:
                await main.bot.send_message(chat_id, text=ABOUT_MESSAGE, reply_markup=MAIN_MENU,
                                            parse_mode='MarkdownV2', disable_web_page_preview=True)
            elif message == CONTACTS_BTN:
                await main.bot.send_message(chat_id, text=CONTACTS_MESSAGE, reply_markup=MAIN_MENU)
            elif message == UP1_BTN:
                await thirdeye.upgrade_img(1, chat_id, message_id)
            elif message == UP2_BTN:
                await thirdeye.upgrade_img(2, chat_id, message_id)
            else:
                check_message = check['message']['text']
                check_message_id = check['message']['message_id']
                if check_message == GENERATE_BTN and check_message_id == (message_id - 2):
                    #print('try gen')
                    thirdeye.main_media_group[chat_id] = None
                    await thirdeye.generate_img(chat_id, message_id, message)
                elif check_message == CANCEL_BTN and check_message_id == (message_id - 2):
                    #print('try regen')
                    thirdeye.main_media_group[chat_id] = None
                    await thirdeye.generate_img(chat_id, message_id, message)
                else:
                    await main.bot.send_message(chat_id, text=EMPTY_MESSAGE, reply_markup=MAIN_MENU,
                                            parse_mode='MarkdownV2', disable_web_page_preview=True)
        except Exception as ex:
            print(ex)
            await main.bot.send_message(chat_id, EXCEPTION_MESSAGE)
    if 'callback_query' in r:
        chat_id = r['callback_query']['message']['chat']['id']
        data = r['callback_query']['data']
        try:
            if data == 'yes':
                await main.bot.send_message(chat_id, MAIN_MESSAGE, reply_markup=MAIN_MENU)
            if data == 'member':
                user_status = await main.bot.get_chat_member(-1001534006781, chat_id)
                if user_status.status == 'left':
                    await main.bot.send_message(chat_id, CHECK_MESSAGE, reply_markup=KEYBOARD_CORRECT_AUTH)
                    await main.bot.send_message(chat_id, AUTH_NO_MESSAGE, reply_markup=MAIN_MENU)
                else:
                    await main.bot.send_message(chat_id, CHECK_MESSAGE)
                    await main.bot.send_message(chat_id, THANKS_MESSAGE)
                    await main.bot.send_message(chat_id, MAIN_MESSAGE, reply_markup=MAIN_MENU)
        except Exception as ex:
            print(ex)
            await main.bot.send_message(chat_id, EXCEPTION_MESSAGE)