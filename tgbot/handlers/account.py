from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import accountKeyboard, keyboardBack, menuKeyBoardAuthorizated
from tgbot.misc.api import api
from tgbot.misc.states import StatesOfMenu, PersonalAccount


async def startAccount(message: Message):
    await StatesOfMenu.personalAccount.set()
    await message.answer("Добро пожаловать в личный кабинет!",
                         reply_markup=accountKeyboard)


async def ordersHistory(message: Message, state: FSMContext):
    await PersonalAccount.ordersHistory.set()
    data = await state.get_data()
    userPhoneNumber = data['userLogin']
    user = api.getUserByPhoneNumber(userPhoneNumber)
    orders = api.getOrdresByUserId(user.id)
    orderHistory: str
    if len(orders) == 0:
        await message.answer("Список заказов пуст",
                             reply_markup=keyboardBack)
    else:
        for order in orders:
            capsule = api.getCapsuleById(order.capsuleId)
            dateStartUsing = order.deliveryDateToClient.split("T")
            dateStartUsing = dateStartUsing[0] + ", " + dateStartUsing[1][0:4]
            orderHistory = f"Заказ №{order.id}\n" \
                            f"Стиль: {capsule.type}" \
                            f"Размер капсулы: {capsule.size}" \
                            f"Цена: {order.price}" \
                            f"Дата начала использования: {dateStartUsing}"
            await message.answer(orderHistory,
                                 reply_markup=keyboardBack)


async def subscribeStatus(message: Message, state: FSMContext):
    # все статусы для заказа
    statuses = {'NEW': 'оформлена', 'COLLECT': 'капсула собирается', 'COLLECTED': 'капсула собрана',
                'WITH_COURIER': 'капсула передана курьеру', 'WITH_CLIENT': 'вещи у вас',
                'CANCELED': 'подписка не активна'}
    await PersonalAccount.subscribeStatus.set()
    data = await state.get_data()
    user = api.getUserByPhoneNumber(data['userLogin'])
    subscribe = api.getCurrentUserSubscribe(user.id)
    if subscribe is None:
        await message.answer("Вы еще не пользовались нашей подпиской, попробуйте!",
                             reply_markup=keyboardBack)
    else:
        await message.answer(f"Статус подписки: {statuses[subscribe.status]}",
                         reply_markup=keyboardBack)


async def backFromSubStatusOrodHist(message: Message, state: FSMContext):
    await StatesOfMenu.personalAccount.set()
    await message.answer("Личный кабинет",
                         reply_markup=accountKeyboard)

async def backFromPersonalAccount(message: Message):
    await StatesOfMenu.menu.set()
    await message.answer("Меню",
                         reply_markup=menuKeyBoardAuthorizated)


def register_account(dp: Dispatcher):
    dp.register_message_handler(startAccount, text="Личный кабинет", state=StatesOfMenu.menu)
    dp.register_message_handler(ordersHistory, text="История заказов", state=StatesOfMenu.personalAccount)
    dp.register_message_handler(subscribeStatus, text="Статус подписки", state=StatesOfMenu.personalAccount)
    dp.register_message_handler(backFromSubStatusOrodHist, text="Назад", state=PersonalAccount)
    dp.register_message_handler(backFromPersonalAccount, text="Назад", state=StatesOfMenu.personalAccount)

