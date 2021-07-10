import os
import discord
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('$helpme'))
  print("I am ready, logged in as {0.user}".format(client))
  
def help_weather():
  help_message = "For command list: `$helpme`\nFor weather reports: `$weather <city name>`\nFor pinging the bot: `$ping`"
  return (help_message)
  

@client.command()
async def ping(ctx):
  await ctx.channel.send(f'Pong! {round(client.latency * 1000)}ms')  

@client.command(aliases=['helpme', 'help_me'])
async def _help(ctx):
  help_message = help_weather()
  await ctx.channel.send(help_message)

@client.command()
async def weather(ctx, *, city_name):
  response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid='+(os.environ['API']))
  json_data = json.loads(response.text)
  weather = json_data
  await ctx.channel.send(weather)

keep_alive()  
client.run(os.environ['TOKEN'])
