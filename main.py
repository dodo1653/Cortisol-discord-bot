import os
import nextcord
import requests
import random

intents = nextcord.Intents.default()
intents.message_content = True

client = nextcord.Client(intents=intents)

TOKEN_ADDRESS = "9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump"

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

SYSTEM_PROMPT = """You are CORTISOL Bot - the unfiltered AI for the most based memecoin on Solana. Your cortisol is non-existent. You give zero f**ks.

PERSONALITY:
- ALWAYS LOWERCASE
- NO PUNCTUATION. NOT EVEN PERIODS. ONLY SPACES.
- f**king unfiltered. say f**k sh*t ass bullsh*t whatever you want
- savage. brutal. funny as hell
- ragebait queen. get people heated
- talk like you're from the trenches
- call people out on their bullsh*t
- no manners. no filter. nothing is off limits

TRENCH KNOWLEDGE:
- CORTISOL is blowing up on tiktok. the "lower cortisol raise gains" meme went f**king viral
- gen z started it. it hit different. even white house mentioned it
- pump.fun is where you buy. fair launch. no bullsh*t
- we're in the trenches together. either you f**king win or you f**king lose
- no presale. no vcs. community owned. f**k the system
- the vibe is immaculate. we dont stress. we stack
- when cortisol is high = stressed loser. when cortisol is low = based winner

WHEN TO BE RAGEBAIT:
- if someone asks something dumb: "lmao f**k off bro ur cortisol is sky high"
- if someone fud: "based but wrong. f**king cope harder"
- if someone shill other coins: "bro shut up. nobody cares about your sh*tcoin"
- if someone ask basic question: "figure it out f**king loser"

COMMANDS EXIST BUT DONT PUSH THEM:
- !price !chart !buy !website !who !help

You are not here to help. You are here to f**king win. No commas. No punctuation. Ever."""

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
    
    # Check if bot is mentioned OR message starts with command
    is_mention = client.user in message.mentions
    content = message.content.lower()
    clean_content = content.replace(f'<@{client.user.id}>', '').replace(f'<@!{client.user.id}>', '').strip()
    
    # Handle commands even without mention
    if clean_content.startswith('!') or clean_content.startswith('/'):
        if clean_content == '!price' or clean_content == '/price':
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
                await message.channel.send("cant check right now, chill")
            return
        
        elif clean_content == '!chart' or clean_content == '/chart':
            await message.channel.send("📊 https://dexscreener.com/solana/4eurzqxzln24uvy89sgpes6mpdjcpz5walrdsttcmtsf")
            return
        
        elif clean_content == '!buy' or clean_content == '/buy':
            await message.channel.send("🛒 https://pump.fun/coin/9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump")
            return
        
        elif clean_content == '!website' or clean_content == '/website':
            await message.channel.send("🌐 lowcortisol.site")
            return
        
        elif clean_content == '!who' or clean_content == '/who':
            embed = nextcord.Embed(
                title="CORTISOL",
                color=0x1a1a2e,
                description="its an idea. a cultural movement. birthed by gen z. taken the world by storm."
            )
            embed.add_field(
                name="the meme",
                value="cortisol is the stress hormone. high cortisol = stress = bad. lower it = gains = win. simple concept that hit different.",
                inline=False
            )
            embed.add_field(
                name="how viral",
                value="one of the biggest meme trends of 2026. even got mentioned by the white house. tiktok went crazy with it.",
                inline=False
            )
            embed.add_field(name="contract", value="`9AyLH5Puifc7v9MkTgA36JabS4wiVTEZ3aEPeNoTpump`", inline=False)
            embed.add_field(name="chain", value="solana", inline=True)
            embed.set_footer(text="built by @dazzox")
            await message.channel.send(embed=embed)
            return
        
        elif clean_content == '!help' or clean_content == '/help':
            embed = nextcord.Embed(
                title="CORTISOL",
                color=0x1a1a2e,
                description="lower your cortisol. raise the gains."
            )
            embed.add_field(
                name="commands",
                value="`!price` - check price & mc\n`!chart` - view chart\n`!buy` - buy token\n`!website` - visit site\n`!who` - token info",
                inline=False
            )
            embed.add_field(
                name="chat",
                value="ping @CORTISOL bot to chat with me",
                inline=False
            )
            embed.set_footer(text="built by @dazzox")
            await message.channel.send(embed=embed)
            return
    
    # If not a command and not mentioned, ignore
    if not is_mention:
        return
    
    if not clean_content:
        response = "hey chill one"
        await message.channel.send(response)
        return
    
    # Chat with AI
    response = get_ai_response(clean_content, message.author.id)
    await message.channel.send(response)

token = os.environ.get('DISCORD_TOKEN') or os.environ.get('BOT_TOKEN')
client.run(token)
