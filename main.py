import discord
from dotenv.main import load_dotenv
import os
import requests
import json
from discord.ext import commands
from datetime import datetime
from dateutil import tz

# If intents related error:  pip3 install -U discord==1.7.3 && pip3 install -U discord.py==1.7.3
client = discord.Client()
client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('$helpme'))
    print("I am ready, logged in as {0.user}".format(client))


def help_weather():
    help_message = "https://i.imgur.com/aSqBAUU.png"
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

    icon = weather['weather'][0]['icon']
    iconurl = "http://openweathermap.org/img/w/" + icon + ".png"
    await ctx.channel.send(iconurl)

    #city name
    city = weather['name']
    city_mod = f"{city}"

    #country name
    country = weather['sys']['country']
    country_mod = f"{country}"

    #temperature
    temp = weather['main']['temp']
    temp_mod = f"{temp}"

    #min temperature
    temp_min = weather['main']['temp_min']
    temp_min_mod = f"{temp_min}"

    #max temperature
    temp_max = weather['main']['temp_max']
    temp_max_mod = f"{temp_max}"

    #feels like temperature
    temp_feels = weather['main']['feels_like']
    temp_feels_mod = f"{temp_feels}"

    #icon
    icon = weather['weather'][0]['icon']

    #description
    description = weather['weather'][0]['description']
    description_mod = f"{description}"

    #wind speed
    wind_speed = weather['wind']['speed']
    wind_speed_mod = F"{wind_speed}"

    #sunrise time
    sunrise_time = int(weather['sys']['sunrise'])
    ts = sunrise_time
    sunrise_utc = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')[:-3]
    sunrise_time_mod = f"{sunrise_utc}"

    #sunset time
    sunset_time = int(weather['sys']['sunset'])
    ts = sunset_time
    sunset_utc = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')[:-3]
    sunset_time_mod = f"{sunset_utc}"

    # lengthy description
    # len_description = weather['alerts'][0]['description']
    # len_description_mod = "Description:         {}".format(description)

    main = f'''
  >>> 
  **City:**\t{city_mod}
  **Country:**\t{country_mod}\n
  **Temperature:**\t{temp_mod} °C
  **Min Temperature:**\t{temp_min_mod} °C
  **Max Temperature:**\t{temp_max_mod} °C
  **Feels Like:**\t{temp_feels_mod} °C\n
  **Description:**\t{description_mod}
  **Wind Speed:**\t{wind_speed_mod} m/s\n
  **Sunrise Time:**\t{sunrise_time_mod}+5:30 IST
  **Sunset Time:**\t{sunset_time_mod}+5:30 IST
  '''

    await ctx.channel.send(main)


@client.command()
async def numfact(ctx, *, number):
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
    json_data = json.loads(response.text)
    response2 = json_data

    image = response2['d'][0]['i']['imageUrl']
    await ctx.channel.send(image)

    rank = response2['d'][0]['rank']
    rank_mod = f"{rank}"

    year = response2['d'][0]['y']
    year_mod = f"{year}"

    type = response2['d'][0]['qid']
    type_mode = f"{type}"

    main_cast = response2['d'][0]['s']
    main_case_mod = f"{main_cast}"
    
    main = f'''
    >>> 
    **Type:** {type_mode}
    **Rank:** {rank_mod}
    **Year:** {year_mod}
    **Cast:** {main_case_mod}
    '''
    await ctx.channel.send(main)

@client.command()
async def metahuman(ctx, *, input_name):
    load_dotenv()
    url = "https://superhero-search.p.rapidapi.com/api/"
    querystring = {"hero":{input_name}}
    headers = {
	    "X-RapidAPI-Key": os.environ['superhero_API'],
	    "X-RapidAPI-Host": "superhero-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    response2 = json_data
    image = response2['images']['lg']
    await ctx.channel.send(image)
    
    name = response2['name']
    name_mod = f"{name}"

    intelligence = response2['powerstats']['intelligence']
    intelligence_mod = f"{intelligence}"

    strength = response2['powerstats']['strength']
    strength_mod = f"{strength}"

    speed = response2['powerstats']['speed']
    speed_mod = f"{speed}"

    durability = response2['powerstats']['durability']
    durability_mod = f"{durability}"

    power = response2['powerstats']['power']
    power_mod = f"{power}"

    combat = response2['powerstats']['combat']
    combat_mod = f"{combat}"

    gender = response2['appearance']['gender']
    gender_mod = f"{gender}"

    race = response2['appearance']['race']
    race_mod = f"{race}"

    height = response2['appearance']['height'][0]
    height_mod = f"{height}"

    weight = response2['appearance']['weight'][1]
    weight_mod = f"{weight}"

    fullname = response2['biography']['fullName']
    fullname_mod = f"{fullname}"

    alias1 = response2['biography']['aliases'][0]
    alias1_mod = f"{alias1}"
    alias2 = response2['biography']['aliases'][1]
    alias2_mod = f"{alias2}"
    alias3 = response2['biography']['aliases'][2]
    alias3_mod = f"{alias3}"

    birthPlace = response2['biography']['placeOfBirth']
    birthPlace_mod = f"{birthPlace}"

    publisher = response2['biography']['publisher']
    publisher_mod = f"{publisher}"

    alignment = response2['biography']['alignment']
    alignment_mod = f"{alignment}"

    occupation = response2['work']['occupation']
    occupation_mod = f"{occupation}"

    groupAffiliation = response2['connections']['groupAffiliation']
    groupAffiliation_mod = f"{groupAffiliation}"

    relatives = response2['connections']['relatives']
    relatives_mod = f"{relatives}"

    main = f'''
    >>> 
    **__Name:__**\t{name_mod}\n
    **__Powerstats:__**
    \t*Intelligence:*\t{intelligence_mod}
    \t*Strength:*\t{strength_mod}
    \t*Speed:*\t{speed_mod}
    \t*Durability:*\t{durability_mod}
    \t*Power:*\t{power_mod}
    \t*Combat:*\t{combat_mod}\n
    **__Appearance:__**
    \t*Gender:*\t{gender_mod}
    \t*Race:*\t{race_mod}
    \t*Height:*\t{height_mod}
    \t*Weight:*\t{weight_mod}\n
    **__Biography:__**
    \t*Full Name:*\t{fullname_mod}
    \t*Aliases:*\t{alias1_mod}, {alias2_mod}, {alias3_mod}
    \t*Place of Birth:*\t{birthPlace_mod}
    \t*Publisher:*\t{publisher_mod}
    \t*Alignment:*\t{alignment_mod}\n
    **__Occupation:__**\t{occupation_mod}\n
    **__Connections:__**
    \t*Group Affiliation:*\t{groupAffiliation}\n
    \t*Relatives:*\t{relatives_mod}
        
    '''
    await ctx.channel.send(main)


load_dotenv()
client.run(os.getenv("TOKEN"))