import discord
from discord import app_commands
from discord.ext import commands
import embeds
from player import Player
from youtube import Video, Playlist, Search

class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}

    async def join_voice(self, interaction: discord.Interaction, silent: bool = False) -> Player:
        if not interaction.user.voice or not interaction.user.voice.channel:
            embed = embeds.bad_embed("No boss in voice room. Bob look, no find.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
            
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.channel == channel:
            embed = embeds.good_embed(f"Boss, Bob no move. Here now. Already in <#{channel.id}>.")
        elif interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
            embed = embeds.good_embed(f"Bob leave old place. Now in <#{channel.id}>.")
        else:
            voice_client = await channel.connect()
            self.players[voice_client.channel.id] = Player(voice_client)
            embed = embeds.good_embed(f"Bob join! Now in <#{channel.id}>, boss.")
            
        if not silent:
            await interaction.response.send_message(embed=embed)
        return self.players[voice_client.channel.id]

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        await self.join_voice(interaction)

    @app_commands.command(name="leave",  description="Leave voice channel that I'm currently sitting at")
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            embed = embeds.bad_embed("Boss, look! Bob no join voice yet.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        channel_id = voice_client.channel.id
        del self.players[channel_id]

        await voice_client.disconnect()
        embed = embeds.good_embed(f"Bob leave boss voice place <#{channel_id}>.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="play", description="Play YouTube video or playlist")
    async def play(self, interaction: discord.Interaction, url: str):
        is_video = Video.extract_id(url) is not None
        is_playlist = Playlist.extract_id(url) is not None
        if is_video and is_playlist:
            embed = embeds.bad_embed(f"Ambiguous, boss.")
            await interaction.response.send_message(embed=embed)
            return

        if is_video:
            player = await self.join_voice(interaction, silent=True)
            video = Video.from_url(url)
            player.add_item(video)
            embed = embeds.video_embed(video)
            await interaction.response.send_message(embed=embed)

        embed = embeds.problem_embed("Sorry, boss. I can't search now.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="skip", description="Skip playing video")
    async def skip(self, interaction: discord.Interaction):
        if interaction.guild.voice_client.channel.id not in self.players:
            embed = embeds.bad_embed("Boss, I'm not even in a voice channel")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        player = self.players[interaction.guild.voice_client.channel.id]

        if not player.voice_client.is_playing():
            embed = embeds.bad_embed("Boss, I'm not playing anything")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player.skip_video()
        embed = embeds.good_embed("Boss, video is skipped")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="stop", description="Stop playing video and clear queue")
    async def stop(self, interaction: discord.Interaction):
        if interaction.guild.voice_client.channel.id not in self.players:
            embed = embeds.bad_embed("Boss, I'm not even in a voice channel")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        player = self.players[interaction.guild.voice_client.channel.id]

        if not player.voice_client.is_playing():
            embed = embeds.bad_embed("Boss, I'm not playing anything")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        player.stop()
        embed = embeds.good_embed("Boss, playback is stopped")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))
