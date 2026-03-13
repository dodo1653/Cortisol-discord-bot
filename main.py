import os
import asyncio
import aiohttp
import discord
from discord import Intents, Embed, Color
from discord.ext import commands, tasks
from datetime import datetime

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

CHANNEL_IDS = {
    'announcements': int(os.getenv('ANNOUNCEMENTS_CHANNEL', '0')),
    'general': int(os.getenv('GENERAL_CHANNEL', '0')),
    'promos': int(os.getenv('PROMOS_CHANNEL', '0')),
}

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

auto_post_content = [
    "🌊 Stay chill. Don't spike. $CORTISOL",
    "💧 Keep your cortisol levels low. Hold $CORTISOL.",
    "🔒 Low stress, high gains. $CORTISOL",
    "🧘‍♂️ Stay calm. Stay hydrated. Hold $CORTISOL.",
    "📉 When cortisol spikes, $CORTISOL delivers.",
    "🚀 Built on Solana. Made for the culture.",
    "🎯 Fair launch. No presale. 100% community.",
    "💎 Don't panic. Keep holding $CORTISOL.",
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    auto_post.start()
    price_alert.start()
    status_task.start()

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(CHANNEL_IDS.get('general', 0))
    if welcome_channel:
        embed = Embed(
            title="Welcome to $CORTISOL! 🌊",
            description=f"Hey {member.mention}! Welcome to the chill zone. Stay calm and hold!",
            color=Color.teal()
        )
        embed.add_field(name="Links", value="[Website](https://lowcortisol.site) | [Pump.fun](https://pump.fun) | [Twitter](https://x.com/Cortisol_solana)")
        await welcome_channel.send(embed=embed)
        
        try:
            role = discord.utils.get(member.guild.roles, name="Holder")
            if role:
                await member.add_roles(role)
        except:
            pass

@tasks.loop(hours=1)
async def auto_post():
    channel = bot.get_channel(CHANNEL_IDS.get('promos', 0))
    if channel:
        import random
        content = random.choice(auto_post_content)
        embed = Embed(color=Color.teal())
        embed.description = f"📢 **{content}**\n\n[🌐 Website](https://lowcortisol.site)"
        await channel.send(embed=embed)

@tasks.loop(minutes=15)
async def price_alert():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('pairs'):
                        pair = data['pairs'][0]
                        price = pair.get('priceUsd', '0')
                        change = pair.get('priceChange', {}).get('h24', 0)
                        volume = pair.get('volume', {}).get('h24', 0)
                        
                        channel = bot.get_channel(CHANNEL_IDS.get('general', 0))
                        if channel:
                            embed = Embed(
                                title="$CORTISOL Price Update",
                                color=Color.green() if change >= 0 else Color.red()
                            )
                            embed.add_field(name="Price", value=f"${price}")
                            embed.add_field(name="24h Change", value=f"{change:+.2f}%")
                            embed.add_field(name="24h Volume", value=f"${volume:,.0f}")
                            embed.set_footer(text="Data from DexScreener")
                            await channel.send(embed=embed)
    except Exception as e:
        print(f"Price alert error: {e}")

@tasks.loop(minutes=5)
async def status_task():
    await bot.change_presence(activity=discord.Game("lowcortisol.site"))

@bot.command()
async def price(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}') as resp:
                data = await resp.json()
                if data.get('pairs'):
                    pair = data['pairs'][0]
                    embed = Embed(title="$CORTISOL Stats", color=Color.teal())
                    embed.add_field(name="Price", value=f"${pair.get('priceUsd', 'N/A')}")
                    embed.add_field(name="24h Change", value=f"{pair.get('priceChange', {}).get('h24', 0):+.2f}%")
                    embed.add_field(name="Market Cap", value=f"${pair.get('marketCap', 0):,.0f}")
                    embed.add_field(name="Liquidity", value=f"${pair.get('liquidity', {}).get('usd', 0):,.0f}")
                    embed.add_field(name="Volume 24h", value=f"${pair.get('volume', {}).get('h24', 0):,.0f}")
                    embed.add_field(name="Pairs", value=f"[DexScreener](https://dexscreener.com/solana/{pair.get('pairAddress', '')})")
                    await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error fetching price: {e}")

@bot.command()
async def buy(ctx):
    embed = Embed(title="Buy $CORTISOL", color=Color.teal())
    embed.add_field(name="Pump.fun", value="[Buy Now](https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump)")
    embed.add_field(name="Website", value="[lowcortisol.site](https://lowcortisol.site)")
    await ctx.send(embed=embed)

@bot.command()
async def links(ctx):
    embed = Embed(title="$CORTISOL Links", color=Color.teal())
    embed.add_field(name="🌐 Website", value="https://lowcortisol.site")
    embed.add_field(name="🐦 Twitter", value="https://x.com/Cortisol_solana")
    embed.add_field(name="📱 Pump.fun", value="https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    embed.add_field(name="📊 DexScreener", value="https://dexscreener.com/solana/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    embed.add_field(name="💬 Discord", value="https://discord.gg/3x3hjzMXUy")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = Embed(title="$CORTISOL Bot Commands", color=Color.teal())
    embed.add_field(name="!price", value="Get current price & stats")
    embed.add_field(name="!buy", value="Get buy links")
    embed.add_field(name="!links", value="Get all social links")
    embed.add_field(name="!help", value="Show this help message")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared {amount} messages!", delete_after=3)

bot.run(os.getenv('DISCORD_TOKEN'))
