import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

KNOWLEDGE = {
    "what is": "$CORTISOL is a meme token on solana. the concept is simple - lower your cortisol (stress), raise the gains. its about staying chill while going for the bag",
    "what's cortisol": "cortisol is a stress hormone. lower it and good things happen. $CORTISOL is the token for the chill generation - stress less gain more",
    "token": "$CORTISOL - the token for the chill generation. born on solana built for those who understand that FOMO is just stress in disguise.",
    "ca": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "contract": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "address": "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump",
    "tiktok": "CORTISOL is blowing up on tiktok fr fr. the 'lower cortisol raise gains' trend is hitting different. everyone talking about staying chill while stacking. this is just the beginning",
    "viral": "CORTISOL going viral on tiktok is inevitable. the concept hits hard - people are tired of stress culture. this is the anti-FUD token. stay calm $CORTISOL",
    "buy": "grab some $CORTISOL at pump.fun - ur ticket to the chill side of crypto. low stress high potential",
    "solana": "$CORTISOL lives on solana - fast cheap and chill. the perfect chain for a stress-free trading experience",
    "team": "the $CORTISOL team is building for the culture. no VC no presale just vibes and gains",
    "roadmap": "CORTISOL roadmap is simple: stay chill keep building let the vibes do the work. were not rushing - good things take time",
    "why": "why $CORTISOL? because life is too short to stress over every price movement. choose calm choose gains",
    "hold": "holding $CORTISOL isnt just about gains - its a lifestyle. lower ur cortisol watch ur portfolio grow",
    "gem": "$CORTISOL is a gem waiting to be discovered. the tiktok buzz is just starting. early chillers get the gains",
}

GREETINGS = [
    "hey bestie",
    "whats good",
    "sup chill one",
    "CORTISOL gang rise up",
    "glad ur here",
]

FUN_RESPONSES = [
    "lol thats crazy",
    "fr fr",
    "lowkey based",
    "CORTISISL nation",
    "staying calm as always",
    "thats kind of cringed but ok",
    "anyways CORTISOL goes brrr",
    "cant relate only vibes here",
    "low cortisol means big gains",
    "stressed? nah bro",
    "chillax",
]

def get_ai_response(msg):
    msg = msg.lower()
    
    for key in KNOWLEDGE:
        if key in msg:
            return KNOWLEDGE[key]
    
    for greet in ["hi", "hello", "hey", "sup", "wassup", "yo", "ping"]:
        if greet in msg:
            return random.choice(GREETINGS)
    
    if any(word in msg for word in ["?", "what", "how", "why", "when", "who"]):
        return random.choice([
            "hmm good question have u tried help",
            "im just a chill bot check help for commands",
            "thats above my paygrade fr but try help",
            "ask me about CORTISOL i know stuff",
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
