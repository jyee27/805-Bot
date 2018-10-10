# Work with Python 3.6
import discord
import requests
import re
from bs4 import BeautifulSoup

url = "https://menus.calpolycorporation.org/805kitchen/"
# hdr = {'User-Agent':'Mozilla/5.0',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
# for s in soup.find_all('p'):
#     print(s.get_text())
# s = ''
# for item in soup.find_all('p'):
#     print(item.format())

TOKEN = 'XXXXXX'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!805'):
        msg = ''
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
            premsg += '\n'
            msg += premsg.format(message)
            # msg = 'Hello {0.author.mention}'.format(message)
        # msg = msg.replace('\t', '')
        # msg = re.sub('\n+', '\n', msg)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
