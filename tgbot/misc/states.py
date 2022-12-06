from aiogram.dispatcher.filters.state import StatesGroup, State

class StatesOfMenu(StatesGroup):
    menu = State()
    authorization = State()
    styles = State()
    FAQ = State()
    getSubscribe = State()

class AuthorizationUser(StatesGroup):
    start = State()
    authorization = State()
    authorizationPassword = State()
    registration = State()
    registrationPassword = State()

class Subscribe(StatesGroup):
    chooseStyle = State()
    chooseCapsuleSize = State()
    chooseClothesSize = State()
    address = State()
    address_street = State()
    address_house = State()
    address_flat = State()
    deliveryDate = State()
    deliveryTime = State()

class Styles(StatesGroup):
    chooseStyles = State()
    casual = State()
    streetwear = State()
    vintage = State()