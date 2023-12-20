import json
import os

import discord
from discord.ext import commands

from src.bot.bot_functions import process_warning, process_warning_for_command
from src.bot.cogs.help_cog import help_cog
from src.bot.cogs.moderation import Moderation
from src.bot.cogs.music_cog import music
from src.loader import bot, TOKEN
from discord.utils import get

BADWORDS = ["лох", "дурак"]
LINKS = ["https", "http", "://", ".com", ".ru"]


if not os.path.exists('users.json'):
    with open('users.json', 'w') as file:
        file.write('{}')
        file.close()
    for guild in bot.guilds:
        for member in guild.members:
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()
            with open('users.json', 'w') as file:
                data[str(member.id)] = {
                    "WARNS": 0,
                    "CAPS": 0
                }

                json.dump(data, file, indent=4)
                file.close()


@bot.event
async def on_message(message):
    WARN = BADWORDS + LINKS

    for warn_word in WARN:
        if warn_word in message.content.lower():
            await process_warning(message, "Ругательства/ссылки")
            await message.delete()
            return

    if message.content.isupper():
        with open('users.json', 'r') as file:
            data = json.load(file)

        author_id = str(message.author.id)

        # Update caps count
        data[author_id]["CAPS"] += 1

        if data[author_id]["CAPS"] >= 3:
            await process_warning(message, "Капс")
            await message.delete()

        # Save the updated data back to the file
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)

    await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.reply('hello')
    await ctx.send('hello2')


@bot.command()
async def test(ctx, *args):
    await ctx.send(args)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def warn(ctx, member: discord.Member, reason: str):
    if reason.lower() == "badwords" or reason.lower() == "links" or reason.lower() == "caps":
        await process_warning_for_command(ctx, member, reason)
        await ctx.send(embed=discord.Embed(
            title="Успешно",
            description="*Предупреждение выдано*",
            timestamp=ctx.message.created_at
        ))
    else:
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description="*Неправильная причина*",
            timestamp=ctx.message.created_at,
            color=discord.Color.red()
        ))


@warn.error
async def error_warn(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description="Использование: !warn <member> <reason>",
            timestamp=ctx.message.created_at
        ))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description="У вас недостаточно прав",
            timestamp=ctx.message.created_at
        ))


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unwarn(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()
    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] -= 1
        json.dump(data, file, indent=4)

        file.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def clear_warns(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()
    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] = 0
        json.dump(data, file, indent=4)

        file.close()


async def setup_bot():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music(bot))
    await bot.add_cog(Moderation(bot))

