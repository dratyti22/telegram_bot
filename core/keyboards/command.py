from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def command(bot: Bot):
    commands= [
        BotCommand(
            command='start',
            description='запустить бота'
        ),
        BotCommand(
            command='a_or_b',
            description='а или б?'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
