import asyncio
import logging
from multiprocessing import Process

from bot import telegram_bot
from cache.api_keys import load_api_keys
from database.users import load_admins
from logic.logger import setup_logger
from web.api import start_api

setup_logger()
logging.info("⏳ Please wait...")


async def main():
    await load_admins()
    await asyncio.gather(telegram_bot.start())


if __name__ == "__main__":
    try:
        asyncio.run(load_api_keys())

        logging.info("⏳ Webserver is starting...")
        api_process = Process(target=start_api)
        api_process.start()

        logging.info("⏳ Bot is starting...")
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Bot stopped.")
