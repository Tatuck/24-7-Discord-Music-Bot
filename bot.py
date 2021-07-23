import json
from discord.ext import commands

config = json.load(open("config.json",encoding="utf8"))
botToken = config["botToken"]

bot = commands.Bot("-", help_command=None)

bot.channelID = config["channelID"]
bot.youtubeID = config["youtubeID"]
bot.youtubeApiKey = config["youtubeApiKey"]

bot.load_extension("cogs.onready")
bot.load_extension("cogs.surpressOff")

bot.run(botToken)