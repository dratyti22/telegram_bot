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


class AddCouponsState(StatesGroup):
    NAME = State()
    PRICE = State()
    QUANTITY = State()


class DeletedCouponsState(StatesGroup):
    ID = State()


class TitleState(StatesGroup):
    TITLE = State()
