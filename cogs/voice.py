import discord
from discord import app_commands
from discord.ext import commands
import embeds

class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            embed = embeds.bad_embed("No boss in voice room. Bob look, no find.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client

        if voice_client and voice_client.channel == channel:
            embed = embeds.good_embed(f"Boss, Bob no move. Here now. Already in <#{channel.id}>.")
            await interaction.response.send_message(embed=embed)
        elif interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
            await interaction.guild.voice_client.move_to(channel)
            embed = embeds.good_embed(f"Bob leave old place. Now in <#{channel.id}>.")
            await interaction.response.send_message(embed=embed)
        else:
            await channel.connect()
            embed = embeds.good_embed(f"Bob join! Now in <#{channel.id}>, boss.")
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave",  description="Leave voice channel that I'm currently sitting in")
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            embed = embeds.bad_embed("Boss, look! Bob no join voice yet.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        channel_id = voice_client.channel.id
        await voice_client.disconnect()
        embed = embeds.good_embed(f"Bob leave boss voice place <#{channel_id}>.")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))
