import asyncio
from bot import telegram_bot
import os

from dotenv import load_dotenv
env_loaded = load_dotenv()
if not env_loaded:
    print("⚠️ .env файл не найден. Переменные окружения могут быть не загружены.")


async def main():
    await asyncio.gather(
        telegram_bot.start()
    )

if __name__ == '__main__':
    try:
        print("Запуск бота прошел успешно.")
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Bot stopped.")