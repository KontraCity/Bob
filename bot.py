import logging
import discord
from config import Config
from utility import configureLogger

class Bot(discord.Client):
    def __init__(self, config: Config):
        self.token = config.getToken()

        intents = discord.Intents.default()
        intents.message_content = True
        super(Bot, self).__init__(intents=intents)
        configureLogger(logging.getLogger("discord"))

    def run(self):
        super(Bot, self).run(self.token, log_handler=None)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
