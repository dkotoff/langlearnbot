from bot.common import bot, settings
from bot.routes.words import bl as words_bl

bot.labeler.load(words_bl)

bot.run_forever()