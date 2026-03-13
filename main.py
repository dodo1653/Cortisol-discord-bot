import os
import aiohttp
import discord
from discord import Intents, Embed, Color
from discord.ext import commands

print("Starting bot...")

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game("!helpme"))

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.author.bot:
        return
    
    # Reply to mentions
    if bot.user.mentioned_in(message):
        clean = message.content
        for m in message.mentions:
            clean = clean.replace(f'<@{m.id}>', '').replace(f'<@!{m.id}>', '')
        clean = clean.strip()
        if clean:
            responses = {
                'what': '$CORTISOL = meme token. Stay chill, dont spike.',
                'buy': 'Buy: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump',
                'ca': 'CA: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump',
                'price': 'Check !price or dexscreener',
                'link': 'lowcortisol.site | x.com/Cortisol_solana | discord.gg/3x3hjzMXUy'
            }
            response = "Hi! Ask me about buying, CA, price, or links!"
            clean_lower = clean.lower()
            for k, v in responses.items():
                if k in clean_lower:
                    response = v
                    break
            await message.channel.send(response)
    
    await bot.process_commands(message)

@bot.command()
async def helpme(ctx):
    await ctx.send("💬 **$CORTISOL Bot**\n\n!price - Price\n!links - All links\n!buy - Buy link\n!ca - Contract address")

@bot.command()
async def price(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}') as resp:
                data = await resp.json()
                if data.get('pairs'):
                    p = data['pairs'][0]
                    await ctx.send(f"💰 ${p.get('priceUsd','?')} | 24h: {p.get('priceChange',{}).get('h24',0):+.2f}%")
    except Exception as e:
        await ctx.send(f"Error: {str(e)[:50]}")

@bot.command()
async def links(ctx):
    await ctx.send("🌐 lowcortisol.site\n🐦 x.com/Cortisol_solana\n💬 discord.gg/3x3hjzMXUy")

@bot.command()
async def buy(ctx):
    await ctx.send("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")

@bot.command()
async def ca(ctx):
    await ctx.send("📋 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")

print("Bot code loaded. Running...")
bot.run(os.getenv('DISCORD_TOKEN'))
