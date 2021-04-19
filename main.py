import os
from server import keep_alive
from dotenv import load_dotenv
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Context, errors

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ROLE = os.getenv('DISCORD_ROLE')
LESSON = os.getenv('LESSON')

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or('Ł'), 
    help_command = commands.DefaultHelpCommand(no_category = 'Commands'),
    intents = intents,
    )

student_list = {}
nincs_bent = []
embed_message = ""


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user.name} kapcsolódott a {guild.name} szerverhez.')

@bot.command(name='becs')
async def becsengo(context: Context):
    if context.author.name != "Laci4":
        if ROLE not in [x.name for x in context.author.roles]:
            return
    
    await context.message.delete()
    await context.send("@everyone\nBecsengettek! Mindenki a helyére!!!")

    await asyncio.sleep(60 * int(LESSON))
    await context.send("@everyone\nKicsengettek! Mindenki mehet a dolgára.")


@bot.command(name='kics')
async def kicsengo(context: Context):
    if context.author.name != "Laci4":
        if ROLE not in [x.name for x in context.author.roles]:
            return
    
    await context.message.delete()
    await context.send("@everyone\nKicsengettek! Mindenki mehet a dolgára.")

@bot.command(name='wc')
async def toilette(context: Context):
    await context.message.delete()

    tanar = discord.utils.get(context.guild.roles, id=776014639796453386)
    await context.send(f'{tanar.mention}\n**{context.author.nick if context.author.nick else context.author.name}** ki szeretne menni mosdóba!')

@bot.command(name='record')
async def record_list_of_students(context: Context):
    if context.author.name != "Laci4":
        if ROLE not in [x.name for x in context.author.roles]:
            return
    

    student_list.clear()
    students = [i for i in context.guild.members if 'Diak' in (l.name for l in i.roles)]
    for i in students:
        student_list[i.name] = i


# innentől jön a kemény dolog
@bot.command(name='névsor')
async def print_list_of_students(context: Context):
    if context.author.name != "Laci4":
        if ROLE not in [x.name for x in context.author.roles]:
            return
    await context.message.delete()

    if not context.author.voice:
        await context.send('Először csatlakoznod kell egy hang csatornába!')
        return

    await record_list_of_students(context)
    global nincs_bent

    bent_van = context.author.voice.channel.members
    nincs_bent = [i for i in student_list.values() if not i in bent_van]

    bent_string = "\n".join([i.nick if i.nick else i.name for i in bent_van])
    nincs_string = "\n".join([i.nick if i.nick else i.name for i in nincs_bent])

    if len(bent_van) < 1: bent_string = "Még senki se csatlakozott :slight_frown:"
    if len(nincs_string) < 1: nincs_string = "Mindenki itt van! :partying_face:"

    embed=discord.Embed(title='Na kik hiányoznak?', color=0x9600ff)
    embed.set_author(name='Osztály névsor', icon_url='https://www.tapolca.hu/nagyboldog/sites/default/files/magyar.jpg', url='https://docs.google.com/spreadsheets/d/1xHS9wCUW2TfYcnZP8K7rTTazc5R3eyNEy3djSwD4vVE/edit#gid=0')
    embed.add_field(name='Jelen lévők', value=bent_string, inline=False)
    embed.add_field(name='Hiányzók', value=nincs_string, inline=False)
    embed.set_footer(text='Reagálj a további műveletekhez!')
    
    message = await context.send(embed=embed)
    await message.add_reaction('⚠️')
    global embed_message
    embed_message = message.id



@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if not reaction.message.id == embed_message:
        return
    await reaction.remove(user)
    if user.name != "Laci4":
        if ROLE not in [x.name for x in user.roles]:
            return
    if not reaction.emoji == '⚠️':
        return

    for diakok in nincs_bent:
        await diakok.send('Tessék szépen jönni órára!! :rage: \nEjnye-bejnye!')


@bot.event
async def on_command_error(context: Context, error: errors):
    if type(error) == discord.ext.commands.errors.MissingRequiredArgument:
        await context.reply(
            'Valami nem okés'
        )
    else:
        print(error)



keep_alive()
bot.run(TOKEN)