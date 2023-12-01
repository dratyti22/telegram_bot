from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from core.keyboards.reply import help_reply, profile_users, start_reply, admin_reply
from core.keyboards.inline import get_products
import os

router = Router()


@router.message(F.text == '🛒 каталог')
async def get_basket(message: Message):
    await message.answer('Товары:', reply_markup=get_products())  # inline клавиатура с коваром


@router.message(F.text == '💲 купить')
async def get_buy(message: Message):
    await message.answer('товары', reply_markup=get_products())  # inline клавиатура с коваром


@router.message(F.text == '❓  помощь')
async def get_help(message: Message):
    await message.answer('связь', reply_markup=help_reply())


@router.message(F.text == 'назад')
async def next_help(message: Message):
    if message.from_user.id == os.getenv('ADMIN_id'):
        await message.answer('вы вернулись в профиль', reply_markup=admin_reply())

    else:
        await message.answer('вы вернулись в профиль', reply_markup=start_reply())


@router.message(F.text == '⚙️ профиль')
async def get_profile(message: Message):
    await message.answer(
        f'ваш баланс =\n'
        f'ваш id: {message.from_user.id}',
        reply_markup=profile_users()
    )


@router.message(F.text == 'главное меню')
async def main_menu(message: Message):
    if message.from_user.id == os.getenv('ADMIN_ID'):
        await message.answer(text='вы вернулись в главное меню',
                             reply_markup=admin_reply()
                             )
    else:
        await message.answer(text='вы вернулись в главное меню',
                             reply_markup=start_reply()
                             )


@router.message(F.text == 'пополнить баланс')
async def top_up_your_balance(message: Message):
    await message.answer('оплата пока не доступна.\n Будет доступна позже')


@router.message(F.text == 'ввести купон')
async def top_up_your_balance(message: Message):
    await message.answer('купоны пока не доступны.\n Будет доступна когда появится пополнение баланса')


@router.callback_query()
async def get_callback(callback: CallbackQuery):
    if callback.data == 'short':
        await callback.message.answer('это шорты')
    elif callback.data == 'boots':
        await callback.message.answer('это ботинки')
    elif callback.data == 'sneakers':
        await callback.message.answer('это кроссовки')
    elif callback.data == 'cap':
        await callback.message.answer('это майка')
