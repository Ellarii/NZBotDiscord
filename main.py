
# Imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import random
import youtube_dl
import asyncio
import datetime as dt


# Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='~', intents=intents)
prefix = '~'
smc = None # Snipe message content
smai = None # Snipe message author id
sman = None # Snipe Message author name
smaa = None # Snipe Message active
emai=None
eman=None
emc=None
emaa=None
snipe_message_id = None
ytdl_format_options = {
    'format': 'bestaudio/best',
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

# Commands (on queue)

# Checks if bot is active
@client.command(name="ping", help="Checks to see if the bot is active. Should respond with 'pong'")
async def ping(ctx):
    await ctx.channel.send("pong")
    print(f"Ping command used in {ctx.guild}")

# Bot echoes
@client.command(name="msg", help="Echoes a single word message")
async def msg(ctx, arg):
    await ctx.channel.send(arg)
    print(f"msg command used in {ctx.guild}")

# Multi word nz.msg
@client.command(name="multimsg", help="Echoes a multiple word message")
async def multimsg(ctx, *args):
    response = ""
    for arg in args:
        response = response + " " + arg
    await ctx.channel.send(response)
    print(f"multimsg command used in {ctx.guild}")

@client.command(name="bing", help=f"Echoes `dong`. Different form of {prefix}ping")
async def bing(ctx):
  await ctx.channel.send("dong")
  print(f"bing command used in {ctx.guild}")

# Spam pinger (variable amount)
@client.command(name="kill", help=f"Spam pings a user. Format `{prefix}kill [UserMention] [Amount]`")
async def kill(ctx, arg, amount=1):
  fail = f"kill command attempted by {ctx.author} in {ctx.guild}"
  if "@" in arg:
    if "@everyone" in arg or "@here" in arg:
      await ctx.channel.send("You are not allowed to ping this user")
      print(fail)
    else:
      print(f"kill command used by {ctx.author} in {ctx.guild}")
      if int(amount) is not ValueError:
        if amount == 1:
          await ctx.channel.send(f"If you wish to have more than one ping, please enter an amount in the following format\n`{prefix}kill [Mention] [Amount]`")
        for number in range(int(amount)):
          await ctx.channel.send(arg)
      elif int(amount) is ValueError:
        await ctx.channel.send("Please enter a number")
    
  elif arg is str:
    await ctx.channel.send("Please ping a user")
    print(fail)
  elif "everyone" in arg or "here" in arg:
    await ctx.channel.send("You are not allowed to ping this user")
    print(fail)
  else:
    await ctx.channel.send(f"This command is used to spam ping a user. To begin, please type `{prefix}kill [UserPing]`!")
    print(fail)

# Sniper command
@client.command(name="snipe", help="Snipes previously deleted message")
async def snipe(ctx):
  print(f"Snipe command used by {ctx.author.display_name} in {ctx.author.guild.name}")
  embed = discord.Embed(title=f"Sniped message:", description=smc)
  embed.set_author(name=sman, icon_url=smaa)
  embed.set_footer(text=f"Sniped message id: {str(smi)}")
  await ctx.send(f"Sniped message requested by {ctx.author.display_name}", embed=embed)
@client.command(name="esnipe", help="Snipes previously edited message **BROKEN**")
async def esnipe(ctx):
  print(f"Snipe command used by {ctx.author.display_name} in {ctx.author.guild.name}")
  embed=discord.Embed(title="Previous message content:", description=emc)
  embed.set_author(name=eman,icon_url=emaa)
  embed.set_footer(text=f"Sniped message id: {str(emi)}")
  await ctx.send(f"Sniped message requested by {ctx.author.display_name}",embed=embed)


# Embed message
@client.command(name="botinfo", help="Displays Bot info = GitHub link")
async def botinfo(ctx):
  embed = discord.Embed(title="Github", url="https://github.com/Nouvelle-Zelande", description="This bot was created by Nouvelle-Zelande#6154.\nFeel free to send any queries/questions their way!", color=000000)
  await ctx.send(embed=embed)
  print(f"botinfo command used in {ctx.guild}")

@client.command(name="numbergen", help=f"Sends a random number between 1 and a specified amount. Format `{prefix}numbergen [MaxParam]`")
async def numbergen(ctx, param):
  number = random.choice(list(range(int(param))))
  embed = discord.Embed(title="The number you generated was:", description=f"The number that you generated (between 1 and {param}) was:\n{number}", color=000000)
  await ctx.send(embed=embed)
  print(f"numbergen command used in {ctx.guild}")

@client.command(name="coinflip", help="Flips a coin")
async def coinflip(ctx):
  options = ["heads", "tails"]
  result = random.choice(options)
  embed = discord.Embed(title="Coin flip result", description=f"The result of your coin flip was:\n", color=000000)
  if result == "heads":
    embed.set_image(url="https://media.discordapp.net/attachments/759929659453866035/920540883735158784/AmericanQuarterHeads.png")
  else:
    embed.set_image(url="https://media.discordapp.net/attachments/759929659453866035/920540884003586048/AmericanQuarterTails.png")
  await ctx.send(embed=embed)
  print(f"coinflip command used in {ctx.guild}")

# Attempted music commands

#Join + leave vc
@client.command(name="joinvc", help="Joins a vc. User must be connected to a vc for this command to work")
async def joinvc(ctx):
  if not ctx.author.voice.channel:
    await ctx.channel.send(f"{ctx.message.author.name} is not connected to a voice channel!")
    print(f"joinvc command failed in {ctx.guild}")
  else:
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.channel.send(f"{channel} successfully joined!")
    print(f"joinvc command used in {ctx.guild}")

@client.command(name="leavevc", help="Leaves a connected vc. Bot must be connected to a vc for this command to work")
async def leavevc(ctx):
  voice_client = ctx.message.guild.voice_client
  if voice_client.is_connected:
    channel = ctx.author.voice.channel
    await ctx.voice_client.disconnect()
    await ctx.channel.send(f"{channel} successfully left!")
    print(f"leavevc command used in {ctx.guild}")
  else:
    await ctx.channel.send(f"I am not connected to a voice channel! To make me join one, join a voice channel and type `{prefix}joinvc`")
    print(f"leavevc command failed in {ctx.guild}")

youtube_dl.utils.bug_reports_message = lambda: ''

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
      loop = loop or asyncio.get_event_loop()
      data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
      if 'entries' in data:
        # take first item from a playlist
        data = data['entries'][0]
      filename = data['title'] if stream else ytdl.prepare_filename(data)
      return filename

@client.command(name='play', help='To play song')
async def play(ctx,url):
    try :
      server = ctx.message.guild
      voice_channel = server.voice_client
      async with ctx.typing():
        filename = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
      await ctx.send('**Now playing:** {}'.format(filename))
      print(f"play command used in {ctx.guild}")
    except:
      await ctx.send("The bot is not connected to a voice channel.")
      print(f"play command failed in {ctx.guild}")



@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
        print(f"pause command used in {ctx.guild}")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        print(f"pause command failed in {ctx.guild}")
    
@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
        print(f"resume command used in {ctx.guild}")
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
        print(f"resume command failed in {ctx.guild}")

@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
        print(f"stop command used in {ctx.guild}")
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        print(f"stop command failed in {ctx.guild}")

@client.command(name="getid", help="Gets the ID of a user **MOD ONLY**")
@commands.has_role(759909993649930250)
async def getid(ctx, user: discord.User):
  embed=discord.Embed(title=f"ID of {user}", description=f"The ID of this user is {user.id}")
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(f"{user.id}", embed=embed)
  print(f"getid command used in {ctx.guild}")


# Always tracking
# On bot begin
@client.event
async def on_ready():
    for guild in client.guilds:
      print(
          f'{client.user} is connected to the following guild:\n'
          f'{guild.name} (id: {guild.id})'
      )
# On member join
@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")
    mc=member.guild.member_count
    if member.guild.id == 756238963240337438: 
      channel=client.get_channel(909954400565485588)
      channel2 = client.get_channel(792281236650459156)
      member_creation_date=member.created_at.timestamp()
      format_date=dt.datetime.utcfromtimestamp(member_creation_date).strftime("%Y/%m/%d %H:%M")
      embed1=discord.Embed(title=f"{member} has joined the server!", description=f"The member count is now {mc}!", color=000)
      embed2 = discord.Embed(title=f"{member} has left the server.", description=f"The member count is now {mc}!\n\n\nAccount Created at: {format_date}", color=000)
      embed2.set_footer(text=f"ID: {member.id}")
      await channel2.send(embed=embed1)
      await channel.send(embed=embed2)
    else:
      await ctx.send("This command doesn't work in this server")

# On member leave
@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")
    mc=member.guild.member_count
    if member.guild.id == 756238963240337438:
      channel = client.get_channel(909954400565485588)
      channel2 = client.get_channel(792281236650459156)
      member_creation_date=member.created_at.timestamp()
      format_date=dt.datetime.utcfromtimestamp(member_creation_date).strftime("%Y/%m/%d %H:%M")
      embed1 = discord.Embed(title=f"{member} has left the server.", description=f"The member count is now {mc}!", color=000)
      embed2 = discord.Embed(title=f"{member} has left the server.", description=f"The member count is now {mc}!\n\n\nAccount Created at: {format_date}", color=000)
      embed2.set_footer(text=f"ID: {member.id}")
      await channel2.send(embed=embed1)
      await channel.send(embed=embed2)
    else:
      await ctx.send("This command doesn't work in this server")
@client.event
async def on_message_delete(message):

    global smc
    global smai
    global sman
    global smi
    global smaa

    smc = message.content
    smai = message.author.id
    sman = message.author.display_name
    smi = message.id
    smaa = message.author.avatar_url
    await asyncio.sleep(60)

    if message.id == smi:
        smai = None
        sman = None
        smc = None
        smi = None
        smaa = None
@client.event
async def on_message_edit(message):
  global emc
  global emai
  global eman
  global emi
  global emaa
  emc=message.content
  emai=message.author.id
  eman=message.author.display_name
  emi=message.id
  emaa=message.author.avatar_url
  await asyncio.sleep(60)
  if message.id==emi:
    emai=None
    eman=None
    emc=None
    emi=None
    emaa=None
  
# End commands
keep_alive()
if __name__ == "__main__":
  client.run(TOKEN)