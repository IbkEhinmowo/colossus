import os
import discord
import ssl
import certifi
import asyncio
from dotenv import load_dotenv
from parsers.marketplace import MarketplaceParser
from models.listing import IncomingListing
from app import app, parsed_listings_queue
import uvicorn

# SSL fixes for macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()
# Override SSL context globally
ssl._create_default_https_context = ssl._create_unverified_context
load_dotenv()



BOT_TOKEN = os.getenv("BOT_TOKEN")
reportChannelID: int = 1400330644562776064
newlistingChannelID: int = 1400945491776241716

# Initialize bot
bot = discord.Bot()
parser= MarketplaceParser()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(reportChannelID)
    if channel:
        await channel.send("Fatoom is ready to work")
        # Start FastAPI server in the background
        config = uvicorn.Config(app, host="127.0.0.1", port=8000)
        server = uvicorn.Server(config)
        bot.loop.create_task(server.serve())
        bot.loop.create_task(check_marketplace_queue())
        
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
            for listing in parsed_listings_queue[1:]:
                channel = bot.get_channel(newlistingChannelID)
                if channel:
                    embed = discord.Embed(
                        title="🏠 New Listing Alert!",
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
        await asyncio.sleep(10)
            
@bot.command()
async def hello(ctx):
    await ctx.send("Hiii! I'm Natasha")
    
    

    
 
if __name__ == "__main__":
    bot.run(BOT_TOKEN)