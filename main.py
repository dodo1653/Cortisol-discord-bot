import os
import discord
from discord import app_commands
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced!")

client = MyClient()

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

def get_token_data():
    try:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('pairs') and len(data['pairs']) > 0:
                return data['pairs'][0]
    except:
        pass
    return None

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Bot ID: {client.user.id}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content.lower()
    
    if content.startswith('!price'):
        pair = get_token_data()
        if pair:
            price = float(pair['priceUsd'])
            change = float(pair['priceChange']['h24'])
            emoji = '📈' if change >= 0 else '📉'
            change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            await message.channel.send(f"${price:.6f} {emoji} ({change_str} 24h)")
        else:
            await message.channel.send("cant check right now, chill 🥒")
    
    elif content.startswith('!chart'):
        await message.channel.send("📊 https://dexscreener.com/solana/4eurzqxzln24uvy89sgpes6mpdjcpz5walrdsttcmtsf")
    
    elif content.startswith('!buy'):
        await message.channel.send("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    
    elif content.startswith('!website'):
        await message.channel.send("🌐 lowcortisol.site")
    
    elif content.startswith('!who'):
        await message.channel.send("$CORTISOL - lower your cortisol, raise the gains 🧊")
    
    elif content.startswith('!help'):
        await message.channel.send("🧊 **$CORTISOL Commands**\n\n!price - check price\n!chart - view chart\n!buy - buy\n!website - visit site\n!who - what is this")

@client.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong 🏓")

@client.tree.command()
async def price(interaction: discord.Interaction):
    pair = get_token_data()
    if pair:
        price = float(pair['priceUsd'])
        change = float(pair['priceChange']['h24'])
        emoji = '📈' if change >= 0 else '📉'
        change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
        await interaction.response.send_message(f"${price:.6f} {emoji} ({change_str} 24h)")
    else:
        await interaction.response.send_message("cant check right now, chill 🥒")

@client.tree.command()
async def chart(interaction: discord.Interaction):
    await interaction.response.send_message("📊 https://dexscreener.com/solana/4eurzqxzln24uvy89sgpes6mpdjcpz5walrdsttcmtsf")

@client.tree.command()
async def buy(interaction: discord.Interaction):
    await interaction.response.send_message("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")

@client.tree.command()
async def website(interaction: discord.Interaction):
    await interaction.response.send_message("🌐 lowcortisol.site")

@client.tree.command()
async def who(interaction: discord.Interaction):
    await interaction.response.send_message("$CORTISOL - lower your cortisol, raise the gains 🧊")

@client.tree.command()
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🧊 **$CORTISOL Commands**\n\n"
        "`/price` - check the price\n"
        "`/chart` - view chart\n"
        "`/buy` - buy $CORTISOL\n"
        "`/website` - visit site\n"
        "`/who` - what is this\n"
        "`/ping` - pong"
    )

client.run(os.getenv('DISCORD_TOKEN'))
