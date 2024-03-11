from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text
from bot.routes.main_menu import menu_handler
import bot.words_selection as ws
from bot.states import States
import datetime
from difflib import SequenceMatcher
from bot.model import User, UserWord
from bot.common import session, bot


bl = BotLabeler()

@bl.private_message(payload_contains={"route": "start_teach"})
async def start_teach_handler(message: Message, user: User):
    if not user.packages:
        return "У вас нету активных языковых пакетов"


    word, category = ws.get_word(user)
    kboard = Keyboard().add(Text("❌ Выход", {"route": "to_menu"}))

    await message.answer(message_by_category(category, word), keyboard=kboard)
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = word) 

def message_by_category(category: int, word: UserWord) -> str:
    if category == 0:
        return f'🔷 Новое слово! "{word.word.value.capitalize()}" - "{word.word.translate.capitalize()}". Напишите перевод для продолжения '
    elif category in [1, 2]:
        return f'🔶 Повторение. Напишите перевод слова "{word.word.value.capitalize()}".'
    elif category <= 3:
        return f'♾ Закрепление. Напишите перевод слова "{word.word.value.capitalize()}:"'


@bl.private_message(state=States.TeachMode)
async def teach_handler(message: Message, user: User):
    if message.payload:
        if message.get_payload_json()["route"] == "to_menu":
            await bot.state_dispenser.delete(message.peer_id)
            await menu_handler(message=message, user=user)
            return

    answer = message.text.lower().replace(" ", "").replace("\n", "")
    word: UserWord = message.state_peer.payload["word"]

    if 0.70 <= SequenceMatcher(None, word.word.translate, answer).ratio() <= 1.0:
        await message.answer("Верно!")
        word.level += 1
        word.last_repetition_time = datetime.datetime.now()
        session.commit()
    else:
        await message.answer(f"Не верно. Перевод: {word.word.translate}")
        word.level -= 1 if word.level > 1 else 0
        word.last_repetition_time = datetime.datetime.now()
        session.commit()

    next_word, category = ws.get_word(user)
    await message.answer(message_by_category(category, next_word))
    await bot.state_dispenser.delete(message.peer_id)
    await bot.state_dispenser.set(message.peer_id, States.TeachMode, word = next_word) 


@bl.private_message(payload_contains = {"route": "to_menu"})
async def menu_handler_alias(message: Message, user: User):
    await menu_handler(message, user)
    return

        
        
    


         