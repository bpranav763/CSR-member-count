"""
═══════════════════════════════════════════════════════════════
👮 Staff Commands - For CSR staff members only
Includes: FAQ, badwords, moderation, wiki updates, announcements, alliances
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from datetime import datetime
import json
import os
import aiohttp
from config import *
from utils import is_staff, load_json, save_json

def setup(bot):
    """Setup staff commands"""
    
    # ═══════════════════════════════════════════════════════════════
    # FAQ COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="addfaq", description="[STAFF] Add a new FAQ entry")
    @app_commands.describe(
        question="The FAQ question",
        answer="The answer to the question"
    )
    async def addfaq(interaction: discord.Interaction, question: str, answer: str):
        """Add FAQ"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        faqs = load_json('data/faqs.json')
        
        faq_id = len(faqs) + 1
        faqs[str(faq_id)] = {
            'question': question,
            'answer': answer,
            'added_by': str(interaction.user.id),
            'added_at': datetime.now().isoformat()
        }
        
        save_json('data/faqs.json', faqs)
        
        await interaction.response.send_message(
            f"✅ Added FAQ #{faq_id}:\n**Q:** {question}\n**A:** {answer}",
            ephemeral=True
        )
    
    @bot.tree.command(name="listfaqs", description="[STAFF] List all FAQ entries")
    async def listfaqs(interaction: discord.Interaction):
        """List FAQs"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        faqs = load_json('data/faqs.json')
        
        if not faqs:
            await interaction.response.send_message(
                "📝 No FAQs found!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="📋 FAQ List",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for faq_id, faq in faqs.items():
            embed.add_field(
                name=f"#{faq_id}: {faq['question']}",
                value=faq['answer'][:100] + "..." if len(faq['answer']) > 100 else faq['answer'],
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="removefaq", description="[STAFF] Remove an FAQ entry")
    @app_commands.describe(faq_id="The FAQ ID to remove")
    async def removefaq(interaction: discord.Interaction, faq_id: int):
        """Remove FAQ"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        faqs = load_json('data/faqs.json')
        
        if str(faq_id) not in faqs:
            await interaction.response.send_message(
                f"❌ FAQ #{faq_id} not found!",
                ephemeral=True
            )
            return
        
        removed_faq = faqs.pop(str(faq_id))
        save_json('data/faqs.json', faqs)
        
        await interaction.response.send_message(
            f"✅ Removed FAQ #{faq_id}: {removed_faq['question']}",
            ephemeral=True
        )
    
    # ═══════════════════════════════════════════════════════════════
    # BADWORD MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="reloadbadwords", description="[STAFF] Reload badwords from file")
    async def reloadbadwords(interaction: discord.Interaction):
        """Reload badwords"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        badwords = load_json('data/badwords.json')
        
        await interaction.response.send_message(
            f"✅ Reloaded {len(badwords.get('words', []))} badwords!",
            ephemeral=True
        )
    
    @bot.tree.command(name="addbadword", description="[STAFF] Add a word to badwords list")
    @app_commands.describe(word="The word to add")
    async def addbadword(interaction: discord.Interaction, word: str):
        """Add badword"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        badwords = load_json('data/badwords.json')
        word_lower = word.lower()
        
        if word_lower in badwords.get('words', []):
            await interaction.response.send_message(
                f"⚠️ '{word}' is already in the badwords list!",
                ephemeral=True
            )
            return
        
        if 'words' not in badwords:
            badwords['words'] = []
        
        badwords['words'].append(word_lower)
        save_json('data/badwords.json', badwords)
        
        await interaction.response.send_message(
            f"✅ Added '{word}' to badwords list!",
            ephemeral=True
        )
    
    @bot.tree.command(name="removebadword", description="[STAFF] Remove a word from badwords list")
    @app_commands.describe(word="The word to remove")
    async def removebadword(interaction: discord.Interaction, word: str):
        """Remove badword"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        badwords = load_json('data/badwords.json')
        word_lower = word.lower()
        
        if word_lower not in badwords.get('words', []):
            await interaction.response.send_message(
                f"❌ '{word}' is not in the badwords list!",
                ephemeral=True
            )
            return
        
        badwords['words'].remove(word_lower)
        save_json('data/badwords.json', badwords)
        
        await interaction.response.send_message(
            f"✅ Removed '{word}' from badwords list!",
            ephemeral=True
        )
    
    @bot.tree.command(name="testmod", description="[STAFF] Test moderation on a message")
    @app_commands.describe(text="Text to test")
    async def testmod(interaction: discord.Interaction, text: str):
        """Test moderation"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        badwords = load_json('data/badwords.json')
        text_lower = text.lower()
        
        found_words = [word for word in badwords.get('words', []) if word in text_lower]
        
        if found_words:
            await interaction.response.send_message(
                f"⚠️ Found badwords: {', '.join(found_words)}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "✅ No badwords detected!",
                ephemeral=True
            )
    
    # ═══════════════════════════════════════════════════════════════
    # WIKI MANAGEMENT
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="forcefetch", description="[STAFF] Force update wiki cache")
    async def forcefetch(interaction: discord.Interaction):
        """Force fetch wiki"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # This would trigger your wiki fetcher
        await interaction.followup.send(
            "✅ Wiki cache update triggered!",
            ephemeral=True
        )
    
    # ═══════════════════════════════════════════════════════════════
    # MODERATION COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="kick", description="[STAFF] Kick a member")
    @app_commands.describe(
        member="Member to kick",
        reason="Reason for kick"
    )
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Kick member"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 Member Kicked",
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to kick member: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="ban", description="[STAFF] Ban a member")
    @app_commands.describe(
        member="Member to ban",
        reason="Reason for ban",
        delete_days="Days of messages to delete (0-7)"
    )
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided", delete_days: int = 0):
        """Ban member"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        try:
            await member.ban(reason=reason, delete_message_days=delete_days)
            
            embed = discord.Embed(
                title="🔨 Member Banned",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to ban member: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="unban", description="[STAFF] Unban a user")
    @app_commands.describe(
        user_id="User ID to unban",
        reason="Reason for unban"
    )
    async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        """Unban user"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        try:
            user = await bot.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title="✅ User Unbanned",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="User", value=f"{user.mention} ({user.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to unban user: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="mute", description="[STAFF] Mute a member")
    @app_commands.describe(
        member="Member to mute",
        duration="Duration in minutes",
        reason="Reason for mute"
    )
    async def mute(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
        """Mute member"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        try:
            from datetime import timedelta
            
            await member.timeout(timedelta(minutes=duration), reason=reason)
            
            embed = discord.Embed(
                title="🔇 Member Muted",
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to mute member: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="unmute", description="[STAFF] Unmute a member")
    @app_commands.describe(
        member="Member to unmute",
        reason="Reason for unmute"
    )
    async def unmute(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Unmute member"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        try:
            await member.timeout(None, reason=reason)
            
            embed = discord.Embed(
                title="🔊 Member Unmuted",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name="Member", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to unmute member: {e}",
                ephemeral=True
            )
    
    # ═══════════════════════════════════════════════════════════════
    # ANNOUNCEMENT COMMAND
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="announcement", description="[STAFF] Send an announcement")
    @app_commands.describe(
        channel="Channel or thread to send announcement",
        title="Announcement title",
        message="Announcement message",
        image_url="Image URL (optional)",
        ping_role="Role to ping (optional)"
    )
    async def announcement(
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        title: str,
        message: str,
        image_url: str = None,
        ping_role: discord.Role = None
    ):
        """Send announcement"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        if image_url:
            embed.set_image(url=image_url)
        
        embed.set_footer(text=f"Announcement by {interaction.user.display_name}")
        
        ping_text = ping_role.mention if ping_role else ""
        
        try:
            await channel.send(content=ping_text, embed=embed)
            
            await interaction.response.send_message(
                f"✅ Announcement sent to {channel.mention}!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to send announcement: {e}",
                ephemeral=True
            )
    
    # ═══════════════════════════════════════════════════════════════
    # ALLIANCE UPDATE COMMAND
    # ═══════════════════════════════════════════════════════════════
    
    async def fetch_roblox_group(group_id: str) -> dict:
        """Fetch Roblox group information from API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get group info
                async with session.get(f"https://groups.roblox.com/v1/groups/{group_id}") as resp:
                    if resp.status != 200:
                        return None
                    group_data = await resp.json()
                
                # Get group icon
                async with session.get(f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={group_id}&size=420x420&format=Png") as resp:
                    if resp.status == 200:
                        thumb_data = await resp.json()
                        if thumb_data.get("data"):
                            group_data["iconUrl"] = thumb_data["data"][0].get("imageUrl")
                    else:
                        group_data["iconUrl"] = None
                
                return group_data
        except Exception as e:
            print(f"❌ Failed to fetch Roblox group: {e}")
            return None
    
    @bot.tree.command(name="allianceupdate", description="[STAFF] Post alliance information")
    @app_commands.describe(
        roblox_group_id="Roblox Group/Community ID (numbers only)",
        leader="Alliance leader (@mention)",
        representative="Alliance representative (@mention)",
        discord_invite="Discord permanent invite link",
        roblox_community_link="Roblox community/group link (optional)"
    )
    async def allianceupdate(
        interaction: discord.Interaction,
        roblox_group_id: str,
        leader: discord.Member,
        representative: discord.Member,
        discord_invite: str,
        roblox_community_link: str = None
    ):
        """Post alliance information"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        # Validate group ID
        if not roblox_group_id.isdigit():
            await interaction.response.send_message(
                "❌ Roblox Group ID must be numbers only!\nExample: `1003228779`",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Fetch Roblox group data
        group_data = await fetch_roblox_group(roblox_group_id)
        
        if not group_data:
            await interaction.followup.send(
                f"❌ Failed to fetch Roblox group with ID: `{roblox_group_id}`\n"
                "Make sure the group ID is correct and the group exists!",
                ephemeral=True
            )
            return
        
        # Get alliance thread
        thread = interaction.guild.get_channel(ALLIANCE_THREAD_ID)
        
        if not thread:
            await interaction.followup.send(
                f"❌ Alliance thread not found! Thread ID: `{ALLIANCE_THREAD_ID}`",
                ephemeral=True
            )
            return
        
        # Extract group info
        guild_name = group_data.get("name", "Unknown")
        description = group_data.get("description", "No description available")
        member_count = group_data.get("memberCount", 0)
        group_icon = group_data.get("iconUrl")
        
        # Build Roblox community link
        if not roblox_community_link:
            roblox_community_link = f"https://www.roblox.com/communities/{roblox_group_id}/about"
        
        # Create embed
        embed = discord.Embed(
            title=f"Allied Guild Name: {guild_name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if group_icon:
            embed.set_thumbnail(url=group_icon)
        
        # Add fields
        embed.add_field(name="Guild Owner:", value=leader.mention, inline=False)
        
        desc_text = description if description.startswith("🗡️") else f"🗡️ {description}"
        embed.add_field(name="Description:", value=desc_text[:1000], inline=False)
        
        embed.add_field(name="Guild ID:", value=f"`{roblox_group_id}`", inline=False)
        embed.add_field(name="Roblox Community:", value=roblox_community_link, inline=False)
        embed.add_field(name="Discord Server:", value=discord_invite, inline=False)
        
        embed.set_footer(
            text=f"👥 {member_count:,} Members | Representative: {representative.display_name}",
            icon_url=representative.avatar.url if representative.avatar else representative.default_avatar.url
        )
        
        if group_icon:
            embed.set_image(url=group_icon)
        
        # Post to alliance thread
        try:
            message = await thread.send(embed=embed)
            
            success_embed = discord.Embed(
                title="✅ Alliance Information Posted!",
                description=f"Successfully posted alliance info for **{guild_name}**",
                color=discord.Color.green()
            )
            
            success_embed.add_field(
                name="📋 Details",
                value=f"**Guild:** {guild_name}\n**Leader:** {leader.mention}\n"
                      f"**Representative:** {representative.mention}\n**Members:** {member_count:,}\n"
                      f"**Posted in:** {thread.mention}",
                inline=False
            )
            
            success_embed.add_field(name="🔗 Message Link", value=f"[Click here]({message.jump_url})", inline=False)
            
            if group_icon:
                success_embed.set_thumbnail(url=group_icon)
            
            await interaction.followup.send(embed=success_embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to post alliance info: {e}", ephemeral=True)
    
    print("✅ Staff commands loaded!")
