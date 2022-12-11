from aiogram import Dispatcher, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import Config
from tgbot.keyboards.reply import menuKeyBoard
from tgbot.misc.states import StatesOfMenu


async def user_start(message: Message, state: FSMContext):
    await state.update_data(is_logged='false')
    await message.answer("Это турбопиздатый бот, через который можно "
                         "офформить подписку на ебейшую одежду!",
                         reply_markup=menuKeyBoard)
    await StatesOfMenu.menu.set()



async def getPhoto(mesage: Message):
    #url = "AgACAgIAAxkBAAIDMWOGDweNlPM90jGUDdq4oobUIYZsAAJJwTEbl3UwSFRaKiNIWTKWAQADAgADeAADKwQ"
    await mesage.answer(mesage.photo[2].file_id)
    #await mesage.answer_photo(url)

    #await mesage.answer_photo(mesage.photo.file_id, caption="caption")



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(getPhoto, content_types=["photo"], state=StatesOfMenu.menu)