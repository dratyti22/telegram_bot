from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards.reply import start_reply, admin_reply, admin_panel_reply
from core.database.db import db_start, cmd_start_db

from dotenv import load_dotenv
import os
from core.keyboards.command import command
load_dotenv()
router = Router()


@router.message(Command('start'))
async def start_bot(message: Message, bot: Bot):
    await db_start()
    await cmd_start_db(message.from_user.id)
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
