from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import inline_kb_styles, inline_kb_capsule_size, inline_kb_gender, create_inline_kb_sizes, \
    create_inline_kb_date_delivery, create_inline_kb_time_delivery, inline_kb_yes_no
from tgbot.keyboards.reply import menuKeyBoardAuthorizated
from tgbot.misc.api import api
from tgbot.misc.states import Subscribe, StatesOfMenu
from tgbot.models.order import Order


async def chooseStyle(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('is_logged') == 'false':
        await message.answer("Для оформления подписки нужно авторизироваться")
        return
    await Subscribe.chooseStyle.set()
    url = "AgACAgIAAxkBAAIDh2OGIcjOmvCqO-aeofyACRknNMqeAAI3wjEbl3UwSEIbId9V8VC8AQADAgADeAADKwQ"
    await message.answer("Выберите стиль", reply_markup=types.ReplyKeyboardRemove())
    await message.answer_photo(url, reply_markup=inline_kb_styles)


async def CallBack_inline_kb_styles(callback: CallbackQuery, state: FSMContext):
    await Subscribe.chooseCapsuleSize.set()
    vintage = "AgACAgIAAxkBAAID-mOMkKamemyEZQ9iiFhZiuvEK7BjAAI7wDEbZ_toSPrWfvKiTgE0AQADAgADeAADKwQ"
    streetwear = "AgACAgIAAxkBAAIEDGOMkpbef7B0YwAB7cdZkPN31CnMjQACRsAxG2f7aEigFAvLe_40YgEAAwIAA3gAAysE"
    casual = "AgACAgIAAxkBAAIEDmOMksBLN374uibSjYfYtEIixpYRAAJHwDEbZ_toSDYDxNevbhg_AQADAgADeAADKwQ"
    url: dict = {"vintage": vintage, "streetwear": streetwear, "casual": casual}
    await callback.message.delete()
    await callback.answer()
    await state.update_data(type=callback.data)
    await callback.message.answer("Выберите размер капсулы")
    # запрос доступных размеров капсул для стиля
    await callback.message.answer_photo(url[callback.data], reply_markup=inline_kb_capsule_size)


async def CallBack_inline_kb_capsule_size(callback: CallbackQuery, state: FSMContext):
    await Subscribe.chooseClothesSize.set()
    await callback.answer()
    await callback.message.delete()
    await state.update_data(capsule_size=callback.data)
    state_data = await state.get_data()
    await callback.message.answer("Выберите размер",
                                  reply_markup=await create_inline_kb_sizes(state_data['type'],
                                                                            state_data['capsule_size']))


async def CallBack_inline_kb_sizes(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith(('m', 'w')):
        await callback.answer("Ниже расположены " + callback.data + " размеры")
        return
    await Subscribe.isCorrectAddress.set()
    await callback.answer()
    await state.update_data(clothes_size=callback.data)
    data: dict = await state.get_data()
    await callback.message.answer("Отлично!\n"
                                  f"Вы заказли капсулу стиля {data.get('type')}, "
                                  f"{data.get('capsule_size')} вещей, "
                                  f"размер одежды - {data.get('clothes_size')[1:]}\n")
    # проверка на наличие адреса в системе текущего пользователя
    user = api.getUserByPhoneNumber(data['userLogin'])
    await callback.message.answer(f"Ваш адресс - {user.address}?",
                                  reply_markup=inline_kb_yes_no)


async def CallBack_inline_kb_yes_no_isCorrectAddress(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "no":
        await callback.message.answer("Введите свой адрес")
        await Subscribe.getNewAddress.set()
    elif callback.data == "yes":
        await chooseDateDelivery(callback.message, state)


async def getNewAddress(message: Message, state: FSMContext):
    state_data = await state.get_data()
    user = api.getUserByPhoneNumber(state_data['userLogin'])
    api.addNewAddress(user.id, message.text)  # заносим новый адрес в базу
    await message.answer("Теперь этот адрес будет считаться основным")
    await chooseDateDelivery(message, state)


async def chooseDateDelivery(message: Message, state: FSMContext):
    await Subscribe.deliveryDate.set()
    state_data = await state.get_data()
    capsule = api.getRandomCapsule(state_data['type'], state_data['capsule_size'])
    user = api.getUserByPhoneNumber(state_data['userLogin'])
    order = api.createOrder(user.id, capsule.id)
    await state.update_data(cur_order_id=order.id)
    await message.answer("Выберите дату доставки",
                         reply_markup=await create_inline_kb_date_delivery())

async def CallBack_inline_kb_date_delivery(callback: CallbackQuery, state: FSMContext):
    await Subscribe.deliveryTime.set()
    await callback.answer()
    await callback.message.delete()
    await state.update_data(delivery_date=callback.data)
    await callback.message.answer("Выберите время для доставки",
                                  reply_markup=await create_inline_kb_time_delivery(callback.data))


async def CallBack_inline_kb_inline_kb_time_delivery(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await StatesOfMenu.menu.set()
    deliveryDate = data['delivery_date'] + 'T' + callback.data
    api.addOrderDeiveryDate(data['cur_order_id'], deliveryDate)
    # добаление времени доставки в заказ
    await callback.message.answer(f"Ожидайте курьера {data.get('delivery_date').replace('-', '.')} в {callback.data}",
                                  reply_markup=menuKeyBoardAuthorizated)



def register_subscribe(dp: Dispatcher):
    dp.register_message_handler(chooseStyle, text="Оформить подписку", state=StatesOfMenu.menu)
    dp.register_callback_query_handler(CallBack_inline_kb_styles, state=Subscribe.chooseStyle)
    dp.register_callback_query_handler(CallBack_inline_kb_capsule_size, state=Subscribe.chooseCapsuleSize)
    dp.register_callback_query_handler(CallBack_inline_kb_sizes, state=Subscribe.chooseClothesSize)
    dp.register_callback_query_handler(CallBack_inline_kb_yes_no_isCorrectAddress, state=Subscribe.isCorrectAddress)
    dp.register_message_handler(getNewAddress, state=Subscribe.getNewAddress)
    dp.register_callback_query_handler(CallBack_inline_kb_date_delivery, state=Subscribe.deliveryDate)
    dp.register_callback_query_handler(CallBack_inline_kb_inline_kb_time_delivery, state=Subscribe.deliveryTime)

