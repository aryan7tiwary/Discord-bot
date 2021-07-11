import os
import discord
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime


client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('$helpme'))
  print("I am ready, logged in as {0.user}".format(client))
  
def help_weather():
  help_message = """
  For command list:    `$helpme`
  For weather reports: `$weather <city name>`
  For weather reports: `$weather <city name>,<Country name>
  For pinging the bot: `$ping`
  """
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
  response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid='+(os.environ['API'])+'&units=metric')
  json_data = json.loads(response.text)
  weather = json_data

  #city name
  city = city_name
  city_mod = "City:                {}".format(city)

  #country name
  country = weather['sys']['country']
  country_mod = "Country:             {}".format(country)

  #temperature
  temp = weather['main']['temp']
  temp_mod = f"Current temperature: {temp} °C"

  #min temperature
  temp_min = weather['main']['temp_min']
  temp_min_mod = f"Minimum temperature: {temp_min} °C"

  #max temperature
  temp_max = weather['main']['temp_max']
  temp_max_mod = f"Maximum temperature: {temp_max} °C"

  #feels like temperature
  temp_feels = weather['main']['feels_like']
  temp_feels_mod = f"Feels like:          {temp_feels} °C"
  
  #description
  description = weather['weather'][0]['description']
  description_mod = "Description:         {}".format(description)

  #wind speed
  wind_speed = weather['wind']['speed']
  wind_speed_mod = "Wind speed:          {} m/s".format(wind_speed)

  #sunrise time
  sunrise_time = int(weather['sys']['sunrise'])
  ts = sunrise_time
  sunrise_utc = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')[:-3]
  sunrise_time_mod = "Sunrise time:        {} UTC*".format(sunrise_utc)

  #sunset time
  sunset_time = int(weather['sys']['sunset'])
  ts = sunset_time
  sunset_utc = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')[:-3]
  sunset_time_mod = "Sunset time:         {} UTC*".format(sunset_utc)

  main = f'''
  ```
  {city_mod}
  {country_mod}
  {temp_mod}
  {temp_min_mod}
  {temp_max_mod}
  {temp_feels_mod}
  {description_mod}
  {wind_speed_mod}
  {sunrise_time_mod}
  {sunset_time_mod}





  *Add 5:30 for IST
  ```
  ''' 

  await ctx.channel.send(main)

keep_alive()  
client.run(os.environ['TOKEN'])
