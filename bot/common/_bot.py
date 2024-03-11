from vkbottle.bot import Bot
from vkbottle import API
import sys
from loguru import logger
from vkbottle.http import AiohttpClient
from ._config import settings
import aiohttp

logger.remove()
logger.add(sys.stderr, level="INFO")

http_client = AiohttpClient(connector=aiohttp.TCPConnector(verify_ssl=False))
api = API(http_client=http_client, token=settings.TOKEN)
bot = Bot(api=api)

