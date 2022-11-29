from aiogram.dispatcher.filters.state import StatesGroup, State

class StatesOfMenu(StatesGroup):
    menu = State()
    authorization = State()
    catalog = State()

class AuthorizationUser(StatesGroup):
    start = State()
    authorization = State()
    authorizationPassword = State()
    registration = State()
    registrationPassword = State()

class Catalog(StatesGroup):
    styles = State()
    casual = State()
    streetwear = State()
    vintage = State()