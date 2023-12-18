import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music(commands.Cog):
    def __init__(self, bot):
        # Инициализация Cog для музыки с передачей экземпляра бота
        self.bot = bot

        # Флаги для отслеживания состояния воспроизведения музыки
        self.is_playing = False
        self.is_paused = False

        # Очередь для хранения информации о музыке
        self.music_queue = []

        # Опции для YoutubeDL и FFmpeg
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ',
                               'options': '-vn'}

        # Voice-клиент
        self.vc = None

    def search_yt(self, item):
        # Поиск песни на YouTube с использованием YoutubeDL
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        # Воспроизведение следующей песни в очереди
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            # Воспроизведение песни с использованием FFmpeg
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        # Воспроизведение музыки в голосовом канале
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            # Подключение к голосовому каналу
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Не удалось подключиться к голосовому каналу")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # Удаление проигранной песни из очереди и воспроизведение следующей
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Воспроизвести выбранную песню с YouTube")
    async def play(self, ctx, *args):
        # Команда для воспроизведения песни
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Подключитесь к голосовому каналу!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Не удалось загрузить песню. Неверный формат, попробуйте другой запрос")
            else:
                await ctx.send("Песня добавлена в очередь")
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Приостановить воспроизведение текущей песни")
    async def pause(self, ctx, *args):
        # Команда для приостановки текущей песни
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Возобновить воспроизведение текущей песни")
    async def resume(self, ctx, *args):
        # Команда для возобновления приостановленной песни
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Пропустить текущую проигрываемую песню")
    async def skip(self, ctx, *args):
        # Команда для пропуска текущей песни
        if self.vc != None and self.vc.is_playing():
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Отобразить все песни, находящиеся в очереди")
    async def queue(self, ctx):
        # Команда для отображения текущей очереди музыки
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4:
                break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("В очереди нет музыки")

    @commands.command(name="clear", aliases=["c", "bin"], help="Остановить текущую песню и очистить очередь")
    async def clear(self, ctx, *args):
        # Команда для очистки очереди музыки
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Очередь музыки очищена")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Изгнать бота из голосового канала")
    async def leave(self, ctx):
        # Команда для выхода бота из голосового канала
        self.is_playing = False
        self.is_paused = False
        await ctx.voice_client.disconnect()
