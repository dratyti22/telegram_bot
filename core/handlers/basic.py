from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards.reply import start_reply, admin_reply, admin_panel_reply
from core.database.db import db_start, cmd_start_db

from dotenv import load_dotenv
import os
load_dotenv()
router = Router()


@router.message(Command('start'))
async def start_bot(message: Message):
    await db_start()
    await cmd_start_db(message.from_user.id)
    await message.answer(
        text=f'Добро пожаловать, {message.from_user.full_name}!\n'
        f'Это магазин чего то либо'
    )
    await message.answer(f'Главное меню', reply_markup=start_reply())
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Ты зашел как админ', reply_markup=admin_reply())


@router.message(F.text == 'админ панель')
async def admin_settings(message: Message):
    await message.reply(
        text='Админ панель для настроек', reply_markup=admin_panel_reply())



# class MainStates(StatesGroup):
#     MENU = State()
#     ACTION_A = State()
#
#
# @dp.message_handler(commands=['start'])
# def start(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     button_a = types.InlineKeyboardButton('A', callback_data='button_a')
#     button_b = types.InlineKeyboardButton('B', callback_data='button_b')
#     keyboard.add(button_a, button_b)
#
#     # Отправляем сообщение с клавиатурой выбора кнопок A и B
#     msg = await message.reply('Выберите кнопку A или B', reply_markup=keyboard)
#
#     # Устанавливаем состояние, в котором находимся (MENU)
#     await MainStates.MENU.set()
#
#     # Сохраняем message_id сообщения, чтобы в дальнейшем изменить его текст и клавиатуру
#     await state.update_data(msg_id=msg.message_id)
#
#
# @dp.callback_query_handler(state=MainStates.MENU)
# async def process_callback_menu(callback_query: types.CallbackQuery, state: FSMContext):
#     if callback_query.data == 'button_a':
#         await bot.answer_callback_query(callback_query.id, text="Вы выбрали A")
#
#         # Выполняем какие-то действия при выборе кнопки A
#
#         # Устанавливаем состояние, в котором находимся (ACTION_A)
#         await MainStates.ACTION_A.set()
#
#         # Отправляем сообщение с текстом и клавиатурой для выбора кнопки
#         message_id = (await state.get_data()).get('msg_id')
#         keyboard = types.InlineKeyboardMarkup()
#         button_back = types.InlineKeyboardButton('Назад', callback_data='back')
#         keyboard.add(button_back)
#         await bot.edit_message_text('Подтвердите выбор', message_id, reply_markup=keyboard)
#
#     elif callback_query.data == 'button_b':
#         await bot.answer_callback_query(callback_query.id, text="Вы выбрали B")
#
#         # Выполняем какие-то действия при выборе кнопки B
#
#         # Отправляем сообщение с текстом и клавиатурой для выбора кнопки
#         message_id = (await state.get_data()).get('msg_id')
#         keyboard = types.InlineKeyboardMarkup()
#         button_back = types.InlineKeyboardButton('Назад', callback_data='back')
#         keyboard.add(button_back)
#         await bot.edit_message_text('Подтвердите выбор', message_id, reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text='back', state=[MainStates.ACTION_A, MainStates.ACTION_B])
# async def process_callback_back(callback_query: types.CallbackQuery, state: FSMContext):
#     await bot.answer_callback_query(callback_query.id)
#
#     # Отправляем сообщение с текстом и клавиатурой для выбора кнопок A и B
#     message_id = (await state.get_data()).get('msg_id')
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     button_a = types.InlineKeyboardButton('A', callback_data='button_a')
#     button_b = types.InlineKeyboardButton('B', callback_data='button_b')
#     keyboard.add(button_a, button_b)
#     await bot.edit_message_text('Выберите кнопку A или B', message_id, reply_markup=keyboard)
#
#     # Возврат к начальному состоянию (MENU)
#     await MainStates.MENU.set()
