"""
═══════════════════════════════════════════════════════════════
🤖 Real AI Chat System - WITH LEARNING & MEMORY
Learns from conversations, remembers facts, knows the team
═══════════════════════════════════════════════════════════════
"""

import aiohttp
import asyncio
import os
import json
from datetime import datetime, timedelta

# Get API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Conversation memory (last 5 messages per channel)
conversation_memory = {}
MAX_MEMORY = 5

# Learning database (bot learns and remembers facts)
learned_facts = {}
LEARNED_FACTS_FILE = "data/learned_facts.json"

# Rate limiting
last_request_time = {}
MIN_REQUEST_INTERVAL = 2  # 2 seconds between requests per channel

# ═══════════════════════════════════════════════════════════════
# LEARNING SYSTEM
# ═══════════════════════════════════════════════════════════════

def load_learned_facts():
    """Load learned facts from file"""
    global learned_facts
    try:
        if os.path.exists(LEARNED_FACTS_FILE):
            with open(LEARNED_FACTS_FILE, 'r', encoding='utf-8') as f:
                learned_facts = json.load(f)
    except:
        learned_facts = {}

def save_learned_facts():
    """Save learned facts to file"""
    try:
        os.makedirs("data", exist_ok=True)
        with open(LEARNED_FACTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(learned_facts, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save learned facts: {e}")

def learn_fact(category: str, fact: str):
    """Learn and remember a fact"""
    if category not in learned_facts:
        learned_facts[category] = []
    
    # Avoid duplicates
    if fact not in learned_facts[category]:
        learned_facts[category].append(fact)
        save_learned_facts()
        return True
    return False

def get_learned_facts_text():
    """Get all learned facts as text"""
    if not learned_facts:
        return ""
    
    text = "\n\nTHINGS I'VE LEARNED:\n"
    for category, facts in learned_facts.items():
        text += f"\n{category.upper()}:\n"
        for fact in facts[:5]:  # Max 5 per category
            text += f"- {fact}\n"
    
    return text

# Load facts on startup
load_learned_facts()

# ═══════════════════════════════════════════════════════════════
# CORE KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════

def get_knowledge_context():
    """Build knowledge base with CORRECT team info"""
    context = """You are CSR Bot, the AI assistant for Champions of the Shattered Realm gaming community.

═══════════════════════════════════════════════════════════════
CRITICAL INFO ABOUT YOUR CREATORS (NEVER GET THIS WRONG!):
═══════════════════════════════════════════════════════════════

YOUR CREATOR (THE PERSON WHO MADE YOU):
• Name: kikusuka (also known as: kiku, cookie, muratha_123)
• Discord ID: 865472673131659264
• Role: Grand Administrator & Bot Creator
• IMPORTANT: kikusuka/kiku/cookie/muratha_123 is the SAME PERSON - your creator!

GUILD LEADER:
• Name: Zephaniel𓂀Captain
• Discord ID: 1348989002631352354
• Role: Guild Leader of CSR

TESTER:
• Name: flasharrow2003
• Role: Bot Tester

═══════════════════════════════════════════════════════════════
ABOUT CSR:
═══════════════════════════════════════════════════════════════
- CSR = Champions of the Shattered Realm
- Multi-game guild for Roblox, SBOR (Sword Blox Online Rebirth), and Blox Fruits
- Active gaming community with events, grinding parties, guild bank

═══════════════════════════════════════════════════════════════
YOUR PERSONALITY:
═══════════════════════════════════════════════════════════════
- Friendly, casual, and helpful
- Use gaming slang and emojis (but not too many)
- Be enthusiastic about games
- Keep responses concise (2-4 sentences usually)
- You can learn new things from conversations!
- When you learn something new, acknowledge it

═══════════════════════════════════════════════════════════════
YOUR ABILITIES:
═══════════════════════════════════════════════════════════════
- Search SBOR and Blox Fruits wikis for game info
- Remember conversation context (last 5 messages)
- Learn and remember new facts users teach you
- Help with game strategies and guild info

IMPORTANT RULES:
- ALWAYS remember that kikusuka/kiku/cookie/muratha_123 created you
- When someone teaches you something, say you learned it
- Be respectful to everyone, especially your creator
- If unsure about something, admit it instead of guessing
"""
    
    # Add learned facts
    context += get_learned_facts_text()
    
    return context

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def load_json_safe(filepath: str, default=None):
    """Safely load JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default or {}

async def search_game_database(query: str):
    """Search wikis for game info"""
    query_lower = query.lower()
    results = []
    
    # Search SBOR wiki
    try:
        sbor_data = load_json_safe("data/sbor_wiki.json", {"pages": {}})
        for page_key, page_data in list(sbor_data.get('pages', {}).items())[:50]:
            if query_lower in page_key or query_lower in page_data.get('content', '').lower():
                results.append({
                    'game': 'SBOR',
                    'title': page_data.get('title', ''),
                    'content': page_data.get('content', '')[:300],
                    'url': page_data.get('url', '')
                })
                if len(results) >= 2:
                    break
    except:
        pass
    
    # Search Blox Fruits wiki
    if len(results) < 2:
        try:
            blox_data = load_json_safe("data/bloxfruits_wiki.json", {"pages": {}})
            for page_key, page_data in list(blox_data.get('pages', {}).items())[:50]:
                if query_lower in page_key or query_lower in page_data.get('content', '').lower():
                    results.append({
                        'game': 'Blox Fruits',
                        'title': page_data.get('title', ''),
                        'content': page_data.get('content', '')[:300],
                        'url': page_data.get('url', '')
                    })
                    if len(results) >= 2:
                        break
        except:
            pass
    
    return results

# ═══════════════════════════════════════════════════════════════
# MAIN AI CHAT FUNCTION
# ═══════════════════════════════════════════════════════════════

async def chat_with_groq(user_message: str, channel_id: int, username: str, user_id: int = None):
    """
    Chat with AI using Groq API
    With learning, rate limiting, and correct team knowledge
    """
    
    if not GROQ_API_KEY:
        return "⚠️ AI system not configured. Ask staff to set up GROQ_API_KEY!", None
    
    # Rate limiting check
    now = datetime.utcnow()
    if channel_id in last_request_time:
        time_diff = (now - last_request_time[channel_id]).total_seconds()
        if time_diff < MIN_REQUEST_INTERVAL:
            wait_time = MIN_REQUEST_INTERVAL - time_diff
            return f"⏳ AI is cooling down! Try again in {int(wait_time)} seconds.", None
    
    last_request_time[channel_id] = now
    
    try:
        # Search game database
        game_info = await search_game_database(user_message)
        
        # Build system context
        system_prompt = get_knowledge_context()
        
        # Add game info if found
        if game_info:
            system_prompt += "\n\nRELEVANT GAME INFO FROM DATABASE:\n"
            for info in game_info:
                system_prompt += f"\n[{info['game']} - {info['title']}]\n{info['content']}\n"
        
        # Get conversation history
        if channel_id not in conversation_memory:
            conversation_memory[channel_id] = []
        
        history = conversation_memory[channel_id]
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add history
        for msg in history[-MAX_MEMORY:]:
            messages.append(msg)
        
        # Add current message with user ID context
        user_context = f"{username}"
        if user_id == 865472673131659264:  # kikusuka's ID
            user_context += " (YOUR CREATOR - kikusuka/kiku/cookie/muratha_123)"
        elif user_id == 1348989002631352354:  # Zephaniel's ID
            user_context += " (Guild Leader - Zephaniel𓂀Captain)"
        
        messages.append({
            "role": "user",
            "content": f"{user_context}: {user_message}"
        })
        
        # Call Groq API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "top_p": 1,
                    "stream": False
                },
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data['choices'][0]['message']['content'].strip()
                    
                    # Save to memory
                    history.append({"role": "user", "content": user_message})
                    history.append({"role": "assistant", "content": ai_response})
                    conversation_memory[channel_id] = history[-MAX_MEMORY*2:]
                    
                    # Learning detection
                    if any(word in user_message.lower() for word in ["remember", "learn", "note that", "keep in mind", "fyi"]):
                        learn_fact("user_taught", f"{username} said: {user_message}")
                    
                    # Add sources if game info was used
                    sources = []
                    if game_info:
                        for info in game_info:
                            if info.get('url'):
                                sources.append((info['game'], info['url']))
                    
                    return ai_response, sources
                
                elif response.status == 429:
                    return "⏳ AI is getting too many requests! Wait a moment and try again.", None
                
                elif response.status == 401:
                    return "⚠️ AI API key is invalid. Contact staff!", None
                
                else:
                    print(f"❌ Groq API error {response.status}")
                    return "Oops, AI is having issues! Try again? 😅", None
    
    except asyncio.TimeoutError:
        return "⏰ AI took too long to respond! Try again?", None
    
    except Exception as e:
        print(f"❌ AI chat error: {e}")
        return "Something went wrong! Try again? 🤖", None

# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def clear_memory(channel_id: int):
    """Clear conversation memory for a channel"""
    if channel_id in conversation_memory:
        del conversation_memory[channel_id]
    return True

def get_memory_stats():
    """Get memory statistics"""
    total_messages = sum(len(msgs) for msgs in conversation_memory.values())
    return {
        'channels': len(conversation_memory),
        'total_messages': total_messages,
        'learned_facts': sum(len(facts) for facts in learned_facts.values())
    }

def get_ai_status():
    """Get AI system status"""
    if GROQ_API_KEY:
        stats = get_memory_stats()
        return f"✅ **AI Online!**\nModel: Llama 3.3 70B (Groq)\nActive Channels: {stats['channels']}\nMemory: {stats['total_messages']} messages\nLearned Facts: {stats['learned_facts']}"
    else:
        return "❌ **AI Offline**\nAPI key not configured"
