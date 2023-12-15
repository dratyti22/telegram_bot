import math
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.database.db import display_entries_user, display_entries_admin

router = Router()


def message_limit_imline_next(page: int, num_pages: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='далее', callback_data='next')
        ],
        [
            InlineKeyboardButton(text=f'страница: {page}/{num_pages}', callback_data='current_page')
        ],

    ])
    return kb


def message_limit_inline_back(page: int, num_pages: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='назад', callback_data='back'),
        ],
        [
            InlineKeyboardButton(text=f'страница: {page}/{num_pages}', callback_data='current_page')
        ],
        [
            InlineKeyboardButton(text='далее', callback_data='next')
        ]
    ])
    return kb


@router.message(Command('next'))
async def process_text(message: Message, state: FSMContext):
    entries_user = await display_entries_user()
    entries_list_user = '\n'.join([f'text: {entry[0]}, price: {entry[1]}' for entry in entries_user])

    user_length = len(entries_list_user)

    if user_length > 30:
        num_pages = math.ceil(user_length / 30)
        message_user = [entries_list_user[i:i + 30] for i in range(0, user_length, 30)]

        await state.update_data(
            packages=message_user,
            current_page=0
        )

        await message.answer(
            text=message_user[0],
            reply_markup=message_limit_imline_next(1, num_pages)
        )
    else:
        await message.answer(text=entries_list_user)


@router.callback_query(F.data == 'next')
async def next_package(callback_query: CallbackQuery, state: FSMContext):
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
async def back_package(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    current_page = state_data.get('current_page', 0) - 1

    packages = state_data.get('packages', [])

    await state.update_data(current_page=current_page)
    if current_page == 1:
        await callback_query.message.edit_text(
            text=packages[current_page],
            reply_markup=message_limit_imline_next(1, len(packages))
        )
    else:
        await callback_query.message.edit_text(
            text=packages[current_page],
            reply_markup=message_limit_inline_back(current_page - 1, len(packages))
        )
    await callback_query.answer()
