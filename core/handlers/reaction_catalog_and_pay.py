from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
import os
from dotenv import load_dotenv
import math
from aiogram.fsm.context import FSMContext

from core.database.db import display_entries_user, display_entries_admin, display_price
from core.keyboards.inline import message_limit_inline_next, message_limit_inline_back, get_products_inline, \
    message_limit_inline_past
from core.database.db_balance_user import subtract_balance, display_balance

load_dotenv()
router = Router()


# @router.message(F.text == '🛒 каталог')
# async def get_basket(message: Message, bot: Bot):
#     if message.from_user.id == int(os.getenv('ADMIN_ID')):
#         entries_admin = await display_entries_admin()
#         if entries_admin:
#             entries_admin_list = '\n'.join(
#                 [f'id: {entry[0]}, text: {entry[1]}, price: {entry[2]}' for entry in entries_admin])
#             await bot.send_message(message.from_user.id, text=entries_admin_list,
#                                    reply_markup=message_limit_imline_next())
#         else:
#             await bot.send_message(message.from_user.id, text='Нет товаров')
#     else:
#         entries_user = await display_entries_user()
#         if entries_user:
#             entries_user_list = '\n'.join([f'text: {entry[0]}, price: {entry[1]}' for entry in entries_user])
#             await bot.send_message(message.from_user.id, text=entries_user_list,
#                                    reply_markup=message_limit_imline_next())
#         else:
#             await bot.send_message(message.from_user.id, text='Нет товаров')


@router.message(F.text == '🛒 каталог')
async def get_basket1(message: Message, state: FSMContext):
    entries_user = await display_entries_user()
    entries_admin = await display_entries_admin()
    entries_list_user = 'n'.join([f'text: {entry[0]}, price: {entry[1]}' for entry in entries_user])
    entries_list_admin = 'n'.join([f'id: {entry[0]}, text: {entry[1]}, price: {entry[2]}' for entry in entries_admin])

    user_length = len(entries_list_user)
    admin_length = len(entries_list_admin)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        if admin_length > 4096:
            num_pages = math.ceil(admin_length / 4096)
            message_admin = [entries_list_admin[i:i + 4096] for i in range(0, admin_length, 4096)]

            await state.update_data(
                packages=message_admin,
                current_page=0
            )

            await message.answer(
                text=message_admin[0],
                reply_markup=message_limit_inline_next(1, num_pages)
            )
        else:
            await message.answer(text=entries_list_admin)
    else:
        if user_length > 4096:
            num_pages = math.ceil(user_length / 4096)
            message_user = [entries_list_user[i:i + 4096] for i in range(0, user_length, 4096)]

            await state.update_data(
                packages=message_user,
                current_page=0
            )

            await message.answer(
                text=message_user[0],
                reply_markup=message_limit_inline_next(1, num_pages)
            )
        else:
            await message.answer(text=entries_list_user)


@router.callback_query(F.data == 'next')
async def next_page(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    current_page = state_data.get('current_page', 0) + 1

    packages = state_data.get('packages', [])

    await state.update_data(current_page=current_page)

    await callback_query.message.edit_text(
        text=packages[current_page],
        reply_markup=message_limit_inline_back(current_page + 1, len(packages))
    )
    await callback_query.answer()


@router.callback_query(F.data == 'back')
async def back_page(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    current_page = state_data.get('current_page', 0) - 1
    packages = state_data.get('packages', [])

    await state.update_data(current_page=current_page)

    if current_page == 0:
        await callback_query.message.edit_text(
            text=packages[current_page],
            reply_markup=message_limit_inline_next(1, len(packages))
        )
    elif current_page == max(current_page):
        await callback_query.message.edit_text(
            text=packages[current_page],
            reply_markup=message_limit_inline_past(max(current_page), len(packages))
        )
    else:
        await callback_query.message.edit_text(
            text=packages[current_page],
            reply_markup=message_limit_inline_back(current_page + 1, len(packages))
        )
    await callback_query.answer()


@router.message(F.text == '💲 купить')
async def get_buy(message: Message, bot: Bot):
    await bot.send_message(message.chat.id, text='Товары', reply_markup=await get_products_inline())


@router.callback_query(F.data.startswith('product_'))
async def get_buy_products(callback_query: CallbackQuery, bot: Bot):
    product_id = callback_query.data.split('_')[1]
    product_price = await display_price(int(product_id))
    balance_entry = await display_balance(callback_query.from_user.id)
    balance = balance_entry[0]
    if product_price <= balance:
        await subtract_balance(callback_query.from_user.id, product_price)
        await bot.send_message(callback_query.from_user.id, text='Товар куплен')
    else:
        await bot.send_message(callback_query.from_user.id, text='Недостаточно средств для покупки')
