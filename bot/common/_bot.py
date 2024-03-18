from vkbottle.bot import Bot
from vkbottle import API
import sys
from loguru import logger
from vkbottle.http import AiohttpClient
from ._config import settings
import aiohttp

// подключение логирования
logger.remove()
logger.add(sys.stderr, level="INFO")
// инициализация http клиента для подключения к вк
http_client = AiohttpClient(connector=aiohttp.TCPConnector(verify_ssl=False))
api = API(http_client=http_client, token=settings.TOKEN)

// инициализация объекта бота
bot = Bot(api=api)

