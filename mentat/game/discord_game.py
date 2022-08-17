import discord
import json
from base64 import b64encode, b64decode

from .game_state import GameState

SERIAL_VERSION = 1

class DiscordGame:
    def __init__(self, guild_id, category_name):
        self.guild_id = guild_id
        self.category_name = category_name
        self.game_state = GameState()

    async def initialize(self, client):
        self.client = client
        self.guild = await client.fetch_guild(self.guild_id)
        await self.refresh()
        await self.read_state()

    async def refresh(self):
        channels = await self.guild.fetch_channels()
        self.category = [
            channel for channel in channels
            if type(channel) is discord.channel.CategoryChannel and channel.name == self.category_name
        ][0]
        text_channels = [
            channel for channel in channels
            if type(channel) is discord.channel.TextChannel
        ]
        self.game_channels = [channel for channel in text_channels if channel.category_id == self.category.id]
        self.command_channel = [channel for channel in self.game_channels if channel.name == 'commands'][0]
        self.data_channel = [channel for channel in self.game_channels if channel.name == 'bot-data'][0]

    async def find_channel_by_name(self, name):
        await self.refresh()
        results = [c for c in self.game_channels if c.name == name]

        return results[0] if len(results) == 1 else None

    async def register_faction(self, id, name, emoji, info_channel_name=None):
        if info_channel_name is None:
            info_channel_name = f"#{name.lower().replace(' ', '-')}-info"

        if await self.find_channel_by_name(info_channel_name) is None:
            raise

        self.game_state.register_faction(id, name, emoji, info_channel_name)

    def delete_game_state(self):
        self.game_state = GameState()

    async def undo_game_state(self):
        state_msgs = await self.data_channel.history(limit=2, oldest_first=False).flatten()
        if len(state_msgs) == 2:
            await self.data_channel.send(state_msgs[1].content)

        self.read_state()

    def serialize(self):
        return {
            'game_state': self.game_state.serialize(),
            'version': SERIAL_VERSION,
        }

    def deserialize(self, state, version):
        self.game_state = GameState()
        self.game_state.deserialize(state['game_state'], state['version'])

    async def write_state(self):
        state = json.dumps(self.serialize()).encode('utf-8')

        encoded_state = b64encode(state).decode('utf-8')
        await self.data_channel.send(encoded_state)

    async def read_state(self):
        state_msgs = await self.data_channel.history(limit=1, oldest_first=False).flatten()
        if len(state_msgs) == 1:
            state = json.loads(b64decode(state_msgs[0].content))
            self.deserialize(state, state['version'])
    