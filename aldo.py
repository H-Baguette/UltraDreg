import logging
import random

import discord
from discord.ext import commands
from discord.utils import get

from resources import COMMAND_PREFIX
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE



#class Post_Aldo():
#
#    def __init__(self,bot):
#        self.bot = bot
#        self.channels_whitelist = [EVERYWHERE]
#        self.channels_blacklist = [SERIOUS_CHANNELS]
#        self.roles_whitelist = [EVERYONE]
#        self.roles_blacklist = []
#        self.on_message = [self.aldopost]
#        self.on_ready = []
#        self.help_content = {'name': 'aldo',
#                             'value': 'Summon a rather based fellow.'}

@commands.command(name='aldo',help='Summon a very handsome gentleman.')
async def aldopost(ctx):
    LOGGER = logging.getLogger('dreg')
        #if not message.content.lower().startswith(COMMAND_PREFIX + 'aldo'):
        #    return False

    LOGGER.debug('ALDOPOSTING')

    aldoposts = ['https://cdn.discordapp.com/attachments/723754451948798054/723789373958651914/image0.jpg',
                 'https://cdn.discordapp.com/attachments/337294427859058694/723780578435923988/image0.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792582253215785/image0.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792583272300574/image2.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792583687405578/image3.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792584564277319/image4.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792585986015242/image5.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792587336450119/image6.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723792587743428618/image7.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793072785326090/image0.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793073057955881/image1.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793073334648892/image2.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793073682907136/image3.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793074018451496/image4.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793074316115988/image5.jpg',
                 'https://cdn.discordapp.com/attachments/723754451948798054/723793074681151578/image6.jpg'
                 ]

    await ctx.send(random.choice(aldoposts))
