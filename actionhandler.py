import discord
import random

def createStatusEmbed(target):
    embed = discord.Embed()
    embed.add_field(name="Name", value=target.user.name)
    embed.add_field(name="Role:", value=target.role)
    embed.add_field(name="Health:", value=target.health)
    embed.add_field(name="Rage:", value=target.rage)
    embed.add_field(name="Invulnerable:", value=target.invulnerable)
    embed.add_field(name="Covered:", value=target.cover)
    #embed.add_field(name="Game Master", value=target.gm)
    #embed.add_field(name="Nickname", value=target.user.nick)
    #embed.add_field(name="Display Name", value=target.user.display_name)
    embed.set_thumbnail(url = f"{target.user.avatar_url}")
    return embed

async def actionHandler(characterData, client, message):
    
    botCommand = message.content.split()[0]

    if (not botCommand in ["!pet", "!slap", "!reset", "!geass", "!lb3", "!status"]):
        print("{botCommand} is not a valid bot command")
        return

    # Set caster Character
    caster = characterData[message.author.id]
    
    # Special Commands -GM

    # Reset 
    if(botCommand == "!reset"):
        if(not caster.isGameMaster()):
            await message.channel.send(f"You're are not authorised to cast {botCommand}")
            return
        else:
            for member in client.get_guild(message.guild.id).members:
                characterData[member.id].health = 100
            
            # await message.channel.send("https://c.tenor.com/ofeCFZeKMZEAAAAC/anduin-world-of-warcraft.gif")
            
            embed = discord.Embed(title = "Crystal Exarch: Beyond the rift", description = "Let's expanse contract, eon become instant!\nChampions from beyond the rift, heed my call!")
            embed.set_image(url = "https://64.media.tumblr.com/11b853e8159827fdfa3d1aa62521a01f/tumblr_puk81unOnO1unwmpzo1_400.gif")
            embed.set_footer(text = "GM Ability: All players are resurrected and restored to maximum HP")
            #embed.set_thumbnail(url = "https://static.wikia.nocookie.net/finalfantasy/images/1/16/Limit_Break_from_Final_Fantasy_XIV_icon.png/revision/latest?cb=20210530020359")
            await message.channel.send(embed = embed)
            return
    
    # Geass 
    if(botCommand == "!geass"):
        if(not caster.isGameMaster()):
            await message.channel.send(f"You're are not authorised to cast {botCommand}")
            return
        else:
            target = characterData[message.mentions[0].id]
            
            # Replace GM's role with target's role
            characterData[message.author.id].role = target.role
            
            embed = discord.Embed(title ="Lelouch vi Britannia: Geass", description = "Hand over your role")
            #embed.set_image(url = "https://media3.giphy.com/media/3PxSmPCeQsVGUl2Q35/giphy.gif?cid=790b76112ba21b37f5e68252e6a1f9545e09ce102b05c9c1&rid=giphy.gif&ct=g")
            #embed.set_thumbnail(url = "https://media3.giphy.com/media/3PxSmPCeQsVGUl2Q35/giphy.gif?cid=790b76112ba21b37f5e68252e6a1f9545e09ce102b05c9c1&rid=giphy.gif&ct=g")
            embed.set_thumbnail(url = "https://c.tenor.com/opMGHMXAgt8AAAAC/geass.gif")
            embed.set_footer(text = f"GM Ability: {caster.user.name} gains control of {target.user.name}'s {target.role} role")
            await message.channel.send(embed = embed)
            return
    

    # Check if caster is alive
    if (caster.isDead()):
        await message.channel.send(f"Unable to execute {botCommand} when dead")
        return

    # Special Commands - Limit Break
    if(botCommand == "!lb3"):
        
        if(caster.role == "healer"):
            for member in client.get_guild(message.guild.id).members:
                if (not characterData[member.id].isDead()):
                    characterData[member.id].health = 100
            
            # await message.channel.send("https://c.tenor.com/ofeCFZeKMZEAAAAC/anduin-world-of-warcraft.gif")
            
            embed = discord.Embed(title = "Anduin Wyrnn: Holy Word Salvation", description = "Stand as one! For the Alliance!")
            embed.set_image(url = "https://c.tenor.com/ofeCFZeKMZEAAAAC/anduin-world-of-warcraft.gif")
            #embed.set_thumbnail(url = "https://c.tenor.com/ofeCFZeKMZEAAAAC/anduin-world-of-warcraft.gif")
            embed.set_footer(text = "Healer Ability: Restores all players to full health. Does not affect dead players")
            await message.channel.send(embed = embed)
            return
    
        elif(caster.role == "tank"):
            for member in client.get_guild(message.guild.id).members:
                if (not characterData[member.id].isDead()):
                    characterData[member.id].invulnerable = True
            
            embed = discord.Embed(title = "Mashu Kyrielight: Lord Camelot", description = "The Noble Phantasm of the Heroic Spirit Galahad. It is the ultimate defense using the Round Table, which sat in the center of the white castle Camelot, as a shield.")
            embed.set_image(url = "https://64.media.tumblr.com/ba91c44a39554e09f310883427659bec/e6c19a7015ad146a-67/s540x810/aa34432fc35d563fa629ee877cc30b95ab0a671d.gif")
            #embed.set_thumbnail(url = "https://64.media.tumblr.com/ba91c44a39554e09f310883427659bec/e6c19a7015ad146a-67/s540x810/aa34432fc35d563fa629ee877cc30b95ab0a671d.gif")
            embed.set_footer(text = "Tank Ability: All Players are invulnerable to the next attack they receive")
            await message.channel.send(embed = embed)
            return
        else:
            await message.channel.send(f"Error: Unable to cast {botCommand} with current role: {caster.role}")

   
    # Generic Commands
    if(botCommand == "!status"):
        
        if (message.mention_everyone):
            if (caster.isGameMaster()):
                for member in client.get_guild(message.guild.id).members:
                    embed = createStatusEmbed(characterData[member.id])
                    await message.channel.send(embed = embed)
            else:
                await message.channel.send(f"{botCommand} @everyone can only be casted by Game Master")
        
        elif(len(message.mentions)):
            target = characterData[message.mentions[0].id]
            embed = createStatusEmbed(target) 
            await message.channel.send(embed = embed)
        else:
            await message.channel.send(f"Error! Usage: {botCommand} @user")

    if(botCommand == "!pet"):
        
        petHeal = 30
        
        
        if(len(message.mentions)):
            target = characterData[message.mentions[0].id]
        else:
            await message.channel.send(f"Error! Usage: {botCommand} @user")
            return
        
        if (target.isDead()):
            
            await message.channel.send(f"{caster.user.mention} gently pets {target.user.mention}'s lifeless body")

        elif (0 < target.health < 100): # If target health is less than 100

            if ( (target.health + petHeal) >= 100):
                characterData[target.user.id].health = 100
            else:
                characterData[target.user.id].health += petHeal

                print(characterData[target.user.id])
        
            await message.channel.send(f"{caster.user.mention} gently pets {target.user.mention}, restoring {petHeal} HP, current HP is {characterData[target.user.id].health}/100")

        elif(target.health == 100):

            await message.channel.send(f"{caster.user.mention} gently pets {target.user.mention}")
        else:
            print("Likely error - Negative health, etc")

    
    if(botCommand == "!slap"):

        slapDamage = 30 + caster.rage
        
        if(len(message.mentions)):
            target = characterData[message.mentions[0].id]
        else:
            await message.channel.send(f"Error! Usage: {botCommand} @user")
            return
        
        if (target.isDead()):

            await message.channel.send(f"{target.user.mention} is already dead")
        
        if(target.isInvulnerable()):
            
            # Remove invulnerability
            characterData[target.user.id].invulnerable = False
            
            # Remove caster rage
            characterData[caster.user.id].rage = 0
            
            await message.channel.send(f"{target.user.mention} is invulnerable! {slapDamage} damage resisted!")
            return

        elif ((target.health - slapDamage) <= 0):
            
            characterData[target.user.id].health = 0
            
            characterData[caster.user.id].rage = 0
            characterData[target.user.id].rage = 0
            
            await message.channel.send(f"{caster.user.mention} slaps {target.user.mention} to death. {slapDamage} damage dealt")
        else:

            characterData[target.user.id].health -= slapDamage
            
            characterData[target.user.id].rage += random.randint(30,70)
            
            characterData[caster.user.id].rage = 0
            
            
            await message.channel.send(f"{caster.user.mention} slaps {target.user.mention} for {slapDamage} damage, current HP is {characterData[target.user.id].health}/100")













