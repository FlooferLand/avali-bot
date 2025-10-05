import discord
from discord import Interaction, InteractionCallbackResponse
from discord.ext.commands import CommandError

async def command_reply(interaction: Interaction, content: str, ephemeral: bool = True, delete_in: float | None = None) -> InteractionCallbackResponse:
    response: InteractionCallbackResponse = await interaction.response.send_message(content, ephemeral=ephemeral)
    if delete_in is not None:
        try:
            message = await interaction.user.fetch_message(response.message_id)
            await message.delete(delay=delete_in)
        except Exception as _:
            pass
    return response

## TODO: Make this log to a log channel
async def log_inter(text: str):
    print(text)

class AddRoleResult:
    ROLE_ADDED = 0
    ROLE_REMOVED = 1

class AddRoleError(Exception):
    pass

async def add_role_to_user(member: discord.Member, role_id: int) -> int:
    role = member.guild.get_role(role_id)
    if role is None:
        raise AddRoleError(f"Unable to find the media role (`id={role_id}`)")

    try:
        if member.get_role(role_id) is None:
            await member.add_roles(role)
            return AddRoleResult.ROLE_ADDED
        else:
            await member.remove_roles(role)
            return AddRoleResult.ROLE_REMOVED
    except CommandError as err:
        raise "Failed to add role. Possible permission error? _(Make sure the bot is higher in the permissions list than the verified role)_"