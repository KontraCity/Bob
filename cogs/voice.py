from discord import app_commands
from discord.ext import commands

class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction):
        await interaction.response.send_message("Join")

    @app_commands.command(name="leave",  description="Leave voice channel that I'm currently sitting in")
    async def leave(self, interaction):
        await interaction.response.send_message("Leave")

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))
