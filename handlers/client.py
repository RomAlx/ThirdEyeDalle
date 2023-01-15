from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import create_bot
from open_ai import thirdeye

from handlers import other
from texts import WELCOME_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE, CONTACTS_MESSAGE, CHECK_MESSAGE, EXCEPTION_MESSAGE, \
    GENERATE_MESSAGE, EMPTY_MESSAGE, MAIN_MESSAGE, AUTH_NO_MESSAGE, THANKS_MESSAGE, UPGRADE_MESSAGE1, UPGRADE_MESSAGE2
from texts import GENERATE_BTN, ABOUT_BTN, CONTACTS_BTN
from keyboards import KEYBOARD_WELCOME, KEYBOARD_CORRECT_AUTH, MAIN_MENU, SPECIAL_MENU


class FSMThirdEye(StatesGroup):
    prompt = State()


#@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    if message.text == '/start':
        try:
            await create_bot.bot.send_message(message.from_user.id, WELCOME_MESSAGE, reply_markup=KEYBOARD_WELCOME,
                                   disable_web_page_preview=True)
        except Exception as e:
            await create_bot.bot.send_message(message.from_user.id, EXCEPTION_MESSAGE)
    if message.text == '/help':
        try:
            await create_bot.bot.send_message(message.from_user.id, HELP_MESSAGE, reply_markup=MAIN_MENU,
                                 disable_web_page_preview=True)
        except Exception as e:
            await create_bot.bot.send_message(message.from_user.id, EXCEPTION_MESSAGE)


#@bot.callback_query_handler(text="yes")
async def yes(call: types.CallbackQuery):
    try:
        await call.message.answer(MAIN_MESSAGE, reply_markup=MAIN_MENU)
        await call.answer()
    except Exception as ex:
        await call.message.answer(EXCEPTION_MESSAGE)
        await call.answer()


#@dp.message_handler(lambda message: 'GENERATE_BTN' in message.text, state=None)
async def generate(message: types.Message):
    try:
        user_status = await create_bot.bot.get_chat_member(-1001534006781, message.from_user.id)
        if user_status.status == 'left':
            await create_bot.bot.send_message(message.from_user.id, CHECK_MESSAGE, reply_markup=KEYBOARD_CORRECT_AUTH)
            await create_bot.bot.send_message(message.from_user.id, AUTH_NO_MESSAGE)
        else:
            await FSMThirdEye.prompt.set()
            await message.reply(GENERATE_MESSAGE)
    except Exception as ex:
        await create_bot.bot.send_message(message.from_user.id, EXCEPTION_MESSAGE)

#@dp.message_handler(lambda message: 'ABOUT_BTN' in message.text)
async def about(message: types.Message):
    await create_bot.bot.send_message(message.from_user.id, ABOUT_MESSAGE, reply_markup=MAIN_MENU, parse_mode='MarkdownV2',
                           disable_web_page_preview=True)


# @dp.message_handler(lambda message: 'CONTACTS_BTN' in message.text)
async def contacts(message: types.Message):
    await create_bot.bot.send_message(message.from_user.id, CONTACTS_MESSAGE, reply_markup=MAIN_MENU)


#@dp.message_handler()
async def rotate(message: types.Message):
    await create_bot.bot.send_message(message.from_user.id, EMPTY_MESSAGE, reply_markup=MAIN_MENU)


# @bot.callback_query_handler(text="member")
async def member(call: types.CallbackQuery):
    try:
        user_status = await create_bot.bot.get_chat_member(-1001534006781, call.message.chat.id)
        if user_status.status == 'left':
            await call.message.answer(CHECK_MESSAGE, reply_markup=KEYBOARD_CORRECT_AUTH)
            await call.message.answer(AUTH_NO_MESSAGE)
        else:
            await call.message.answer(CHECK_MESSAGE)
            await call.message.answer(THANKS_MESSAGE)
            await call.message.answer(MAIN_MESSAGE, reply_markup=MAIN_MENU)
    except Exception as ex:
        await call.message.answer(EXCEPTION_MESSAGE)
    await call.answer()


# @bot.callback_query_handler(text="cancel", state=None)
async def cancel(call: types.CallbackQuery):
    try:
        thirdeye.main_media_group[call.message.chat.id] = None
        await FSMThirdEye.prompt.set()
        await call.message.answer(GENERATE_MESSAGE)
    except Exception as ex:
        await call.message.answer(EXCEPTION_MESSAGE)
    await call.answer()


# @bot.callback_query_handler(text="upgrade1")
async def upgrade1(call: types.CallbackQuery):
    try:
        i = call.from_user.id
        await thirdeye.upgrade_img(call, 1, i)
    except Exception as ex:
        await call.message.answer(EXCEPTION_MESSAGE)


# @bot.callback_query_handler(text="upgrade2")
async def upgrade2(call: types.CallbackQuery):
    try:
        i = call.from_user.id
        await thirdeye.upgrade_img(call, 2, i)
    except Exception as ex:
        await call.message.answer(EXCEPTION_MESSAGE)


#@dp.message_handler( state=FSMThirdEye.prompt)
async def load_prompt(message: types.Message, state: FSMThirdEye):
    async with state.proxy() as data:
        data['prompt'] = message.text
    async with state.proxy() as data:
        await thirdeye.generate_img(message=message, prompt=data['prompt'])
    await state.finish()



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_callback_query_handler(yes, text="yes")
    dp.register_message_handler(generate, lambda message: GENERATE_BTN in message.text, state=None)
    dp.register_message_handler(about, lambda message: ABOUT_BTN in message.text)
    dp.register_message_handler(contacts, lambda message: CONTACTS_BTN in message.text)
    dp.register_callback_query_handler(member, text="member")
    dp.register_callback_query_handler(cancel, text="cancel", state=None)
    dp.register_callback_query_handler(upgrade1, text="upgrade1")
    dp.register_callback_query_handler(upgrade2, text="upgrade2")
    dp.register_message_handler(load_prompt, state=FSMThirdEye.prompt)
    dp.register_message_handler(rotate)
