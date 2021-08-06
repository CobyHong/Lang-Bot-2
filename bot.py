import discord
from discord.ext import commands
from itranslate import itranslate as itrans
from gtts import gTTS
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
client = commands.Bot(command_prefix='!')


# bot on startup.
@client.event
async def on_ready():
	try:
		print("Translator Bot is Online.")
		return await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="August Update!"))
	except:
		print("Failed to perform on_ready.")
		return


# join user's voice channel currently residing in.
@client.command(pass_context=True)
async def trjoin(ctx):
	try:
		print("Channel joined")
		await ctx.author.voice.channel.connect()
		return
	except:
		print("Could not find channel or user already connected.")
		await ctx.voice_client.disconnect()
		return


#leave user's voice channel currently residing in.
@client.command()
async def trleave(ctx):
	try:
		print("Left channel.")
		await ctx.voice_client.disconnect()
	except:
		print("Could not leave channel or never connected.")
		return


#bot help command.
@client.command()
async def trhelp(ctx):
	try:
		print("Help command sent.")
		output = "    !tr\n    !trjoin\n    !trleave\n    !trabout\n    !trping\n   !trhelp"
		embed = discord.Embed(color=0xffdd00)
		embed.add_field(name="**Commands:**",
						value= output,
						inline=True)
		await ctx.send(embed=embed)
	except:
		print("Help command failed.")
		return


#bot ping command.
@client.command()
async def trping(ctx):
	try:
		print("Ping command sent.")
		output = "Hello **{}**! We are live! :earth_americas:".format(ctx.author)
		embed = discord.Embed(color=0xffdd00)
		embed.add_field(name="...",
						value=output,
						inline=True)
		await ctx.send(embed=embed)
	except:
		print("Print command failed")
		return


#provides information about creator.
@client.command()
async def trabout(ctx):
	try:
		print("About command sent.")
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
	except:
		print("About command failed")
		return


#provides link to GitHub page containing list of usable languages.
@client.command()
async def trlangs(ctx):
	try:
		print("Langs command sent")
		output = "https://github.com/CobyHong/Lang-Bot-2"

		embed = discord.Embed(color=0xffdd00)
		embed.add_field(name="**Languages (In GitHub Page):**",
	                    value=output,
	                    inline=True)
		await ctx.author.send(embed=embed)
	except:
		print("langs command failed.")
		return


#"!tr {lang} {msg}" command.
@client.command()
async def tr(ctx, *, msg=""):

	try:
		print("translating message.")
		#converting string into an array.
		msg_array = msg.split(' ')
		#getting chosen language key from first index.
		language_key = msg_array[0]
		#parsing message to remove the language command from it.
		message = ' '.join(msg_array[1:])

		#checking argument length / validate command.
		if(len(msg_array) < 2):
			embed = invalid_usage()
			await ctx.send(embed=embed)
			return

		#see if the language key chosen exist in our library.
		if language_key in languages.LANGUAGES:
			new_language = itrans(message, to_lang=language_key)
			embed = message_format(ctx, message, new_language)
			await ctx.send(embed=embed)

			#if connected to channel, playing text-to-speech.
			channel = ctx.voice_client
			if(channel is not None):
				channel.pause()
				channel.stop()
				tts = gTTS(new_language, lang=language_key)
				tts.save("./audio_output/output.mp3")
				channel.play(discord.FFmpegPCMAudio("./audio_output/output.mp3"))

		elif language_key == "uwu":
			msg = "I can't believe you were stupid enough to try this. You are a stupid weeb. Have some decency. Shame on you..."
			embed = message_format(ctx, "God", msg)
			await ctx.send(embed=embed)

			#if connected to channel, playing text-to-speech.
			channel = ctx.voice_client
			if(channel is not None):
				channel.pause()
				channel.stop()
				tts = gTTS(msg, lang='en')
				tts.save("./audio_output/output.mp3")
				channel.play(discord.FFmpegPCMAudio("./audio_output/output.mp3"))

			embed = invalid_input()
			await ctx.send(embed=embed)
			return
	except:
		print("translation error.")
		return


#returns invalid usage message string based upon user's own language.
def invalid_usage():
	invalid_msg = "Invalid command usage.\nUsage: !tr ( language ) ( message )"
	embed = discord.Embed(color=0xffdd00)
	embed.add_field(name="...",
					value=invalid_msg,
					inline=True)
	return embed


#returns invalid language message input string based upon user's own language.  
def invalid_input():
	invalid_msg = "Invalid language input.\nPlease try again!"
	embed = discord.Embed(color=0xffdd00)
	embed.add_field(name="...",
					value=invalid_msg,
					inline=True)
	return embed


#formatting message before sendoff.
def message_format(ctx, original_message, translated_message):
    embed = discord.Embed(color=0xffdd00)
    embed.add_field(name="__{}__:".format(ctx.author),
                    value= '"' + original_message + '"' + " :arrow_right: " + '"' + translated_message + '"',
                    inline=True)
    return embed


client.run(str(token))