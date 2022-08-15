from googlesearch import search 
import discord
from discord.ext import commands
from dpyConsole import Console
import random
import os
import sys
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from asyncio import Event
import re
import time
import json
from os.path import exists
from threading import Thread
from typing import Optional, Tuple, List, Callable
from unittest.mock import Mock
import ffmpeg
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from datetime import datetime
from youtube_dl import YoutubeDL
import logging
from discord.embeds import Embed
from discord.file import File
from cogs.musicCog import MusicCog
from cogs.errorCog import ErrorCog
from cogs.otherCog import CommandsCog
CHANNEL_ID_LENGTH = 18
with open('badwords.txt', 'r') as f:
    words = f.read()
    badwords = words.split()
with open('status.txt', 'r') as f:
    statusmsg = f.read()

description = '''A bot originaly for the nerd bin server'''

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
load_dotenv()
bot = commands.Bot(command_prefix='.', description=description, intents=intents)
client = bot
# log error output to file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# adds command functionality from cogs.py
bot.add_cog(MusicCog(bot))
bot.add_cog(CommandsCog(bot))
# REMEMBER TO UNCOMMENT THIS
bot.add_cog(ErrorCog(bot))
my_console = Console(client)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bcchannel = discord.utils.get(bot.get_all_channels(), name="bot-interface")
    if bcchannel.name == "bot-interface":
        await bcchannel.send('Now Online')
    else:
        newbcchannel = await guild.create_text_channel('bot-interface')
        await newbcchannel.send('Now Online')
    
    await bot.change_presence(activity=discord.Game(statusmsg))  

@bot.command(brief='Changes the bots status')
async def status(ctx, *, msg: str):
    f = open("status.txt", "w")
    f.write(msg)
    f.close()
    await bot.change_presence(activity=discord.Game(msg))
@bot.command(brief='if the bot says you need to be in a voice channel use this')
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command(brief='Second leave command if the first one doesnt work')
async def leave1(ctx):
    await ctx.voice_client.disconnect()
@bot.command(brief='Restarts the bot (admin)')
@has_permissions(administrator=True)
async def reset(ctx):
    await os.system("sh startbot.sh")
    await exit()
@bot.command(brief='Generates a random pokemon')
async def pokeman(ctx):
    n = random.randrange(1, 896)
    query = f"\n what is pokemon {n} pokemon.com"
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        await ctx.send(f"\nRandom Pokemon {j}")
@bot.event
async def on_raw_reaction_add(payload):
    reaction = payload
    user = payload.member
    channel = bot.get_channel(payload.channel_id)
    rrdict = "rrstorage/" + str(reaction.guild_id) + "rrdict.json"
    rrid = "rrstorage/" + str(reaction.guild_id) + "rrid.txt"
    rrid1 = await load_if_exists(rrid)
    emojidict = await load_if_exists(rrdict)
    if str(reaction.message_id) != str(rrid1):
        print(rrid1)
        print(reaction.message_id)
        print("killme")
        return
    else:
        if emojidict != False:
            if rrid1 != False:
                rcji = str(reaction.emoji)
                print(rcji)
                if rcji in emojidict:
                    print(emojidict[rcji])
                    rname = emojidict[rcji]
                    role = discord.utils.get(user.guild.roles, name=rname)
                    await user.add_roles(role)
                else:
                    await channel.send("role not found, add it using .newrr")
            else:
                return    
        else:
            await new_from_default(rrdict, "rrstorage/rrdictdefault.json")
@bot.command(brief='sets the message you react to to get roles')
@has_permissions(administrator=True)
async def newrrmsg(ctx):
    rrid = "rrstorage/" + str(ctx.guild.id) + "rrid.txt"
    await ctx.channel.purge(limit=1)
    print("new rrmessage")
    sent_message = await ctx.channel.send(content="React Here for roles")
    print(sent_message.id)
    with open(rrid, 'w') as f:
        f.write(str(sent_message.id))
@bot.command(brief='must be owner of the bot to use this')
@commands.is_owner()
async def system(ctx, cmm: str):
    await os.system(cmm)
@bot.command(brief='deletes a specified amount of messages from a channel')
@has_permissions(administrator=True)
async def delete(ctx, num: int):
    await ctx.channel.purge(limit=(num + 1))
@bot.command(brief='cant decide between two things, use this command')
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))
@bot.command(brief='adds a new role command')
@has_permissions(administrator=True)
async def newrc(ctx, trigger, role, perms):
    crcfile = "crcstorage/" + str(ctx.guild.id) + "crcdict.json"
    crcpfile = "crcstorage/" + str(ctx.guild.id) + "crcperms.json"
    crcdict = await load_if_exists(crcfile)
    crcperms = await load_if_exists(crcpfile)
    if crcdict != False:
        newdata = {trigger : role}
        newdata2 = {trigger : int(perms)}
        crcdict.update(newdata)
        crcperms.update(newdata2)
        print(json.dumps(crcdict))
        print(json.dumps(crcperms))
        with open(crcfile, "w") as outfile:
            json.dump(crcdict, outfile)
        with open(crcpfile, "w") as outfile:
            json.dump(crcperms, outfile)
@bot.command(brief='repeats up to 29 times')
async def r(ctx, msg: str, times: int):
    if times < 300:
        for i in range(times):
            await ctx.send(msg)

@bot.command(brief='find top ten results on google for the message')
async def se(ctx, *, query: str):
    async with ctx.typing():
        for j in search(query, tld="co.in", num=10, stop=10, pause=2):  
            await ctx.send(f"\n:point_right: {j}")
@bot.command(brief='finds one result on google for the message')
async def se1(ctx, *, query: str):
    async with ctx.typing():
        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                await ctx.send(f"\n:point_right: {j}")

@bot.command(brief='dms a user from the bot')
async def dm(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)
@bot.command(brief='create a poll for important desicions')
async def poll(ctx, *, question):
    await ctx.channel.purge(limit=1)
    message = await ctx.send("Poll: " + question + " :white_check_mark:=Y :x:=N")
    reaction1 = '✔'
    reaction2 =  '❌'
    await message.add_reaction(reaction1)
    await message.add_reaction(reaction2)
@bot.command(brief='check your level')
async def level(ctx, mention: discord.User):
    lvldict = "levelstorage/" + str(ctx.guild.id) + "lvldict.json"
    with open(lvldict) as json_file:
        leveldict = json.load(json_file)
    if str(mention.id) in leveldict:
        points = leveldict[str(mention.id)]
        await ctx.reply(getLevel(points))
        return
    else:
        if str(ctx.author.id) in leveldict:
            points = leveldict[str(ctx.author.id)]
            ctx.reply(getLevel(points))
            print(leveldict)
def getLevel(points):
    levels=[20,50,75,100,150,200,250,500,750,1500,2500,5000,10000,15000,20000,30000,50000,100000,250000]
    lvl = len([x for x in levels if points > x])
    return lvl
@bot.command(brief='allows a role to be assigned with an emoji')
@has_permissions(administrator=True)
async def newrr(ctx, emoji: str, rname: str):
    rrdict = "rrstorage/" + str(ctx.guild.id) + "rrdict.json"
    newdata = {emoji : rname}
    with open(rrdict) as json_file:
        emojidict = json.load(json_file)
    emojidict.update(newdata)
    print(json.dumps(emojidict))
    with open(rrdict, "w") as outfile:
        json.dump(emojidict, outfile)
@bot.command(brief='removes the role and emoji from react role list')
@has_permissions(administrator=True)
async def delrr(ctx, emoji:str):
    rrdict = "rrstorage/" + str(ctx.guild.id) + "rrdict.json"
    emojidict  = json.load(open(rrdict))                                                     
    del emojidict[emoji]
    print(emojidict)
    print(json.dumps(emojidict))
    with open(rrdict, "w") as outfile:
        json.dump(emojidict, outfile)
@bot.group(brief='are you cool')
async def cool(ctx, msg: str):
    cool = random.choice([1, 2])
    if cool < 2:
        await ctx.send(msg+" is cool")
    if cool > 1:
        await ctx.send(msg+" is not cool")
@bot.event
async def on_message_edit(before, after):
    message = after
    msg = message.content
    for word in badwords:
        if word in msg:
            await message.delete()
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(bot.get_all_channels(), name="general")
    await channel.send("welcome " + str(member))
async def load_if_exists(ffile):
    if os.path.exists(ffile):
        with open(ffile) as json_file:
            ffdict = json.load(json_file)
            return ffdict
    else:
        return False
async def new_from_default(fname, defname):
    with open(defname) as f:
        data = json.load(f)
    with open(fname, 'w') as f:
        json.dump(data, f, indent=2)
        print("New json file is created from " + str(defname) + " file")
async def run_command(message):
    msg1 = message.content.lower().split()
    crcfile = "crcstorage/" + str(message.guild.id) + "crcdict.json"
    crcpfile = "crcstorage/" + str(message.guild.id) + "crcperms.json"
    crcdefault = "crcstorage/crcdefault.json"
    crcpdefault = "crcstorage/crcpdefault.json"
    crcdict = await load_if_exists(crcfile)
    perms = message.channel.permissions_for(message.author)
    crcperms = await load_if_exists(crcpfile)
    try:
        user=message.mentions[0]
    except IndexError:
        user=message.author
    if crcdict != False:
        if crcperms != False:
            for word in msg1:
                if word in crcdict:
                    if crcperms[word] == 1:
                        if message.author.guild_permissions.manage_roles == True:
                            crcname = crcdict[word]
                            role = discord.utils.get(message.guild.roles, name=crcname)
                            if role in user.roles:
                                await user.remove_roles(role)
                            else:
                                await user.add_roles(role)
                    if crcperms[word] == 2:
                        crcname = crcdict[word]
                        role = discord.utils.get(message.guild.roles, name=crcname)
                        if role in user.roles:
                            await user.remove_roles(role)
                        else:
                            await user.add_roles(role)
                else:
                    if word.startswith("."):
                        return False
                        break
        else:
            await new_from_default(crcpfile, crcpdefault)
    else:
        await new_from_default(crcfile, crcdefault)
async def filterply(message):
    msg1 = message.content.lower().split()
    filterdic = await load_if_exists("filterdicfile.json")
    bpc = await load_if_exists("bpcfile.json")
    print(msg1)
    for word in msg1:
        print(word)
        if word in filterdic:
            if filterdic[word] == "f1":
                await message.delete()
            elif filterdic[word] == "f2":
                await message.reply('mama', mention_author=False)
            elif filterdic[word] == "f3":
                await message.reply('balls', mention_author=False)
            elif filterdic[word] == "f4":
                if str(bot.user.id) in str(message.content):
                    if word == "good":
                        if "good night" in message.content.lower():
                            await message.reply('goodnight :sleeping:', mention_author=True)
                    else:
                        await message.reply('goodnight :sleeping:', mention_author=True)
            elif filterdic[word] == "f5":
                await message.reply('https://www.shrekthemusical.co.uk/wp-content/uploads/2022/05/Shrek.jpg', mention_author=False)
            elif filterdic[word] == "f6":
                if word == "kill":
                        if "kill yourself" in message.content.lower() or "kill myself" in message.content.lower():
                            bpnum = str(random.randrange(1, 10))
                            await message.reply(bpc[bpnum], mention_author=True)
                else:
                    bpnum = str(random.randrange(1, 10))
                    await message.reply(bpc[bpnum], mention_author=True)
async def levelsys(message):
    msg1 = message.content.lower().split()
    lvldict = "levelstorage/" + str(message.guild.id) + "lvldict.json"
    mid = str(message.author.id)
    leveldict = await load_if_exists(lvldict)
    if leveldict != False:
        if mid in leveldict:
            init_num = leveldict[mid]
            init_num += 1
            leveldict[mid] = init_num
            print(leveldict)
            with open(lvldict, "w") as outfile:
                json.dump(leveldict, outfile)
        elif mid not in leveldict:
            newdata = {mid : 1}
            leveldict.update(newdata)
            print(json.dumps(leveldict))
            with open(lvldict, "w") as outfile:
                json.dump(leveldict, outfile)
    else:
        await new_from_default(lvldict, "levelstorage\leveldefault.json")
@bot.event
async def on_message(message):
    COMMAND_PREFIX = "."
    msg1 = message.content.lower().split()
    if message.author == client.user:
        return
    if not message.content.startswith(COMMAND_PREFIX):
        await filterply(message)
        await levelsys(message)
        return
    rcresult = await run_command(message)
    if rcresult == False:
        await bot.process_commands(message)
    
 

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
bottokenfile = open("token.txt", 'r')
bottoken = bottokenfile.read()
bottokenfile.close()
my_console.start()
bot.run(bottoken)

