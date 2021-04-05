import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import asyncio
import youtube_dl

from random import choice

client = commands.Bot(command_prefix='bebo ')
statusi=['slusam losu muziku..', 'necu da ucim!', 'cekam da se mateja vrati kuci :c', 'tiltujem u valorantu', 'tekken sama u sobi']

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%USERPROFILE%\Desktop\%(title)s-%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


@client.event
async def on_ready():
    change_status.start()
    print("evo me!")

@client.command(name='lgm', help='probaj pa vidi')
async def lgm(ctx):
    await ctx.send(f'looooooomi ga matke za {round(client.latency * 1000)}ms')

@client.command(name='cao', help='pozdravi me')
async def cao(ctx):
    odgovori=['cao bebo!', 'ljubi te brat bebo', 'ostavi me na miru bebo :weary:', 'idemo po taj hleb bebo', 'gde si do sad bebo? :heart_eyes:']
    await ctx.send(choice(odgovori))

@client.command(name='git', help='moj github')
async def git(ctx):
    await ctx.send('https://github.com/yazecchi :revolving_hearts:')

@client.command(name='potd', help='person of the day')
async def potd(ctx):
    osobe=['olja','masa','ivana','nevena','stefke','ognjen','miksi','fedja','mateja']
    await ctx.send(f'najbolja osoba danas je {choice(osobe)} :smiling_face_with_3_hearts: :kiss: :sparkles: ')

@client.command(name='pusti', help='pusta pesmu')
async def pusti(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('nisi u voice kanalu, nemoj da trolujes ://')
        return
    else:
        channel=ctx.message.author.voice.channel
    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    player = await YTDLSource.from_url(url, loop=client.loop)
    voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)


@client.command(name='izadji', help='izlazi iz vc')
async def izadji(ctx):
    voice_client=ctx.message.guild.voice_client
    await voice_client.disconnect()
    await ctx.send('zbogom.. :sob:')

@tasks.loop(seconds=7200)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(statusi)))

client.run('ODI4NDE0NjQ5NzQ5MjA5MDg5.YGpPQw.WovFEkanXIEQveJ6I867SfeVx2A')



