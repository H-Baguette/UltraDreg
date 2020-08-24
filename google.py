import logging
import re
from googlesearch import search

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.errors import MissingRequiredArgument

import resources
from channels import EVERYWHERE
from roles import EVERYONE

LOGGER = logging.getLogger('dreg')

@commands.command(name='google',help='Search the internet and post a result.')
async def google(ctx, *, query = None):

    if query != None:
        for j in search(query, tld="co.in", num=10, stop=1, pause=2):
            await ctx.send(j)
    else:
        await ctx.send(f'<:pinkwojak:473491909755797504> You need to specify what you want to search!')