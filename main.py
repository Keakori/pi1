import discord
from discord.ext import commands
import requests
import random

with open("tokendbot.txt", "r") as tf:
    TOKEN_LIST = tf.readlines()
TOKEN = ''.join(map(str.strip, TOKEN_LIST))

Bot = commands.Bot(command_prefix="!!")

WEATHER_API_KEY = "dc972cf9-8a9d-49ca-acca-bdf6f98dc450"
headers={"X-Yandex-API-Key" : WEATHER_API_KEY}

def weather_response(plase):
    #53.213253, 50.239387
    coords= ("50.239387", "53.213253")
    weather_api_server = "https://api.weather.yandex.ru/v1/forecast?"
    weather_param = {
        "lon" : float(coords[0]),
        "lat" : float(coords[1]),
        "lang": "ru_RU"
    }
    response =requests.get(weather_api_server, weather_param, headers={"X-Yandex-API-Key" : WEATHER_API_KEY})
    return response.json()

def current_weather(response):
    city = response["info"]["tzinfo"]["name"].split('/')[-1]
    date = response["now_dt"][:10]
    offset = response["info"]["tzinfo"]["offset"] // 3600
    time = response["now_dt"][11:16]
    h, m = map(int, time.split(':'))
    time = f'{h + offset}:{m:02}'
    fact = response["fact"]
    temp = fact["temp"]
    condition = fact["condition"]
    wind_dir = fact["wind_dir"]
    wind_speed = fact["wind_speed"]
    pressure = fact["pressure_mm"]
    humidity = fact["humidity"]
    return f'Current weather in {city} today {date} at time {time}:\n' \
           f'Temperature: {temp},\n' \
           f'Pressure: {pressure} mm,\n' \
           f'Humidity: {humidity}%,\n' \
           f'{condition},\n' \
           f'Wind {wind_dir}, {wind_speed} m/s.'


@Bot.event
async def on_ready():
    print(f'{Bot.user} подключен к Discord!')
    for guild in Bot.guilds:
        print(
            f'{Bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )

@Bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send("Привет мой аналоговый друг!")


@Bot.command(name="current")
async def current(ctx):
    response = weather_response("Самара")
    message = current_weather(response)
    await ctx.send(message)



@Bot.command(name="randint")
async def my_randint(ctx, min_int, max_int):
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)

# @Bot.event
# async def on_message(message):
#     if message.author == Bot.user:
#         return
#     await message.channel.send(f"{message.author} : {message.content}")


Bot.run(TOKEN)

# client = discord.Client()
# @client.event
# async def on_ready():
#     print(f'{client.user} подключен к Discord!')
#     for guild in client.guilds:
#         print(
#             f'{client.user} подключились к чату:\n'
#             f'{guild.name}(id: {guild.id})'
#         )

# client.run(TOKEN)