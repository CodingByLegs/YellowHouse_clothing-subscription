from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startMenuButtonNames = ["Каталог", "Авторизация"]

button1 = KeyboardButton("Авторизация")
button2 = KeyboardButton("Каталог")
button3 = KeyboardButton("Личный кабинет")

menuKeyBoard = ReplyKeyboardMarkup(resize_keyboard=True)
for name in startMenuButtonNames:
    menuKeyBoard.add(KeyboardButton(name))
menuKeyBoardAuthorizated = ReplyKeyboardMarkup(resize_keyboard=True).add(button2).add(button3)

registerButton = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Регистрация"))
sharePhoneNumber = ReplyKeyboardMarkup(
    resize_keyboard=True).add(KeyboardButton("Отправить номер телефона", request_contact=True))
