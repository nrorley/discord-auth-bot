import aiohttp
import discord
from discord.ext import commands
import secrets
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
VALID_ROLE_ID = os.getenv('VALID_ROLE_ID')
VALID_GUILD = os.getenv('VALID_GUILD')

VALID_ROLE_ID = int(VALID_ROLE_ID)
VALID_GUILD = int(VALID_GUILD)

discord_client = discord.Client

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
async def verify(ctx):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        
        guild = bot.get_guild(id = VALID_GUILD)
        member = await guild.fetch_member(ctx.author.id)

        has_role = False
        for role in member.roles:
            if role.id == VALID_ROLE_ID:
                has_role = True
        
        if member:
            if has_role == True:

                bot_key = secrets.token_urlsafe(30)
                
                headers = {
                    'accept': 'application/json'
                }

                json_data = {
                    'id': str(ctx.author.id),
                    'key': str(bot_key),
                    'session': 'None',
                    'mint': 'placeholder',
                    'auth_token': 'sqWQXSV9aMytZ2lC7L31HQDhy8mQxivE8psYYxRdJIz6OdhmmQv',
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(url = 'https://www.mintmatenft.com/api/v1/auth/users/', headers = headers,json = json_data) as response:
                        if response.status == 200:
                            await ctx.channel.send('Congratulations! You have been successfully registered!')
                            await ctx.channel.send('Please keep this key safe and use this to authenticate your copy of Mint Mate. If you believe this key has been compromised then you can generate a new one by sending me the \'!key\' command. ```' + str(bot_key) + '```')
                        elif response.status == 400:
                            await ctx.channel.send('User is already registered. You can check with the \'!info\' command. If you think this is a mistake please contact an admin!')
                        else:
                            await ctx.channel.send('An error has occured. Please check to see if you have been verified with the \'!info\' command. If this shows an error please contact an admin!')
            else: 
                await ctx.channel.send('You do not have permission to use this function')

@bot.command(pass_context=True)
async def info(ctx):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        
        guild = bot.get_guild(id = VALID_GUILD)
        member = await guild.fetch_member(ctx.author.id)

        has_role = False
        for role in member.roles:
            if role.id == VALID_ROLE_ID:
                has_role = True
        
        if member:
            if has_role == True:
                
                headers = {
                    'accept': 'application/json'
                }

                json_data = {
                    'auth_token': 'sqWQXSV9aMytZ2lC7L31HQDhy8mQxivE8psYYxRdJIz6OdhmmQv',
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(url = 'https://www.mintmatenft.com/api/v1/auth/user/search/id/' + str(ctx.author.id), headers = headers,json = json_data) as response:
                        if response.status == 200:
                            response_json = await response.json()
                            response_message = 'Details for User : ' + response_json['id'] + '\nKey : ' + str(response_json['key']) + '\nCurrent Session : ' + str(response_json['session']) + '\nLinked Mint : ' + str(response_json['mint'])
                            await ctx.channel.send('```' + response_message + '```')

                        elif response.status == 404:
                            await ctx.channel.send('User not found!')
                        else:
                            await ctx.channel.send('An error has occured. Please try again. If this issue persists please contact an admin!')
            else: 
                await ctx.channel.send('You do not have permission to use this function')

@bot.command(pass_context=True)
async def reset(ctx):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        
        guild = bot.get_guild(id = VALID_GUILD)
        member = await guild.fetch_member(ctx.author.id)

        has_role = False
        for role in member.roles:
            if role.id == VALID_ROLE_ID:
                has_role = True
        
        if member:
            if has_role == True:
                
                headers = {
                    'accept': 'application/json'
                }

                json_data = {
                    'session' : 'None',
                    'auth_token': 'sqWQXSV9aMytZ2lC7L31HQDhy8mQxivE8psYYxRdJIz6OdhmmQv',
                }

                async with aiohttp.ClientSession() as session:
                    async with session.patch(url = 'https://www.mintmatenft.com/api/v1/auth/users/' + str(ctx.author.id), headers = headers,json = json_data) as response:
                        if response.status == 200:
                            response_json = await response.json()
                            await ctx.channel.send('Your session has been reset! You can double check with the \'!info\' command!')

                        elif response.status == 404:
                            await ctx.channel.send('User not found!')
                        else:
                            await ctx.channel.send('An error has occured. Please try again. If this issue persists please contact an admin!')
            else: 
                await ctx.channel.send('You do not have permission to use this function')

@bot.command(pass_context=True)
async def key(ctx):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        
        guild = bot.get_guild(id = VALID_GUILD)
        member = await guild.fetch_member(ctx.author.id)

        has_role = False
        for role in member.roles:
            if role.id == VALID_ROLE_ID:
                has_role = True
        
        if member:
            if has_role == True:
                
                bot_key = secrets.token_urlsafe(30)

                headers = {
                    'accept': 'application/json'
                }

                json_data = {
                    'key' : str(bot_key),
                    'auth_token': 'sqWQXSV9aMytZ2lC7L31HQDhy8mQxivE8psYYxRdJIz6OdhmmQv',
                }

                async with aiohttp.ClientSession() as session:
                    async with session.patch(url = 'https://www.mintmatenft.com/api/v1/auth/users/' + str(ctx.author.id), headers = headers,json = json_data) as response:
                        if response.status == 200:
                            response_json = await response.json()
                            await ctx.channel.send('Your key has been reset! Your new key is ```' + str(response_json['key']) + '```')

                        elif response.status == 404:
                            await ctx.channel.send('User not found!')
                        else:
                            await ctx.channel.send('An error has occured. Please try again. If this issue persists please contact an admin!')
            else: 
                await ctx.channel.send('You do not have permission to use this function')


if __name__ == '__main__':
    bot.run(TOKEN)