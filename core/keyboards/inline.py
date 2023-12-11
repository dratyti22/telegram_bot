from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def payment_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='👍 Оплатить', callback_data='payment')
        ]
    ])
    return keyboard


def products_next_inline1():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Далее', callback_data='next1'),
            InlineKeyboardButton(text=f'страница {1}|3', callback_data='next1')
        ]
    ])
    return kb


def products_further_inline1():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='назад', callback_data='further'),
            InlineKeyboardButton(text=f'страница {2}/3', callback_data='further')
        ]
    ])
    return kb


# def products_further_inline1()


def get_products():
    kb = InlineKeyboardBuilder()
    kb.button(text='шорты', callback_data='short')
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
