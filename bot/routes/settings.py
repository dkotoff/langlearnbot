from vkbottle.bot import BotLabeler, Message, MessageEvent
from bot.model import User

from bot.common import bot, session
from bot.database.users import get_user_by_vkid
from typing import Tuple, List
from vkbottle import Keyboard, KeyboardButtonColor, Callback, GroupEventType, Text

bl = BotLabeler()


async def settings_messages(user: User) -> Tuple[List[str], List[Keyboard]]:
    kbaords = []
    messages = []

    kboard = Keyboard(inline=True)

    for button_value in [2, 5, 10, 15]:
        color = KeyboardButtonColor.POSITIVE if user.day_goal == button_value else KeyboardButtonColor.PRIMARY

        kboard.add(Callback(str(button_value), {"action": "set_goal", "value": str(button_value)}), color=color)

    kbaords.append(kboard)
    messages.append("Интенсивность (Новых слов в день):")

    kboard = Keyboard(inline=True)

    for button_value in ["Утро", "День", "Вечер", "выкл."]:
        color = KeyboardButtonColor.POSITIVE if user.notification == button_value else KeyboardButtonColor.PRIMARY

        kboard.add(Callback(button_value, {"action": "set_notification", "value": button_value}), color=color)

    kbaords.append(kboard)
    messages.append("Уведомления:")

    return messages, kbaords

async def send_settings(user: User):
    messages, keyboards = await settings_messages(user=user)

    for index, message in enumerate(messages):
        await bot.api.messages.send(message=message, keyboard=keyboards[index], random_id=0, peer_id=user.vkid)

    await bot.api.messages.send(user_id=user.vkid, message="Настройки", random_id=0, keyboard=Keyboard().add(Text("Назад", {"route": "to_menu"})))
    return


@bl.private_message(payload_contains={"route": "settings"})
async def settings_handler(message: Message, user: User):
    await send_settings(user=user)
    return 


@bl.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent, payload_contains={"action": "set_goal"})
async def user_set_goal_event(event: MessageEvent):
    payload = event.get_payload_json()
    user = get_user_by_vkid(event.object.peer_id)
    user.day_goal = payload["value"]
    session.commit()

    kboard = Keyboard(inline=True)

    for button_value in [2, 5, 10, 15]:
        color = KeyboardButtonColor.POSITIVE if user.day_goal == button_value else KeyboardButtonColor.PRIMARY

        kboard.add(Callback(str(button_value), {"action": "set_goal", "value": str(button_value)}), color=color)

    
    await event.edit_message(message="Интенсивность (Новых слов в день):", keyboard=kboard)

@bl.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent, payload_contains={"action": "set_notification"})
async def user_set_notif_event(event: MessageEvent):
    payload = event.get_payload_json()
    user = get_user_by_vkid(event.object.peer_id)
    user.notification = payload["value"]
    session.commit()

    kboard = Keyboard(inline=True)


    for button_value in ["Утро", "День", "Вечер", "выкл."]:
        color = KeyboardButtonColor.POSITIVE if user.notification == button_value else KeyboardButtonColor.PRIMARY

        kboard.add(Callback(button_value, {"action": "set_notification", "value": button_value}), color=color)

    await event.edit_message(message="Уведомления:", keyboard=kboard)