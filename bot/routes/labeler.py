from vkbottle.bot import BotLabeler
from bot.middlewares import UserReqMiddleware
from .main_menu import bl as main_menu_labeler
from .packages import bl as packages_labeler
from .words import bl as words_labeler
from .settings import bl as settings_labeler

bl = BotLabeler()
bl.vbml_ignore_case = True
bl.message_view.register_middleware(UserReqMiddleware)

for labeler in [main_menu_labeler, packages_labeler, words_labeler, settings_labeler]:
    bl.load(labeler)