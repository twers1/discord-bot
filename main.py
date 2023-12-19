from src.bot.bot import setup_bot
from src.loader import bot, TOKEN
import asyncio

if __name__ == '__main__':
    asyncio.run(setup_bot())

    bot.run(TOKEN)
