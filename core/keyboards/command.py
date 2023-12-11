from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def command(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='запустить бота'
        ),
        BotCommand(
            command='a_or_b',
            description='а или б?'
        ),
        BotCommand(
            command='a_or_b2',
            description='а или б2?'
        ),
        BotCommand(
            command='message_limit',
            description='проверка максимальной длины сообщения'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
