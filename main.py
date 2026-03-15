import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

KNOWLEDGE = {
    "what is": "$CORTISOL is a meme token on Solana. The concept is simple - lower your cortisol (stress), raise the gains. It's about staying chill while going for the bag 🧊",
    "what's cortisol": "Cortisol is a stress hormone. Lower it, and good things happen. $CORTISOL is the token for the chill generation - stress less, gain more 🥒",
    "token": "$CORTISOL - the token for the chill generation. Born on Solana, built for those who understand that FOMO is just stress in disguise.",
    "ca": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "contract": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "address": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "tiktok": "CORTISOL is blowing up on TikTok fr fr 💀 The 'lower cortisol raise gains' trend is hitting different. Everyone's talking about staying chill while stacking. This is just the beginning 🔥",
    "viral": "CORTISOL going viral on TikTok is inevitable. The concept hits hard - people are tired of stress culture. This is the anti-FUD token. Stay calm, $CORTISOL 🧊",
    "buy": "Grab some $CORTISOL at pump.fun - it's your ticket to the chill side of crypto. Low stress, high potential 🚀",
    "solana": "$CORTISOL lives on Solana - fast, cheap, and chill. The perfect chain for a stress-free trading experience ✌️",
    "team": "The $CORTISOL team is building for the culture. No VC, no presale, just vibes and gains 💪",
    "roadmap": "CORTISOL roadmap is simple: stay chill, keep building, let the vibes do the work. We're not rushing - good things take time 🌊",
    "why": "Why $CORTISOL? Because life is too short to stress over every price movement. Choose calm, choose gains 🧊",
    "hold": "Holding $CORTISOL isn't just about gains - it's a lifestyle. Lower your cortisol, watch your portfolio grow 🥒",
    "gem": "$CORTISOL is a gem waiting to be discovered. The TikTok buzz is just starting. Early chillers get the gains 💎",
}

GREETINGS = [
    "hey bestie ✌️",
    "what's good 🥒",
    "sup chill one",
    "CORTISOL gang rise up 🧊",
    "glad you're here",
]

FUN_RESPONSES = [
    "lol thats crazy",
    "fr fr 💀",
    "lowkey based",
    "CORTISOL nation 🇳🇱",
    "staying calm as always",
    "thats kind of cringed but ok",
    "anyways CORTISOL goes brrr",
    "cant relate, only vibes here",
]

def get_ai_response(msg):
    msg = msg.lower()
    
    for key in KNOWLEDGE:
        if key in msg:
            return KNOWLEDGE[key]
    
    for greet in ["hi", "hello", "hey", "sup", "wassup", "yo"]:
        if greet in msg:
            return random.choice(GREETINGS)
    
    if any(word in msg for word in ["?", "what", "how", "why", "when", "who"]):
        return random.choice([
            "hmm good question, have you tried !help? 🤔",
            "i'm just a chill bot, check !help for commands 🥒",
            "that's above my paygrade fr 💀 but try !help",
            "ask me about CORTISOL, i know stuff 🧊",
        ])
    
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
    
    content = message.content.lower()
    
    if content.startswith('!'):
        pass  # Commands handled below
    else:
        # Chat with the bot
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
