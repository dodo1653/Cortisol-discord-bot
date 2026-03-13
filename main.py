import os
import aiohttp
import discord
from discord import Intents, Embed, Color
from discord.ext import commands

print("Loading bot...")

intents = Intents.all()
print(f"Intents: {intents}")

bot = commands.Bot(command_prefix='!', intents=intents)
print("Bot created")

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

@bot.event
async def on_ready():
    print(f'READY: Logged in as {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game("!helpme"))

@bot.event
async def on_message(message):
    print(f"MSG: {message.author}: {message.content[:50]}")
    try:
        await bot.process_commands(message)
    except Exception as e:
        print(f"Error: {e}")

@bot.command()
async def test(ctx):
    print(f"Test command from {ctx.author}")
    await ctx.send("✅ Bot is working!")

@bot.command()
async def helpme(ctx):
    await ctx.send("💬 **$CORTISOL Bot Commands:**\n\n!test - Test bot\n!price - Get price\n!links - All links\n!buy - Buy link\n!ca - Contract address")

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
        await ctx.send(f"Error: {str(e)[:100]}")

@bot.command()
async def links(ctx):
    await ctx.send("🌐 lowcortisol.site\n🐦 x.com/Cortisol_solana\n💬 discord.gg/3x3hjzMXUy")

@bot.command()
async def buy(ctx):
    await ctx.send("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")

@bot.command()
async def ca(ctx):
    await ctx.send("📋 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")

print("Starting bot...")
bot.run(os.getenv('DISCORD_TOKEN'))
