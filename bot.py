import os, discord, requests, feedparser
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime, timezone

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The most recent post so that we can filter out old posts
        self.most_recent_post = "0"

    async def setup_hook(self) -> None:
        self.get_manga_rss_feed.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(hours=1) 
    async def get_manga_rss_feed(self):
        channel = self.get_channel(1109310622346264577)
        MAX_MESSAGE_LENGTH = 2000

        # Get RSS Feed
        queries = [
            "flair%3A%22DISC%22&",
            f"&before={self.most_recent_post}"
            "restrict_sr=on",
            "sort=new",
            "t=all"
        ]
        feed = feedparser.parse('https://www.reddit.com/r/manga/search.rss?q=flair%3A%22DISC%22&restrict_sr=on&sort=new&t=all')
        # feed = feedparser.parse(r"E:\Programming\\r_manga_bot\\test2.xml")
        message = ""
        self.most_recent_post = feed['entries'][0]['id']
        for entry in feed['entries']:
            if len(message) + len(entry['title']) + len(entry['link']) > MAX_MESSAGE_LENGTH:
                await channel.send(message, suppress_embeds=True)
                message = ""
            message += f"{entry['title']}: {entry['link']})\n"

        await channel.send(message, suppress_embeds=True)

    @get_manga_rss_feed.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)