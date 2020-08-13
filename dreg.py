# Core
import discord
from discord import ext
from discord.ext import commands
import sys
import asyncio
import logging
from logging import handlers
# Modules
from join import Join
from dreg_help import DREG_Help
from togglerole import Toggle_Role
from togglefilter import Toggle_Filter
from filtermsg import Run_Filter
from status import Status
from linkforum import Link_Forum
from aldo import Post_Aldo
from streamnotifier import Stream_Notify
from based import Based_On_What
from checkrep import Check_Rep
from ratio import Check_Ratio
# Constants
from roles import has_any_role
import channels

# set up logging
log_file_handler = handlers.TimedRotatingFileHandler(
    filename='dreg.log', encoding='utf-8', backupCount=6, when='D', interval=7)
log_file_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s:      %(message)s'))
    
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.WARNING)
root_logger = logging.getLogger()
root_logger.addHandler(log_file_handler)

LOGGER = logging.getLogger('dreg')
LOGGER.setLevel(logging.DEBUG)

# command prefix defined in resources.py, i know its janky but its the
# only way i can get it to work, otherwise it shits itself
bot = ext.commands.Bot(command_prefix='', case_insensitive=True)

# register modules
MODULES = [
    #Join(bot),
    Post_Aldo(bot),
    Stream_Notify(bot),
    Toggle_Role(bot),
    Toggle_Filter(bot),
    Run_Filter(bot),
    Based_On_What(bot)
    #Link_Forum(bot),
    #Check_Rep(bot),
    #Check_Ratio(bot)
]

MODULES.append(DREG_Help(bot, MODULES))
MODULES.append(Status(bot, MODULES))

@bot.event
async def on_message(message: discord.Message):
    # ignore all messages by any bot (incldues webhooks)
    if message.author.bot:
        LOGGER.debug('Ignoring bot message.')
        return

    for module in MODULES:
        channel_valid = message.channel.name not in module.channels_blacklist and (
            message.channel.name in module.channels_whitelist or channels.EVERYWHERE in module.channels_whitelist)
        roles_valid = has_any_role(message.author, module.roles_whitelist) and not has_any_role(
            message.author, module.roles_blacklist)
        if channel_valid and roles_valid:
            for listener in module.on_message:
                # when a listener returns True, event has been handled
                LOGGER.debug(
                    f'Executing listener: {str(listener)} for message: [{message.content}] in server {message.guild.name}')
                if await listener(message):
                    LOGGER.debug('Listener returned true. Terminating early.')
                    return
    LOGGER.debug('Module stack execution complete.')
    
    
@bot.event
async def on_member_join(member: discord.Member):
    for module in MODULES:
        try:
            await module.on_member_join(member)
        except AttributeError:
            # do not raise an error, if this is not defined
            pass


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Type d!help for info."))
    for module in MODULES:
        for listener in module.on_ready:
            # start these concurrently, so they do not block each other
            asyncio.ensure_future(listener())


@bot.event
async def on_error(event, *args, **kwargs):
    LOGGER.error(
        f'Exception encountered while handling message with content [{args[0].content}] in channel [{args[0].channel.name}]', exc_info=True)

bot.run(sys.argv[1])
