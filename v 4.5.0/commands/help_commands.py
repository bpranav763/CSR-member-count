"""
═══════════════════════════════════════════════════════════════
📖 Help Command - Interactive command guide
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from datetime import datetime
from config import *
from utils import is_staff, is_admin

class HelpView(discord.ui.View):
    """Interactive help menu with buttons"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Only allow the command user to interact"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This help menu is not for you! Use `/help` to get your own.",
                ephemeral=True
            )
            return False
        return True
    
    @discord.ui.button(label="👤 User Commands", style=discord.ButtonStyle.primary, emoji="👤")
    async def user_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show user commands"""
        embed = get_user_commands_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="👮 Staff Commands", style=discord.ButtonStyle.secondary, emoji="👮")
    async def staff_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show staff commands"""
        embed = get_staff_commands_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⚡ Admin Commands", style=discord.ButtonStyle.secondary, emoji="⚡")
    async def admin_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show admin commands"""
        embed = get_admin_commands_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🤖 AI Chat", style=discord.ButtonStyle.success, emoji="🤖")
    async def ai_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show AI chat help"""
        embed = get_ai_help_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏠 Home", style=discord.ButtonStyle.primary, emoji="🏠")
    async def home(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Back to home"""
        embed = get_main_help_embed()
        await interaction.response.edit_message(embed=embed, view=self)

def get_main_help_embed():
    """Main help embed"""
    embed = discord.Embed(
        title="📖 CSR Bot Help",
        description=(
            "**Welcome to CSR Bot!**\n"
            "Your all-in-one gaming community assistant.\n\n"
            "Click the buttons below to explore different command categories!"
        ),
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="🎯 Quick Start",
        value=(
            "**AI Chat:** `.csr <message>` or mention me!\n"
            "**Commands:** Use `/` to see all slash commands\n"
            "**Help:** Click buttons below for detailed info"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📚 Categories",
        value=(
            "👤 **User Commands** - Available to everyone\n"
            "👮 **Staff Commands** - For CSR staff only\n"
            "⚡ **Admin Commands** - For administrators\n"
            "🤖 **AI Chat** - How to chat with the bot"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"CSR Bot v{BOT_VERSION} • Made by {BOT_AUTHOR}")
    
    return embed

def get_user_commands_embed():
    """User commands embed"""
    embed = discord.Embed(
        title="👤 User Commands",
        description="Commands available to all members",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="📊 General",
        value=(
            "`/ping` - Check bot latency\n"
            "`/about` - About CSR Bot\n"
            "`/statmetrics` - Bot statistics\n"
            "`/help` - This help menu"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👤 Profile & Settings",
        value=(
            "`/profile [@user]` - View user profile\n"
            "`/settings` - Configure your preferences\n"
            "`/setlanguage` - Change language\n"
            "`/settimezone` - Set timezone"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📚 Wiki & Info",
        value=(
            "`/wikisearch <query>` - Search game wikis\n"
            "`/wikiinfo` - View wiki statistics"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💬 Community",
        value=(
            "`/suggestions <text>` - Send suggestion to staff\n"
            "`/aistatus` - Check AI status\n"
            "`/clearmemory` - Clear AI conversation"
        ),
        inline=False
    )
    
    embed.set_footer(text="Use /command to run any command")
    
    return embed

def get_staff_commands_embed():
    """Staff commands embed"""
    embed = discord.Embed(
        title="👮 Staff Commands",
        description="Commands for CSR staff members",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="❓ FAQ Management",
        value=(
            "`/addfaq` - Add FAQ entry\n"
            "`/listfaqs` - List all FAQs\n"
            "`/removefaq` - Remove FAQ"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value=(
            "`/kick` - Kick member\n"
            "`/ban` - Ban member\n"
            "`/unban` - Unban user\n"
            "`/mute` - Mute member\n"
            "`/unmute` - Unmute member"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 Management",
        value=(
            "`/addbadword` - Add badword\n"
            "`/removebadword` - Remove badword\n"
            "`/testmod` - Test moderation\n"
            "`/forcefetch` - Update wiki cache\n"
            "`/announcement` - Send announcement\n"
            "`/allianceupdate` - Post alliance info"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🤖 AI Testing",
        value=(
            "`/aitest <message>` - Test AI response"
        ),
        inline=False
    )
    
    embed.set_footer(text="Staff commands require CSR role")
    
    return embed

def get_admin_commands_embed():
    """Admin commands embed"""
    embed = discord.Embed(
        title="⚡ Admin Commands",
        description="Commands for administrators only",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="🔧 System",
        value=(
            "`/shutdown` - Shutdown bot\n"
            "`/sync` - Sync slash commands"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation",
        value=(
            "`/purge <amount>` - Delete messages\n"
            "`/slowmode <seconds>` - Set slowmode\n"
            "`/lock [channel]` - Lock channel\n"
            "`/unlock [channel]` - Unlock channel"
        ),
        inline=False
    )
    
    embed.set_footer(text="Admin commands require Administrator permission")
    
    return embed

def get_ai_help_embed():
    """AI chat help embed"""
    embed = discord.Embed(
        title="🤖 AI Chat Guide",
        description="How to chat with CSR Bot's AI",
        color=discord.Color.purple(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="💬 Ways to Chat",
        value=(
            "**Prefix:** `.csr your message`\n"
            "**Alternative:** `csr your message` (no dot)\n"
            "**Mention:** `@CSR SYSTEM your message`\n"
            "**Reply:** Reply to any of my messages"
        ),
        inline=False
    )
    
    embed.add_field(
        name="✨ Features",
        value=(
            "✅ Natural conversations\n"
            "✅ Remembers last 5 messages per channel\n"
            "✅ Searches SBOR & Blox Fruits wikis\n"
            "✅ Gaming-focused personality\n"
            "✅ Fast responses (1-2 seconds)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📝 Examples",
        value=(
            "`.csr hey how are you?`\n"
            "`.csr what's the best sword in sbor?`\n"
            "`.csr should I grind for leopard fruit?`\n"
            "`.csr tell me about CSR guild`"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 Commands",
        value=(
            "`/aistatus` - Check AI system status\n"
            "`/clearmemory` - Reset conversation\n"
            "`/aitest` - Test AI (staff only)"
        ),
        inline=False
    )
    
    embed.set_footer(text="Powered by Llama 3.3 70B (Groq)")
    
    return embed

def setup(bot):
    """Setup help command"""
    
    @bot.tree.command(name="help", description="View bot commands and features")
    async def help_command(interaction: discord.Interaction):
        """Interactive help menu"""
        
        embed = get_main_help_embed()
        view = HelpView(interaction.user.id)
        
        await interaction.response.send_message(embed=embed, view=view)
    
    print("  ✅ Help command")
