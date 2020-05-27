
import os
import shutil
from os import system
import datetime
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get


PREFIX = '.'
client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')
bad_words = open('bad_words.txt', 'r').readline()
players = {}


@client.event
async def on_ready():
    print('BOT_CONNECTED')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# обработка ошибок


@client.event
async def on_command_error(ctx, error):
    pass


@client.event
async def on_member_join(member):
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(469583134900617238)

    role = discord.utils.get(member.guild.roles, id=694437070638153748)

    await member.add_roles(role)
    await channel.send(emb=discord.Embed(description=f'Welcome ``{member.name}``', colo=discord.Color.green()))


@client.command(pass_context=True)
async def hello(ctx, arg):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    await ctx.send(f' {author.mention} ' + arg)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):

    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=discord.Embed(description=f'Было удалено {amount} сообщений'))

# BOT_CONNECTED


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason='dolbaeb'):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)

    await ctx.send(f'kick use {member.mention}')


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason='dolbaeb'):

    emb = discord.Embed(title='Ban', color=discord.Color.red())
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='', value='Banned user:{}'.format(member.mention))
    emb.set_footer(text='Was banned by {}'.format(
        ctx.author.mention), icon_url=ctx.author.avatar_url())

    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)

    await ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):

    await ctx.channel.purge(limit=1)
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned user {user.mention}')
            return


@client.command(pass_context=True)
async def lul(ctx, arg):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    await ctx.send(f' {author.mention} ' + arg)


@client.command(pass_context=True)
async def time(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(
        title='Your title', color=discord.Color.green(), url='https://vk.com/frag_er')
    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text='Зачем меня призвали!')
    emb.set_thumbnail(
        url='https://sun9-59.userapi.com/c205720/v205720104/f984/vVd2is_VlJg.jpg')

    now_date = datetime.datetime.now()

    emb.add_field(name='Time', value='Time: {}'.format(now_date))

    await ctx.send(embed=emb)


@client.command(pass_context=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Навигация по командам')
    emb.add_field(name='{}clear'.format(PREFIX), value='очистка чата')
    emb.add_field(name='{}ban'.format(PREFIX), value='бан')
    emb.add_field(name='{}kick'.format(PREFIX), value='кик')
    emb.add_field(name='{}unban'.format(PREFIX), value='разбан')
    await ctx.send(embed=emb)


@client.command()
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='MUTE')
    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} was muted')


@client.command()
async def send_to(ctx, member: discord.Member, *, smth):

    await ctx.channel.purge(limit=1)
    await member.send(f'Привет от {ctx.author.mention} ' + smth)


# Errors


@clear.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, missing argument!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, you do not have enough permissions!')


@user_mute.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, missing argument!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, you do not have enough permissions!')


@ban.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, missing argument!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, you do not have enough permissions!')


@unban.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, missing argument!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, you do not have enough permissions!')


@kick.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, missing argument!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit=1)
        await ctx.send(f'{ctx.author.mention}, you do not have enough permissions!')

# музыка


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(
                os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"),
                           after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"),
               after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


queues = {}


@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")


@client.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing")
        await ctx.send("No music playing failed")


token = open('token.txt', 'r').readline()

client.run(token)
