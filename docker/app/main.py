import asyncio
from bot import telegram_bot

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