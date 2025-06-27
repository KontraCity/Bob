import discord
from discord import app_commands
from discord.ext import commands
from embeds import *
from player import Player
from youtube import Video

class VoiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = self.bot.logger
        self.players = {}

    def log_message(self, interaction: discord.Interaction, message: str) -> str:
        guild = interaction.guild.name if interaction.guild else "DM"
        user = interaction.user.name
        command = interaction.command.name
        options = interaction.data.get("options", [])

        if command == "play":
            url = options[0]["value"]
            return f"\"{guild}\" / \"{user}\": /{command} \"{url}\": {message}"
        return f"\"{guild}\" / \"{user}\": /{command}: {message}"

    async def join_voice(self, interaction: discord.Interaction, silent: bool = False) -> Player:
        if not interaction.user.voice or not interaction.user.voice.channel:
            self.logger.info(self.log_message(interaction, "User not in voice channel"))
            await interaction.response.send_message(embed=bad_embed("Join a voice channel first"), ephemeral=True)
            return None
            
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.channel == channel:
            embed = good_embed(f"Already in <#{channel.id}>")
            message = self.log_message(interaction, f"Already in #{channel.name}")
        elif interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
            embed = good_embed(f"Moved to <#{channel.id}>")
            message = self.log_message(interaction, f"Moved to #{channel.name}")
        else:
            voice_client = await channel.connect()
            self.players[voice_client.guild.id] = Player(voice_client)
            embed = good_embed(f"Joined <#{channel.id}>")
            message = self.log_message(interaction, f"Joined #{channel.name}")

        if not silent:
            self.logger.info(message)
            await interaction.response.send_message(embed=embed)
        return self.players[voice_client.guild.id]

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        await self.join_voice(interaction)

    @app_commands.command(name="leave",  description="Leave voice channel that I'm currently sitting at")
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_connected():
            self.logger.info(self.log_message(interaction, "User not in voice channel"))
            await interaction.response.send_message(embed=bad_embed("Not in voice channel"), ephemeral=True)
            return
        
        channel_id, channel_name = voice_client.channel.id, voice_client.channel.name
        del self.players[voice_client.guild.id]
        await voice_client.disconnect()

        self.logger.info(self.log_message(interaction, f"Left #{channel_name}"))
        await interaction.response.send_message(embed=good_embed(f"Left <#{channel_id}>"))

    @app_commands.command(name="play", description="Play YouTube video")
    @app_commands.describe(url="Name or URL of the video that you want me to play")
    async def play(self, interaction: discord.Interaction, url: str):
        is_video_url = Video.extract_id(url) is not None
        player = await self.join_voice(interaction, silent=True)
        if not player:
            return

        await interaction.response.defer()
        video = Video.from_url(url) if is_video_url else Video.from_query(url)
        player.add_item(video)
        self.logger.info(self.log_message(interaction, f"Added \"{video.title}\""))
        await interaction.followup.send(embed=video_embed(video))

    @app_commands.command(name="skip", description="Skip playing video")
    async def skip(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            self.logger.info(self.log_message(interaction, "User not in voice channel"))
            await interaction.response.send_message(embed=bad_embed("Not in voice channel"), ephemeral=True)
            return
        player = self.players[interaction.guild.id]

        if not player.voice_client.is_playing():
            self.logger.info(self.log_message(interaction, "Bot is not playing"))
            await interaction.response.send_message(embed=bad_embed("Not playing"), ephemeral=True)
            return

        player.skip_video()
        self.logger.info(self.log_message(interaction, "Video skipped"))
        await interaction.response.send_message(embed=good_embed("Video skipped"))

    @app_commands.command(name="stop", description="Stop playing video and clear queue")
    async def stop(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            self.logger.info(self.log_message(interaction, "User not in voice channel"))
            await interaction.response.send_message(embed=bad_embed("Not in a voice channel"), ephemeral=True)
            return
        player = self.players[interaction.guild.id]

        if not player.voice_client.is_playing():
            self.logger.info(self.log_message(interaction, "Bot is not playing"))
            await interaction.response.send_message(embed=bad_embed("Not playing"), ephemeral=True)
            return

        player.stop()
        self.logger.info(self.log_message(interaction, "Playback stopped"))
        await interaction.response.send_message(embed=good_embed("Playback stopped"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        
        voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if not voice_client or not voice_client.channel:
            return

        if before.channel == voice_client.channel:
            remaining_humans = [member for member in before.channel.members if not member.bot]
            if len(remaining_humans) == 0:
                self.logger.info(f"\"{member.guild.name}\": Everybody left the voice channel, leaving")
                del self.players[voice_client.guild.id]
                await voice_client.disconnect()

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceCog(bot))
