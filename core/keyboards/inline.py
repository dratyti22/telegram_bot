from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from core.database.db import display_entries_admin


def payment_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='👍 Оплатить', callback_data='payment')
        ]
    ])
    return keyboard


def message_limit_inline_next(page: int, num_pages: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Далее', callback_data='next'),
            InlineKeyboardButton(text=f'страница {page}/{num_pages}', callback_data='current_page')
        ]
    ])
    return kb


def message_limit_inline_back(page: int, num_pages: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='назад', callback_data='back'),
            InlineKeyboardButton(text=f'страница {page}/{num_pages}', callback_data='current_page'),
            InlineKeyboardButton(text='далее', callback_data='next')
        ]
    ])
    return kb


async def get_products_inline():
    entries = await display_entries_admin()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=entry[1], callback_data=f'product_{entry[0]}'),
        ] for entry in entries
    ])
    return kb


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
