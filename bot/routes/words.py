from vkbottle.bot import BotLabeler, Message, MessageEvent
from vkbottle import Keyboard, KeyboardButtonColor, Text,  Callback, GroupEventType
from bot.database.package import get_all_packages, get_package_by_id, package_user_active, get_user_packages
from bot.database.users import get_user_by_vkid, delete_package_from_user, add_package_to_user, get_user_words_count
from bot.words_selection import *
import humanize
from bot.states import States
import datetime
from difflib import SequenceMatcher
from bot.model import User, UserWord
from bot.common import session, bot
from bot.middlewares import UserReqMiddleware


bl = BotLabeler()
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserReqMiddleware)

@bl.private_message(text=["начать"])
async def start_menu_handler(message: Message, user: User):
    vkuser = await message.get_user()
    kboard = Keyboard().add(Text("в меню", {"route": "menu"}))
    await message.answer(f"привет  {vkuser.first_name.lower()}\n\n добро пожаловать в llrn. бот основанный на системе интервального повторения", keyboard=kboard)


@bl.private_message(payload_contains={"route": "packages_choose"})
async def packages_choose(message: Message, user: User):
    for package in get_all_packages():
        if package_user_active(user_id=user.id, package_id=package.id):
            color = KeyboardButtonColor.POSITIVE
            msg = "активен"
        else:
            color = KeyboardButtonColor.NEGATIVE
            msg = "не активен"


        await message.answer(f"название: {package.name}", keyboard=Keyboard(inline=True).add(Callback(msg, {"route": "choose_package", "pid": package.id}), color))
        
    await message.answer("выберите нужные языковые пакеты", keyboard=Keyboard().add(Text("вернуться в меню", {"route": "menu"})))

@bl.private_message(payload_contains={"route": "menu"})
@bl.private_message(text=["меню"])
async def menu_handler(message: Message, user: User):
    kboard = (Keyboard()
              .add(Text("🗂 выбрать языковые пакеты", {"route": "packages_choose"}))
              .add(Text("🔍 учить", {"route": "start_teach"})))
    await message.answer(f"сейчас {datetime.datetime.now().strftime('%a %d %b %Y, %H:%M')}\n слов выучено: {get_user_words_count(user)}",
                          keyboard=kboard,
                        attachment="photo-224471611_457239019")


@bl.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent, payload_contains={"route": "choose_package"})
async def handle_message_event(event: MessageEvent):   
    package = get_package_by_id(event.get_payload_json()["pid"])
    user = get_user_by_vkid(vkid=event.peer_id)
    if package_user_active(user_id=user.id, package_id=package.id):
        delete_package_from_user(package.id, user)
    else:
        add_package_to_user(user, package)

    session.commit()

    if package_user_active(user_id=user.id, package_id=package.id):
        color = KeyboardButtonColor.POSITIVE
        msg = "активен"
    else:
        color = KeyboardButtonColor.NEGATIVE
        msg = "не активен"

    await event.edit_message(f"название: {package.name}", keyboard=Keyboard(inline=True).add(Callback(msg, {"route": "choose_package", "pid": package.id}), color))



@bl.private_message(payload_contains={"route": "start_teach"})
async def start_teach_handler(message: Message, user: User):
    if not user.packages:
        return "у вас нету активных языковых пакетов"


    word, category = get_word(user)
    kboard = Keyboard().add(Text("❌ выход", {"route": "to_menu"}))

    await message.answer(message_by_category(category, word), keyboard=kboard)
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = word) 

def message_by_category(category: int, word: UserWord) -> str:
    if category == 0:
        return f"🔷 новое слово! '{word.word.value.capitalize()}' - '{word.word.translate.capitalize()}'. напишите перевод для продолжения"
    elif category <= 3:
        return f"🔶 повторение. напишите перевод слова '{word.word.value.capitalize()}'."
    elif category >= 4:
        return f"♾ закрепление. напишите перевод слова '{word.word.value.capitalize()}'"


@bl.private_message(state=States.TeachMode)
async def teach_handler(message: Message, user: User):
    if message.payload:
        if message.get_payload_json()["route"] == "to_menu":
            await bot.state_dispenser.delete(message.peer_id)
            await menu_handler(message=message, user=user)
            return

    answer = message.text.lower().replace(" ", "").replace("\n", "")
    word: UserWord = message.state_peer.payload["word"]

    if 0.85 <= SequenceMatcher(None, word.word.translate, answer).ratio() <= 1.0:
        await message.answer("Верно!")
        word.level += 1
        word.last_repetition_time = datetime.datetime.now()
        session.commit()
    else:
        await message.answer(f"Не верно. Перевод: {word.word.translate}")
        word.level -= 1 if word.level > 1 else 0
        word.last_repetition_time = datetime.datetime.now()
        session.commit()

    next_word, category = get_word(user)
    await message.answer(message_by_category(category, next_word))
    await bot.state_dispenser.delete(message.peer_id)
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = next_word) 


@bl.private_message(payload_contains = {"route": "to_menu"})
async def menu_handler_alias(message: Message, user: User):
    await menu_handler(message, user)
    return

        
        
    


         