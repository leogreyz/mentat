import discord
from discord.ext import commands
import re
import os

DISCORD_BOT_KEY = os.environ.get('DISCORD_BOT_KEY')
GUILD_ID = '895004152986480751'

class TreacherCardServiceClient(discord.Client):
    tc_name_regex = re.compile(r'^Name: (.+)$', re.M)
    tc_in_message_regex = re.compile(r'\<:treachery:\d+\>(.{1,30})\<:treachery:\d+\>', re.M)
    tc = {}
    async def on_ready(self):
        print('Started')
        guild = await self.fetch_guild(GUILD_ID)
        channels = await guild.fetch_channels()
        text_channels = [
            channel for channel in channels
            if type(channel) is discord.channel.TextChannel
        ]

        tc_channel = [channel for channel in text_channels if channel.name == 'treachery-cards'][0]
        async for tc_message in tc_channel.history(limit=400):
            tc_name = self.tc_name_regex.search(tc_message.content).group(1).lower().strip()
            tc_image_url = tc_message.attachments[0].url

            self.tc[tc_name] = tc_image_url

    async def on_message(self, message):
        results = self.tc_in_message_regex.search(message.content)

        if results:
            tc_name = results.group(1).lower().strip()
            tc_url = self.tc.get(tc_name)
            if tc_url:
                await message.channel.send(tc_url)

client = TreacherCardServiceClient()
client.run(DISCORD_BOT_KEY)