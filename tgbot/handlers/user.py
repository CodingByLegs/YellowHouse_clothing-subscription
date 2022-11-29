from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.reply import menuKeyBoard
from tgbot.misc.states import StatesOfMenu


async def user_start(message: Message):
    await message.answer("Это турбопиздатый бот, через который можно "
                         "офформить подписку на ебейшую одежду!",
                         reply_markup=menuKeyBoard)
    await StatesOfMenu.menu.set()



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
