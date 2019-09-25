import requests
import discord
from discord.ext import commands


# function to get weather via openweathermap.org
def get_weather(city):
    parameters = {'q': str(city),
                  'APPID': 'eb40ee84dcd396fe4f4c745a79b01809'}
    try:
        response = requests.api.get(url='https://api.openweathermap.org/data/2.5/weather', params=parameters)
    except requests.exceptions.RequestException as e:
        return f"Error: Connection Error. Details:\n\n{e.args[0]}"
    else:
        if response.status_code == 200:
            cur_weather = response.json()
            return "\nWeather Report".upper() + \
                   "\n-----------------------" + \
                   f"\nCity: {cur_weather['name']}, {cur_weather['sys']['country']}" + \
                   f"\nTemperature: {'%.1f' % (cur_weather['main'].get('temp') - 273.15)}°C, " \
                   f"(Minimum: {'%.1f' % (cur_weather['main'].get('temp_min') - 273.15)}°C, " + \
                   f"Maximum: {'%.1f' % (cur_weather['main'].get('temp_max') - 273.15)}°C)" + \
                   f"\nHumidity: {cur_weather['main'].get('humidity')}%" + \
                   f"\n{cur_weather['weather'][0].get('description').capitalize()}." + \
                   "\n-----------------------" + \
                   "\nWeather service provided by openweathermap.org."
        else:
            errors = {400: "Error 400: Bad request.",
                      401: "Error 401: Auth token expired.",
                      404: "Error 404: Not found. Please check city name and/or country code.",
                      500: "Error 500: Internal server error.",
                      503: "Error 503: Weather service currently unavailable."}
            return errors[response.status_code]


# initialise a discord bot
token = open('token.txt', 'r').read()
bot = commands.Bot(command_prefix="!")
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"ID: {bot.user.id}")
    print('------')


@bot.command()
async def weather(ctx, *, city):
    await ctx.send(get_weather(city))


@bot.command()
async def info(ctx):
    bot_info = discord.Embed(title="Weatherman", description="A bot that shows the real-time weather of cities.")
    bot_info.add_field(name="Author", value="Deep5201")
    await ctx.send(embed=bot_info)


# remove default help command
@bot.command()
async def help(ctx):
    help_info = discord.Embed(title="Weatherman", description="List of commands:")
    help_info.add_field(name="!help", value="Show this message.")
    help_info.add_field(name="!info", value="Show info about the bot.")
    help_info.add_field(name="!weather <city>", value="Display real time weather of a specific city."
                                                      "For cities that share a common name, **ISO 3166 country codes** "
                                                      "can be specified.")
    await ctx.send(embed=help_info)


bot.run(token)
