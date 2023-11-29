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


def a_or_b_inline():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='A', callback_data='button_a')
    keyboard.button(text='B', callback_data='button_b')
    keyboard.adjust(2)
    return keyboard.as_markup()


def a_or_b_inline_next():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Назад', callback_data='back')
    return keyboard.as_markup()
