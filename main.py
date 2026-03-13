import os
import re
import aiohttp
import discord
from discord import Intents, Embed, Color
from discord.ext import commands

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

# Knowledge base about $CORTISOL
KNOWLEDGE = {
    'what': [
        "$CORTISOL is a meme token on Solana, inspired by the viral 'cortisol spike' meme.",
        "$CORTISOL is a meme coin built on Solana. The meme is about stress hormones - when your cortisol spikes, you make bad decisions. $CORTISOL says stay chill, don't spike.",
        "A meme token on Solana dedicated to staying calm. The meme: when cortisol spikes, you FOMO in. We say stay unbothered."
    ],
    'buy': [
        "You can buy $CORTISOL on Pump.fun: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
        "Buy $CORTISOL here: https://lowcortisol.site - click 'View Token' to buy on Pump.fun!"
    ],
    'contract': [
        "CA: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
        "Contract Address: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump (Solana)"
    ],
    'ca': [
        "CA: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
        "Contract Address: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
    ],
    'price': [
        "Check the price with !price command or visit https://dexscreener.com/solana/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
    ],
    'where': [
        "Buy $CORTISOL on Pump.fun: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
        "Trade $CORTISOL on https://dexscreener.com/solana/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
    ],
    'how to': [
        "To buy $CORTISOL: 1) Get a Solana wallet (Phantom/Solflare) 2) Buy SOL 3) Go to https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump 4) Swap SOL for $CORTISOL"
    ],
    'who': [
        "$CORTISOL is a community-owned meme token. No team allocation, fair launch.",
        "Built by the community, for the community. Fair launch, no presale."
    ],
    'website': [
        "Official website: https://lowcortisol.site"
    ],
    'link': [
        "Website: https://lowcortisol.site\nTwitter: https://x.com/Cortisol_solana\nPump.fun: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump\nDiscord: https://discord.gg/3x3hjzMXUy"
    ],
    'twitter': [
        "Twitter: https://x.com/Cortisol_solana"
    ],
    'x.com': [
        "Twitter: https://x.com/Cortisol_solana"
    ],
    'discord': [
        "Discord: https://discord.gg/3x3hjzMXUy"
    ],
    'tiktok': [
        "TikTok: https://www.tiktok.com/@foreverlowcortisol"
    ],
    'solana': [
        "$CORTISOL is built on Solana blockchain - fast, cheap transactions."
    ],
    'utility': [
        "$CORTISOL is purely a meme token. It raises awareness about stress management and mental health."
    ],
    'supply': [
        "Total supply: 1 billion tokens (1B)"
    ],
    'tax': [
        "0% buy tax / 0% sell tax"
    ],
    'hello': [
        "Hey! Welcome to $CORTISOL! Stay chill, don't spike."
    ],
    'hi': [
        "Hi there! Stay calm, hold $CORTISOL!"
    ],
    'hey': [
        "Hey! Need info about $CORTISOL? Just ask!"
    ],
    'sup': [
        "All good! Just here staying chill with $CORTISOL"
    ],
    'gm': [
        "GM! Hope your cortisol levels are low today!"
    ],
    'gn': [
        "GN! Sleep well, don't let cortisol spike!"
    ],
    'help': [
        "I can answer questions about $CORTISOL! Ask me about:\n- What is $CORTISOL\n- How to buy\n- Contract address\n- Price\n- Links\n\nOr use commands: !price, !links, !buy"
    ]
}

def get_response(message):
    msg = message.lower()
    for key, responses in KNOWLEDGE.items():
        if key in msg:
            import random
            return random.choice(responses)
    return "I'm here to help with $CORTISOL! Ask me about buying, the contract address, price, or check out !links for all our socials!"

# ===== CHATBOT =====

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    bot_mentioned = bot.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)
    
    if bot_mentioned or is_dm:
        clean_message = message.content
        for mention in message.mentions:
            clean_message = clean_message.replace(f'@{mention.name}', '').replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        
        if clean_message.strip():
            response = get_response(clean_message.strip())
            await message.channel.send(response)
    
    await bot.process_commands(message)

# ===== COMMANDS =====

@bot.command()
async def ask(ctx, *, question):
    response = get_response(question)
    await ctx.send(response)

@bot.command()
async def price(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                if data.get('pairs') and len(data['pairs']) > 0:
                    pair = data['pairs'][0]
                    embed = Embed(title="$CORTISOL Stats", color=Color.teal())
                    embed.add_field(name="Price", value=f"${pair.get('priceUsd', 'N/A')}")
                    embed.add_field(name="24h", value=f"{pair.get('priceChange', {}).get('h24', 0):+.2f}%")
                    embed.add_field(name="MC", value=f"${pair.get('marketCap', 0):,.0f}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Could not fetch price")
    except:
        await ctx.send("Error fetching price")

@bot.command()
async def links(ctx):
    embed = Embed(title="$CORTISOL Links", color=Color.teal())
    embed.add_field(name="Website", value="https://lowcortisol.site")
    embed.add_field(name="Twitter", value="https://x.com/Cortisol_solana")
    embed.add_field(name="Pump.fun", value="https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    embed.add_field(name="Discord", value="https://discord.gg/3x3hjzMXUy")
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx):
    embed = Embed(title="Buy $CORTISOL", color=Color.teal())
    embed.add_field(name="Pump.fun", value="https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    await ctx.send(embed=embed)

@bot.command()
async def ca(ctx):
    await ctx.send("CA: `9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump`")

@bot.command()
async def helpme(ctx):
    embed = Embed(title="$CORTISOL Bot", color=Color.teal())
    embed.add_field(name="Chat", value="Tag me or DM me with your questions!")
    embed.add_field(name="Commands", value="!ask [question], !price, !links, !buy, !ca")
    await ctx.send(embed=embed)

# Moderation
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages", delete_after=3)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, message):
    embed = Embed(title="Announcement", description=message, color=Color.teal())
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def promo(ctx, *, message):
    embed = Embed(description=f"{message}", color=Color.teal())
    embed.add_field(name="Links", value="Website: lowcortisol.site | X: @Cortisol_solana")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game("!helpme | Ask me about $CORTISOL"))

# Run bot
token = os.getenv('DISCORD_TOKEN')
if not token:
    print("ERROR: Set DISCORD_TOKEN environment variable!")
else:
    bot.run(token)
