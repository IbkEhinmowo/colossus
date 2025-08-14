import os
import asyncio
import uvicorn
import discord
from dotenv import load_dotenv
from discord.ext import commands
from parsers.marketplace import MarketplaceParser
from app import app, parsed_listings_queue

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
reportChannelID: int = int(os.getenv("DISCORD_REPORT_CHANNEL_ID"))
newlistingChannelID: int = int(os.getenv("DISCORD_NEW_LISTINGS_CHANNEL_ID"))

# Initialize bot (discord.py)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
parser = MarketplaceParser()

async def start_uvicorn():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send("Fatoom is ready to work")
        asyncio.create_task(start_uvicorn())
        asyncio.create_task(check_marketplace_queue())
    else:
        print(f"Could not find channel with ID {reportChannelID}")
async def check_marketplace_queue():
    """This function will run forever in the background"""
    while True:  # This makes it run forever
        # Check if there are items in the queue
        if parsed_listings_queue:
            print(f"Found {len(parsed_listings_queue)} listings!")
            # Do something with the listings here
            #Process each listing
            for listing in parsed_listings_queue:
                channel = bot.get_channel(newlistingChannelID)
                if channel:
                    embed = discord.Embed(
                        title=f"🏠 New find: {listing.title}",
                        color=0x00ff00,
                        url=listing.link
                    )
                    embed.add_field(name="📝 Title", value=listing.title, inline=False)
                    embed.add_field(name="💰 Price", value=listing.price, inline=True)
                    embed.add_field(name="📍 Location", value=listing.location, inline=True)

                    await channel.send(embed=embed)           
            # Clear the queue
            parsed_listings_queue.clear()
            
        else:
            print("No new listings")
        
        # Wait 15 seconds before checking again
        await asyncio.sleep(25)
        
        
        
        
##### BOT COMMANDS #####
            
@bot.command()
async def hello(ctx):
    await ctx.send("Hiii! I'm Natasha")
    
    
@bot.command()
async def clearchat(ctx):
    """Clears the report channel."""
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.purge(limit=1000)
 
@bot.command()
async def DBpurge(ctx):
    """Clears the database."""
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send("Purging database...")
        
        # Here you would add your database purge logic
        # For example, using SQLAlchemy or raw SQL queries
        await channel.send("Database purged successfully!")
    else:
        print(f"Could not find channel with ID {reportChannelID}")
 
 
 
 
 
 
 
 
if __name__ == "__main__":
    bot.run(BOT_TOKEN)