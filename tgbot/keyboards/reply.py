from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startMenuButtonNames = ["", ""]

button1 = KeyboardButton("Оформить подписку")
button2 = KeyboardButton("F.A.Q.")
button3 = KeyboardButton("Авторизация")
button4 = KeyboardButton("Личный кабинет")


menuKeyBoard = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).row(button2, button3)
menuKeyBoardAuthorizated = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2).add(button4)



registerButton = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Регистрация"))
sharePhoneNumber = ReplyKeyboardMarkup(
    resize_keyboard=True).add(KeyboardButton("Отправить номер телефона", request_contact=True))
