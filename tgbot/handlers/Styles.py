from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.keyboards.inline import inline_kb_styles
from tgbot.misc.states import StatesOfMenu

stylesPhotoURL: dict = {'vintage': "AgACAgIAAxkBAAIDMWOGDweNlPM90jGUDdq4oobUIYZsAAJJwTEbl3UwSFRaKiNIWTKWAQADAgADeAADKwQ",
                'casual': "AgACAgIAAxkBAAIDWmOGEXpydLOiYfE1ueENLwkqDt_1AAJgwTEbl3UwSKU1u7ODftbyAQADAgADeAADKwQ",
                'streetwear': "AgACAgIAAxkBAAIDXWOGEaI6iXgXqKPxWzri5mZ3TvhaAAJkwTEbl3UwSB4rkYKm1deLAQADAgADeAADKwQ"}
stylesPhotoName = ['vintage', 'casual', 'streetwear']




def register_Styles(dp: Dispatcher):
    pass
