import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from googletrans import Translator
import languages
import asyncio
import os


#Bot by Coby Hong using discord.py and free google translate API for Python.
#Welcome to edit and use code as long as some form of credit is given.

#GITHUB:	https://github.com/CobyHong
#Website:	www.coby.tech
#Email:		CobyHong@gmail.com

# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
# hhhhhhyyyyyhhhysssssssyhhhhhhh
# hhhhhhysssyhhhssssssssyhhhhhhh
# hhhhhhs///shhhssssssssyhhhhhhh
# hhhhhho:::shhhssssssssyhhhhhhh
# hhhhhho:::shhh////////ohhhhhhh
# hhhhhho:::shhh////////ohhhhhhh
# hhhhhho:::shhh////////ohhhhhhh
# hhhhhho:::osss////////oyhhhhhh
# hhhhhho:::+ooooooooooooyhhhhhh
# hhhhhho::::::::::::::::ohhhhhh
# hhhhhhs++++++++++++++++shhhhhh
# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh


#bot initialization.
token = os.environ.get('BOT_TOKEN')
bot = commands.Bot(command_prefix='!')


#Google translate initialization.
translator = Translator()


#bot on startup.
@bot.event
async def on_ready():
    print("Translator Bot is Online.")
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Anime"))


#join user's voice channel currently residing in.
@bot.command(pass_context=True)
async def trjoin(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="...",
                    value="Joining your channel...",
                    inline=True)
    await client.send(embed)

#leave user's voice channel currently residing in.
@bot.command()
async def trleave(ctx):
    await ctx.voice_client.disconnect()

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="...",
                    value="Leaving your channel...",
                    inline=True)
    await client.send(embed)


#bot help command.
@bot.command()
async def trhelp(ctx):
    output = "    !tr\n    !trabout\n    !trping\n   !trhelp"
    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="**Commands:**",
                    value= output,
                    inline=True)
    await ctx.send(embed=embed)


#bot ping command.
@bot.command()
async def trping(ctx):
    output = "Hello **{}**! We are live! :earth_americas:".format(ctx.author)

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="...",
                    value=output,
                    inline=True)
    await ctx.send(embed=embed)


#"!tr {lang} {msg}" command.
@bot.command()
async def tr(ctx, *, msg):

    #converting string into an array.
    msg_array = msg.split(' ')
    #getting chosen language key from first index.
    language_key = msg_array[0]
    #parsing message to remove the language command from it.
    message = msg.replace(language_key + ' ', '')
    #getting the language the user is in.
    detected_language = translator.detect(message).lang

    #checking argument length / validate command.
    if(len(msg_array) < 2 or msg is None):
        embed = invalid_usage(msg, detected_language)
        await ctx.send(embed=embed)

    #see if the language key chosen exist in our library.
    elif language_key in languages.LANGUAGES.keys():
        new_language = translator.translate(message, language_key).text
        embed = message_format(ctx, message, new_language)
        await ctx.send(embed=embed)

    else:
        embed = invalid_input(message, detected_language)
        await ctx.send(embed=embed)


#provides information about creator.
@bot.command()
async def trabout(ctx):
    str1 = "Hi my name is Coby Hong\n"
    str2 = "This bot was made for fun so that everyone of different backgrounds could communicate!\n"
    str3 = "If you have any questions, here is my general info:\n"
    str4 = "@GITHUB:\thttps://github.com/CobyHong\n@Website:\twww.coby.tech\n@Email:\t\tCobyHong@gmail.com"
    output = str1 + str2 + str3 + str4

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="**About:**",
                    value= output,
                    inline=True)
    await ctx.author.send(embed=embed)


#provides link to GitHub page containing list of usable languages.
@bot.command()
async def trlangs(ctx):
    output = "https://github.com/CobyHong/Lang-Bot-2"

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="**Languages (In GitHub Page):**",
                    value=output,
                    inline=True)
    await ctx.author.send(embed=embed)


#returns invalid usage message string based upon user's own language.
def invalid_usage(message, language):
    invalid_msg = "Invalid command usage.\nUsage: !tr ( language ) ( message )"
    translated_invalid_msg = translator.translate(invalid_msg, language).text

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="...",
                    value=translated_invalid_msg,
                    inline=True)
    return embed


#returns invalid language message input string based upon user's own language.  
def invalid_input(message, language):
    invalid_msg = "Invalid language input.\nPlease try again!"
    translated_invalid_msg = translator.translate(invalid_msg, language).text

    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="...",
                    value=translated_invalid_msg,
                    inline=True)
    return embed


#formatting message before sendoff.
def message_format(ctx, original_message, translated_message):
    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="__{}__:".format(ctx.author),
                    value= '"' + original_message + '"' + " :arrow_right: " + '"' + translated_message + '"',
                    inline=True)
    return embed


bot.run(str(token))

