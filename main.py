from src.bot.help_cog import help_cog
from src.bot.music_cog import music
from src.loader import bot, TOKEN
import asyncio


async def setup_bot():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music(bot))

if __name__ == '__main__':
    asyncio.run(setup_bot())
    bot.run(TOKEN)
