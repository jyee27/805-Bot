# Work with Python 3.6
import discord
import requests
from bs4 import BeautifulSoup

url = "https://menus.calpolycorporation.org/805kitchen/"
# hdr = {'User-Agent':'Mozilla/5.0',
#        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
# for s in soup.find_all('p'):
#     print(s.get_text())

TOKEN = 'XXXXXXXXXXXXXX'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!805'):
        for s in soup.find_all('p'):
            msg = s.get_text().format(message)
            # msg = 'Hello {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)