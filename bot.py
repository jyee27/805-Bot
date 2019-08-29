# Work with Python 3.6
import discord
import requests
import re
import datetime
import asyncio
from bs4 import BeautifulSoup

url = "https://menus.calpolycorporation.org/805kitchen/"
# hdr = {'User-Agent':'Mozilla/5.0',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# for s in soup.find_all('p'):
#     print(s.get_text())
# s = ''
# for item in soup.find_all('p'):
#     print(item.format())

TOKEN = 'insert token here'
CHANNEL_ID = 'insert channel id here'

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!805t'):
        msgs = get_message_list()
        for msg in msgs:
            await client.send_message(message.channel, msg)
    elif message.content.startswith('!805'):
        emblst = get_message_embed_list()
        for emb in emblst:
            await client.send_message(message.channel, embed=emb)


async def scheduled_message():
    await client.wait_until_ready()
    channel = discord.Object(id=CHANNEL_ID)
    while not client.is_closed:
        t = datetime.datetime.now()
        if t.hour == 8 and t.minute == 5:
            emblst = get_message_embed_list()
            for emb in emblst:
                await client.send_message(channel, embed=emb)
            await asyncio.sleep(84600) # wait 23 hours and 30 minutes before checking again
        await asyncio.sleep(60)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def get_message_list():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    msg = ''
    lst = []
    title = "***805 Kitchen Menu***\n"
    for s in soup.find_all('h3'):
        if s.get_text() != 'Legend':
            title += "*" + s.get_text() + "*"
    title += "\n"
    msg += title
    for s in soup.find_all(['h2', 'h4', 'p']):
        premsg = s.get_text()
        premsg = premsg.replace('\t', '')
        premsg = re.sub('\n+', '', premsg)
        premsg = premsg.strip()
        if s.name == 'h2':
            premsg = '\n**' + premsg + '**'
        elif s.name == 'h4':
            premsg = '\n\t*' + premsg + '*'
        elif s.name == 'p':
            premsg = '\t\t' + premsg
            for img in s.find_all('img'):
                if img['alt'] == 'Vegetarian':
                    premsg += ' <:vegetarian:499693084117041153>'
                if img['alt'] == 'Vegan':
                    premsg += ' <:vegan:499693108825554945>'
        premsg += '\n'
        if len(msg) + len(premsg) > 2000:
            lst.append(msg)
            msg = premsg
        msg += premsg
    if len(msg) > 0:
        lst.append(msg)
    return lst


def get_message_embed_list():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ttl = "**805 Kitchen Menu**"
    embed = discord.Embed(title=ttl)
    lst = []
    fname = ''
    fval = ''
    current_embed_empty = True
    for s in soup.find_all('h3'):
        if s.get_text() != 'Legend':
            embed.description = s.get_text()
    lst.append(embed)
    embed = discord.Embed(title='')
    embed_length = 0
    num_fields = 0
    for s in soup.find_all(['h2', 'h4', 'p']):
        premsg = s.get_text()
        premsg = premsg.replace('\t', '')
        premsg = re.sub('\n+', '', premsg)
        premsg = premsg.strip()
        if s.name == 'h2':
            if len(embed.title) > 0:
                if not current_embed_empty:
                   lst.append(embed)
                embed_length = 0
                embed = discord.Embed(title='')
                current_embed_empty = True
            embed.title = '**' + premsg + '**'
            embed_length += len(premsg) + 4
        elif s.name == 'h4':
            if len(fname) > 0:
                if len(fval) == 0:
                    fval += '[empty]'
                else:
                    current_embed_empty = False
                embed_length += len(fname) + len(fval)
                embed.add_field(name=fname, value=fval, inline=False)
                fval = ''
            fname = premsg
        elif s.name == 'p':
            if(len(fval) + len(premsg) + 64 > 1024):
                embed.add_field(name=fname, value=fval, inline=False)
                fval = ''
                fname = '--'
            for img in s.find_all('img'):
                if img['alt'] == 'Vegetarian':
                    premsg += ' <:vegetarian:499693084117041153>'
                if img['alt'] == 'Vegan':
                    premsg += ' <:vegan:499693108825554945>'
            fval += premsg + '\n'
        if embed_length + len(fname) + len(fval) > 5500 or len(embed.fields) > 23:
            # Add current embed to list and start a new one
            if not current_embed_empty:
                lst.append(embed)
            embed = discord.Embed(title='')
            embed_length = 0
            current_embed_empty = True
    if len(fname) > 0:
        if len(fval) == 0:
            fval += '[empty]'
        embed.add_field(name=fname, value=fval, inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    if not current_embed_empty:
        lst.append(embed)
    return lst
    
    
async def dontcrash(): # ping discord every 50 seconds
    channels = client.get_all_channels()
    asyncio.sleep(50)
    

if __name__ == "__main__":
    client.loop.create_task(scheduled_message())
    client.loop.create_task(dontcrash())
    client.run(TOKEN)
