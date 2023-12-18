from src.bot.help_cog import help_cog
from src.bot.music_cog import music
from src.loader import bot, TOKEN

@bot.command()
async def hello(ctx):
    await ctx.reply('hello')
    await ctx.send('hello2')

@bot.command()
async def test(ctx, *args):
    await ctx.send(args)



bot.run(TOKEN)
