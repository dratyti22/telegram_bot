from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_products():
    kb = InlineKeyboardBuilder()
    kb.button(text='шорта', callback_data='short')
    kb.button(text='ботинки', callback_data='boots')
    kb.button(text='кроссовки', callback_data='sneakers')
    kb.button(text='майка', callback_data='cap')
    kb.adjust(2)
    return kb.as_markup()

