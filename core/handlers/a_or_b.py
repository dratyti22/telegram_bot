from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from aiogram.filters import Command
from core.keyboards.inline import a_or_b_inline, a_or_b_inline_next
from aiogram.types import Message, CallbackQuery
router = Router()


class MainStates(StatesGroup):
    MENU = State()
    ACTION_A = State()
    ACTION_B = State()


@router.message(Command('a_or_b'))
async def a_or_b(message: Message, state: FSMContext):

    # Отправляем сообщение с клавиатурой выбора кнопок A и B
    msg = await message.reply(text='Выберите кнопку A или B', reply_markup=a_or_b_inline())

    # Устанавливаем состояние, в котором находимся (MENU)
    await state.set_state(MainStates.MENU)

    # Сохраняем message_id сообщения, чтобы в дальнейшем изменить его текст и клавиатуру
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(MainStates.MENU)
async def process_callback_menu(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if callback_query.data == 'button_a':
        await bot.answer_callback_query(callback_query.id, text="Вы выбрали A")
        # Выполняем какие-то действия при выборе кнопки A

        # Устанавливаем состояние, в котором находимся (ACTION_A)
        await state.set_state(MainStates.ACTION_A)

        # Отправляем сообщение с текстом и клавиатурой для выбора кнопки
        message_id = (await state.get_data()).get('msg_id')
        await bot.edit_message_text('Подтвердите выбор', message_id, reply_markup=a_or_b_inline_next())

    elif callback_query.data == 'button_b':
        await bot.answer_callback_query(callback_query.id, text="Вы выбрали B")

        # Выполняем какие-то действия при выборе кнопки B

        # Отправляем сообщение с текстом и клавиатурой для выбора кнопки
        message_id = (await state.get_data()).get('msg_id')
        await bot.edit_message_text('Подтвердите выбор', message_id, reply_markup=a_or_b_inline_next())


@router.callback_query(F.text == 'back', MainStates.ACTION_A, MainStates.ACTION_B)
async def process_callback_back(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.answer_callback_query(callback_query.id)

    # Отправляем сообщение с текстом и клавиатурой для выбора кнопок A и B
    message_id = (await state.get_data()).get('msg_id')
    await bot.edit_message_text('Выберите кнопку A или B', message_id, reply_markup=a_or_b_inline())

    # Возврат к начальному состоянию (MENU)
    await state.set_state(MainStates.MENU)