import logging
import pymysql.cursors
import random

import discord
from discord.ext import commands
from discord.utils import get

import resources
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE, MODERATION_ROLES, has_any_role

LOGGER = logging.getLogger('dreg')



@commands.command(name='begorrah',help='Toggle the wordfilter.')
async def togglefilter(ctx):
    if not has_any_role(ctx.author, MODERATION_ROLES):
        await ctx.send("<:pinkwojak:473491909755797504> You don't have permission to do that!")
        return False

    LOGGER.debug('TOGGLING ST PATRICKS DAY FILTER')

    connection = pymysql.connect(
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
                
