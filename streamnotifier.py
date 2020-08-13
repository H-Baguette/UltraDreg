import logging
import random

import discord
from discord.ext import commands
from discord.utils import get

from resources import COMMAND_PREFIX
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

# initialize whitelist
streamWhitelist = [
    'twitch.tv/hbaguette',
    'twitch.tv/noamfan95',
    'twitch.tv/thebadmrfrosty',
    'twitch.tv/cliffracerfan95',
    'twitch.tv/samourai1468',
    'twitch.tv/sock_online',
    'twitch.tv/peter_plays',
    'twitch.tv/ronaldgaming',
    'twitch.tv/aldomatica'
    ]


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


        if any(stroomer in message.content.lower() for stroomer in streamWhitelist) == False:
            return False

        LOGGER.debug('NOTIFYING OF STREAM')
        roleID=738518308113874994
        await message.channel.send("<@&"+str(roleID)+"> Stream time, friends <:soylose:713029487222194227>")
