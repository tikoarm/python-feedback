import asyncio
from bot import telegram_bot
from database.users import load_admins
from cache.api_keys import load_api_keys
from multiprocessing import Process
from web.api import start_api
import time
import logging
from logic.logger import setup_logger


setup_logger()
logging.info("⏳ Please wait...")
time.sleep(2)


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
