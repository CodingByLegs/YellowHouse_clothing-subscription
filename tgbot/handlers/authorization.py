import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import registerButton, sharePhoneNumber, menuKeyBoard, menuKeyBoardAuthorizated
from tgbot.misc.states import AuthorizationUser, StatesOfMenu

users: dict = {'test': '123', '!Мираж': 'карта говна'}


async def Start(message: Message):
    await AuthorizationUser.start.set()
    await message.answer("Введите почту или номер телефона, затем пароль\n"
                         "Если вы тут первый раз, то нажмите кнопку регестрации",
                         reply_markup=registerButton)


async def Authorization(message: Message, state: FSMContext):
    if not (message.text in users.keys()):  # проверка на наличие такого логина в системе
        await message.answer("Пользователь с таким логином не найден, "
                             "попробуйте снова или зарегистрируйтесь",
                             reply_markup=registerButton)
        return
    await AuthorizationUser.authorizationPassword.set()
    await state.update_data(userLogin=message.text)
    await message.answer("Введите пароль",
                         reply_markup=types.ReplyKeyboardRemove())

async def AuthorizationPassword(message: Message, state: FSMContext):
    data : dict = await state.get_data()
    if message.text != users[data['userLogin']]:  # проверка на правильность пароля пользователя
        await message.answer("Неверный пароль, попробуйте снова")
        return
    await StatesOfMenu.menu.set()
    await state.update_data(password=message.text)
    await state.update_data(is_logged='true')
    await message.answer("Вы в системе...",
                         reply_markup=menuKeyBoardAuthorizated)  # поменять!



async def Registration(message: Message):
    await AuthorizationUser.registration.set()
    await message.answer("Для регистрации нам нужен номер телефон\n"
                         "Введите номер, начиная с 9",
                         reply_markup=sharePhoneNumber)


async def CreateNewUserLoggin(message: Message, state: FSMContext):

    userLogin: str
    phoneNumberPattern = "^([9]{1}[0-9]{9})?$"
    if message.contact:
        await message.answer(f"Ваш номер:{message.contact.phone_number}")
        userLogin = message.contact.phone_number
    elif re.fullmatch(phoneNumberPattern, message.text):
            await message.answer(f"Ваш номер: {message.text}")
    else:
        await message.answer("Формат вводна неверный, поворобуйте снова")
        return
    userLogin = message.text
    # проверка на наличие такого пользователя в базе
    await AuthorizationUser.registrationPassword.set()
    await message.answer("Придумайте пароль\n"
                         "Он должен содержать не менее 6 символов",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(userLogin=userLogin)


async def CreateNewUserPassword(message: Message, state: FSMContext):
    if len(message.text) < 6:
        await message.answer("Пароль должен содержать не менее 6 символов\n"
                             "Попробуйте снова")
        return
    elif len(message.text) > 30:
        await message.answer("Пароль не может быть таким большим\n"
                             "Попробуйте снова")
        return
    await StatesOfMenu.menu.set()
    dataFromState = await state.get_data()
    phoneNumber = dataFromState['userLogin']
    password = message.text
    # запрос на создание нового пользователя
    await state.update_data(is_logged='true')
    await message.answer(f"Вы успешно зарегистрированы!\n"
                         f"логин: {phoneNumber}, пароль: {password}",
                         reply_markup=menuKeyBoardAuthorizated)


def register_Authorization(dp: Dispatcher):
    dp.register_message_handler(Start, text="Авторизация", state=StatesOfMenu.menu)
    dp.register_message_handler(Registration, text="Регистрация", state=AuthorizationUser.start)
    dp.register_message_handler(CreateNewUserLoggin, content_types=types.ContentTypes.CONTACT,
                                state=AuthorizationUser.registration)
    dp.register_message_handler(CreateNewUserLoggin, state=AuthorizationUser.registration)
    dp.register_message_handler(CreateNewUserPassword, state=AuthorizationUser.registrationPassword)
    dp.register_message_handler(Authorization, state=AuthorizationUser.start)
    dp.register_message_handler(AuthorizationPassword, state=AuthorizationUser.authorizationPassword)