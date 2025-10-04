import os
from asyncio import sleep

import discord
from discord import Intents, ActivityType
from discord.ext import commands
from discord.ext.commands import Bot, CommandError
from discord.utils import get

from storage import VERIFIED_ROLE
from utils import command_reply, log_inter

ERROR_DELETE_TIME = 2.0  # Seconds

intents = Intents.default()
bot = Bot(
    intents=intents,
    activity=discord.Activity(type=ActivityType.watching, name="twitch.tv/StorytellerWMD"),
    command_prefix="s$"
)

# Commands
@bot.tree.command(name="verify", description="Adds the verified role to someone, or removes it if they already have it.")
@commands.has_permissions(manage_roles=True)
async def verify(interaction: discord.Interaction, member: discord.Member):
    verified_role = member.guild.get_role(VERIFIED_ROLE)
    if verified_role is None:
        await command_reply(interaction, f"Unable to find verified role (`id={VERIFIED_ROLE}`)", delete_in=ERROR_DELETE_TIME)
        return

    try:
        if member.get_role(VERIFIED_ROLE) is None:
            await member.add_roles(verified_role)
            await command_reply(interaction, f"Verified `@{member.name}`!", ephemeral=False)
            await log_inter(f"{interaction.user.name} verified `@{member.name}`!")
        else:
            await member.remove_roles(verified_role)
            await command_reply(interaction, f"Unverified `@{member.name}`!", ephemeral=True)
            await log_inter(f"{interaction.user.name} unverified `@{member.name}`!")
    except CommandError as err:
        await command_reply(
            interaction,
            "Failed to add role. Possible permission error? _(Make sure the bot is higher in the permissions list than the verified role)_",
            delete_in=ERROR_DELETE_TIME
        )

# Events
@bot.event
async def on_ready():
    print(f"Logged in as `{bot.user}`!")

    # Syncing
    await bot.tree.sync()

# Running the bot
bot.run(os.getenv("DISCORD_TOKEN"), log_level=0)
