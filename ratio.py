import logging
import MySQLdb
import re

import discord
from discord.ext import commands
from discord.utils import get

import resources
from channels import EVERYWHERE
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

class Check_Ratio():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.ratio]
        self.on_ready = []
        self.help_content = {'name': 'ratio',
                             'value': 'Check a poster\'s nod ratio. Needs their Discord account to be linked to TheTLDR.'}

    async def ratio(self, message: discord.Message):

        if not message.content.lower().startswith(resources.COMMAND_PREFIX + 'ratio'):
            return False

        await message.channel.send("Checking...")
        try:
            target = re.compile('[0-9]+').search(message.content.split(' ')[1]).group(0)
            LOGGER.debug("CHECKING TARGET")
        except (IndexError,AttributeError):
            target = message.author.id
            LOGGER.debug("CHECKING MESSAGE AUTHOR")

        connection = MySQLdb.connect(
            host = resources.TOKENSTORE_HOST,
            user = resources.TOKENSTORE_USER,
            passwd = resources.TOKENSTORE_PASS)

        cursor = connection.cursor()

        cursor.execute("USE users")
        cursor.execute("SHOW TABLES")

        try:
            cursor.execute("SELECT ForumToken FROM userids WHERE DiscordID = "+str(target))
            hasToken = cursor.fetchone()[0]

            cursor.close()
            connection.close()
            LOGGER.debug("CONNECTION TO LOCAL USER DATABASE CLOSED")
            if hasToken == None:
                await message.channel.send("That user hasn't linked their account yet.")
                return


            connection = MySQLdb.connect(
                host = resources.TLDR_HOST,
                user = resources.TLDR_USER,
                passwd = resources.TLDR_PASS)

            cursor = connection.cursor()

            cursor.execute("USE thetldrc_thetldr3")
            cursor.execute("SHOW TABLES")

            cursor.execute("SELECT name FROM MemberReputation WHERE field_17 = "+str(hasToken))
            targetName = cursor.fetchone()[0]
            cursor.execute("SELECT pp_reputation_points FROM MemberReputation WHERE field_17 = "+str(hasToken))
            targetRep = float(cursor.fetchone()[0])
            cursor.execute("SELECT member_posts FROM MemberReputation WHERE field_17 = "+str(hasToken))
            targetPosts = float(cursor.fetchone()[0])

            targetRatio = float(targetRep/targetPosts)
            await message.channel.send("**"+str(targetName)+"** has a nod ratio of **"+format(targetRatio, '.2f')+"**.")
            if targetRatio < 0.6:
                await message.channel.send("Cuh-ringe!")
            elif targetRatio > 2:
                await message.channel.send("B-B-B-B-Based!")

        finally:
            cursor.close()
            connection.close()


