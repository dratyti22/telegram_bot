from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from core.keyboards.reply import start_reply, admin_reply
import os
from dotenv import load_dotenv

from core.database.db import display_entries_admin, display_entries_user


load_dotenv()
router = Router()


@router.message(F.text == 'Посмотреть все товары')
async def view_all_products_admin(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        entries = await display_entries_admin()
        if entries:
            entry_list = '\n'.join([f'id: {entry[0]}, text: {entry[1]}, price: {entry[2]}' for entry in entries])
            await message.answer(entry_list)
        else:
            await message.answer('Нет товаров')
    else:
        await message.answer('Вы не являетесь админом')


@router.message(F.text == 'главное меню')
async def main_menu(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='вы вернулись в главное меню как админ',
                             reply_markup=admin_reply()
                             )
    else:
        await message.answer(text='вы вернулись в главное меню',
                             reply_markup=start_reply()
                             )


@router.message(F.text == 'ввести купон')
async def top_up_your_balance(message: Message):
    await message.answer('купоны пока не доступны.')
