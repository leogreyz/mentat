from dis import disco
import discord
from discord.ext import commands
import re
import os
from mentat.game.discord_game import DiscordGame

DISCORD_BOT_KEY = os.environ.get('DISCORD_BOT_KEY')
GUILD_ID = '895004152986480751'

game_category = "DUNE DISCORD BOT"

def command_channel(ctx):
    return ctx.channel.name == 'commands' and ctx.channel.category.name == game_category

class GameTrackerServiceClient(discord.Client):
    async def on_ready(self):
        print('Started')
        guild = await self.fetch_guild(GUILD_ID)
        channels = await guild.fetch_channels()
        category_channels = [
            channel for channel in channels
            if type(channel) is discord.channel.CategoryChannel
        ]
        text_channels = [
            channel for channel in channels
            if type(channel) is discord.channel.TextChannel
        ]

        self.game_category = [category for category in category_channels if category.name == game_category][0]

        self.game_channels = [channel for channel in text_channels if channel.category_id == self.game_category.id]


# client = GameTrackerServiceClient()
# client.run(DISCORD_BOT_KEY)
discord_game = DiscordGame(GUILD_ID, game_category)

bot = commands.Bot(command_prefix="$")

@bot.command()
async def create_faction(ctx, id, name, emoji, info_channel):
    if command_channel(ctx):
        await discord_game.register_faction(id, name, emoji, info_channel)
        await discord_game.write_state()
        await ctx.channel.send(f"""
Faction added with:
    ID: {id}
    Name: {name}
    Emoji: {emoji}
    Info Channel: #{info_channel}
        """)

@bot.command()
async def create_game_resource(ctx, name, starting_value):
    if command_channel(ctx):
        discord_game.game_state.register_game_resource(name, starting_value)
        await discord_game.write_state()
        await ctx.channel.send(f"""
Game Resource added with:
    Name: {name}
    Starting Value: {starting_value}
        """)

@bot.command()
async def create_faction_resource(ctx, faction_id, name, starting_value):
    if command_channel(ctx):
        discord_game.game_state.register_faction_resource(faction_id, name, starting_value)
        await discord_game.write_state()
        await ctx.channel.send(f"""
Faction Resource added with:
    Faction ID: {faction_id}
    Name: {name}
    Starting Value: {starting_value}
        """)

@bot.command()
async def delete_game_state(ctx):
    if command_channel(ctx):
        discord_game.delete_game_state()
        await discord_game.write_state()
        await ctx.channel.send('Game State Deleted')    

@bot.command()
async def undo(ctx):
    if command_channel(ctx):
        await discord_game.undo_game_state()
        await ctx.channel.send('Last action undone')

@bot.event
async def on_ready():
    print('Ready!')
    await discord_game.initialize(bot)
bot.run(DISCORD_BOT_KEY)

