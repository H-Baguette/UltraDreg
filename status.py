import logging
from pathlib import Path

import discord
from channels import EVERYWHERE
import roles
from resources import TLDR_LOGO, COMMAND_PREFIX

LOGGER = logging.getLogger('dreg')


def read_version() -> str:
    if not Path('.git').exists():
        return '[unable to read version information]'

    return Path('.git/HEAD').read_text()


class Status():
    '''
    This module can give a short report on the bot.
    '''

    def __init__(self, bot, modules):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [roles.EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.report_status]
        self.on_ready = []
        self.help_content = {'name': 'bot_status',
                             'value': 'Get a status report from the bot.'}
        self.modules = modules

    async def report_status(self, message: discord.Message):
        '''
        Creates an embed with some debug info about the bot.
        '''
        if message.content.lower() != str(COMMAND_PREFIX+'bot_status'):
            return False

        embed = discord.Embed(
            title='DREG status report', description='DREG [ONLINE]', color=0x00ff45)
        embed.set_thumbnail(url=TLDR_LOGO)

        embed.add_field(name='deployed commit',
                        value=read_version(), inline=False)
        embed.add_field(name='active modules', value=[
            module.__class__.__name__ for module in self.modules],inline=False)

        await message.channel.send(embed=embed)
        return False
