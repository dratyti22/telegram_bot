from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
import os
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from core.database.db import display_entries_admin
from core.database.db_user_id import DataBaseUser
from core.handlers.state import TextMailingListState
from core.keyboards.reply import start_reply, admin_reply, admin_panel_reply, help_reply
from core.handlers.state import TitleState
from core.database.db_balance_user import add_balance
from core.database.db_coupons import get_coupon_details, decrement_coupon_amount

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
async def top_up_your_balance(message: Message, state: FSMContext):
    await message.answer('Введите название купона:')
    await state.set_state(TitleState.TITLE)


@router.message(TitleState.TITLE)
async def title_state(message: Message, state: FSMContext):
    coupon_name = message.text
    price, amount = await get_coupon_details(coupon_name)
    if price is not None:
        if amount >= 1:
            await add_balance(message.from_user.id, price)
            await decrement_coupon_amount(coupon_name)
            await message.answer(f'Купон "{coupon_name}" успешно использован! Вам добавлена сумма {price} рублей.')
            await state.clear()
        else:
            await message.answer(f'Купон "{coupon_name}" больше не доступен.')
            await state.clear()
    else:
        await message.answer(f'Купон с названием "{coupon_name}" не найден.')
        await state.clear()


@router.message(F.text == 'админ панель')
async def admin_settings(message: Message):
    await message.reply(
        text='Админ панель для настроек', reply_markup=admin_panel_reply())


@router.message(F.text == '❓  помощь')
async def get_help(message: Message):
    await message.answer('связь', reply_markup=help_reply())


@router.message(F.text == 'админ')
async def get_help_admins(message: Message):
    await message.answer(text='Что бы спросить у админа напишите ему.\n@user_nameeeeeeeeeeee')


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
