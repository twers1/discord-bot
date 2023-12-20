import json
import discord
from discord.utils import get


async def process_warning(ctx, reason):
    # Load data from the file
    with open('users.json', 'r') as file:
        data = json.load(file)

    # Update data with a new warning
    data[str(ctx.author.id)]['WARNS'] += 1

    # Save the updated data back to the file
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

    # Create and send an embed
    emb = discord.Embed(
        title="Нарушение",
        description=f"Раннее у нарушителя было уже {data[str(ctx.author.id)]['WARNS'] - 1}"
                    f" нарушений, после 7 он будет забанен!",
        timestamp=ctx.created_at
    )

    emb.add_field(name="Канал:", value=ctx.channel.mention, inline=True)
    emb.add_field(name="Нарушитель:", value=ctx.author.mention, inline=True)
    emb.add_field(name="Тип нарушения:", value=reason, inline=True)

    await ctx.guild.get_channel(1186750128405622874).send(embed=emb)

    # Check if the user should be banned
    if data[str(ctx.author.id)]['WARNS'] >= 7:
        await ctx.author.ban(reason="Вы превысили допустимое кол-во нарушений")


async def process_warning_for_command(ctx, member, reason):
    # Load data from the file
    with open('users.json', 'r') as file:
        data = json.load(file)

    # Update data with a new warning
    data[str(member.id)]['WARNS'] += 1

    # Save the updated data back to the file
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

    # Create and send an embed
    emb = discord.Embed(
        title="Нарушение",
        description=f"Раннее у нарушителя было уже {data[str(member.id)]['WARNS'] - 1}"
                    f" нарушений, после 7 он будет забанен!",
        timestamp=ctx.created_at
    )

    emb.add_field(name="Канал:", value=ctx.channel.mention, inline=True)
    emb.add_field(name="Нарушитель:", value=ctx.author.mention, inline=True)
    emb.add_field(name="Тип нарушения:", value=reason, inline=True)

    await get(ctx.message.guild.text_channels, id=1186750128405622874).send(embed=emb)

    # Check if the user should be banned
    if data[str(member.id)]['WARNS'] >= 7:
        await member.ban(reason="Вы превысили допустимое кол-во нарушений")

