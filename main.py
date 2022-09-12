#!/usr/bin/python3

import discord

from properties import botToken, guildId, channelName, gm_role, tank_role, healer_role, dps_role
from character import *
from actionhandler import *

client = discord.Client(intents=discord.Intents.all())
discord.AllowedMentions(everyone = True)

@client.event
async def on_ready():
    
    # Specify a specific server so we do not mix character data from other servers
    global guild 
    guild = client.get_guild(guildId) # Lopporrit Appreciation
    
    
    global characterData
    characterData = {}
    
    print(f"Using guildId: {guildId}")
    print(guild)
    print('We have logged in as {0.user}'.format(client))

    # Populate characterData Dictionary with user id as keys and Character object as values
    for member in guild.members:

        characterData[member.id] = Character(member)
        
        # Set GM Flags
        if (member.display_name in gm_role):
            characterData[member.id].gm=True
        
        # Set Roles
        if (member.display_name in tank_role):
            characterData[member.id].role="tank"

        if (member.display_name in healer_role):
            characterData[member.id].role="healer"

        if (member.display_name in dps_role):
            characterData[member.id].role="dps"

@client.event
async def on_message(message):
    
    global characterData
    global guild
    
    if message.content.startswith('!'):
        if (message.author == client.user):
            return  # Do nothing if message from bot

        if(message.guild.id == guildId and message.channel.name == channelName):
            await actionHandler(characterData, client, message)
        else:
            # Whether or not it is a bot command or string that starts with !, we should not respond in the channel but log the incident internally only
            print(f"ERROR: This bot is configured to be used in Server: {guild.name}, Channel: {channelName}")

            return


        
client.run(botToken)

