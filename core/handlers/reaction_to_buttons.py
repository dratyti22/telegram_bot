from aiogram import Router, F
from aiogram.types import Message
from core.keyboards.reply import help_reply

router = Router()


@router.message(F.text == '🛒 каталог')
async def get_basket(message: Message):
    await message.answer('Корзина нету товаров')#inline клавиатура с коваром)


@router.message(F.text == '💲 купить')
async def get_buy(message: Message):
    await message.answer('товар нету')#inline клавиатура с коваром)


@router.message(F.text == '❓  помощь')
async def get_help(message: Message):
    await message.answer('связь', reply_markup=help_reply())


@router.message(F.text == '⚙️ профиль')
async def get_profile(message: Message):
    await message.answer(f'ваш id: {message.from_user.id}')
