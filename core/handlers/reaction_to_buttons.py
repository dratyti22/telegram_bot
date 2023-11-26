from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from core.keyboards.reply import help_reply
from core.keyboards.inline import get_products

router = Router()


@router.message(F.text == '🛒 каталог')
async def get_basket(message: Message):
    await message.answer('Товары:', reply_markup=get_products())  # inline клавиатура с коваром)


@router.message(F.text == '💲 купить')
async def get_buy(message: Message):
    await message.answer('товар нету')  # inline клавиатура с коваром)


@router.message(F.text == '❓  помощь')
async def get_help(message: Message):
    await message.answer('связь', reply_markup=help_reply())


@router.message(F.text == '⚙️ профиль')
async def get_profile(message: Message):
    await message.answer(f'ваш id: {message.from_user.id}')


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
