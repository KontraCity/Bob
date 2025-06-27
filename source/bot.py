import glob, logging
from discord import Intents
from discord.ext import commands
from config import Config
from utility import configureLogger

class Bot(commands.Bot):
    def __init__(self, config: Config):
        configureLogger(logging.getLogger("discord"))
        intents = Intents.default()
        intents.voice_states = True
        super(Bot, self).__init__(command_prefix="!", intents=intents)
        super(Bot, self).run(config.token, log_handler=None)

    async def setup_hook(self) -> None:
        await self.load_extension("voice_cog")
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user}")
