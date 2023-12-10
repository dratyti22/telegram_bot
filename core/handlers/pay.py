from aiogram import Bot
from aiogram.types import Message, LabeledPrice
import os
from dotenv import load_dotenv
load_dotenv()


async def payment_for_the_purchase(message: Message, bot: Bot, price: int):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Пополнение баланса',
        description='Пополнение баланса в магазине',
        provider_token=os.getenv("PROVIDER_TOKEN"),
        currency='rub',
        payload='test',
        prices=[
            LabeledPrice(
                label='Прайс',
                amount=price * 100
            )
        ]
    )
