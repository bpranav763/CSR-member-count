"""
═══════════════════════════════════════════════════════════════
⚡ On Ready Event - Startup and background tasks
═══════════════════════════════════════════════════════════════
"""

import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import asyncio
from config import *
from utils import get_moderation_status, get_badword_count, load_json

PROFILES_FILE = "data/user_profiles.json"

def setup(bot):
    """Setup on_ready event"""
    
    @bot.event
    async def on_ready():
        """Bot startup event"""
        print("═" * 60)
        print(f"🤖 CSR Bot v{BOT_VERSION}")
        print(f"📝 Created by: {BOT_AUTHOR}")
        print(f"🧪 Tester: flasharrow2003")
        print(f"👤 Logged in as: {bot.user}")
        print(f"📊 Connected to {len(bot.guilds)} guilds")
        print(f"👥 Serving {sum(g.member_count for g in bot.guilds)} members")
        print("─" * 60)
        
        # Moderation status
        print(f"🛡️ Moderation: {get_moderation_status()}")
        print(f"📝 Badwords loaded: {get_badword_count()}")
        
        # API status
        if PERSPECTIVE_API_KEY:
            print("✅ Perspective API: Active (100+ languages)")
        if GROQ_API_KEY:
            print("✅ Groq AI: Active")
        
        print("═" * 60)
        
        # Sync commands
        try:
            synced = await bot.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
        
        print("═" * 60)
        print("🚀 Bot is ready!")
        print("═" * 60)
        
        # Start background tasks
        if not update_member_count.is_running():
            update_member_count.start()
        if not check_birthdays.is_running():
            check_birthdays.start()
    
    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def update_member_count():
        """Update member count in thread"""
        try:
            channel = bot.get_channel(MEMBER_COUNT_CHANNEL_ID)
            if not channel:
                return
            
            guild = bot.guilds[0] if bot.guilds else None
            if not guild:
                return
            
            member_count = guild.member_count
            
            # Create embed
            embed = discord.Embed(
                title="🌟 CSR Member Count",
                description=f"**Total Members: `{member_count}`**",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=GUILD_IMAGE)
            embed.set_footer(text=f"Updates every {UPDATE_INTERVAL//60} minutes")
            
            # Try to edit last message, or send new one
            try:
                last_msg = None
                async for msg in channel.history(limit=10):
                    if msg.author == bot.user and msg.embeds:
                        last_msg = msg
                        break
                
                if last_msg:
                    await last_msg.edit(embed=embed)
                else:
                    await channel.send(embed=embed)
            except:
                await channel.send(embed=embed)
        
        except Exception as e:
            print(f"⚠️ Member count update error: {e}")
    
    @tasks.loop(hours=24)
    async def check_birthdays():
        """Check for birthdays daily at midnight UTC"""
        try:
            today = datetime.utcnow().strftime('%m-%d')
            
            profiles = load_json(PROFILES_FILE, {})
            birthday_channel = bot.get_channel(DAILYCHECKS_CHANNEL_ID)
            
            if not birthday_channel:
                return
            
            for user_id_str, profile in profiles.items():
                if profile.get('birthday') == today:
                    try:
                        user = bot.get_user(int(user_id_str))
                        if not user:
                            continue
                        
                        embed = discord.Embed(
                            title="🎂 Happy Birthday! 🎉",
                            description=f"Everyone wish {user.mention} a happy birthday! 🎊",
                            color=discord.Color.gold()
                        )
                        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
                        embed.add_field(
                            name="🎈 Celebration Time!",
                            value=f"Hope you have an amazing day!",
                            inline=False
                        )
                        embed.set_footer(text="CSR Bot • Birthday Reminder", icon_url=GUILD_IMAGE)
                        
                        await birthday_channel.send("@everyone 🎂", embed=embed)
                    
                    except Exception as e:
                        print(f"⚠️ Birthday announcement error: {e}")
        
        except Exception as e:
            print(f"❌ Birthday check error: {e}")
    
    @update_member_count.before_loop
    async def before_update_member_count():
        await bot.wait_until_ready()
    
    @check_birthdays.before_loop
    async def before_check_birthdays():
        await bot.wait_until_ready()
        # Wait until next midnight UTC
        now = datetime.utcnow()
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep((tomorrow - now).total_seconds())
