import logging
import redis
import aiofiles
from datetime import datetime as dt
from aiopath import AsyncPath
from aiogram import Dispatcher

import config
from loader import db
from utils import queries


# проверка работы редиса
async def check_redis(dp: Dispatcher):
    r = redis.Redis(host=config.REDIS_HOST,
                    password=config.REDIS_PASSWORD,
                    socket_connect_timeout=1)
    try:
        r.ping()
    except (redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError):
        await dp.bot.send_message(
            chat_id=config.ADMIN_ID,
            text='‼REDIS УПАЛ‼')
        logging.info('Checking redis connection - FAIL')


# очистка лог-файла
async def clear_logs(dp: Dispatcher):
    try:
        file = AsyncPath(config.LOG_FILE)
        if await file.is_file():
            async with aiofiles.open(file, 'w') as file:
                pass
    except Exception as error:
        logging.info('Clear logs fail: %s', error)
