import json
import os

import discord

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


@bot.event
async def on_ready():
    # print("Данные бота")
    # print(f"Имя бота {bot.user.name}")
    # print(f"ID бота: {bot.user.id}")

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
    for i in range(0, len(WARN)):
        if WARN[i] in message.content.lower():
            await message.delete()
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()
            with open('users.json', 'w') as file:
                data[str(message.author.id)]['WARNS'] +=1
                json.dump(data, file, indent=4)

                file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"Раннее у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1}"
                            f" нарушений, после 7 он будет забанен!",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

            await get(message.guild.text_channels, id=1186750128405622874).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason="Вы превысили допустимое кол-во нарушений")

    if message.content.isupper():
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json', 'w') as file:
            data[str(message.author.id)]["CAPS"] +=1
            json.dump(data, file, indent=4)
        data[str(message.author.id)]["CAPS"] +=1

        if data[str(message.author.id)]["CAPS"] >= 3:
            await message.delete()
            with open('users.json', 'w') as file:
                data[str(message.author.id)]["CAPS"] = 0
                data[str(message.author.id)]["WARNS"] += 1

                json.dump(data, file, indent=4)

            emb = discord.Embed(
                title="Нарушение",
                description=f"Раннее у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1}"
                            f" нарушений, после 7 он будет забанен!",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

            await get(message.guild.text_channels, id=1186750128405622874).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason="Вы превысили допустимое кол-во нарушений")




@bot.command()
async def hello(ctx):
    await ctx.reply('hello')
    await ctx.send('hello2')


@bot.command()
async def test(ctx, *args):
    await ctx.send(args)


async def setup_bot():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music(bot))
    await bot.add_cog(Moderation(bot))

