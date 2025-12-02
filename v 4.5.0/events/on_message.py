"""
═══════════════════════════════════════════════════════════════
💬 On Message Event - REAL AI chat + moderation
═══════════════════════════════════════════════════════════════
"""

import discord
import asyncio
import re
from datetime import datetime
from config import CHAT_FILTER_ENABLED, AI_MODERATION_ENABLED, MODLOG_CHANNEL_ID

# Import moderation
try:
    from utils import check_message_toxicity
    MODERATION_AVAILABLE = True
except:
    MODERATION_AVAILABLE = False
    print("⚠️ Moderation not available")

# Import AI chat system
try:
    from utils.ai_chat import chat_with_groq, get_ai_status
    AI_AVAILABLE = True
    print("✅ AI chat system loaded!")
    print(get_ai_status())
except Exception as e:
    AI_AVAILABLE = False
    print(f"⚠️ AI chat not available: {e}")
    print("   Make sure GROQ_API_KEY is set in .env file")

def setup(bot):
    """Setup on_message event"""
    
    @bot.event
    async def on_message(message):
        """Handle incoming messages"""
        
        # Ignore bots
        if message.author.bot:
            return
        
        # Ignore DMs (handle them separately if needed)
        if not message.guild:
            return
        
        # ═══════════════════════════════════════════════════════
        # REAL AI CHAT
        # ═══════════════════════════════════════════════════════
        
        # Check if bot is mentioned or message starts with "csr" or ".csr"
        bot_mentioned = bot.user in message.mentions
        content_lower = message.content.lower().strip()
        starts_with_csr = content_lower.startswith("csr ") or content_lower.startswith(".csr ")
        
        # Check if replying to bot
        is_reply_to_bot = False
        if message.reference and message.reference.resolved:
            is_reply_to_bot = message.reference.resolved.author == bot.user
        
        if bot_mentioned or starts_with_csr or is_reply_to_bot:
            if not AI_AVAILABLE:
                await message.reply(
                    "⚠️ **AI chat is not configured!**\n\n"
                    "**Setup Instructions:**\n"
                    "1. Get a free API key: https://console.groq.com\n"
                    "2. Add to `.env` file: `GROQ_API_KEY=your_key_here`\n"
                    "3. Restart the bot\n\n"
                    "Ask staff for help!",
                    mention_author=False
                )
                return
            
            # Show typing indicator
            async with message.channel.typing():
                # Clean message
                clean_msg = message.content
                
                # Remove bot mentions
                for mention in message.mentions:
                    clean_msg = clean_msg.replace(f"<@{mention.id}>", "")
                    clean_msg = clean_msg.replace(f"<@!{mention.id}>", "")
                
                # Remove "csr" or ".csr" prefix
                clean_msg = re.sub(r"^\.?csr\s+", "", clean_msg, flags=re.IGNORECASE).strip()
                
                # If message is empty after cleaning
                if not clean_msg or len(clean_msg) < 1:
                    responses = [
                        "Hey! What's up? 😊",
                        "Hi there! How can I help? 🎮",
                        "Yo! Need something? ✨",
                        "What's good? Ask me anything! 💪"
                    ]
                    import random
                    await message.reply(random.choice(responses), mention_author=False)
                    return
                
                try:
                    # Get AI response
                    print(f"💬 AI Chat from {message.author.name}: {clean_msg[:50]}...")
                    
                    ai_response, sources = await chat_with_groq(
                        clean_msg,
                        message.channel.id,
                        message.author.name
                    )
                    
                    # Build response
                    response = ai_response
                    
                    # Add source links if any
                    if sources and len(sources) > 0:
                        response += "\n\n**📚 Wiki Sources:**\n"
                        for game, title, url in sources[:2]:  # Max 2 sources
                            response += f"• [{game}: {title}]({url})\n"
                    
                    # Split if too long (Discord limit is 2000 chars)
                    if len(response) > 2000:
                        chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                        for i, chunk in enumerate(chunks):
                            if i == 0:
                                await message.reply(chunk, mention_author=False)
                            else:
                                await message.channel.send(chunk)
                    else:
                        await message.reply(response, mention_author=False)
                    
                    print(f"✅ AI Response sent to {message.author.name}")
                
                except Exception as e:
                    print(f"❌ AI chat error: {type(e).__name__}: {e}")
                    await message.reply(
                        f"Oops, something went wrong! 😅\n"
                        f"Error: `{type(e).__name__}`\n"
                        f"Try again or contact staff if this keeps happening.",
                        mention_author=False
                    )
            
            # Don't process commands if it was an AI chat
            return
        
        # ═══════════════════════════════════════════════════════
        # MODERATION (if enabled)
        # ═══════════════════════════════════════════════════════
        
        if MODERATION_AVAILABLE and (CHAT_FILTER_ENABLED or AI_MODERATION_ENABLED):
            try:
                is_toxic, category, confidence = await check_message_toxicity(message.content)
                
                if is_toxic:
                    # Delete message
                    try:
                        await message.delete()
                    except:
                        pass
                    
                    # Send warning to channel
                    try:
                        warning = await message.channel.send(
                            f"⚠️ {message.author.mention} Your message was removed.\n"
                            f"**Reason:** {category}"
                        )
                        # Auto-delete warning after 10 seconds
                        await asyncio.sleep(10)
                        await warning.delete()
                    except:
                        pass
                    
                    # Log to modlog
                    try:
                        modlog = bot.get_channel(MODLOG_CHANNEL_ID)
                        if modlog:
                            embed = discord.Embed(
                                title="⚠️ Message Deleted",
                                description=f"**User:** {message.author.mention}\n**Channel:** {message.channel.mention}",
                                color=discord.Color.red(),
                                timestamp=datetime.utcnow()
                            )
                            embed.add_field(
                                name="Content",
                                value=f"```{message.content[:500]}```",
                                inline=False
                            )
                            embed.add_field(
                                name="Detection",
                                value=f"{category} ({confidence:.0%})",
                                inline=False
                            )
                            embed.set_footer(text=f"User ID: {message.author.id}")
                            
                            await modlog.send(embed=embed)
                    except Exception as e:
                        print(f"⚠️ Modlog error: {e}")
                    
                    return  # Don't process commands if message is toxic
            
            except Exception as e:
                print(f"❌ Moderation error: {e}")
        
        # Process commands (IMPORTANT!)
        await bot.process_commands(message)
    
    print("✅ Message handler loaded!")
