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
    kb.button(text='добавить товар')
    kb.button(text='удалить товар')
    kb.button(text='сделать рассылку')
    return kb.as_markup(resize_keyboard=True)
