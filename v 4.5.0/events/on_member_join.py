"""
═══════════════════════════════════════════════════════════════
👋 On Member Join Event - Welcome messages
═══════════════════════════════════════════════════════════════
"""

import discord
from datetime import datetime
from config import *

def setup(bot):
    """Setup on_member_join event"""
    
    @bot.event
    async def on_member_join(member):
        """Handle new member joins"""
        
        # ═══════════════════════════════════════════════════════
        # WELCOME MESSAGE
        # ═══════════════════════════════════════════════════════
        
        try:
            # Create welcome embed
            embed = discord.Embed(
                title=f"🎮 Welcome to {member.guild.name}!",
                description=f"Hey {member.mention}! Welcome to **Champions of the Shattered Realm**!",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            
            embed.add_field(
                name="📋 Get Started",
                value=f"1. Read the rules\n"
                      f"2. Head to <#{VERIFICATION_CHANNEL_ID}> to verify\n"
                      f"3. Check out <#{HELP_CHANNEL_ID}> if you need help!",
                inline=False
            )
            
            embed.add_field(
                name="🎯 What We Offer",
                value=f"• Active community\n"
                      f"• Game guides & tips\n"
                      f"• Events & giveaways\n"
                      f"• AI assistant (mention me!)",
                inline=False
            )
            
            embed.set_footer(
                text=f"Member #{member.guild.member_count}",
                icon_url=GUILD_IMAGE
            )
            
            # Send welcome message
            if member.guild.system_channel:
                await member.guild.system_channel.send(embed=embed)
        
        except Exception as e:
            print(f"⚠️ Failed to send welcome message: {e}")
        
        # ═══════════════════════════════════════════════════════
        # ADD VERIFICATION PENDING ROLE
        # ═══════════════════════════════════════════════════════
        
        try:
            pending_role = member.guild.get_role(VERIFICATION_PENDING_ROLE_ID)
            if pending_role:
                await member.add_roles(pending_role, reason="New member - pending verification")
        except Exception as e:
            print(f"⚠️ Failed to add pending role: {e}")
