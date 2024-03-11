from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text
from bot.database.users import get_user_words_count
from bot.words_selection import *  # noqa: F403
import datetime
from bot.model import User


bl = BotLabeler()

@bl.private_message(text=["начать"])
async def start_menu_handler(message: Message, user: User):
    vkuser = await message.get_user()
    kboard = Keyboard().add(Text(" меню", {"route": "menu"}))
    await message.answer(f"Привет  {vkuser.first_name.lower()}\n\n Добро пожаловать в llrn. Бот основанный на системе интервального повторения", keyboard=kboard)


@bl.private_message(payload_contains={"route": "menu"})
@bl.private_message(text=["меню"])
async def menu_handler(message: Message, user: User):
    kboard = (Keyboard()
              .add(Text("🗂 Выбрать языковые пакеты", {"route": "packages_choose"}))
              .add(Text("🔍 Учить", {"route": "start_teach"})))
    await message.answer(f"Сейчас {datetime.datetime.now().strftime('%a %d %b %Y, %H:%M')}\nСлов выучено: {get_user_words_count(user)}",
                          keyboard=kboard,
                        attachment="photo-224471611_457239019")