from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text
from bot.database.users import get_user_words_count
from bot.words_selection import *  # noqa: F403
from bot.routes.settings import send_settings
import datetime
from bot.model import User


bl = BotLabeler()

@bl.private_message(text=["Начать"])
async def start_menu_handler(message: Message, user: User):
    kboard = Keyboard().add(Text("Меню", {"route": "menu"}))
    if user.day_goal == 0:
        await message.answer(f"Привет {user.name}! Добро пожаловать.\nДля начала давай выберем интенсивность твоего обучения")
        await send_settings(user)
        return

    await message.answer(f"Привет  {user.name.capitalize()}! Рады видеть тебя снова", keyboard=kboard)


@bl.private_message(payload_contains={"route": "menu"})
@bl.private_message(text=["меню"])
async def menu_handler(message: Message, user: User):
    kboard = (Keyboard()
              .add(Text("🗂 Выбрать языковые пакеты", {"route": "packages_choose"}))
              .add(Text("🔍 Учить", {"route": "start_teach"}))
              .row()
              .add(Text("Настройки", {"route": "settings"})))
    await message.answer(f"Сейчас {datetime.datetime.now().strftime('%a %d %b %Y, %H:%M')}\nСлов выучено: {get_user_words_count(user)}",
                        attachment="photo-224471611_457239020", keyboard=kboard)
