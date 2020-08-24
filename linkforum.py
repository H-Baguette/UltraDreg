import logging
import pymysql.cursors
import random

import discord
from discord.ext import commands
from discord.utils import get

from resources import COMMAND_PREFIX
from channels import EVERYWHERE
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

class Link_Forum():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.linkaccount]
        self.on_ready = []
        self.help_content = {'name': 'linkaccount',
                             'value': 'Links your Discord account to TheTLDR.com.'}

    async def linkaccount(self, message: discord.Message):

        if not message.content.lower().startswith(COMMAND_PREFIX + 'linkaccount'):
            return False

        LOGGER.debug('Linking user to forum')

        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'toor') # create the connection

        cursor = connection.cursor() # get the cursor


        cursor.execute("USE "+ resources.TOKENSTORE_DB) # select the database
        cursor.execute("SHOW TABLES") # execute 'SHOW TABLES' (doesnt return data)

        try:
            testcheck = cursor.execute("SELECT EXISTS(SELECT ForumToken FROM userids WHERE DiscordID = "+str(message.author.id)+")")
            cursor.execute("SELECT ForumToken FROM userids WHERE DiscordID = "+str(message.author.id))
            LOGGER.debug("FOUND DISCORD USERID: " + str(message.author.id))
            tokenExists = cursor.fetchone()
            LOGGER.debug("FOUND FORUM TOKEN: " + str(tokenExists))
            LOGGER.debug("TESTCHECK VALUE IS " + str(testcheck))

            if tokenExists == None:
                token = random.randint(10,9999999)
                LOGGER.debug("NO TOKEN DETECTED, GENERATING NEW")
                isTokenDuplicate = cursor.execute("SELECT ForumToken FROM userids WHERE ForumToken = "+str(token))
                LOGGER.debug(str(isTokenDuplicate))
                while isTokenDuplicate != 0:
                    token = random.randint(10,9999999)
                    isTokenDuplicate = cursor.execute("SELECT ForumToken FROM userids WHERE ForumToken = "+str(token))

                if isTokenDuplicate == 0:
                    cursor.execute("INSERT INTO userids(DiscordID,ForumToken) VALUES ("+str(message.author.id)+","+str(token)+")")
                    cursor.execute("COMMIT")
                    await message.author.send("Your TheTLDR Auth token is: **" + str(token) + "**\nEnter it into the 'Ultradreg Token' field on your 'edit profile' page.")
                    await message.channel.send("Auth token sent.")
                else:
                    LOGGER.debug("GENERATED DUPLICATE TOKEN")
                    await message.author.send("Somehow I generated a duplicate token. Baguette wrote me bad, bitch!")

            elif tokenExists != None:
                await message.author.send("You already have an auth token. Yours is: "+str(tokenExists))
                await message.channel.send(message.author.mention + " You already have a token, bitch!!!!!")

            else:
                await message.channel.send("Something broke. <@!144189675261788160> FIX IT FIX IT FIX IT FIX IT FIX IT")
                
                
        finally:
            cursor.close()
            connection.close()
            LOGGER.debug('USER DATABASE CONNECTION CLOSED')
            
