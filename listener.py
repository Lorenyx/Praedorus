import discord
from discord.ext import commands
import random

description = '''I lost my Guardian during the Red Legion's assault.
I now assist all Warriors of the Light that I can, for I 
never want to see another Guardian die.

-------

Basic commands are listed here and type $help <command> for 
more info about that command'''
bot = commands.Bot(command_prefix='$', description=description)
guardians = {}

@bot.event
async def on_ready():
    print('+------>')
    print("|" +'Logged in as: ')
    print("|" +bot.user.name)
    print('+------>')

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

guardians = {}

@bot.command()
async def fireteam(name=None, light=None): #pclass is player's class, shortened for simplicity
    """Adds a guardian to a \**Fireteam\** roster.

All fields are required for command. The variable
'name' is your Guardian's in game name, 'light level'
is the in game power level and can be shown as
-200 (below 200 power level), +200 (above 200 power),
+240 (above 240 power), +270, or +300.

NOTE: Nothing yet."""
    if (name == None) | (light == None):
        await bot.say("Stuff")
        return
    else:
        guardians[str(name)] = light
        await bot.say("...roster updated...")

@bot.command()
async def roster(*options):
    """Shows Guardians in current fireteam"""
    if options:
        try:
            if options[0] == "remove":
                del guardians[options[1]]
                await bot.say("...{} removed...".format(options[1]))
        except IndexError:
            await bot.say("...missing variables...")
            return

    else:
        if len(guardians) > 0:
            result = ""
            for pc in guardians:
                result += "{:<14}{:>6}".format(pc, guardians[pc]) + "\n"
            await bot.say("{:<15}\n**```\n{}\n```**".format("__**The Fireteam**__", result))
        else:
            await bot.say("...roster empty...")

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

@bot.event
async def on_member_join(member):
        # Actions to take when a new member joins the server.
    channel = discord.Object(id=377497779611893761)
    msg = ":new: {0} joined the server. Current member count: **{1}**".format(
        member.mention, member.server.member_count
    )
    tmp = await bot.send_message(channel, msg)
    channel = discord.Object(id=376884253297737731)
    msg = ":new: | Welcome to **The Fireteam**, {}! <:glimmer:377100398055522304>".format(member.mention)
    tmp = await bot.send_message(channel, msg)
    role = discord.utils.get(member.server, name="Guardians")
    await bot.add_roles(member, role)


bot.run('token')


