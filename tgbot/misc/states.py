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
    registrationFirstName = State()
    registrationLastName = State()
    registrationAddress = State()

class Subscribe(StatesGroup):
    chooseStyle = State()
    chooseCapsuleSize = State()
    chooseClothesSize = State()
    isCorrectAddress = State()
    getNewAddress = State()
    deliveryDate = State()
    deliveryTime = State()

class CollectOrder(StatesGroup):
    getOrder = State()
    collectOrder = State()