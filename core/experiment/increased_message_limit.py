import math
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


def message_limit_imline_next():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Далее', callback_data='next'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
            InlineKeyboardButton(text=f'страница: 1|3', callback_data='current_package')
            # текущая страница должна увеличиваться
        ]
    ])
    return keyboard


def message_limit_inline_back():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='назад', callback_data='back'),
            InlineKeyboardButton(text='Далее', callback_data='next'),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
            InlineKeyboardButton(text=f'страница: 2|3', callback_data='current_package')
        ]
    ])
    return kb


class MessageState(StatesGroup):
    MESSAGE = State()


@router.message(Command('message_limit'))
async def message_limit(message: Message):
    await message.answer('Привет! Пожалуйста, отправь мне длинное сообщение.')


# Обработчик текстовых сообщений
@router.message(F.text)
async def process_text(message: Message, state: FSMContext):
    # Получаем длину сообщения
    message_length = len(message.text)

    # Проверяем, превышает ли длина сообщения лимит
    if message_length > 10:
        # Вычисляем количество пакетов сообщений, которые нужно отправить
        num_packages = math.ceil(message_length / 10)

        # Разбиваем сообщение на пакеты по 10 символов
        message_packages = [message.text[i:i + 10] for i in range(0, message_length, 10)]

        # Сохраняем пакеты сообщений в состоянии пользователя
        await state.update_data(
            packages=message_packages,
            current_package=0
        )

        # Отправляем первый пакет сообщения с кнопками
        await message.answer(
            text=message_packages[0],
            reply_markup=message_limit_imline_next()
        )
    else:
        # Если длина сообщения не превышает лимит, отправляем его как обычное сообщение
        await message.answer(text=message.text)


# Обработчик кнопок InlineKeyboard
@router.callback_query(F.data == 'next')
async def next_package(callback_query: CallbackQuery, state: FSMContext):
    # Получаем данные состояния пользователя
    state_data = await state.get_data()

    # Увеличиваем индекс текущего пакета
    current_package = state_data.get('current_package', 0) + 1

    # Получаем список пакетов сообщений
    packages = state_data.get('packages', [])

    # Проверяем, достигнут ли конец списка пакетов
    if current_package >= len(packages):
        # Если достигнут конец, завершаем обработку
        await callback_query.answer(text='Это последний пакет сообщений.')
        return

    # Обновляем данные состояния пользователя с новым индексом текущего пакета
    await state.update_data(current_package=current_package)

    # Отправляем следующий пакет сообщения с кнопками
    await callback_query.message.edit_text(
        text=packages[current_package],
        reply_markup=message_limit_imline_next()
    )

    # Ответим на callback_query
    await callback_query.answer()


# Обработчик кнопки "Отмена"
@router.callback_query(F.data == 'cancel')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    # Очищаем состояние пользователя
    await state.clear()
    await callback_query.answer(text='Отменено.')
