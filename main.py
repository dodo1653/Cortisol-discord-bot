import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

KNOWLEDGE = {
    "what is cortisol token": "CORTISOL is a meme token on solana. the idea is simple - lower ur cortisol (stress), raise the gains. stay chill while making that bread",
    "what is": "CORTISOL is a meme token on solana. the idea is simple - lower ur cortisol (stress), raise the gains. stay chill while making that bread",
    "cortisol": "cortisol is the stress hormone. high cortisol = stress = bad gains. CORTISOL token is the solution - stay calm and stack",
    "token": "CORTISOL - the chill token on solana. no stress just gains. ca: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "ca": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "contract": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "address": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "tiktok": "CORTISOL is blowing up on tiktok. the lower cortisol raise gains trend is going crazy. everyone wants to be chill while stacking",
    "viral": "CORTISOL going viral on tiktok is just the start. the stress culture is dying - CORTISOL represents the new way",
    "buy": "get CORTISOL here: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "how to buy": "get CORTISOL here: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "solana": "CORTISOL is on solana - fast transactions low fees perfect for chill trading",
    "team": "devs are building for the culture. no vc no presale just vibes and gains",
    "roadmap": "just chill and watch. good things come to those who wait",
    "why": "because life is too short to stress. CORTISOL = calm mind = fat wallet",
    "hold": "holding CORTISOL is a lifestyle choice. lower cortisol raise gains simple as that",
    "gem": "CORTISOL is the gem. tiktok is just warming up. early chillers eat well",
    "price": "type !price to see the current price and market cap",
    "chart": "type !chart to see the dex screener chart",
    "website": "lowcortisol.site",
    "when": "soon. patience is a virtue. good things come to those who wait",
    "who made": "the CORTISOL team built this for the culture. all about that chill life",
    "utility": "CORTISOL is a meme token. sometimes a token is just a token. the vibes are the utility",
}

GREETINGS = [
    "hey bestie",
    "whats good",
    "sup chill one",
    "CORTISOL gang rise up",
    "glad ur here",
    "ping",
    "pong",
]

FUN_RESPONSES = [
    "lol thats crazy",
    "fr fr",
    "lowkey based",
    "CORTISOL nation",
    "staying calm as always",
    "thats kind of cringed but ok",
    "anyways CORTISOL goes brrr",
    "cant relate only vibes here",
    "low cortisol means big gains",
    "stressed? nah bro",
    "chillax",
    "based",
    "true that",
    "fr fr no cap",
]

def get_ai_response(msg):
    msg = msg.lower().strip()
    
    # exact matches first
    for key in KNOWLEDGE:
        if key in msg or msg in key:
            return KNOWLEDGE[key]
    
    # question handling
    if "what" in msg:
        if "price" in msg or "worth" in msg or "value" in msg:
            return "type !price to see current price and market cap"
        if "ca" in msg or "contract" in msg or "address" in msg:
            return "ca: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
        if "buy" in msg or "get" in msg:
            return "buy here: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
        if "cortisol" in msg or "token" in msg:
            return "CORTISOL = chill token on solana. lower cortisol raise gains. ca: 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
    
    if "how" in msg and "buy" in msg:
        return "buy here: https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"
    
    if "where" in msg and "buy" in msg:
        return "pump.fun bro just search CORTISOL"
    
    if "when" in msg:
        return "soon. the vibes are building. patience"
    
    if "who" in msg:
        if "dev" in msg or "made" in msg or "team" in msg:
            return "the team is building for the culture. no names just gains"
        return "CORTISOL. the chill token. solana chain"
    
    if "why" in msg:
        return "because stress is the enemy of gains. CORTISOL solves it"
    
    # greetings
    for greet in ["hi", "hello", "hey", "sup", "yo", "wassup", "what's good", "what up"]:
        if greet in msg:
            return random.choice(GREETINGS)
    
    # default responses
    if "?" in msg:
        return "good question. try asking about price buy tiktok or just type !help for commands"
    
    return random.choice(FUN_RESPONSES)

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
        response = random.choice(GREETINGS)
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
