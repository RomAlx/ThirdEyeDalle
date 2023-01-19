from aiogram import types

from texts import WELCOME_BTN, CORRECT_AUTH_BTN, GENERATE_BTN, ABOUT_BTN, CONTACTS_BTN, CANCEL_BTN, UP1_BTN, UP2_BTN

KEYBOARD_CORRECT_AUTH = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_auth_correct = types.InlineKeyboardButton(text=CORRECT_AUTH_BTN, callback_data='member')
KEYBOARD_CORRECT_AUTH.add(btn_auth_correct)

KEYBOARD_WELCOME = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)  # наша клавиатура
btn_yes = types.InlineKeyboardButton(text=WELCOME_BTN, callback_data='yes')
KEYBOARD_WELCOME.add(btn_yes)

KEYBOARD_WORK = types.InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_cancel = types.InlineKeyboardButton(text=CANCEL_BTN, callback_data='cancel')
btn_up1 = types.InlineKeyboardButton(text=UP1_BTN, callback_data='upgrade1')
btn_up2 = types.InlineKeyboardButton(text=UP2_BTN, callback_data='upgrade2')
KEYBOARD_WORK.row(btn_up1, btn_up2)
KEYBOARD_WORK.add(btn_cancel)


btn_gen = types.KeyboardButton(GENERATE_BTN)
btn_about = types.KeyboardButton(ABOUT_BTN)
btn_contacts = types.KeyboardButton(CONTACTS_BTN)
btn_cancel = types.KeyboardButton(CANCEL_BTN)
btn_up1 = types.KeyboardButton(UP1_BTN)
btn_up2 = types.KeyboardButton(UP2_BTN)


MAIN_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
MAIN_MENU.add(btn_gen)
MAIN_MENU.row(btn_about, btn_contacts)

SPECIAL_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
SPECIAL_MENU.row(btn_up1, btn_up2)
SPECIAL_MENU.add(btn_cancel)
SPECIAL_MENU.row(btn_about, btn_contacts)

