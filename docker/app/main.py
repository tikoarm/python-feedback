import asyncio
from bot import telegram_bot
import os
from database.users import load_admins

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

import time
logging.info("⏳ Please wait...")
time.sleep(2)

async def main():
    await load_admins()
    await asyncio.gather(
        telegram_bot.start()
    )

if __name__ == '__main__':
    try:
        logging.info("⏳ Bot is starting...")
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Bot stopped.")