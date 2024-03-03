from vkbottle.bot import Bot
from vkbottle import API
from vkbottle.http import AiohttpClient
from ._config import settings
import aiohttp

http_client = AiohttpClient(connector=aiohttp.TCPConnector(verify_ssl=False))
api = API(http_client=http_client, token=settings.TOKEN)
bot = Bot(api=api)

