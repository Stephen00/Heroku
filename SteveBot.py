import asyncio
import datetime
import time

import discord

from datetime import datetime
from discord.ext import commands
from discord.utils import get


# Defines the bot command prefix
client = commands.Bot(command_prefix=".")
global msg_id


@client.event
async def on_ready():
    print('SteveBot is ready')


#######################################################
# Birthday message functionality
#######################################################

birthdayFile = './bdays.txt'


# Background command to check if a user has a birthday and display a message
@client.command()
async def checkTodaysBirthdays():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.strftime(datetime.now(), '%H:%M')
        if now == "00:00":
            channel = client.get_channel(722099507634110514)
            fileName = open(birthdayFile, 'r')
            today = time.strftime('%d%m')
            flag = 0
            for line in fileName:
                print(today in line)
                if today in line:
                    print(today)
                    line = line.split(' ')
                    flag = 1
                    user = line[2].strip('\n')
                    await channel.send("Happy Birthday <@!" + user + ">" + " Have a banging day lad!")
            if flag == 0:
                print('Nobody has a birthday today')
        await asyncio.sleep(60)


# Admin command to allow a staff to manually add a user's birthday
@commands.has_role('Hogwarts staff')
@client.command()
async def forceadd(ctx, user: discord.Member, date):
    bday = date.split("/")
    txt = bday[0] + bday[1] + ' ' + user.display_name + ' ' + str(user.id)
    flag = 0

    # Check if user has a birthday logged already
    filename = open(birthdayFile, 'r')
    for line in filename:
        if str(user.id) in line:
            print('User already has a birthday logged')
            flag = 1
    # Add user's birthday to file if not already added
    if flag == 0:
        with open('./bdays.txt', 'a') as f:
            f.write(txt + '\n')
            f.close()
            await ctx.channel.send(user.display_name + '\'s Birthday has been logged!')
    else:
        await ctx.channel.send('This user already has a birthday logged')


@client.command()
async def bday(ctx):
    flag = 0
    user = ctx.message.author
    await ctx.send("What is your birthday? Please use DD/MM format.")

    msg = await client.wait_for('message', check=lambda msg: msg.author == ctx.author)
    msg = msg.content

    # Check to see if the date provided is valid
    try:
        list = msg.split("/")
        if int(list[1]) > 13 or int(list[1]) < 1:
            await ctx.send("Invalid date.")
            return
        else:
            pass

        if int(list[1]) in (1, 3, 5, 7, 8, 10, 12):
            if int(list[0]) > 31 or int(list[0]) < 1:
                await ctx.send("Invalid date.")
                return
            else:
                pass
        elif int(list[1]) in (4, 6, 9, 11):
            if int(list[0]) > 30 or int(list[0]) < 1:
                await ctx.send("Invalid date.")
                return
            else:
                pass
        elif int(list[1]) == 2:
            if int(list[0]) > 29 or int(list[0]) < 1:
                await ctx.send("Invalid date.")
                return
            else:
                pass
        else:
            await ctx.send("Invalid date.")
            return
    except:
        await ctx.send("Invalid date.")
        return

    txt = list[0] + list[1] + ' ' + user.display_name + ' ' + str(user.id)
    print(txt)

    # Check if user has a birthday logged already
    fileName = open(birthdayFile, 'r')
    for line in fileName:
        if str(user.id) in line:
            print('User already has a birthday logged')
            flag = 1
    # Add user's birthday to file if not already added
    if flag == 0:
        with open('./bdays.txt', 'a') as f:
            f.write(txt + '\n')
            f.close()
            await ctx.channel.send('Your Birthday has been logged!')
    else:
        await ctx.channel.send('You already has a birthday logged')


#######################################################
# Hogwarts House functionality
#######################################################


# When a user reacts to the sorting hat message it grants them a role
@client.event
async def on_raw_reaction_add(ctx):
    # Checks that the message is from the sortinghat command
    message_id = ctx.message_id
    if msg_id:
        if message_id == msg_id:
            guild_id = ctx.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            # Determines which role the user has selected
            if ctx.emoji.name == 'Ravenclaw':
                role = discord.utils.get(guild.roles, name='Ravenclaw')
            elif ctx.emoji.name == 'Hufflepuff':
                role = discord.utils.get(guild.roles, name='Hufflepuff')
            elif ctx.emoji.name == 'Slytherin':
                role = discord.utils.get(guild.roles, name='Slytherin')
            elif ctx.emoji.name == 'Gryffindor':
                role = discord.utils.get(guild.roles, name='Gryffindor')
            else:
                role = None

            houses = ['Ravenclaw', 'Hufflepuff', 'Slytherin', 'Gryffindor']
            member = discord.utils.find(lambda m: m.id == ctx.user_id, guild.members)

            # Checks that the member is not SteveBot
            # Iterates through the user's roles and checks that they are not already in a house
            if member.id != 704317548849790976:
                if member is not None:
                    role_names = [role.name for role in member.roles]
                    house = set(role_names) & set(houses)

                    if len(house) < 1:
                        channel = client.get_channel(719661161095758027)
                        await member.add_roles(role)
                        await channel.send(
                            '**' + member.display_name + '** has been placed into the ' + role.mention + ' house!')
                    else:
                        print('member has a house already')
                else:
                    print('Member not found')


# Command that returns the member count to the channel
@client.command()
async def members(ctx):
    guild = ctx.guild
    memberCount = guild.member_count
    await ctx.channel.send('There are **' + str(memberCount) + '** beautiful members in the server')


# Command to let a user get their designated house as a role
@client.command(pass_context=True)
async def sortinghat(ctx):
    channel_id = 719661161095758027
    if ctx.channel.id == channel_id:
        user = ctx.author
        if not user:
            return
        pfp = user.avatar_url
        user_name = ctx.author.display_name

        # Command to return each house emojji in a dictionary
        def get_emojis():
            ravenclaw = get(ctx.message.guild.emojis, name='Ravenclaw')
            hufflepuff = get(ctx.message.guild.emojis, name='Hufflepuff')
            slytherin = get(ctx.message.guild.emojis, name='Slytherin')
            gryffindor = get(ctx.message.guild.emojis, name='Gryffindor')

            emoji_dict = {'r': str(ravenclaw), 'h': str(hufflepuff), 's': str(slytherin), 'g': str(gryffindor)}

            return emoji_dict

        houses = get_emojis()

        msg = await ctx.channel.send(
            'Hello **' + user_name + '** it is time for you to be placed into your designated house...' +
            '\nPlease take the sorting hat quiz below to be allocated to your house:\n' +
            '\nhttps://my.wizardingworld.com/passport' +
            '\n\n Afterwards react with the corrosponding house that you have been selected for below ')

        # Global message ID so that it can be checked in the on_react events
        global msg_id
        msg_id = msg.id

        # Adds reaction of each house the bot message
        for emoji in houses.values():
            await msg.add_reaction(emoji)
    else:
        print('Command was used in the incorrect channel')


# Prints a neatly embedded message to describe how the sorting hat command operates
@client.command()
@commands.has_role('Hogwarts staff')
async def houseinfo(ctx):
    embed = discord.Embed(title="**How To Get Placed Into Your Hogwarts House**",
                          description="To get placed into your hogwarts house, use this wee command:\n"
                                      "\n```.sortinghat```\nSteveBot will then sent a message including a link to the sorting quiz which"
                                      " you can react to afterward in order to recieve your house role",
                          color=discord.Color.dark_gold())
    embed.set_thumbnail(
        url="https://www.freepnglogos.com/uploads/hogwarts-logo-png/hogwarts-logo-shadopro-deviantart-0.png")

    await ctx.channel.send(embed=embed)


# Prints a list of user's birthdays
@client.command()
@commands.has_role('Hogwarts staff')
async def bdaylist(ctx):
    with open('bdays.txt') as f:
        output = ""
        for line in f:
            line = line.split(' ')
            output += line[2] + ' ' + line[1] + ': ' + line[0] + '\n'
        await ctx.channel.send(output)

# Background task that will run once every day
client.loop.create_task(checkTodaysBirthdays())
if __name__ == "__main__":
    client.run('INSERT_KEY_HERE')
