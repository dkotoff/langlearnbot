from vkbottle.bot import Message
from bot.database.users import user_exist, get_user_by_vkid, add_user
from bot.common import bot, session
from vkbottle import BaseMiddleware

class UserReqMiddleware(BaseMiddleware[Message]):

    async def pre(self):
        vk_user = await bot.api.users.get([self.event.peer_id])
        if not user_exist(self.event.peer_id):
            user = add_user(vkid=self.event.peer_id, name=vk_user[0].first_name)
            session.commit()
        else:
            user = get_user_by_vkid(vkid=self.event.peer_id)
        
        self.send({"user": user})