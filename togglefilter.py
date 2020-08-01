import logging
import MySQLdb
import random

import discord
from discord.ext import commands
from discord.utils import get

import resources
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE, MODERATION_ROLES, has_any_role

LOGGER = logging.getLogger('dreg')

class Toggle_Filter():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.togglefilter]
        self.on_ready = []
        self.help_content = {'name': 'begorrah',
                             'value': 'Toggle the St. Patrick\'s Day Filter.'}

    async def togglefilter(self, message: discord.Message):

        if not message.content.lower().startswith(resources.COMMAND_PREFIX + 'begorrah'):
            return False
        if not has_any_role(message.author, MODERATION_ROLES):
            return False

        LOGGER.debug('TOGGLING ST PATRICKS DAY FILTER')

        connection = MySQLdb.connect(
            host = resources.TOKENSTORE_HOST,
            user = resources.TOKENSTORE_USER,
            passwd = resources.TOKENSTORE_PASS) # create the connection

        LOGGER.debug('CONNECTED TO LOCAL DATABASE SERVER')
        cursor = connection.cursor() # get the cursor

        cursor.execute("USE "+ resources.TOKENSTORE_DB) # select database
        cursor.execute("SHOW TABLES") # execute 'SHOW TABLES' (doesn't return data)

        try:
            togglecheck = cursor.execute("SELECT FilterOn FROM filter WHERE FilterName = 'begorrah';")
            filterOn = cursor.fetchone()[0]
            LOGGER.debug('[FILTER STATUS DB] filterOn is '+str(filterOn))
            if str(filterOn) == '0':
                cursor.execute("UPDATE filter SET FilterOn = 1 WHERE FilterName = 'begorrah';")
                cursor.execute("COMMIT")
            else:
                cursor.execute("UPDATE filter SET FilterOn = 0 WHERE FilterName = 'begorrah';")
                cursor.execute("COMMIT")

            LOGGER.debug('[FILTER STATUS DB] FILTER TOGGLED')

        finally:
            cursor.close()
            connection.close()
            LOGGER.debug('LOCAL DATABASE CONNECTION CLOSED')
                
