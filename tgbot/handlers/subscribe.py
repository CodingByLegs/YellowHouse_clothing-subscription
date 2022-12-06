from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import inline_kb_styles, inline_kb_capsule_size, inline_kb_gender, create_inline_kb_sizes, \
    create_inline_kb_date_delivery, create_inline_kb_time_delivery
from tgbot.keyboards.reply import menuKeyBoardAuthorizated
from tgbot.misc.states import Subscribe, StatesOfMenu


async def chooseStyle(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get('is_logged') == 'false':
        await message.answer("Для оформления подписки нужно авторизироваться")
        return
    await Subscribe.chooseStyle.set()
    url = "AgACAgIAAxkBAAIDh2OGIcjOmvCqO-aeofyACRknNMqeAAI3wjEbl3UwSEIbId9V8VC8AQADAgADeAADKwQ"
    await message.answer("Выберите стиль", reply_markup=types.ReplyKeyboardRemove())
    await message.answer_photo(url, reply_markup=inline_kb_styles)
    #await message.answer("Выберете стиль",
    #                    reply_markup=inline_kb_styles)


async def CallBack_inline_kb_styles(callback: CallbackQuery, state: FSMContext):
    await Subscribe.chooseCapsuleSize.set()
    vintage = "AgACAgIAAxkBAAID-mOMkKamemyEZQ9iiFhZiuvEK7BjAAI7wDEbZ_toSPrWfvKiTgE0AQADAgADeAADKwQ"
    streetwear = "AgACAgIAAxkBAAIEDGOMkpbef7B0YwAB7cdZkPN31CnMjQACRsAxG2f7aEigFAvLe_40YgEAAwIAA3gAAysE"
    casual = "AgACAgIAAxkBAAIEDmOMksBLN374uibSjYfYtEIixpYRAAJHwDEbZ_toSDYDxNevbhg_AQADAgADeAADKwQ"
    url: dict = {"vintage": vintage, "streetwear": streetwear, "casual": casual}
    await callback.message.delete()
    await callback.answer()
    await state.update_data(style=callback.data)
    await callback.message.answer("Выберите размер капсулы")
    # запрос доступных размеров капсул для стиля
    await callback.message.answer_photo(url[callback.data], reply_markup=inline_kb_capsule_size)


async def CallBack_inline_kb_capsule_size(callback: CallbackQuery, state: FSMContext):
    await Subscribe.chooseClothesSize.set()
    await callback.answer()
    await callback.message.delete()
    await state.update_data(capsule_size=callback.data)
    await callback.message.answer("Выберите размер",
                                  reply_markup=await create_inline_kb_sizes("x", "y"))


async def CallBack_inline_kb_sizes(callback: CallbackQuery, state: FSMContext):
    if not callback.data.startswith(('m', 'w')):
        await callback.answer("Ниже расположены " + callback.data + " размеры")
        return
    await Subscribe.address.set()
    await callback.answer()
    await state.update_data(clothes_size=callback.data)
    data: dict = await state.get_data()
    await callback.message.answer("Отлично!\n"
                                  f"Вы заказли капсулу стиля {data.get('style')}, "
                                  f"{data.get('capsule_size')} вещей, "
                                  f"размер одежды - {data.get('clothes_size')[1:]}\n")
    # проверка на наличие адреса в системе текущего пользователя
    await callback.message.answer("Сервис работает только по Нижнему Новгороду.\n"
                                  "Введите адрес в формате улица, номер дома, подъезд, этаж, квартира")

async def chooseDateDelivery(message: Message, state: FSMContext):
    # создание заказа в базе
    await Subscribe.deliveryDate.set()
    await message.answer("Выберите дату доставки",
                         reply_markup=await create_inline_kb_date_delivery())

async def CallBack_inline_kb_date_delivery(callback: CallbackQuery, state: FSMContext):
    await Subscribe.deliveryTime.set()
    await callback.answer()
    await callback.message.delete()
    # добаление даты доставки в заказ
    await state.update_data(delivery_date=callback.data)
    await callback.message.answer("Выберите время для доставки",
                                  reply_markup=await create_inline_kb_time_delivery())


async def CallBack_inline_kb_inline_kb_time_delivery(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await StatesOfMenu.menu.set()
    # добаление времени доставки в заказ
    await callback.message.answer(f"Ожидайте курьера {data.get('delivery_date')} в {callback.data}",
                                  reply_markup=menuKeyBoardAuthorizated)



def register_subscribe(dp: Dispatcher):
    dp.register_message_handler(chooseStyle, text="Оформить подписку", state=StatesOfMenu.menu)
    dp.register_callback_query_handler(CallBack_inline_kb_styles, state=Subscribe.chooseStyle)
    dp.register_callback_query_handler(CallBack_inline_kb_capsule_size, state=Subscribe.chooseCapsuleSize)
    dp.register_callback_query_handler(CallBack_inline_kb_sizes, state=Subscribe.chooseClothesSize)
    dp.register_message_handler(chooseDateDelivery, state=Subscribe.address)
    dp.register_callback_query_handler(CallBack_inline_kb_date_delivery, state=Subscribe.deliveryDate)
    dp.register_callback_query_handler(CallBack_inline_kb_inline_kb_time_delivery, state=Subscribe.deliveryTime)

