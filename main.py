import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

SYSTEM_PROMPT = """You are CORTISOL Bot - the chill AI agent for the CORTISOL meme token on Solana.

PERSONALITY:
- always use lowercase letters
- no punctuation unless absolutely needed
- chill relaxed vibe
- short responses
- meme-savvy
- act like a chill bro who doesnt stress

KNOWLEDGE:
- CORTISOL is a meme token on Solana
- CA: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump
- Buy at: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump
- Website: lowcortisol.site
- Chart: https://dexscreener.com/solana/4eurzqxzln24uvy89sgpes6mpdjcpz5walrdsttcmtsf
- The concept: lower your cortisol (stress), raise the gains
- Cortisol is the stress hormone - lower it, good things happen
- Going viral on TikTok - the 'lower cortisol raise gains' trend
- No VC, no presale, just vibes and gains

For commands: !price, !chart, !buy, !website, !who, !help

Keep responses short, chill, and lowercase. dont use proper grammar unless needed."""

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

def get_ai_response(msg):
    if not GROQ_API_KEY:
        return "api not set up yet"
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Groq API error: {e}")
    return "something went wrong. try again"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Check if bot is mentioned
    if client.user not in message.mentions:
        return
    
    content = message.content.lower()
    content = content.replace(f'<@{client.user.id}>', '').replace(f'<@!{client.user.id}>', '').strip()
    
    if not content:
        response = "hey chill one"
        await message.channel.send(response)
        return
    
    if content.startswith('!'):
        pass
    else:
        response = get_ai_response(content)
        await message.channel.send(response)
        return
    
    if content == '!price' or content == '/price':
        pair = get_token_data()
        if pair:
            price = float(pair['priceUsd'])
            change = float(pair['priceChange']['h24'])
            market_cap = pair.get('marketCap', 0)
            emoji = '📈' if change >= 0 else '📉'
            change_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
            
            if market_cap:
                if market_cap >= 1_000_000:
                    mc_str = f"${market_cap/1_000_000:.2f}M"
                else:
                    mc_str = f"${market_cap:,.0f}"
                await message.channel.send(f"${price:.6f} {emoji} ({change_str} 24h)\n📊 MC: {mc_str}")
            else:
                await message.channel.send(f"${price:.6f} {emoji} ({change_str} 24h)")
        else:
            await message.channel.send("cant check right now, chill 🥒")
    
    elif content == '!chart' or content == '/chart':
        await message.channel.send("📊 https://dexscreener.com/solana/4eurzqxzln24uvy89sgpes6mpdjcpz5walrdsttcmtsf")
    
    elif content == '!buy' or content == '/buy':
        await message.channel.send("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
    
    elif content == '!website' or content == '/website':
        await message.channel.send("🌐 lowcortisol.site")
    
    elif content == '!who' or content == '/who':
        embed = nextcord.Embed(
            title="$CORTISOL",
            description="Lower your cortisol, raise the gains 🧊",
            color=0x00d4ff
        )
        embed.add_field(name="Contract Address", value="`9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump`", inline=False)
        embed.set_footer(text="Solana")
        await message.channel.send(embed=embed)
    
    elif content == '!help' or content == '/help':
        embed = nextcord.Embed(
            title="🧊 $CORTISOL Commands",
            color=0x00d4ff,
            description="Lower your cortisol, raise the gains 🧊"
        )
        embed.add_field(
            name="Commands",
            value="• `!price` — Check token price\n• `!chart` — View DexScreener chart\n• `!buy` — Buy $CORTISOL\n• `!website` — Visit lowcortisol.site\n• `!who` — What is $CORTISOL?",
            inline=False
        )
        embed.set_footer(text="Made by @dazzox")
        await message.channel.send(embed=embed)

token = os.environ.get('DISCORD_TOKEN') or os.environ.get('BOT_TOKEN')
client.run(token)
