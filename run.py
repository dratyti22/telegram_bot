from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
import logging
import os
import asyncio
from core.handlers import basic, reaction_to_buttons, reaction_catalog_and_pay
from core.experiment import a_or_b, a_or_b2, increased_message_limit2


async def starting_bot(bot: Bot):
    await bot.send_message(1356288006, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(1356288006, 'Бот остановлен')


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    dp = Dispatcher()

    dp.startup.register(starting_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(basic.router, reaction_to_buttons.router, reaction_catalog_and_pay.router)
    dp.include_routers(a_or_b.router, a_or_b2.router, increased_message_limit2.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
