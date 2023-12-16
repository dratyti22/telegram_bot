import sqlite3 as sq
from aiogram import Router, F, Bot
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

from core.keyboards.command import command_admin, command_user
from core.keyboards.reply import start_reply, admin_reply, admin_panel_reply, help_reply, profile_users
from core.database.db import create_database_prices_text, add_entry, delete_entry
from core.database.db_user_id import cmd_start_db
from core.handlers.state import TOPUPYOURBALANCESTATE, AddProductsAdminState, DeletedProductsAdminState
from core.database.db_balance_user import create_user_id_and_balance, add_balance, display_balance
from core.keyboards.inline import payment_inline
from core.handlers.pay import payment_for_the_purchase
from core.database.db_coupons import create_coupons, add_coupons, deleted_coupons, display_coupons
from core.handlers.state import AddCouponsState, DeletedCouponsState

load_dotenv()
router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, bot: Bot):
    await create_database_prices_text()
    await create_user_id_and_balance(message.from_user.id)
    await cmd_start_db(message.from_user.id)
    await create_coupons()
    await message.answer(
        text=f'Добро пожаловать, {message.from_user.full_name}!\n'
             f'Это магазин чего то либо'
    )
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Ты зашел как админ', reply_markup=admin_reply())
        await command_admin(bot)
    else:
        await message.answer(f'Главное меню', reply_markup=start_reply())
        await command_user(bot)


@router.message(F.text == 'Создать купон')
async def create_add_coupons(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='Введите название купона:')
        await state.set_state(AddCouponsState.NAME)


@router.message(AddCouponsState.NAME)
async def add_coupons_name(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.update_data(name=message.text)
        await message.answer(text='Введите цену купона в рублях:')
        await state.set_state(AddCouponsState.PRICE)


@router.message(AddCouponsState.PRICE)
async def add_coupons_price(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.update_data(price=message.text)
        await message.answer(text='Теперь напишите кол-во купонов:')
        await state.set_state(AddCouponsState.QUANTITY)


@router.message(AddCouponsState.QUANTITY)
async def add_coupons_quantity(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.update_data(quantity=message.text)
        data = await state.get_data()
        await add_coupons(str(data['name']), int(data['price']), int(data['quantity']))
        await message.answer(text='Купоны созданы')
        await state.clear()


@router.message(F.text == 'Удалить купон')
async def deleted_coupons_number(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text='Введите id купона:')
        await state.set_state(DeletedCouponsState.ID)


@router.message(DeletedCouponsState.ID)
async def deleted_coupons_id(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await state.update_data(id=message.text)
        data = await state.get_data()
        await deleted_coupons(int(data['id']))
        await message.answer(text='Купон удален')
        await state.clear()


@router.message(F.text == 'Посмотреть все купоны')
async def display_coupons_admin(message: Message):
    entries = await display_coupons()
    if entries:
        text = '\n'.join(f'id: {entry[0]} name: {entry[1]} price: {entry[2]} quantity: {entry[3]}' for entry in entries)
        await message.answer(text=text)
    else:
        await message.answer(text='Купонов нет')


@router.message(F.text == '⚙️ профиль')
async def get_profile(message: Message):
    entries = await display_balance(message.from_user.id)
    if entries:
        balance, user_id = entries
        text = f"Ваш баланс: {balance}\nВаш id: {user_id}"
    else:
        text = 'Пользователь не найден'
    await message.answer(text, reply_markup=profile_users())


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


@router.message(F.text == 'пополнить баланс')
async def top_up_your_balance(message: Message, state: FSMContext):
    await message.answer('Введите сумму пополнения баланса в рублях, не менее 60 рублей:')
    await state.set_state(TOPUPYOURBALANCESTATE.NUMBER)


@router.message(TOPUPYOURBALANCESTATE.NUMBER)
async def add_number(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(amount=int(message.text))
        data = await state.get_data()
        await message.answer(f'Пополнение баланса на сумму: {data["amount"]}',
                             reply_markup=payment_inline())
    else:
        await message.reply(text='Введите сумму пополнения в цифрах')


@router.callback_query(F.data == 'payment')
async def payment_verification(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await payment_for_the_purchase(callback_query.message, bot, int(data['amount']))
    await add_balance(callback_query.from_user.id, int(data['amount']))
    await state.clear()


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    msg = f"платеж на сумму: {message.successful_payment.total_amount // 100}{message.successful_payment.currency} \
    Выполнен"
    await message.answer(msg)
