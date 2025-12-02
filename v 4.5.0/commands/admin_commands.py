"""
═══════════════════════════════════════════════════════════════
⚡ Admin Commands - For administrators only
System management and advanced controls
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from datetime import datetime
from config import *
from utils import is_admin

def setup(bot):
    """Setup admin commands"""
    
    @bot.tree.command(name="shutdown", description="[ADMIN] Shutdown the bot")
    async def shutdown(interaction: discord.Interaction):
        """Shutdown bot"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "🛑 Shutting down bot...",
            ephemeral=True
        )
        
        await bot.close()
    
    @bot.tree.command(name="sync", description="[ADMIN] Sync slash commands")
    async def sync(interaction: discord.Interaction):
        """Sync commands"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            synced = await bot.tree.sync()
            await interaction.followup.send(
                f"✅ Synced {len(synced)} slash commands!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Failed to sync commands: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="purge", description="[ADMIN] Delete multiple messages")
    @app_commands.describe(
        amount="Number of messages to delete (1-100)",
        channel="Channel to purge (leave empty for current)"
    )
    async def purge(interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None):
        """Purge messages"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        target_channel = channel or interaction.channel
        
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "❌ Amount must be between 1 and 100!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            deleted = await target_channel.purge(limit=amount)
            
            await interaction.followup.send(
                f"✅ Deleted {len(deleted)} messages from {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Failed to purge messages: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="slowmode", description="[ADMIN] Set channel slowmode")
    @app_commands.describe(
        seconds="Slowmode duration in seconds (0 to disable)",
        channel="Channel to apply slowmode (leave empty for current)"
    )
    async def slowmode(interaction: discord.Interaction, seconds: int, channel: discord.TextChannel = None):
        """Set slowmode"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        target_channel = channel or interaction.channel
        
        if seconds < 0 or seconds > 21600:
            await interaction.response.send_message(
                "❌ Slowmode must be between 0 and 21600 seconds (6 hours)!",
                ephemeral=True
            )
            return
        
        try:
            await target_channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                await interaction.response.send_message(
                    f"✅ Disabled slowmode in {target_channel.mention}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"✅ Set slowmode to {seconds} seconds in {target_channel.mention}",
                    ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to set slowmode: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="lock", description="[ADMIN] Lock a channel")
    @app_commands.describe(channel="Channel to lock (leave empty for current)")
    async def lock(interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Lock channel"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        target_channel = channel or interaction.channel
        
        try:
            await target_channel.set_permissions(
                interaction.guild.default_role,
                send_messages=False
            )
            
            await interaction.response.send_message(
                f"🔒 Locked {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to lock channel: {e}",
                ephemeral=True
            )
    
    @bot.tree.command(name="unlock", description="[ADMIN] Unlock a channel")
    @app_commands.describe(channel="Channel to unlock (leave empty for current)")
    async def unlock(interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Unlock channel"""
        if not is_admin(interaction):
            await interaction.response.send_message(
                "❌ This command is for administrators only!",
                ephemeral=True
            )
            return
        
        target_channel = channel or interaction.channel
        
        try:
            await target_channel.set_permissions(
                interaction.guild.default_role,
                send_messages=True
            )
            
            await interaction.response.send_message(
                f"🔓 Unlocked {target_channel.mention}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to unlock channel: {e}",
                ephemeral=True
            )
    
    print("✅ Admin commands loaded!")
