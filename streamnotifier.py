import logging
import random

import discord
from discord.ext import commands
from discord.utils import get

from resources import COMMAND_PREFIX
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

class Stream_Notify():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = [SERIOUS_CHANNELS]
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.streamnotify]
        self.on_ready = []

    async def streamnotify(self, message: discord.Message):

        if "https://twitch.tv/" not in message.content.lower() and "https://www.twitch.tv/" not in message.content.lower():
            return False

        LOGGER.debug('NOTIFYING OF STREAM')
        roleID=738518308113874994
        await message.channel.send("<@&"+str(roleID)+"> Stream time, friends <:soylose:713029487222194227>")
