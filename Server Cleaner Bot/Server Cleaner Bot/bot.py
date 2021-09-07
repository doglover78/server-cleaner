import discord
from discord import member
from discord import message
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord_components import *
import datetime
import asyncio
import aiohttp
import random
import json
import os
import time
from discord.utils import get
from time import sleep

from discord.ext.commands.errors import MissingPermissions


#-------------------------------------------------
#config

discordbotversion = "1.1.4"

lastupdate = "3 Sep 2021"

discordbotprefix = "c!"


#-------------------------------------------------




intents = discord.Intents().all()

bot = commands.Bot(discordbotprefix, intents=intents)


bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='c! | servercleaner.xyz', url='https://www.twitch.tv/discord'))
    DiscordComponents(bot)
    print('Server Cleaner Is Ready!')
    print(len(bot.users), " Members")
    print(len(bot.guilds), "Server/s")
    



#----------------------------------------------------------------------------------------------
#moderator commands
  
@bot.command()
@commands.has_permissions(manage_messages=True)  
async def clean(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)   
    await ctx.send(f"<a:Bomb:876482377050906654> **Messages Deleted, Requested By** {ctx.author.mention}**!**")


        

@bot.command()
@commands.has_permissions(manage_channels=True)  
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    slowmodeembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```This Channels Slowmode Has Been Set To {seconds} By {ctx.message.author.name}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    slowmodeembed.set_author(name="Slowmode Set", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    slowmodeembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=slowmodeembed)




@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    lockembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```This Channel Has Been Locked By {ctx.message.author.name}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    lockembed.set_author(name="Channel Locked", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    lockembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=lockembed)



 
@bot.command()
@commands.has_permissions(manage_channels=True)  
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    unlockembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```This Channel Has Been Unlocked By {ctx.message.author.name}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    unlockembed.set_author(name="Channel Locked", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    unlockembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=unlockembed)






@bot.command()
async def help(ctx):
    helpembed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com")

    helpembed.set_author(name="Server Cleaner Commands.", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    helpembed.set_footer(text=f"Requested By {ctx.message.author.name}.", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    helpembed.add_field(name="Moderation Commands:", value="```c!clean [amount] c!slowmode [amount] c!lock c!unlock c!ban [user] [reason] c!unban [user] c!membercount.```", inline=False)
    helpembed.add_field(name="Game Commands:", value="```c!typeracer c!quote c!kill [user] c!slap [user] c!kiss [user] c!hug [user]```", inline=False)
    helpembed.add_field(name="Misc Commands:", value="```c!help c!vote c!invite c!website c!setup  c!version ```", inline=False)
    helpembed.add_field(name="Support Server:", value="||servercleaner.xyz||", inline=False)

    await ctx.send(content=f"{ctx.author.mention}", embed=helpembed)

    

@bot.command()
@commands.has_permissions(ban_members=True)  
async def ban (ctx, member:discord.User=None, reason =None):
    if member == ctx.message.author:
        
        banyourselfembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```Sorry But You Cant Ban Yourself Please Mention Another User To Ban```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        banyourselfembed.set_author(name="You Cant Do That", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        banyourselfembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=banyourselfembed)

        return
    if member == None:
        invalidargumentembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```Please Make Sure You Mention A Member To Ban```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        invalidargumentembed.set_author(name="Inavlid Argument", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        invalidargumentembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=invalidargumentembed)


    await ctx.guild.ban(member, reason=reason)



    banembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```Member: {member}\nModerator: {ctx.message.author.name}\nReason: {reason}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    banembed.set_author(name="Member Banned", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    banembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=banembed)







@bot.command()
@commands.has_permissions(ban_members=True)  
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)

    unbanembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```I Have Unbanned A User With The Id {id}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    unbanembed.set_author(name="Unbanned User", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    unbanembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=unbanembed)







#----------------------------------------------------------------------------------------------
#notes for the above commands are bellow.
#Most of the commands have custom
#emojis these can be found in the
#server cleaner support discord
#server.
#----------------------------------------------------------------------------------------------
#fun commands

@bot.command()
async def typeracer(ctx):
    starttime = time.time()

    randomsentences = ['The builder build something quite extraordinary.', 'The rocket manufacturer was spacex.', 'Leo had a very insucure password', 'Leo had a very insecure password', 'Some people like brave browser.', 'bon loves speed running minecraft in his spare time.']
    answer = random.choice(randomsentences)

    timer = 15.0
    await ctx.send(f'**You Have** `{timer}` **Seconds To Type:** `"{answer}"`')

    def is_correct(msg):
        return msg.author==ctx.author

    try:
        guess = await bot.wait_for('message', check=is_correct)
    except asyncio.TimeoutError:
        return await ctx.send('**It Seems You Took A Little Too Long.**')

    if guess.content == answer:
        await ctx.send('**You Got It Correct!**')
    else:
        await ctx.send('**Your Answer Wasnt Correct.**')



@bot.command()
async def quote(ctx):
    randomsentences = ['“Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten.” ― Neil Gaiman', '“Be yourself; everyone else is already taken.” ― Oscar Wilde', '“Darkness cannot drive out darkness: only light can do that. Hate cannot drive out hate: only love can do that.” ― Martin Luther King Jr', '“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.” ― Albert Einstein', '“I am enough of an artist to draw freely upon my imagination. Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.” ― Albert Einstein', '“You may say Im a dreamer, but Im not the only one.” ― John Lennon']
    randomquote = random.choice(randomsentences)
    await ctx.message.channel.send(f'**{randomquote}**')



        
@bot.command()
async def kill(ctx, member: discord.Member):  

    kill_messages = [
        f'<a:police:876803100684468244> {ctx.message.author.mention} **killed** {member.mention} **With A Baseball Bat**', 
        f'<a:police:876803100684468244> {ctx.message.author.mention} **killed** {member.mention} **With A Frying Pan**',
        f'<a:police:876803100684468244> {ctx.message.author.mention} **killed** {member.mention} **With A Tennis Racket**',
        f'<a:police:876803100684468244> {ctx.message.author.mention} **killed** {member.mention} **With A Golf Club**',
        f'<a:police:876803100684468244> {ctx.message.author.mention} **Got Caught Trying To Kill** {member.mention} **They Have Now Been Arrested!**',
    ]  
    await ctx.send(random.choice(kill_messages))
    




@bot.command()
async def slap(ctx, member: discord.Member):
        await ctx.send(f"<a:police:876803100684468244> {ctx.message.author.mention} **Slapped** {member.mention}") 


@bot.command()
async def kiss(ctx, member: discord.Member):
        await ctx.send(f"<a:Hearts:876482395522625592>  {ctx.message.author.mention} **Kissed** {member.mention}") 
        


@bot.command()
async def hug(ctx, member: discord.Member):
        await ctx.send(f"<a:Hearts:876482395522625592>  {ctx.message.author.mention} **Hugged** {member.mention}") 


#-----------------------------------------------------------------
#notes for the commands above are bellow.
#
#
#
#
#
#-----------------------------------------------------------------


#-----------------------------------------------------------------
#error handling.

@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        lockerrorembed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Sorry, You Need The MANAGE CHANNELS To Do That If You Think This Is A Bug Please Report It.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        lockerrorembed.set_author(name="Missing Permission", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        lockerrorembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=lockerrorembed)



@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        unlockerrorembed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Sorry, You Need The MANAGE CHANNELS To Do That If You Think This Is A Bug Please Report It.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        unlockerrorembed.set_author(name="Missing Permission", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        unlockerrorembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=unlockerrorembed)



@clean.error
async def clean_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        cleanerrorembed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Sorry, You Need The MANAGE MESSAGES To Do That If You Think This Is A Bug Please Report It.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        cleanerrorembed.set_author(name="Missing Permission", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        cleanerrorembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=cleanerrorembed)




@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        slowmoderrorembed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Sorry, You Need The MANAGE CHANNELS To Do That If You Think This Is A Bug Please Report It.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

        slowmoderrorembed.set_author(name="Missing Permission", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
        slowmoderrorembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

        await ctx.send(embed=slowmoderrorembed)




@bot.listen()
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    missingcommanderror = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Sorry, I Cant Find That Command If Your Sure Its A Command Do c!help To Make Sure You Didnt Misspell Anything.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    missingcommanderror.set_author(name="Cant Quite Find That", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    missingcommanderror.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=missingcommanderror)

#-----------------------------------------------------------------
#misc commands.

@bot.command()
async def invite(ctx):
    inviteembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```Click On Invite Me To Invite Me To Your Server Today. Need More Help Inviting Me? Do c!website For A Link To Our Website Were You Can Find Out More.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    inviteembed.set_author(name="Invite Me", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    inviteembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=inviteembed)



@bot.command()
async def website(ctx):
    websiteembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```Click On The Text Above To Goto The Server Cleaner Offical Website! (Here You Can Find The Invite A List Of Features Ect.)```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    websiteembed.set_author(name="Server Cleaner Website", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    websiteembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=websiteembed)


@bot.command()
async def version(ctx):
    versionembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```My Current Version Is {discordbotversion} And I Was Last Updated {lastupdate}```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    versionembed.set_author(name="Server Cleaner Bot Version", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    versionembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=versionembed)


@bot.command()
async def setup(ctx):
    setupembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```This Feature Is Not Yet Available However It Will Be Soon, Until Then Use c!help For A List Of Commands.```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    setupembed.set_author(name="Coming Soon", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    setupembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=setupembed)


@bot.command()
async def vote(ctx):
    voteembed = discord.Embed(colour=discord.Colour(0xd0021b), description="```You Can Vote For Server Cleaner At The Links Bellow, Voting Really Helps The Bot And Is Appreciated``` [Top.gg](https://top.gg/bot/744922928084287569)\n[Discord Bot List](https://discordbotlist.com/bots/server-cleaner)", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    voteembed.set_author(name="Vote For Me", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    voteembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=voteembed)



@bot.command()
async def membercount(ctx):
    membercountembed = discord.Embed(colour=discord.Colour(0xd0021b), description=f"```This Servers Current Member Count Is {ctx.guild.member_count}\n\nNote: This May Not Be Accurate Due To The Member Coutn Always Updating. ```", timestamp=datetime.datetime.utcfromtimestamp(1629708958))

    membercountembed.set_author(name="Current Member Count", url="https://servercleaner.xyz", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    membercountembed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    await ctx.send(embed=membercountembed)


#-----------------------------------------------------------------

@bot.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(colour=discord.Colour(0xd0021b), url="https://discordapp.com", description="```Thanks For Inviting Server Cleaner, Read Bellow To Get Started With Me.```")

    embed.set_author(name="Server Cleaner", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")
    embed.set_footer(text="Server Cleaner", icon_url="https://cdn.discordapp.com/attachments/853262975514968084/866659453617438730/server_cleaner.png")

    embed.add_field(name="Prefix:", value="```My Prefix Here Is c!```", inline=False)
    embed.add_field(name="Getting Started:", value="```To Get Started With The Bot We Recommend Running c!setup.```", inline=False)
    embed.add_field(name="How To Get Help:", value="```You Can Get Help By Doing The Command c!help Or Can Join The Discord Server.```", inline=False)

    await channel.send(embed=embed)









bot.run('')








