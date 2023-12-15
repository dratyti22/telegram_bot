from aiogram.fsm.state import State, StatesGroup


class ProductsState(StatesGroup):
    MENU = State()
    FURTHER = State()
    NEXT = State()


class TOPUPYOURBALANCESTATE(StatesGroup):
    NUMBER = State()
    PAYMENTSYSTEM = State()


class AddProductsAdminState(StatesGroup):
    PRICE = State()
    NAME = State()


class DeletedProductsAdminState(StatesGroup):
    NUMBER = State()


class TextMailingListState(StatesGroup):
    TEXT = State()
