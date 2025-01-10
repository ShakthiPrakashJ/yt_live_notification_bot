import os
import discord
from discord.ext import commands, tasks
import requests
import asyncio

# Replace these with your own bot token and API key
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
YOUTUBE_API_KEY = "AIzaSyBktLhl2YLBe1Gc530AhfXAy_8sjDxoep4"
CHANNEL_ID = "UCL0PiZPhY-KNp0EhK9OmjEg"  # Replace with the YouTube channel ID
DISCORD_CHANNEL_ID = 855284222704877578  # Replace with your Discord channel ID

# Create bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Store the last video ID to prevent duplicate notifications
last_video_id = None

@tasks.loop(minutes=1)
async def check_youtube():
    global last_video_id
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&type=video&eventType=live&key={YOUTUBE_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])

        if items:
            video_id = items[0]["id"]["videoId"]

            if video_id != last_video_id:
                last_video_id = video_id
                video_title = items[0]["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                # Send a message to the Discord channel
                channel = bot.get_channel(DISCORD_CHANNEL_ID)
                if channel:
                    await channel.send(f"🔴  **Two9 Gaming is on live  📢\n{video_title}\nDo watch it here: {video_url}\n\nDo like ❤️, share 🔗 and Subscribe 🙏 Guys,\nThank you!!\n@everyone**")
    else:
        print(f"Failed to fetch YouTube data: {response.status_code}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_youtube.start()

bot.run(os.getenv("DISCORD_BOT_TOKEN"))

