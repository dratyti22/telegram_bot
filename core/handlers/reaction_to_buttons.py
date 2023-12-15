from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from core.keyboards.reply import start_reply, admin_reply
import os
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from core.database.db import display_entries_admin, display_entries_user
from core.database.db_user_id import DataBaseUser
from core.handlers.state import TextMailingListState

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


@router.message(F.text == 'сделать рассылку')
async def make_a_newsletter(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='Введите сообщение которое надо разослать:')
        await state.set_state(TextMailingListState.TEXT)
    else:
        await message.answer('Вы не являетесь админом')


@router.message(TextMailingListState.TEXT)
async def make_a_newsletter_text(message: Message, state: FSMContext, bot: Bot):
    db = DataBaseUser('tg.db')
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.update_data(text=message.text)
        data = await state.get_data()
        users = db.get_users()
        for i in users:
            try:
                await bot.send_message(i[0], data['text'])
                if int(i[1]) != 1:
                    db.set_activate(i[0], 1)
            except:
                db.set_activate(i[0], 0)
        await bot.send_message(message.from_user.id, 'Рассылка завершена')
        await state.clear()
    else:
        await message.answer('Вы не являетесь админом')
