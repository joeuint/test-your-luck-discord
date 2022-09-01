# Import necessary libraries
import discord
from discord import commands
import dotenv
import pytz
import random
import os
from uuid import uuid4
import datetime

tz = pytz.timezone('America/Toronto')

def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

# Define the max value (higher the less likely to win)
MAX = 4096
WIN = 69

# Close Hours
CLOSE = datetime.time(23, 0)
OPEN = datetime.time(10, 0)

# Load the .env file and extract the token
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

# Set intents
intents = discord.Intents.default()

# Define the client
bot = discord.Bot(intents=intents, debug_guilds=["1011668530778865674"])


@bot.event
async def on_ready():
    print("I'm logged in!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with your mom"))

@bot.slash_command(name="test-luck", description="Test your luck!")
async def test_luck(ctx):
    if not ctx.channel.id == 1011668742930972714:
        await ctx.respond("Wrong channel buddy", ephemeral=True)
        return

    if not time_in_range(OPEN, CLOSE, datetime.datetime.now(tz).time()):
        await ctx.respond(f"Test Your Luck is closed! It opens at {OPEN.strftime('%I:%M %p')} and closes at {CLOSE.strftime('%I:%M %p')}", ephemeral=True)
        return

    # Generate a random number
    rand_num = random.randint(0, MAX)

    entry_number = None

    entry_uuid = uuid4()

    lose_color = 0xff0000
    win_color = 0x00FF00

    # Read the uses text file
    with open ("uses.txt", "r+") as myfile:
        uses = myfile.read()
        entry_number = int(uses) + 1
        myfile.seek(0)
        myfile.truncate()
        myfile.write(str(entry_number))
        myfile.close()


    # Check if the number is equal to the winning value
    won = False
    if rand_num == WIN:
        won = True
        print("WIN")
    else:
        print("Loser")

    # Generate a cool embed
    description = "Congrats you won contact <@457910942114512930> to claim!" if won else "You lost lol"

    embed=discord.Embed(title=f"Entry #{entry_number}", description=description, color=win_color if won else lose_color)
    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar)
    embed.set_footer(text=f"Your Value is {rand_num}! Contact owner to report bugs. UUID: {entry_uuid}")

    await ctx.respond(embed=embed)

    if won:
        await ctx.send("Channel Locked!")
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

@bot.slash_command(name="uses", description="The amount of times test-luck was used")
async def uses(ctx):
    with open ("uses.txt", "r") as myfile:
        await ctx.respond(myfile.read())

# Run the bot using the token
bot.run(TOKEN)