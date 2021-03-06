  
# Imports
import os, discord, random, asyncio, sys, json, glob
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import datetime as dt
from word_blacklist import bad_words
# Setup
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
words_snipe_censor = os.getenv('SCENSOR')
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='~', intents=intents)
prefix = '~'
original_stdout = sys.stdout
smc = None # Snipe message content
smai = None # Snipe message author id
sman = None # Snipe Message author name
smaa= "https://cdn.discordapp.com/attachments/782748743748419603/922352397773307944/placeholder.png"
smi=None
emai=None
emi=None
eman=None
emaa="https://cdn.discordapp.com/attachments/782748743748419603/922352397773307944/placeholder.png"
embc=None
emac=None
logging_bypass = [270904126974590976, 716390085896962058, 408785106942164992, 920398992632860792, 282859044593598464, 204255221017214977]
words_autoban = []
with open('json/lvl_d.json', 'r') as lf:
  level_log=json.load(lf)
file_path_type = "./assets/raccoonstore/*.gif"
raccoons = glob.glob(file_path_type)

# Commands (on queue)
# Checks if bot is active
@client.command(name="ping", help="Checks to see if the bot is active. Should respond with 'pong'")
async def ping(ctx):
     
    await ctx.channel.send("pong")
    print(f"Ping command used in {ctx.guild}")

@client.command(name="bing", help=f"Echoes `dong`. Different form of {prefix}ping")
async def bing(ctx):
   
  await ctx.channel.send("dong")
  print(f"bing command used in {ctx.guild}")

@client.command(name="raccoon", aliases=['rac', 'ra', 'redpanda', 'red', 're'], help="Haha raccoon")
async def raccoon(ctx):
  print("raccoon generated")
  async with ctx.typing():
    embed = discord.Embed(title="The rategoon/red panda you have generated is:")
    file = discord.File(f"{random.choice(raccoons)}", filename="image.gif")
    embed.set_image(url="attachment://image.gif")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text="Source: Misc Images")
    await asyncio.sleep(3)
  await ctx.send("Generation Successful!",file=file, embed=embed)

# Spam pinger (variable amount)
@client.command(name="kill", aliases=["k"], help=f"Spam pings a user. format `{prefix}kill [UserMention]`")
async def kill(ctx, member: discord.User):
  if ctx.author.guild.id == 850685567628607509:
    await ctx.send("You cannot use that here")
    print(f"Kill command Failed by {ctx.author.display_name} in {ctx.author.guild}")
  else:
    channel = ctx.message.channel
    for number in range(10):
      await channel.send(f"<@{member.id}>")
    print(f"Kill command used by {ctx.author.display_name} in {ctx.author.guild}")

@client.command(name="ishedead", aliases = ["ihd"], help="is dea d he s?")
async def ishedead(ctx, member:discord.User):
  if member.discriminator == "7818":
    await ctx.send("lmao die")
  elif member.discriminator == "7948":
    await ctx.send("lmao i see")
  else:
    await ctx.send("lmao live")

@client.command(name="rank", aliases=["r"], help="Displays your xp")
async def rank(ctx, member:discord.User):
  with open('lvl_d.json', 'r') as f:
    lvlstr = json.load(f)
  guild = client.get_guild(ctx.author.guild.id)
  user = discord.utils.get(guild.members, name=f"{member.name}", discriminator=f"{member.discriminator}")
  if str(user) in lvlstr:
    xp = lvlstr[f"{user}"]
  else:
    xp = 0
  e = discord.Embed(title = f"{ctx.author.name}\'s XP!")
  e.add_field(name="XP", value=f"This user has {xp} XP!", inline = False)
  e.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)
  await ctx.send(embed=e)

# Sniper command
@client.command(name="snipe", aliases=["s"], help="Snipes previously deleted message")
async def snipe(ctx):
   
  print(f"Snipe command used by {ctx.author.display_name} in {ctx.author.guild.name}")
  if smc in words_snipe_censor:
    await ctx.send("Snipe failed - Bad Word")
    print("User failed snipe - Bad Words")
  else:
    embed = discord.Embed(title=f"Sniped message:", description=smc)
    embed.set_author(name=sman, icon_url=smaa)
    embed.set_footer(text=f"Sniped message id: {str(smi)}")
    await ctx.send(f"Sniped message requested by {ctx.author.display_name}", embed=embed)
@client.command(name="esnipe", aliases=["e"], help="Snipes previously edited message")
async def esnipe(ctx):
   
  print(f"Esnipe command used by {ctx.author.display_name} in {ctx.author.guild.name}")
  if (embc in words_snipe_censor) or (emac in words_snipe_censor):
    print("User failed esnipe - bad words")
    await ctx.send("Snipe failed - Bad word")
  else:
    embed=discord.Embed(title="Message content:")
    embed.add_field(name="Before Edit", value=embc, inline=True)
    embed.add_field(name="After Edit", value=emac, inline=True)
    embed.set_author(name=eman,icon_url=emaa)
    embed.set_footer(text=f"Edit sniped message id: {str(emi)}")
    await ctx.send(f"Sniped message requested by {ctx.author.display_name}",embed=embed)

# Embed message
@client.command(name="botinfo", help="Displays Bot info = GitHub link")
async def botinfo(ctx):
   
  embed = discord.Embed(title="Github", url="https://github.com/Nouvelle-Zelande", description="This bot was created by Nouvelle-Zelande#6154.\nFeel free to send any queries/questions their way!", color=000000)
  await ctx.send(embed=embed)
  print(f"botinfo command used in {ctx.guild}")
  await ctx.message.delete()

@client.command(name="numbergen", help=f"Sends a random number between 1 and a specified amount. Format `{prefix}numbergen [MaxParam]`")
async def numbergen(ctx, param):
   
  number = random.choice(list(range(int(param))))
  embed = discord.Embed(title="The number you generated was:", description=f"The number that you generated (between 1 and {param}) was:\n{number}", color=000000)
  await ctx.send(embed=embed)
  print(f"numbergen command used in {ctx.guild}")
  await ctx.message.delete()

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
  await ctx.message.delete()

@client.command(name="getid", help="Gets the ID of a user **MOD ONLY**")
@commands.has_role(759909993649930250)
async def getid(ctx, user: discord.User):
   
  embed=discord.Embed(title=f"ID of {user}", description=f"The ID of this user is {user.id}")
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  await ctx.send(f"{user.id}", embed=embed)
  print(f"getid command used in {ctx.guild}")
  await ctx.message.delete()

@client.command(name="sd", help="a")
async def sd(ctx, guildid, *args):
  count=0
  if ctx.message.author.id == 375759240171618305:
    response = ""
    ch = client.get_channel(int(guildid))
    for arg in args:
      if count == 0:
        response = arg
      else:
        response = response + " " + arg
      count+=1
    await ctx.send(f"`{response}` successfully sent to channel!")
    await ch.send(response)
  else:
    await ch.send("no")
  
# Always tracking (events)
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
      embed2 = discord.Embed(title=f"{member} has joined the server.", description=f"The member count is now {mc}!\n\n\nAccount Created at: {format_date}", color=000)
      embed2.set_footer(text=f"ID: {member.id}")
      await channel2.send(embed=embed1)
      await channel.send(embed=embed2)
    else:
      print("This command doesn't work in this server (on join embed)")

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
      print("This command doesn't work in this server (on join embed)")

# On deletion of Message
@client.event
async def on_message_delete(message):
    if message.author.id not in logging_bypass:
      if message.guild.id == 756238963240337438: # So it actually logs in thr right place
        channel=client.get_channel(792281236650459156)
        if not any(word in message.content.lower() for word in bad_words):
          embed=discord.Embed(title="Deleted Message Logged:", description=f"Deleted message sent by {message.author.name} detected")
          embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
          if len(message.embeds) >=1:
            embed.add_field(name="\nDeleted Message Content (embed)", value="`This message has an embed, which is unable to be logged`", inline = False)
          elif len(message.embeds) == 0:
            embed.add_field(name="\nDeleted Message Content:", value=message.content, inline=False)
          embed.set_footer(text=message.id)
          await channel.send("Deleted Message Detected", embed=embed)
      elif message.guild.id == 661318259043467264:
        channel=client.get_channel(753236539093549066)
        if not any(word in message.content.lower() for word in bad_words):
          embed=discord.Embed(title="Deleted Message Logged:", description=f"Deleted message sent by {message.author.name} detected")
          embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
          if len(message.embeds) >=1:
            embed.add_field(name="\nDeleted Message Content (embed)", value="`This message has an embed, which is unable to be logged`", inline = False)
          elif len(message.embeds) == 0:
            embed.add_field(name="\nDeleted Message Content:", value=message.content, inline=False)
          embed.set_footer(text=message.id)
          await channel.send("Deleted Message Detected", embed=embed)
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
        smaa= "https://cdn.discordapp.com/attachments/782748743748419603/922352397773307944/placeholder.png"

#On Edit of Message
@client.event
async def on_message_edit(message_before, message_after):
  checkid = message_before.author.id
  if checkid not in logging_bypass:
    if message_before.guild.id == 756238963240337438: # So it actually logs in thr right place
      channel=client.get_channel(792281236650459156)
      if not any(word in message_before.content.lower() for word in bad_words) or not any(word in message_after.content.lower() for word in bad_words):
        embed=discord.Embed(title="Edited Message Logged:", description=f"Edited message sent by {message_before.author.name} detected")
        embed.set_author(name=message_before.author.name, icon_url=message_before.author.avatar_url)          
        if len(message_before.embeds) == 0:
          embed.add_field(name="\nMessage Content before edit", value=message_before.content, inline = True)
        elif len(message_before.embeds)>= 1:
          embed.add_field(name = "\nMessage Content before edit (embed)",value="`This message has an embed, which are unable to be logged`", inline=True)
        if len(message_after.embeds) == 0:
          embed.add_field(name="\nMessage Content after edit", value =  message_after.content, inline = True)
        elif len(message_after.embeds)>=1:
          embed.add_field(name="\nMessage Content after edit (embed)", value="`This message has an embed, which is unable to be logged`", inline = True)
        embed.set_footer(text=f"Message ID: {message_before.id}")
        await channel.send("Edited Message Detected", embed=embed)
    if message_before.guild.id == 661318259043467264: # So it actually logs in thr right place
      channel = client.get_channel(753236539093549066)
      if not any(word in message_before.content.lower() for word in bad_words) or not any(word in message_after.content.lower() for word in bad_words):
        embed=discord.Embed(title="Edited Message Logged:", description=f"Edited message sent by {message_before.author.name} detected")
        embed.set_author(name=message_before.author.name, icon_url=message_before.author.avatar_url)          
        if len(message_before.embeds) == 0:
          embed.add_field(name="\nMessage Content before edit", value=message_before.content, inline = True)
        elif len(message_before.embeds)>= 1:
          embed.add_field(name = "\nMessage Content before edit (embed)",value="`This message has an embed, which are unable to be logged`", inline=True)
        if len(message_after.embeds) == 0:
          embed.add_field(name="\nMessage Content after edit", value =  message_after.content, inline = True)
        elif len(message_after.embeds)>=1:
          embed.add_field(name="\nMessage Content after edit (embed)", value="`This message has an embed, which is unable to be logged`", inline = True)
        embed.set_footer(text=f"Message ID: {message_before.id}")
        await channel.send("Edited Message Detected", embed=embed)
    
  global embc
  global emac
  global emai
  global eman
  global emi
  global emaa
  embc=message_before.content
  emac=message_after.content
  emai=message_before.author.id
  eman=message_before.author.display_name
  emi=message_before.id
  emaa=message_before.author.avatar_url
  await asyncio.sleep(60)
  if message_before.id==emi:
    emai=None
    eman=None
    embc=None
    emac=None
    emi=None
    emaa= "https://cdn.discordapp.com/attachments/782748743748419603/922352397773307944/placeholder.png"

#On Message
@client.event
async def on_message(message):
  level_int = random.choice(list(range(3,6)))
  if message.guild.id != 850685567628607509:
    if any(word in message.content.lower() for word in bad_words):
      msgcont=message.content
      embed=discord.Embed(title="Banned word detected", description=f"Bad word sent by {message.author.name} were auto deleted. Escalate further if necessary.")
      embed.set_author(name=f"{message.author.name}", icon_url=message.author.avatar_url)
      embed.set_footer(text=f"Automodded message id = {message.id}")
      embed.add_field(name="\nMessage as follows", value=f"{msgcont}", inline=False)
      channel = client.get_channel(792281236650459156)
      await message.delete()
      await channel.send("Banned words detected:", embed=embed)
  with open('lvl_d.json', 'w') as lf:
    if message.author.id in logging_bypass:
      pass
    else:
      if message.author.id in level_log:
        level_log[message.author.id] += level_int
      else:
        level_log[message.author.id] = 0
        level_log[message.author.id] += level_int

    json.dump(level_log, lf)
  if message.content.lower() == "i see":
    await message.add_reaction("<:ISee:853899039271419924>")
  await client.process_commands(message)


# End commands
keep_alive()
if __name__ == "__main__":
  client.run(TOKEN)