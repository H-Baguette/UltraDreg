from discord.ext import commands
from discord.utils import get
import discord
import messages
from roles import EVERYONE
from channels import SODOM_MAIN, DEV_MAIN

JOIN_SUCCESS = [
    'Whaddup, foo!',
    'Hmm. Better post good, bitch!',
    'Who let this cringe bitch in here?!',
]


class Join():
    ''' This Cog listens for a new member joining the channel and posts a message.'''

    def __init__(self, bot):
        self.bot = bot
        self.channels_whitelist = [SODOM_MAIN,DEV_MAIN]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = []
        self.on_ready = []

    async def on_member_join(self, member: discord.Member):
        '''On join, post a message'''
        serverChannel = [str(guild_channel) for guild_channel in message.guild_channel]
        if SODOM_MAIN == message.guild_channel:
            joinChannel = SODOM_MAIN
        elif DEV_MAIN == message.guild_channel:
            joinChannel = DEV_MAIN
        main_channel = get(
            message.guild.text_channels, name=joinChannel)
        await messages.answer(joinchannel, message.author, JOIN_SUCCESS)

        return True
