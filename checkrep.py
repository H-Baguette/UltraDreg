import logging
import pymysql.cursors
import re

import discord
from discord.ext import commands
from discord.utils import get

import resources
from channels import EVERYWHERE
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

class Check_Rep():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.checkrep]
        self.on_ready = []
        self.help_content = {'name': 'checkrep',
                             'value': 'Checks someone\'s forum rep, if their account is linked.'}

    async def checkrep(self, message: discord.Message):

        if not message.content.lower().startswith(resources.COMMAND_PREFIX + 'checkrep'):
            return False

        await message.channel.send("Checking...")
        try:
            target = re.compile('[0-9]+').search(message.content.split(' ')[1]).group(0)
            LOGGER.debug("CHECKING TARGET")
        except (IndexError, AttributeError):
            target = message.author.id
            LOGGER.debug("CHECKING MESSAGE AUTHOR")
        
        LOGGER.debug('Checking rep of ' + str(target))
        LOGGER.debug("TARGET ID IS "+str(target))

        connection = pymysql.connect(
            host = resources.TOKENSTORE_HOST,
            user = resources.TOKENSTORE_USER,
            passwd = resources.TOKENSTORE_PASS)

        cursor = connection.cursor()

        cursor.execute("USE "+ resources.TOKENSTORE_DB)
        cursor.execute("SHOW TABLES")

        try:
            cursor.execute("SELECT ForumToken FROM userids WHERE DiscordID = "+str(target))
            hasToken = cursor.fetchone()

            cursor.close()
            connection.close()
            LOGGER.debug("CONNECTION TO LOCAL USER DATABASE CLOSED")
            if hasToken == None:
                await message.channel.send("That user hasn't linked their account yet.")
                return
            hasToken = hasToken[0]

            connection = pymysql.cursors.connect(
                host = resources.TLDR_HOST,
                user = resources.TLDR_USER,
                passwd = resources.TLDR_PASS)

            cursor = connection.cursor()

            cursor.execute("USE thetldrc_thetldr4")

            cursor.execute("SHOW TABLES")
            
            LOGGER.debug("TOKEN IS " +str(hasToken))
            cursor.execute("SELECT member_id FROM MemberReputation WHERE field_17 = "+str(hasToken))
            memberID = cursor.fetchone()[0]
            LOGGER.debug("MEMBER ID IS " + str(memberID))
            cursor.execute("SELECT pp_reputation_points FROM MemberReputation WHERE field_17 = "+str(hasToken))
            targetRep = cursor.fetchone()[0]
            cursor.execute("SELECT name FROM MemberReputation WHERE field_17 = "+str(hasToken))
            targetName = cursor.fetchone()[0]
            await message.channel.send("**"+str(targetName)+"** has **"+str(targetRep)+"** Reputation.")
            
            

        finally:
            cursor.close()
            connection.close()
