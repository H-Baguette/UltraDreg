import logging

import discord
from discord.ext import commands
from discord.utils import get

from resources import COMMAND_PREFIX
from channels import EVERYWHERE
import roles

LOGGER = logging.getLogger('dreg')

class Toggle_Role():

    def __init__(self, bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [roles.EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.togglerole]
        self.on_ready = []
        self.help_content = {'name': 'togglerole',
                             'value': 'toggle a role for yourself'}

    async def togglerole(self, message: discord.Message):

        if not message.content.lower().startswith(COMMAND_PREFIX + 'togglerole '):
            return False

        LOGGER.debug('Message is valid for toggling a role')

        user = message.author
        try:
            role = message.content.split(' ')[1]
        except IndexError:
            await message.channel.send('Toggle *what* role, bitch!?!?!?!?')
            return

        if not get(message.guild.roles, name=role):
            await message.channel.send('That role doesn\'t exist, bitch!!!!!!!!!!!!!')
            return    
        
        checkrole = discord.utils.get(user.guild.roles, name=role)
        if checkrole in message.author.roles:
            try:
                await user.remove_roles(checkrole)
                await message.channel.send(f':white_check_mark: ' + str(user.name) + ' is no longer ' + str(role))
            except discord.errors.Forbidden:
                await message.channel.send(f'I\'m not allowed to do that, bitch!')
            return
        else:
            try:
                await user.add_roles(checkrole)
                await message.channel.send(f':white_check_mark: ' + str(user.name) + ' is now ' + str(role))
            except discord.errors.Forbidden:
                await message.channel.send(f'I\'m not allowed to do that, bitch!')
            return

        async def on_command_error(ctx,error):
            LOGGER.debug(error)
        
