import os
import aiohttp
import discord
from discord import Intents, Embed, Color
from discord.ext import commands

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

async def fetch_price():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}') as resp:
                data = await resp.json()
                if data.get('pairs'):
                    pair = data['pairs'][0]
                    return {
                        'price': pair.get('priceUsd', 'N/A'),
                        'change': pair.get('priceChange', {}).get('h24', 0),
                        'volume': pair.get('volume', {}).get('h24', 0),
                        'market_cap': pair.get('marketCap', 0)
                    }
    except:
        pass
    return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    price_data = await fetch_price()
    if price_data:
        mc = price_data['market_cap']
        if mc >= 1000000:
            mc_str = f"${mc/1000000:.1f}M"
        else:
            mc_str = f"${mc:,.0f}"
        await bot.change_presence(activity=discord.Game(f"MC: {mc_str} | lowcortisol.site"))
    else:
        await bot.change_presence(activity=discord.Game("lowcortisol.site"))

# ===== MODERATION =====

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clear messages"""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Cleared {amount} messages", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member"""
    await member.kick(reason=reason)
    await ctx.send(f"✅ Kicked {member.mention}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a member"""
    await member.ban(reason=reason)
    await ctx.send(f"✅ Banned {member.mention}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    """Mute a member"""
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f"✅ Muted {member.mention}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """Unmute a member"""
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role:
        await member.remove_roles(muted_role)
        await ctx.send(f"✅ Unmuted {member.mention}")

# ===== ANNOUNCEMENTS =====

@bot.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, message):
    """Post an announcement embed"""
    embed = Embed(
        title="📢 Announcement",
        description=message,
        color=Color.teal()
    )
    embed.set_footer(text="$CORTISOL")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def promo(ctx, *, message):
    """Post a promotional embed"""
    embed = Embed(
        description=f"**{message}**",
        color=Color.teal()
    )
    embed.add_field(name="🌐 Links", value="[Website](https://lowcortisol.site) | [Twitter](https://x.com/Cortisol_solana) | [Discord](https://discord.gg/3x3hjzMXUy)")
    embed.set_footer(text="$CORTISOL")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(manage_messages=True)
async def priceembed(ctx):
    """Post current price embed"""
    price_data = await fetch_price()
    
    if price_data:
        embed = Embed(
            title="$CORTISOL Price Update",
            color=Color.green() if price_data['change'] >= 0 else Color.red()
        )
        embed.add_field(name="💰 Price", value=f"${price_data['price']}")
        embed.add_field(name="📈 24h Change", value=f"{price_data['change']:+.2f}%")
        embed.add_field(name="📊 Market Cap", value=f"${price_data['market_cap']:,.0f}")
        embed.add_field(name="🔥 Volume 24h", value=f"${price_data['volume']:,.0f}")
        embed.add_field(name="🔗 Links", value="[Buy](https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump) | [DexScreener](https://dexscreener.com/solana/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump)")
        embed.set_footer(text="Data from DexScreener")
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.send("❌ Could not fetch price data")

# ===== INFO COMMANDS =====

@bot.command()
async def price(ctx):
    """Get current price"""
    price_data = await fetch_price()
    if price_data:
        embed = Embed(title="$CORTISOL Stats", color=Color.teal())
        embed.add_field(name="Price", value=f"${price_data['price']}")
        embed.add_field(name="24h Change", value=f"{price_data['change']:+.2f}%")
        embed.add_field(name="Market Cap", value=f"${price_data['market_cap']:,.0f}")
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Could not fetch price")

@bot.command()
async def links(ctx):
    """Get all links"""
    embed = Embed(title="$CORTISOL Links", color=Color.teal())
    embed.add_field(name="🌐 Website", value="https://lowcortisol.site")
    embed.add_field(name="🐦 Twitter", value="https://x.com/Cortisol_solana")
    embed.add_field(name="📱 Pump.fun", value="https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    embed.add_field(name="📊 DexScreener", value="https://dexscreener.com/solana/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    embed.add_field(name="💬 Discord", value="https://discord.gg/3x3hjzMXUy")
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx):
    """Get buy links"""
    embed = Embed(title="Buy $CORTISOL", color=Color.teal())
    embed.add_field(name="Pump.fun", value="[Buy Now](https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump)")
    embed.add_field(name="Website", value="[lowcortisol.site](https://lowcortisol.site)")
    await ctx.send(embed=embed)

@bot.command()
async def helpme(ctx):
    """Show help menu"""
    embed = Embed(title="$CORTISOL Bot Commands", color=Color.teal())
    embed.add_field(name="📊 Info", value="`!price` - Get price\n`!links` - All links\n`!buy` - Buy links")
    embed.add_field(name="🎛️ Moderation", value="`!clear [amount]` - Clear messages\n`!kick @user` - Kick\n`!ban @user` - Ban\n`!mute @user` - Mute\n`!unmute @user` - Unmute")
    embed.add_field(name="📢 Announcements", value="`!announce [msg]` - Announcement\n`!promo [msg]` - Promo\n`!priceembed` - Price update")
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        await ctx.send(f"❌ Error: {str(error)}")

bot.run(os.getenv('DISCORD_TOKEN'))
