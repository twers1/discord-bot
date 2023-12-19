import datetime

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided!"):
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.mention} is Banned from {ctx.guild.name} by {ctx.author.mention}\n"
                        f"Reason: {reason}",
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(),
        )
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(
                embed=discord.Embed(
                    title="Missing permissions",
                    description="The bot doesn't have the required permissions to ban a member",
                    color=discord.Color.red(),
                )
            )

    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided!"):
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} is Kicked from {ctx.guild.name} by {ctx.author.mention}\n"
                        f"Reason: {reason}",
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(),
        )
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(
                embed=discord.Embed(
                    title="Missing permissions",
                    description="The bot doesn't have the required permissions to kick a member",
                    color=discord.Color.red(),
                )
            )

    @commands.command(aliases=["ub"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id):
        user = await self.bot.fetch_user(member_id)
        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} is unbanned from {ctx.guild.name} by {ctx.author.mention}",
            color=discord.Color.random(),
            timestamp=datetime.datetime.now(),
        )
        try:
            await ctx.guild.unban(user)
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(embed=discord.Embed(title="Member not found", color=discord.Color.red()))

    @commands.command(name="clear_chat", aliases=["cc"])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int = 2):
        if amount < 1:
            await ctx.send("Amount should be more than 1 ")
            return
        try:
            await ctx.channel.purge(limit=amount + 1)
        except:
            await ctx.send(
                embed=discord.Embed(
                    title="Missing permissions",
                    description="The bot doesn't have the required permissions to ban a member",
                    color=discord.Color.red(),
                )
            )
