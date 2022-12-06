from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.keyboards.inline import inline_kb_styles
from tgbot.misc.states import Styles, StatesOfMenu

stylesPhotoURL: dict = {'vintage': "AgACAgIAAxkBAAIDMWOGDweNlPM90jGUDdq4oobUIYZsAAJJwTEbl3UwSFRaKiNIWTKWAQADAgADeAADKwQ",
                'casual': "AgACAgIAAxkBAAIDWmOGEXpydLOiYfE1ueENLwkqDt_1AAJgwTEbl3UwSKU1u7ODftbyAQADAgADeAADKwQ",
                'streetwear': "AgACAgIAAxkBAAIDXWOGEaI6iXgXqKPxWzri5mZ3TvhaAAJkwTEbl3UwSB4rkYKm1deLAQADAgADeAADKwQ"}
stylesPhotoName = ['vintage', 'casual', 'streetwear']

async def Start(message: Message):
    await Styles.chooseStyles.set()
    media = types.MediaGroup()
    for name in stylesPhotoName:
        media.attach_photo(stylesPhotoURL[name])
    await message.answer_media_group(media)
    await message.answer("Узнайтие о стиле больше!",
                         reply_markup=inline_kb_styles)


def register_Styles(dp: Dispatcher):
    dp.register_message_handler(Start, text="О стилях", state=StatesOfMenu.menu)
