from bot.common import bot
from bot.routes import routes_labeler
bot.labeler.load(routes_labeler)

bot.run_forever()