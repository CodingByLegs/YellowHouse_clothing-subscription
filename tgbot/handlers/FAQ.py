from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import FAQkeyboard, menuKeyBoardAuthorizated, menuKeyBoard
from tgbot.misc.states import StatesOfMenu


async def FAQ(message: Message, state: FSMContext):
    await message.answer("Рубрика вопрос-ответ, нажимай на интересующие тебя вопросы!",
                         reply_markup=FAQkeyboard)
    await StatesOfMenu.FAQ.set()

async def back(message: Message, state: FSMContext):
    await StatesOfMenu.menu.set()
    data = await state.get_data()
    if data['is_logged'] == 'true':
        await message.answer("Меню",
                         reply_markup=menuKeyBoardAuthorizated)
    else:
        await message.answer("Меню",
                             reply_markup=menuKeyBoard)

async def faq1(messsage: Message):
    await messsage.answer("В назначенную время к вам приезжает наш курьер с вещами, у вас будет 15 минут "
                          "проверить вещи на наличие дефектов. В последующие разы к вам так же приезжает "
                          "курьер с новой капсулой, а вы отдаете капсулу предыдущего месяца на проверку "
                          "дефектов, это займет не больше 15 минут.")


async def faq2(messsage: Message):
    await messsage.answer("В случае если вы хотите выкупить вещь из капсулы, которая "
                          "сейчас у вас. За 5 дней до окончание срока использование вы заходите "
                          "на сайт в раздел \"моя капсула\" и выбираете ее из списка вещей "
                          "и нажимаете  кнопку \"выкупить\"")


async def faq3(messsage: Message):
    await messsage.answer("В случае порчи вещей и обнаружение дефекта при проверке курьером. "
                          "Мы оставляем вещь у вас и вы принудительно выкупаете вещь из капсулы.")


async def faq4(messsage: Message):
    await messsage.answer("Если вы не можете принять курьера в отведенный срок, за 2 дня "
                          "до встречи вы должны поменять дату и время встречи с курьером")


def register_FAQ(dp: Dispatcher):
    dp.register_message_handler(FAQ, text="F.A.Q.", state=StatesOfMenu.menu)
    dp.register_message_handler(back, text="Назад", state=StatesOfMenu.FAQ)
    dp.register_message_handler(faq1, text="Как происходит доставка?", state=StatesOfMenu.FAQ)
    dp.register_message_handler(faq2, text="Как купить вещь из капсулы, которая мне понравилась?", state=StatesOfMenu.FAQ)
    dp.register_message_handler(faq3, text="Что будет если я испорчу вещь?", state=StatesOfMenu.FAQ)
    dp.register_message_handler(faq4, text="Что делать если я не смогу отдать/получить вещи в установленный срок?",
                                state=StatesOfMenu.FAQ)