from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def command_admin(bot: Bot):
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
            command='next',
            description='переход к следующему пакету'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def command_user(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='запустить бота'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
