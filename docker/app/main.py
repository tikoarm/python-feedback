import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'bot'))

import telegram_bot

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