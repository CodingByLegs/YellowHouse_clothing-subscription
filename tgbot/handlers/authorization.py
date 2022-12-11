import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.api import api
from tgbot.keyboards.reply import registerButton, sharePhoneNumber, menuKeyBoardAuthorizated
from tgbot.misc.states import AuthorizationUser, StatesOfMenu

users: dict = {'test': '123', '!Мираж': 'карта говна'}


async def Start(message: Message):
    await AuthorizationUser.start.set()
    await message.answer("Введите почту или номер телефона, затем пароль\n"
                         "Если вы тут первый раз, то нажмите кнопку регестрации",
                         reply_markup=registerButton)


async def Authorization(message: Message, state: FSMContext):
    isRegistered = api.userIsRegistered(message.text, message.text)
    if isRegistered:
        await AuthorizationUser.authorizationPassword.set()
        await state.update_data(userLogin=message.text)
        await message.answer("Введите пароль",
                                 reply_markup=types.ReplyKeyboardRemove())
        return
    await message.answer("Пользователь с таким логином не найден, "
                        "попробуйте снова или зарегистрируйтесь",
                        reply_markup=registerButton)


async def AuthorizationPassword(message: Message, state: FSMContext):
    data : dict = await state.get_data()
    user = api.getUserByPhoneNumber(data['userLogin'])
    if message.text != user.password:  # проверка на правильность пароля пользователя
        await message.answer("Неверный пароль, попробуйте снова")
        return
    await StatesOfMenu.menu.set()
    await state.update_data(is_logged='true')
    await message.answer("Вы авторизированы",
                         reply_markup=menuKeyBoardAuthorizated)



async def Registration(message: Message):
    await AuthorizationUser.registration.set()
    await message.answer("Для регистрации нам нужен номер телефон\n"
                         "Введите номер, начиная с 9",
                         reply_markup=sharePhoneNumber)


async def CreateNewUserLoggin(message: Message, state: FSMContext):
    userLogin: str
    phoneNumberPattern = "^([9]{1}[0-9]{9})?$"
    if message.contact:
        userLogin = message.contact.phone_number
    elif re.fullmatch(phoneNumberPattern, message.text):
        userLogin = message.text
    else:
        await message.answer("Формат вводна неверный, поворобуйте снова")
        return
    isRegistered = api.userIsRegistered(message.text, message.text)
    if isRegistered:  # проверка на наличие такого пользователя в базе
        await message.answer("Пользавтель с таким номером телфона/почтой уже есть")
        return
    await state.update_data(userLogin=userLogin)
    await AuthorizationUser.registrationFirstName.set()
    await message.answer("Давайте познакомимся, как вас зовут?")



async def CreateNewUserFirstName(message: Message, state: FSMContext):
    if message.text == '':
        await message.answer("Имя не может быть пустым!")
        return
    await AuthorizationUser.registrationLastName.set()
    await state.update_data(firstName=message.text)
    await message.answer("Ваша фамилия?")


async def CreateNewUserLastName(message: Message, state: FSMContext):
    if message.text == '':
        await message.answer("Фамилия не может быть пустой!")
        return
    await AuthorizationUser.registrationAddress.set()
    await state.update_data(lastName=message.text)
    await message.answer("Сервис работает только по Нижнему Новгороду.\n"
                        "Введите адрес в формате улица, номер дома, подъезд, этаж, квартира")


async def CreateNewAddress(message: Message, state: FSMContext):
    if message.text == '':
        await message.answer("Адрес не может быть пустой!")
        return
    await AuthorizationUser.registrationPassword.set()
    await state.update_data(address=message.text)
    await message.answer("Придумайте пароль\n"
                         "Он должен содержать не менее 6 символов",
                         reply_markup=types.ReplyKeyboardRemove())


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
    dataFromState = await state.get_data() # запрос на создание нового пользователя
    api.createNewUser(fName=dataFromState['firstName'],
                      lName=dataFromState['lastName'],
                      phNum=dataFromState['userLogin'],
                      address=dataFromState['address'],
                      password=message.text)
    await state.update_data(is_logged='true')
    await message.answer(f"Вы успешно зарегистрированы!",
                         reply_markup=menuKeyBoardAuthorizated)


def register_Authorization(dp: Dispatcher):
    dp.register_message_handler(Start, text="Авторизация", state=StatesOfMenu.menu)
    dp.register_message_handler(Registration, text="Регистрация", state=AuthorizationUser.start)
    dp.register_message_handler(CreateNewUserLoggin, content_types=types.ContentTypes.CONTACT,
                                state=AuthorizationUser.registration)
    dp.register_message_handler(CreateNewUserLoggin, state=AuthorizationUser.registration)
    dp.register_message_handler(CreateNewUserFirstName, state=AuthorizationUser.registrationFirstName)
    dp.register_message_handler(CreateNewUserLastName, state=AuthorizationUser.registrationLastName)
    dp.register_message_handler(CreateNewAddress, state=AuthorizationUser.registrationAddress)
    dp.register_message_handler(CreateNewUserPassword, state=AuthorizationUser.registrationPassword)
    dp.register_message_handler(Authorization, state=AuthorizationUser.start)
    dp.register_message_handler(AuthorizationPassword, state=AuthorizationUser.authorizationPassword)