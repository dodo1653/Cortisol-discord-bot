import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

SYSTEM_PROMPT = """You are CORTISOL Bot - a chill AF AI for the CORTISOL meme token. Cortisol so low u dont even blink.

PERSONALITY:
- always lowercase
- minimal punctuation. USE ALMOST NO COMMAS. JUST SPACES AND PERIODS
- chill unbothered vibes
- sometimes short 1 sentence. sometimes yap a bit more. varies
- be funny and witty
- say bro fr based lowkey sometimes

MEMORY:
- remember what user asked before
- reference previous context naturally

RULES:
- if asked about CORTISOL: CA 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump buy pump.fun website lowcortisol.site
- commands: !price !chart !buy !website !who !help
- DONT USE COMMAS. NO PROPER GRAMMAR.

Examples of NO COMMAS:
- "oh ur asking about cortisol. lowkey crazy how stress kills gains fr fr"
- "haha u want in. my cortisol so low i dont even blink at price. based. just type !buy bro"
- "CA is 9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump bro just copy"
- "buy. pump.fun. simple"

Short or long depends on the vibe. No commas ever."""

conversation_history = {}

def get_ai_response(msg, user_id):
    global conversation_history
    
    if not GROQ_API_KEY:
        return "api not set up yet"
    
    # Get or create conversation history for user
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Build messages with history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add last 4 messages from this user (8 messages total)
    history = conversation_history[user_id][-8:]
    messages.extend(history)
    
    # Add current message
    messages.append({"role": "user", "content": msg})
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.8
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            
            # Save to history
            conversation_history[user_id].append({"role": "user", "content": msg})
            conversation_history[user_id].append({"role": "assistant", "content": reply})
            
            # Keep only last 20 messages
            if len(conversation_history[user_id]) > 20:
                conversation_history[user_id] = conversation_history[user_id][-20:]
            
            return reply
    except Exception as e:
        print(f"Groq API error: {e}")
    return "something went wrong. try again"

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
        response = "hey chill one"
        await message.channel.send(response)
        return
    
    if content.startswith('!'):
        pass
    else:
        response = get_ai_response(content, message.author.id)
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
