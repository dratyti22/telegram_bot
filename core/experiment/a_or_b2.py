from aiogram import Router, types, Bot, F
from aiogram.filters import Command

router = Router()


@router.message(Command('a_or_b2'))
async def aaaaa(message: types.Message, bot: Bot):
    kp = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn1')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn2')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn3')
        ],

        [
            types.InlineKeyboardButton(text='❤', callback_data='btn4')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn5')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn6')
        ],

        [
            types.InlineKeyboardButton(text='❤', callback_data='btn7')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn8')
        ],
        [
            types.InlineKeyboardButton(text='❤', callback_data='btn9')
        ],
    ])

    await bot.send_message(message.from_user.id, 'Генерация поля', reply_markup=kp)


@router.callback_query(F.data.startswith('btn'))
async def back(call: types.CallbackQuery, bot: Bot):
    if call.data == 'btn1':
        kp = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text='Тестовый код', callback_data='Тест')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn2')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn3')
            ],

            [
                types.InlineKeyboardButton(text='❤', callback_data='btn4')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn5')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn6')
            ],

            [
                types.InlineKeyboardButton(text='❤', callback_data='btn7')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn8')
            ],
            [
                types.InlineKeyboardButton(text='❤', callback_data='btn9')
            ],
        ])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kp,
                                    text='я смог это сделать')
