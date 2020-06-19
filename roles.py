import discord
from discord.utils import get
from typing import List

LOUNGER = 'Lounger'
SOCK = 'Sock'
NG = 'The Dragon Lord'

MODERATION_ROLES = [SOCK, NG]

EVERYONE = '@everyone'

def has_role(member: discord.Member, role: str) -> bool:
    return get(member.roles, name=role) is not None

def has_any_role(member: discord.Member, roles: List[str]) -> bool:
    return any([has_role(member, role) for role in roles])
