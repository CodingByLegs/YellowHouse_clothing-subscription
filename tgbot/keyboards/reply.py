from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

startMenuButtonNames = ["", ""]

button1 = KeyboardButton("Оформить подписку")
button2 = KeyboardButton("F.A.Q.")
button3 = KeyboardButton("Авторизация")
button4 = KeyboardButton("Личный кабинет")

menuKeyBoard = ReplyKeyboardMarkup(resize_keyboard=True).add(button3).row(button2, button1)
menuKeyBoardAuthorizated = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2, button4)


FAQkeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
FAQ = ["Как происходит доставка?", "Как купить вещь из капсулы, которая мне понравилась?",
       "Что будет если я испорчу вещь?", "Что делать если я не смогу отдать/получить вещи в установленный срок?",
       "Назад"]
for text in FAQ:
    FAQkeyboard.add(KeyboardButton(text))

async def create_reply_order_collected(orderId):
    button = KeyboardButton(f"Заказ №{orderId} собран")
    keyBoard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    return keyBoard

registerButton = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Регистрация"))
sharePhoneNumber = ReplyKeyboardMarkup(
    resize_keyboard=True).add(KeyboardButton("Отправить номер телефона", request_contact=True))
