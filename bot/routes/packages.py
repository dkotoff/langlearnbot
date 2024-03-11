from vkbottle.bot import BotLabeler, Message, MessageEvent
from vkbottle import Keyboard, KeyboardButtonColor, Text,  Callback, GroupEventType
from bot.database.package import get_all_packages, package_user_active, get_package_by_id
from bot.database.users import get_user_by_vkid, delete_package_from_user, add_package_to_user
from bot.common import session
from bot.model import User

bl = BotLabeler()



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
        
    await message.answer("Выберите нужные языковые пакеты", keyboard=Keyboard().add(Text("вернуться в меню", {"route": "menu"})))


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
