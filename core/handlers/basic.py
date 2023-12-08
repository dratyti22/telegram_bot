import sqlite3 as sq
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

from core.keyboards.command import command
from core.keyboards.reply import start_reply, admin_reply, admin_panel_reply
from core.database.db import create_database_prices_text, add_entry, delete_entry
from core.database.db_user_id import cmd_start_db
from core.handlers.state import TOPUPYOURBALANCESTATE, AddProductsAdminState, DeletedProductsAdminState

load_dotenv()
router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, bot: Bot):
    await cmd_start_db(message.from_user.id),
    await create_database_prices_text()
    await message.answer(
        text=f'Добро пожаловать, {message.from_user.full_name}!\n'
             f'Это магазин чего то либо'
    )
    await message.answer(f'Главное меню', reply_markup=start_reply())
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await command(bot)
        await message.answer('Ты зашел как админ', reply_markup=admin_reply())


@router.message(F.text == 'админ панель')
async def admin_settings(message: Message):
    await message.reply(
        text='Админ панель для настроек', reply_markup=admin_panel_reply())


@router.message(F.text == 'добавить товар')
async def add_products_admin(message: Message, state: FSMContext):
    await message.answer(text='напиши название товара:')
    await state.set_state(AddProductsAdminState.NAME)


@router.message(AddProductsAdminState.NAME)
async def addproductsadminname(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='теперь напиши цену в рублях:')
    await state.set_state(AddProductsAdminState.PRICE)


@router.message(AddProductsAdminState.PRICE)
async def addproductsadminprice(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await message.answer(text=f'товар добавлен, вы ввели название: {data["name"]}, цена: {data["price"]}')
    await add_entry(data['name'], data['price'])
    await state.clear()


@router.message(F.text == 'удалить товар')
async def deleted_product(message: Message, state: FSMContext):
    await message.answer('Введите id товара которого вы хотите удалить:')
    await state.set_state(DeletedProductsAdminState.NUMBER)


@router.message(DeletedProductsAdminState.NUMBER)
async def deleted_products_admin(message: Message, state: FSMContext):
    await state.update_data(number=int(message.text))
    data = await state.get_data()
    conn = sq.connect('text_prices.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM text_prices WHERE id = ?", (data["number"],))
    entry = cursor.fetchone()
    if entry:
        await message.answer(text=f'Вы удалили товар под id: {data["number"]}')
        await delete_entry(data["number"])
        await state.clear()
    else:
        await message.answer('Такого id нет\nВведите новый id:')
        await state.set_state(DeletedProductsAdminState.NUMBER)

# @router.message(F.text == 'пополнить баланс')
# async def top_up_your_balance(message: Message, state: FSMContext):
#     await message.answer('Введите сумму пополнения баланса в рублях')
#     await state.set_state(TOPUPYOURBALANCESTATE.NUMBER)
#
#
# @router.message(TOPUPYOURBALANCESTATE.NUMBER)
# async def add_number(message: Message, state: FSMContext):
#     await state.update_data(amout=int(message.text))
#     await message.answer('Выберите платёжную систему:', reply_markup=
