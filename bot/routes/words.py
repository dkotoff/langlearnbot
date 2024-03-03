from vkbottle.bot import BotLabeler, Message, MessageEvent
from vkbottle import Keyboard, KeyboardButtonColor, Text,  Callback, GroupEventType
from bot.database.package import get_all_packages, get_package_by_id, package_user_active, get_user_random_packge
from bot.database.word import get_random_word_from_package_with_no_user, add_word_to_user, get_random_userword_by_level
from bot.database.users import get_user_by_vkid, delete_package_from_user, add_package_to_user
from bot.states import States
import datetime
import random
from difflib import SequenceMatcher
from bot.model import User, UserWord
from bot.common import session, bot
from bot.middlewares import UserReqMiddleware


bl = BotLabeler()
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserReqMiddleware)

@bl.private_message(text=["начать"])
async def start_menu_handler(message: Message, user: User):
    await message.answer("Добро пожаловать")


@bl.private_message(payload_contains={"route": "packages_choose"})
async def packages_choose(message: Message, user: User):
    for package in get_all_packages():
        if package_user_active(user_id=user.id, package_id=package.id):
            color = KeyboardButtonColor.POSITIVE
            msg = "Активен"
        else:
            color = KeyboardButtonColor.NEGATIVE
            msg = "Не активен"


        await message.answer(f"Название: {package.name}", keyboard=Keyboard(inline=True).add(Callback(msg, {"route": "choose_package", "pid": package.id}), color))
        
    await message.answer("Выберите нужные языковые пакеты", keyboard=Keyboard().add(Text("Вернуться в меню")))


@bl.private_message(text=["меню"])
async def menu_handler(message: Message, user: User):
    kboard = (Keyboard()
              .add(Text("Выбрать языковые пакеты", {"route": "packages_choose"}))
              .add(Text("Учить", {"route": "start_teach"})))
    await message.answer("Меню:", keyboard=kboard)


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
        msg = "Активен"
    else:
        color = KeyboardButtonColor.NEGATIVE
        msg = "Не активен"

    await event.edit_message(f"Название: {package.name}", keyboard=Keyboard(inline=True).add(Callback(msg, {"route": "choose_package", "pid": package.id}), color))



@bl.private_message(payload_contains={"route": "start_teach"})
async def start_teach_handler(message: Message, user: User):
    word = get_word(user=user)   
    await message.answer(f"Введите перевод слова <<{word.word.value}>>")
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = word) 


def random_category() -> int:
    rnum = random.randint(0, 100)
    if 80 < rnum <= 100:
        return 0
    elif 50 < rnum <= 80:
        return 1
    elif 25 < rnum <= 50:
        return 2
    elif 8 < rnum <= 25:
        return 3
    else:
        return 4

def get_word(user: User) -> UserWord:
    category = random_category()
    package = get_user_random_packge(user)

    while True:
        if category == 0:
            word = get_random_word_from_package_with_no_user(user=user, package=package)
            if not word:
                category+=1
                continue
            word = add_word_to_user(word, user)
            session.commit()
            break
        elif 1 <= category <= 4:
            word = get_random_userword_by_level(user=user, level=category)
            if not word:
                category+=1
                continue
            break
        else:
            word = get_random_word_from_package_with_no_user(user=user, package=package)
            word = add_word_to_user(word, user)
            session.commit()
            break
    return word


@bl.private_message(state=States.TeachMode)
async def teach_handler(message: Message, user: User):
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

    next_word = get_word(user)
    await message.answer(f"Введите перевод слова <<{next_word.word.value}>>")
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = word) 





        
        
    


         