import logging

import discord
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

class Based_On_What():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = [SERIOUS_CHANNELS]
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.basedonwhat]
        self.on_ready = []

    async def basedonwhat(self, message: discord.Message):

        if 'based' not in message.content.lower():
            return False
        
        LOGGER.debug('ASKING "BASED ON WHAT?"')
        await message.channel.send("Based on what?")

        
