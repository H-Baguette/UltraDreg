import logging
import random

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


        basedInMessage = False
        punctuation = '\~!@#$%^&\*()-=[]\\;\',./\_+{}|:"?'
        tokens = message.content.split(' ')

        for index, token in enumerate(tokens):
            word = token
            try:
                while word[0] in punctuation:
                    word = word[1:]
                while word[-1] in punctuation:
                    word = word[:-1]

            except IndexError:
                continue

            if word.lower() == 'based':
                basedInMessage = True
                continue

        if basedInMessage == False:
            return False

        if random.randint(1,10000) <= 10:
            LOGGER.debug('ASKING "BASED ON WHAT?"')
            if random.randint(1,10000) == 1:
                await message.channel.send("βάση? με βάση τι?")
            else:
                await message.channel.send("Based on what?")

        
