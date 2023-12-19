import discord
from discord.ext import commands


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
            ```
  h      Displays all the available commands
music:
  clear  Stops the current song and clears the queue
  leave  Kick the bot from the voice channel
  pause  Pause the currect song being played
  play   Play the selected song from youtube
  queue  Displays all the songs currently in the queue
  resume Resume playing the currect song
  skip   Skips the currectly played song

Type /help command for more info on a command.
You can also type /help category for more info on a category.
            ```
        """
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)

        await self.send_to_all(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="h", help="Displays all the available commands")
    async def custom_help(self, ctx):
        await ctx.send(self.help_message)
