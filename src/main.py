import os

import discord
from discord import Intents, ActivityType
from discord.ext import commands
from discord.ext.commands import Bot

from storage import MEDIA_ROLE
from utils import add_role_to_user, AddRoleError, AddRoleResult
from storage import VERIFIED_ROLE
from utils import command_reply, log_inter

ERROR_DELETE_TIME = 2.0  # Seconds

intents = Intents.default()
intents.members = True
intents.message_content = True
bot = Bot(
    intents=intents,
    activity=discord.Activity(type=ActivityType.watching, name="twitch.tv/StorytellerWMD"),
    command_prefix="s$"
)

# Commands
@bot.tree.command(name="verify", description="Adds the verified role to someone, or removes it if they already have it.")
@commands.has_permissions(manage_roles=True)
async def verify(interaction: discord.Interaction, member: discord.Member, reason: str | None):
    try:
        result = await add_role_to_user(member, VERIFIED_ROLE)
        reason_insert: str = ""
        if reason is not None: reason_insert = f" for reason ||{reason.replace("||", "\\|\\|")}||"
        match result:
            case AddRoleResult.ROLE_ADDED:
                await command_reply(interaction, f"Verified `@{member.name}`{reason_insert}!", ephemeral=False)
                await log_inter(f"{interaction.user.name} verified `@{member.name}`{reason_insert}!")
            case AddRoleResult.ROLE_REMOVED:
                await command_reply(interaction, f"Unverified `@{member.name}`{reason_insert}!", ephemeral=True)
                await log_inter(f"{interaction.user.name} unverified `@{member.name}`{reason_insert}!")
    except AddRoleError as err:
        await command_reply(interaction, str(err), delete_in=ERROR_DELETE_TIME)

@bot.tree.command(name="media", description="Adds the media role to someone, or removes it if they already have it.")
@commands.has_permissions(manage_roles=True)
async def media(interaction: discord.Interaction, member: discord.Member):
    try:
        result = await add_role_to_user(member, MEDIA_ROLE)
        match result:
            case AddRoleResult.ROLE_ADDED:
                await command_reply(interaction, f"`@{member.name}` now has media permissions!", ephemeral=True)
                await log_inter(f"{interaction.user.name} added 'media' to `@{member.name}`!")
            case AddRoleResult.ROLE_REMOVED:
                await command_reply(interaction, f"`@{member.name}` no longer has media permissions.", ephemeral=True)
                await log_inter(f"{interaction.user.name} removed 'media' from `@{member.name}`!")
    except AddRoleError as err:
        await command_reply(interaction, str(err), delete_in=ERROR_DELETE_TIME)

@bot.tree.command(name="view_unverified", description="See all the unverified users.")
@commands.has_permissions(manage_roles=True)
async def view_unverified(interaction: discord.Interaction):
    unverified: list[str] = []
    async for member in interaction.guild.fetch_members():
        if member.get_role(VERIFIED_ROLE) is None \
                and not member.bot \
                and not member.guild_permissions.manage_roles:
            unverified.append(f"- '{member.display_name}' `(@{member.name})`")

    if len(unverified) > 0:
        out: str = f"### Unverified:\n{"\n".join(unverified)}"
        await command_reply(interaction, out)
    else:
        out: str = f"All users have already been verified!"
        await command_reply(interaction, out)

# Events
@bot.event
async def on_ready():
    print(f"Logged in as `{bot.user}`!")

    # Syncing
    await bot.tree.sync()

# Running the bot
TOKEN: str | None = os.getenv("DISCORD_TOKEN")
if TOKEN is not None:
    bot.run(TOKEN, log_level=0)
else:
    print("DISCORD_TOKEN was not set")
