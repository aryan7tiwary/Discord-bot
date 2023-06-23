import discord
from dotenv.main import load_dotenv
import os
import requests
import json
from discord.ext import commands
from datetime import datetime

client = discord.Client()
client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('$helpme'))
    print("I am ready, logged in as {0.user}".format(client))


def help_weather():
    help_message = """
  ```
  \nFor command list -----> $helpme

  \nFor weather reports --> $weather <city name>
                        $weather <city name/country>
                        $weather <country>

  \nFor jokes ------------> $joke
  \nFor number facts -----> $fact <number>

  \nFor date facts -------> $datefact <month/date>
                        eg: $datefact 3/11

  \nFor math facts -------> $mathfact <number>

  \nFor pinging the bot --> $ping
  ```
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
    load_dotenv()
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid='
        + os.environ['API'] + '&units=metric')
    json_data = json.loads(response.text)
    weather = json_data

    #city name
    city = weather['name']
    city_mod = "Place:               {}".format(city)

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

  *Add 5:30 for IST*
  ```
  '''

    await ctx.channel.send(main)


@client.command()
async def fact(ctx, *, number):
    fact_response = requests.get(f"http://numbersapi.com/{number}")
    fact_data = fact_response.text
    fact_mod = (f"```{fact_data}```")
    await ctx.channel.send(fact_mod)


@client.command()
async def datefact(ctx, *, input_date):
    date_response = requests.get(f"http://numbersapi.com/{input_date}/date")
    date_fact = date_response.text
    date_mod = (f"```{date_fact}```")
    await ctx.channel.send(date_mod)


@client.command()
async def mathfact(ctx, *, input_math):
    math_response = requests.get(f"http://numbersapi.com/{input_math}/math")
    math_fact = math_response.text
    math_mod = (f"```{math_fact}```")
    await ctx.channel.send(math_mod)


@client.command()
async def joke(ctx):
    joke_response = requests.get(f"https://v2.jokeapi.dev/joke/Any?format=txt")
    joke = joke_response.text
    joke_mod = (f"```{joke}```")
    await ctx.channel.send(joke_mod)


@client.command()
async def imdb(ctx, *, input_movie):
    load_dotenv()
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    querystring = {"q": {input_movie}}
    headers = {
        "X-RapidAPI-Key": os.environ['imdb_API'],
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    response = requests.request("GET",
                                url,
                                headers=headers,
                                params=querystring)
    response2 = response.text
    await ctx.channel.send(response2)

load_dotenv()
client.run(os.getenv("TOKEN"))