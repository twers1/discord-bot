import json
import os

import discord
from discord.ext import commands

from src.bot.bot_functions import process_warning, process_warning_for_command
from src.bot.cogs.help_cog import help_cog
from src.bot.cogs.moderation import Moderation
from src.bot.cogs.music_cog import music
from src.loader import bot


BADWORDS = ["лох", "дурак"]
LINKS = ["https", "http", "://", ".com", ".ru"]

intents = discord.Intents.default()
intents.reactions = True


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
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Найти канал, в который нужно отправить сообщение
    channel_id = 1186337943841935372  # Замените на ID вашего канала
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="Выберите свою роль:",
            description="Реакции ниже представляют собой доступные роли.",
            color=0x00ff00
        )
        embed.add_field(name="Роль 1", value="🔴", inline=True)
        embed.add_field(name="Роль 2", value="🔵", inline=True)
        embed.add_field(name="Роль 3", value="🟢", inline=True)

        message = await channel.send(embed=embed)

        roles = {"🔴": "Название_Роли1", "🔵": "Название_Роли2", "🟢": "Название_Роли3"}

        for reaction in roles.values():
            # Проверяем, есть ли роль на сервере, и если нет, то создаем ее
            if discord.utils.get(channel.guild.roles, name=reaction) is None:
                await channel.guild.create_role(name=reaction)

        for reaction in roles.keys():
            await message.add_reaction(reaction)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    roles = {"🔴": "Название_Роли1", "🔵": "Название_Роли2", "🟢": "Название_Роли3"}

    if reaction.emoji in roles.keys():
        guild = bot.get_guild(reaction.message.guild.id)
        role = discord.utils.get(guild.roles, name=roles[reaction.emoji])

        if role:
            await user.add_roles(role)
            print(f"Added role {role.name} to {user.name}")


@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return

    roles = {"🔴": "Название_Роли1", "🔵": "Название_Роли2", "🟢": "Название_Роли3"}

    if reaction.emoji in roles.keys():
        guild = bot.get_guild(reaction.message.guild.id)
        role = discord.utils.get(guild.roles, name=roles[reaction.emoji])

        if role:
            await user.remove_roles(role)
            print(f"Removed role {role.name} from {user.name}")


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

