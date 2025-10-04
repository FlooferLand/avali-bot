from discord import Interaction, InteractionCallbackResponse

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
