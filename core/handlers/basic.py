from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from core.keyboards.reply import start_reply, admin_reply

from dotenv import load_dotenv
import os
load_dotenv()
router = Router()


@router.message(Command('start'))
async def start_bot(message: Message):
    await message.answer(
        text=f'Добро пожаловать, {message.from_user.full_name}!\n'
        f'Это магазин чего то либо'
    )
    await message.answer(f'Главное меню', reply_markup=start_reply())
    if message.chat.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Ты звшел как админ', reply_markup=admin_reply())
