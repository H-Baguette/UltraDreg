import os
import logging
import pymysql.cursors
import random
# from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

import resources
from channels import EVERYWHERE, SERIOUS_CHANNELS
from roles import EVERYONE, MODERATION_ROLES

# load_dotenv()
LOGGER = logging.getLogger('dreg')

class Run_Filter():

    def __init__(self,bot):
        self.bot = bot
        self.channels_whitelist = [EVERYWHERE]
        self.channels_blacklist = []
        self.roles_whitelist = [EVERYONE]
        self.roles_blacklist = []
        self.on_message = [self.filtermsg]
        self.on_ready = []

    async def filtermsg(self, message: discord.Message):

        LOGGER.debug('CHECKING FILTER STATUS')

        connection = pymysql.connect(
            host = resources.TOKENSTORE_HOST,
            user = resources.TOKENSTORE_USER,
            passwd = resources.TOKENSTORE_PASS) # create the connection

        LOGGER.debug('CONNECTED TO LOCAL DATABASE SERVER')
        cursor = connection.cursor() # get the cursor

        cursor.execute("USE "+resources.TOKENSTORE_DB) # select database
        cursor.execute("SHOW TABLES") # execute 'SHOW TABLES' (doesn't return data)

        try:
            togglecheck = cursor.execute("SELECT FilterOn FROM filter WHERE FilterName = 'begorrah';")
            filterOn = cursor.fetchone()[0]
            LOGGER.debug('[FILTER STATUS DB] filterOn is '+str(filterOn))
        finally:
            cursor.close()
            connection.close()
            LOGGER.debug('LOCAL DATABASE CONNECTION CLOSED')

        if not filterOn == '1':
            return False

        replacements = {
        'exampleinput': 'exampleoutput'
        }

        punctuation = '\~!@#$%^&\*()-=[]\\;\',./\_+{}|:"?' # importantly, <> are absent from this

        # split message into "tokens", with spaces between them. token = word + punctuation
        #scuffedfix = ctx.content.lower()
        #tokens = scuffedfix.split(' ')
        tokens = message.content.split(' ')
        

        for index, token in enumerate(tokens):

            # find the word, without punctuation
            word = token

            try:
                while word[0] in punctuation:
                    word = word[1:]
                while word[-1] in punctuation:
                    word = word[:-1]
            
            # if the "word" is just punctuation, ignore it
            except IndexError:
                continue

            # replace entire word if it's a complete match
            if word in replacements:
                tokens[index] = token.replace(word, replacements[word])
                continue

            # try to find a matching suffix
            try:
                suffix = next(r[1:] for r in replacements if word.endswith(r[1:]) and r[0] == '*')
                tokens[index] = token.replace(suffix, replacements['*' + suffix])
            
            # if no matching suffix exists, we leave the word as it is
            except StopIteration:
                continue

        # piece together the message again
        edit = ' '.join(tokens)

        # things that should be filtered no matter what
        edit = edit.replace("exampleinput", "exampleoutput")


        if len(edit) > 0 and edit[0] == '%':
            edit = '.' + edit
                


        
        piss = discord.utils.find(lambda hook: hook.name == 'begorrahhook', await message.channel.webhooks())
        if piss is None:
            piss = await message.channel.create_webhook(name='begorrahhook')
            print(piss.url)
        try:
            files = [await a.to_file() for a in message.attachments]
            await message.delete()
            if message.author.nick == None:
                postname = message.author.name
            else:
                postname = message.author.nick
            if message.attachments == None:
                postfile = None
            else:
                postfile = message.attachments
            postmsg = await piss.send(content=edit, wait=True, username=postname,avatar_url=message.author.avatar_url,tts=False,file=None,files=files,embed=None,embeds=None)
            #print(postmsg)
        except discord.errors.NotFound:
            LOGGER.debug('not found')
