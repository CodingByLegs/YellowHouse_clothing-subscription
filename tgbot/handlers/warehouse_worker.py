import asyncio
from typing import List

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config


# async def give_order(order_id):
#     # вытаскиваем информацию о заказе
#     config: Config = bot.get('config')
#     for id in config.tg_bot.warehouse_workers_chat_ids:
#         await bot.send_message(id, "пришел новый заказ!")
from tgbot.keyboards.inline import create_inline_kb_accept, create_inline_order_collected
from tgbot.keyboards.reply import create_reply_order_collected
from tgbot.misc.api import api
from tgbot.misc.states import CollectOrder


async def wh_worker_start(message: Message, state: FSMContext):
    flag = True
    await message.answer(f"Првиет, работник склада,твой chat id - {message.chat.id}")
    config: Config = message.bot.get('config')
    await waitNewOrder(message, state)


async def waitNewOrder(message: Message, state: FSMContext):
    orders = api.getOrders()
    ordersCountCur = len(orders)
    while True:
        orders = api.getOrders()  #отправляем запрос в базу на наличие нового запроса
        if len(orders) > ordersCountCur:
            await CollectOrder.getOrder.set()
            await state.update_data(new_order_id=orders[ordersCountCur].id)  # заведи тут массив
            await message.answer(f"Новый заказ! №{orders[ordersCountCur].id}",
                                 reply_markup=await create_inline_kb_accept(orders[ordersCountCur].id))
            ordersCountCur += 1
        await asyncio.sleep(5)


async def CallBack_inline_kb_accept_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    await CollectOrder.collectOrder.set()
    order = api.getOrderById(callback.data)
    capsule = api.getCapsuleById(order.capsuleId)
    clothesNames = ""
    for clothesId in capsule.clothesInCapsulaIds:
        clothesName = api.getClothesById(clothesId).name
        clothesNames += clothesName + '\n'
    await callback.message.answer(f"Заказ №{order.id}\n"
                                  f"Тип капсулы: {capsule.type}\n"
                                  f"Размер капсулы: {capsule.size}\n"
                                  f"Состав капсулы:\n"
                                  f"{clothesNames}",
                                  reply_markup=await create_reply_order_collected(order.id))

async def CallBack_inline_kb_accept_busy(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Соберите уже принятый заказ!")


async def reply_order_collected(message: Message, state: FSMContext):
    await CollectOrder.getOrder.set()
    await message.answer("Можете приступать собирать следующий заказ\n"
                         "Курьеру выслано уведомление о готовности заказа!",
                         reply_markup=types.ReplyKeyboardRemove())


def register_warehouse_worker(dp: Dispatcher):
    dp.register_message_handler(wh_worker_start, commands=["start"], state="*", is_wh_worker=True)
    dp.register_message_handler(reply_order_collected, state=CollectOrder.collectOrder, is_wh_worker=True)
    dp.register_callback_query_handler(CallBack_inline_kb_accept_first, state=CollectOrder.getOrder, is_wh_worker=True)
    dp.register_callback_query_handler(CallBack_inline_kb_accept_busy,  state=CollectOrder.collectOrder,
                                       is_wh_worker=True)
