from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_reply():
    kb = ReplyKeyboardBuilder()
    kb.button(text='🛒 корзина')
    kb.button(text='💲 купить')
    kb.button(text='❓  помощь')
    kb.button(text='⚙️ профиль')
    kb.adjust(2, 1, 1)
    return kb.as_markup(resize_keyboard=True)


def admin_reply():
    kb = ReplyKeyboardBuilder()
    kb.button(text='🛒 каталог')
    kb.button(text='💲 купить')
    kb.button(text='❓  помощь')
    kb.button(text='⚙️ профиль')
    kb.button(text='админ панель')
    kb.adjust(2, 1, 1, 1)
    return kb.as_markup(resize_keyboard=True)


def admin_panel_reply():
    kb = ReplyKeyboardBuilder()
    kb.button(text='главное меню')
    kb.button(text='добавить товар')
    kb.button(text='удалить товар')
    kb.button(text='сделать рассылку')
    kb.button(text='Посмотреть все товары')
    kb.adjust(1, 2, 1, 1)
    return kb.as_markup(resize_keyboard=True)


def help_reply():
    kb = ReplyKeyboardBuilder()
    kb.button(text='админ')
    kb.button(text='главное меню')
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)


def profile_users():
    kb = ReplyKeyboardBuilder()
    kb.button(text='главное меню')
    kb.button(text='ввести купон')
    kb.button(text='пополнить баланс')
    kb.adjust(1, 2)
    return kb.as_markup(resize_keyboard=True)
