import asyncio
from bot import telegram_bot
import os
from database.users import load_admins
import time

import time
print("⏳ Please wait...")
time.sleep(2)

async def main():
    await load_admins()
    await asyncio.gather(
        telegram_bot.start()
    )

if __name__ == '__main__':
    try:
        print("Запуск бота прошел успешно.")
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Bot stopped.")