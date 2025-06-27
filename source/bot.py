import logging
from discord import Intents
from discord.ext import commands
from config import Config
import utility

class Bot(commands.Bot):
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        utility.configureLogger(self.logger)
        utility.configureLogger(logging.getLogger("discord"))
        intents = Intents.default()
        intents.voice_states = True
        intents.members = True
        intents.message_content = True
        super(Bot, self).__init__(command_prefix="!", intents=intents)
        super(Bot, self).run(config.token, log_handler=None)

    async def setup_hook(self) -> None:
        await self.load_extension("voice_cog")
        await self.tree.sync()
        self.logger.info("Extentions loaded, tree synced")

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user}")
