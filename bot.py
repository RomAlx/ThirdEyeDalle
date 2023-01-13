import telebot
import openai
import requests
import os
import pymysql

from telebot import types
from telebot.types import InputMediaPhoto

from auth_data import Token_Bot, Secret_OpenAI
from texts import WELCOME_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, CONTACTS_MESSAGE, CHECK_MESSAGE
from config_data_base import host, user, password, db_name

openai.api_key = Secret_OpenAI

main_media_group = {}

item1=types.KeyboardButton("🚀 Сгенерировать изображение")
item2=types.KeyboardButton("👁 О проекте")
item3=types.KeyboardButton("👨🏻‍💻 Контакты")

main_menu=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu.add(item1)
main_menu.row(item2, item3)

special_menu=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
special_menu.row(item2, item3)


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    def db_write_data(message):
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfuly connected...")
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `user` (`user_id`, `user_prompt`) VALUES (%s, %s)"
                    cursor.execute(insert_query, (str(message.chat.id), str(message.text)))
                    connection.commit()
                    print("db commited")
            finally:
                connection.close()
                print("connection close")
        except Exception as ex:
            print("Connection refused...")
            print(ex)

    def check_accept(message):
        global main_menu
        try:
            user_id = message.chat.id
            if bot.get_chat_member(-1001534006781, user_id).status == "left":
                keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
                key_yes = types.InlineKeyboardButton(text='✅ Я вступил!', callback_data='member')  # кнопка «Да»
                keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
                bot.send_message(message.chat.id, CHECK_MESSAGE, reply_markup=keyboard)
                return False
            else:
                return True
        except Exception as e:
            bot.reply_to(message, '🤖 Упс, попробуй снова\n/start')

    @bot.message_handler(commands=["start"])
    def start_message(message):
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='🌚 Да, вперед', callback_data='yes') # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=keyboard, disable_web_page_preview=True)

    @bot.message_handler(commands=["help"])
    def help_message(message):
        global main_menu
        if check_accept(message):
            bot.send_message(message.from_user.id, HELP_MESSAGE, reply_markup=main_menu, disable_web_page_preview=True)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):

        global main_media_group
        global main_menu
        global special_menu

        if call.data == "yes":
            try:
                bot.send_message(call.message.chat.id, "🌝 Чем могу помочь?", reply_markup=main_menu)
            except Exception as e:
                bot.reply_to(call.message, '🤖 Упс, попробуй снова\n/start')
        if call.data == "member":
            if bot.get_chat_member(-1001534006781, call.message.chat.id).status == "left":
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=CHECK_MESSAGE)
                    bot.send_message(call.message.chat.id, "😢 Вы не подписаны на наш канал", reply_markup=main_menu)
                except Exception as e:
                    bot.reply_to(call.message, '🤖 Упс, попробуй снова\n/start')
            else:
                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=CHECK_MESSAGE)
                    bot.send_message(call.message.chat.id, "🖤 Спасибо!", reply_markup=main_menu)
                    bot.send_message(call.message.chat.id, "🌝 Чем могу помочь?", reply_markup=main_menu)
                except Exception as e:
                    bot.reply_to(call.message, '🤖 Упс, попробуй снова\n/start')
        elif call.data == "cancel":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=main_media_group[call.message.chat.id][0], disable_web_page_preview=True)
            main_media_group[call.message.chat.id] = None
            bot.send_message(call.message.chat.id,
                             "Введите текстовый запрос\n\n *Желательно на английском языке для лучшего результата", reply_markup=special_menu)
            bot.register_next_step_handler(call.message, generate_img)
        elif call.data == "upgrade1":
            main_media_group[call.message.chat.id][3] = 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'👁 {main_media_group[call.message.chat.id][0]}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                  parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.send_message(call.message.chat.id, "🎯 Минуточку, улучшаю первое изображение")
            generate_img(call.message)
        elif call.data == "upgrade2":
            main_media_group[call.message.chat.id][3] = 2
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'👁 {main_media_group[call.message.chat.id][0]}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                  parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.send_message(call.message.chat.id, "🎯 Минуточку, улучшаю второе изображение")
            generate_img(call.message)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        global main_menu
        global special_menu
        if message.text == "🚀 Сгенерировать изображение":
            if check_accept(message):
                bot.send_message(message.from_user.id, "Введите текстовый запрос\n\n *Желательно на английском языке для лучшего результата",
                                 reply_markup=special_menu)
                bot.register_next_step_handler(message, generate_img)
        elif message.text == "👁 О проекте":
            bot.send_message(message.from_user.id, ABOUT_MESSAGE, reply_markup=main_menu, parse_mode='MarkdownV2', disable_web_page_preview=True)
        elif message.text == "👨🏻‍💻 Контакты":
            bot.send_message(message.from_user.id, CONTACTS_MESSAGE, reply_markup=main_menu)
        else:
            bot.send_message(message.from_user.id, "💁‍♂️ Я такой команды не знаю\n Если нужна подсказка, то напишите /help.", reply_markup=main_menu)

    def generate_img(message):
        global main_menu
        global main_media_group
        global special_menu

        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_cancel = types.InlineKeyboardButton(text='🕹 Сгенерировать ещё', callback_data='cancel')
        key_upgrade1 = types.InlineKeyboardButton(text='1️⃣ Улучшить', callback_data='upgrade1')
        key_upgrade2 = types.InlineKeyboardButton(text='2️⃣ Улучшить', callback_data='upgrade2')
        keyboard.row(key_upgrade1, key_upgrade2)
        keyboard.add(key_cancel)

        if check_accept(message):

            media_group=[]

            main = main_media_group.get(message.chat.id)
            if message.text == "👁 О проекте":
                bot.send_message(message.from_user.id, ABOUT_MESSAGE, reply_markup=main_menu, parse_mode='MarkdownV2',
                                 disable_web_page_preview=True)
            elif message.text == "👨🏻‍💻 Контакты":
                bot.send_message(message.from_user.id, CONTACTS_MESSAGE, reply_markup=main_menu)
            elif message.text == "🚀 Сгенерировать изображение":
                bot.send_message(message.from_user.id,
                                 "Введите текстовый запрос\n\n *Желательно на английском языке для лучшего результата",
                                 reply_markup=special_menu)
                bot.register_next_step_handler(message, generate_img)
            else:
                if main is None:
                    db_write_data(message)
                    msg = bot.send_message(message.from_user.id, "⚙️ Минутку, генерирую изображение", reply_markup=special_menu)
                    prompt = message.text
                    response = openai.Image.create(
                        prompt=prompt,
                        n=2,
                        size="1024x1024"
                    )

                    media_group.append(InputMediaPhoto(media=response['data'][0]['url']))
                    media_group.append(InputMediaPhoto(media=response['data'][1]['url']))

                    main_media_group[message.chat.id] = [prompt, response['data'][0]['url'], response['data'][1]['url'], 0]

                    bot.send_media_group(chat_id=message.chat.id, media=media_group)
                    bot.send_message(message.from_user.id,
                                     text=f'👁 {prompt}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                     parse_mode='MarkdownV2', disable_web_page_preview=True, reply_markup=keyboard)

                elif main[3] == 1:

                    r = requests.get(main[1])
                    with open(f'img/{message.chat.id}.png', 'wb') as f:
                        f.write(r.content)
                    main_media_group[message.chat.id] = None
                    response = openai.Image.create_variation(
                        image=open(f'img/{message.chat.id}.png', 'rb'),
                        n=1,
                        size="1024x1024"
                    )
                    os.remove(f'img/{message.chat.id}.png')
                    image_url = response['data'][0]['url']
                    bot.send_photo(chat_id=message.chat.id, photo=image_url,
                                   caption=f'👁 {main[0]}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                   parse_mode='MarkdownV2', reply_markup=main_menu)

                elif main[3] == 2:

                    r = requests.get(main[2])
                    with open(f'img/{message.chat.id}.png', 'wb') as f:
                        f.write(r.content)
                    main_media_group[message.chat.id] = None
                    response = openai.Image.create_variation(
                        image=open(f'img/{message.chat.id}.png', 'rb'),
                        n=1,
                        size="1024x1024"
                    )
                    os.remove(f'img/{message.chat.id}.png')
                    image_url = response['data'][0]['url']
                    bot.send_photo(chat_id=message.chat.id, photo=image_url,
                                   caption=f'👁 {main[0]}\n\n[Третий Глаз](https://t.me/+BPwAeq0kYfxkZjMy)',
                                   parse_mode='MarkdownV2', reply_markup=main_menu)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(Token_Bot)
