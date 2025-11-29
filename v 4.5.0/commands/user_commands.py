"""
═══════════════════════════════════════════════════════════════
👤 User Commands - Available to all members
COMPLETE with profile tracking, settings, wiki search, suggestions
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands, ui
from datetime import datetime
import re
from config import *
from utils import (
    get_user_language,
    set_user_language,
    get_user_timezone,
    set_user_timezone,
    get_user_profile,
    update_user_profile,
    get_moderation_status,
    get_badword_count
)
from utils.wiki_fetcher import search_wikis, get_wiki_stats

# ═══════════════════════════════════════════════════════════════
# PROFILE EDIT MODAL
# ═══════════════════════════════════════════════════════════════

class ProfileEditModal(ui.Modal, title="✏️ Edit Your Profile"):
    """Modal for editing user profile"""
    
    bio = ui.TextInput(
        label="Bio / Status",
        style=discord.TextStyle.short,
        placeholder="Your status or bio...",
        required=False,
        max_length=150
    )
    
    birthday = ui.TextInput(
        label="Birthday (MM-DD format)",
        style=discord.TextStyle.short,
        placeholder="Example: 03-15",
        required=False,
        max_length=5
    )
    
    favorite_color = ui.TextInput(
        label="Favorite Color",
        style=discord.TextStyle.short,
        placeholder="Example: Blue",
        required=False,
        max_length=20
    )
    
    roblox_username = ui.TextInput(
        label="Roblox Username",
        style=discord.TextStyle.short,
        placeholder="Your Roblox username",
        required=False,
        max_length=20
    )
    
    roblox_id = ui.TextInput(
        label="Roblox User ID",
        style=discord.TextStyle.short,
        placeholder="Your Roblox user ID (numbers only)",
        required=False,
        max_length=15
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle profile edit submission"""
        
        # Validate birthday format
        if self.birthday.value:
            if not re.match(r'^\d{2}-\d{2}$', self.birthday.value):
                await interaction.response.send_message(
                    "❌ Birthday must be in MM-DD format (example: 03-15)",
                    ephemeral=True
                )
                return
        
        # Validate Roblox ID
        if self.roblox_id.value and not self.roblox_id.value.isdigit():
            await interaction.response.send_message(
                "❌ Roblox ID must be numbers only",
                ephemeral=True
            )
            return
        
        # Get current profile
        profile = get_user_profile(interaction.user.id)
        
        # Track username changes
        current_discord_name = f"{interaction.user.name}#{interaction.user.discriminator}"
        if current_discord_name not in profile.get("discord_usernames", []):
            if "discord_usernames" not in profile:
                profile["discord_usernames"] = []
            profile["discord_usernames"].append(current_discord_name)
        
        # Track Roblox username changes
        if self.roblox_username.value:
            if self.roblox_username.value not in profile.get("roblox_usernames", []):
                if "roblox_usernames" not in profile:
                    profile["roblox_usernames"] = []
                profile["roblox_usernames"].append(self.roblox_username.value)
        
        # Update profile
        update_data = {
            "bio": self.bio.value if self.bio.value else profile.get("bio"),
            "birthday": self.birthday.value if self.birthday.value else profile.get("birthday"),
            "favorite_color": self.favorite_color.value if self.favorite_color.value else profile.get("favorite_color"),
            "roblox_username": self.roblox_username.value if self.roblox_username.value else profile.get("roblox_username"),
            "roblox_id": self.roblox_id.value if self.roblox_id.value else profile.get("roblox_id"),
            "discord_usernames": profile.get("discord_usernames", []),
            "roblox_usernames": profile.get("roblox_usernames", []),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        if update_user_profile(interaction.user.id, update_data):
            # Update tracking message
            await update_tracking_message(interaction.user, update_data)
            
            await interaction.response.send_message(
                "✅ Profile updated successfully!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to update profile",
                ephemeral=True
            )

class ProfileView(ui.View):
    """View with edit button for profiles"""
    
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
    
    @ui.button(label="Edit Profile", style=discord.ButtonStyle.primary, emoji="✏️")
    async def edit_button(self, interaction: discord.Interaction, button: ui.Button):
        """Open profile edit modal"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ You can only edit your own profile!",
                ephemeral=True
            )
            return
        
        # Pre-fill modal with current data
        modal = ProfileEditModal()
        profile = get_user_profile(self.user_id)
        
        if profile.get("bio"):
            modal.bio.default = profile["bio"]
        if profile.get("birthday"):
            modal.birthday.default = profile["birthday"]
        if profile.get("favorite_color"):
            modal.favorite_color.default = profile["favorite_color"]
        if profile.get("roblox_username"):
            modal.roblox_username.default = profile["roblox_username"]
        if profile.get("roblox_id"):
            modal.roblox_id.default = profile["roblox_id"]
        
        await interaction.response.send_modal(modal)

# ═══════════════════════════════════════════════════════════════
# PROFILE TRACKING SYSTEM
# ═══════════════════════════════════════════════════════════════

async def update_tracking_message(user: discord.Member, profile_data: dict):
    """Update or create tracking message for user"""
    try:
        # Get tracking channel
        channel = user.guild.get_channel(PROFILE_TRACKING_CHANNEL_ID)
        if not channel:
            return
        
        # Get profile
        profile = get_user_profile(user.id)
        
        # Create embed
        embed = discord.Embed(
            title=f"👤 Profile: {user.display_name}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Current info
        current_info = f"**Discord:** {user.mention} ({user.name}#{user.discriminator})\n"
        current_info += f"**Discord ID:** {user.id}\n"
        
        if profile_data.get("roblox_username"):
            current_info += f"**Roblox:** {profile_data['roblox_username']}\n"
        if profile_data.get("roblox_id"):
            current_info += f"**Roblox ID:** {profile_data['roblox_id']}\n"
        
        embed.add_field(name="📋 Current Info", value=current_info, inline=False)
        
        # Previous names
        previous_names = []
        
        # Discord username history
        discord_usernames = profile_data.get("discord_usernames", [])
        current_name = f"{user.name}#{user.discriminator}"
        old_discord_names = [n for n in discord_usernames if n != current_name]
        
        if old_discord_names:
            previous_names.extend([f"Discord: {name}" for name in old_discord_names[-3:]])  # Last 3
        
        # Roblox username history
        roblox_usernames = profile_data.get("roblox_usernames", [])
        current_roblox = profile_data.get("roblox_username")
        old_roblox_names = [n for n in roblox_usernames if n != current_roblox]
        
        if old_roblox_names:
            previous_names.extend([f"Roblox: {name}" for name in old_roblox_names[-3:]])  # Last 3
        
        if previous_names:
            embed.add_field(
                name="📜 Previous Names",
                value="\n".join(f"- {name}" for name in previous_names),
                inline=False
            )
        
        embed.set_footer(text=f"Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        # Check if tracking message exists
        message_id = profile.get("tracking_message_id")
        
        if message_id:
            try:
                # Try to edit existing message
                message = await channel.fetch_message(message_id)
                await message.edit(embed=embed)
            except:
                # Message not found, create new one
                message = await channel.send(embed=embed)
                update_user_profile(user.id, {"tracking_message_id": message.id})
        else:
            # Create new tracking message
            message = await channel.send(embed=embed)
            update_user_profile(user.id, {"tracking_message_id": message.id})
    
    except Exception as e:
        print(f"⚠️ Failed to update tracking message: {e}")

# ═══════════════════════════════════════════════════════════════
# SETUP COMMANDS
# ═══════════════════════════════════════════════════════════════

def setup(bot):
    """Setup user commands"""
    
    # ═══════════════════════════════════════════════════════════════
    # PROFILE COMMAND
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="profile", description="View user profile with cool stats")
    @app_commands.describe(member="User to view (leave empty for yourself)")
    async def profile(interaction: discord.Interaction, member: discord.Member = None):
        """View user profile"""
        
        target = member or interaction.user
        profile_data = get_user_profile(target.id)
        
        # Determine color based on top role
        color = target.top_role.color if target.top_role.color != discord.Color.default() else discord.Color.blue()
        
        # Create embed
        embed = discord.Embed(
            title=f"👤 {target.display_name}'s Profile",
            color=color,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
        
        # Status
        status_emoji = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }
        
        # Basic info
        basic_info = f"{status_emoji.get(target.status, '⚫')} **Status:** {target.status}\n"
        
        if profile_data.get("bio"):
            basic_info += f"📝 **Bio:** {profile_data['bio']}\n"
        
        embed.add_field(name="ℹ️ Basic Info", value=basic_info, inline=False)
        
        # Server info
        roles = [role.mention for role in target.roles[1:]][:5]  # Top 5 roles (excluding @everyone)
        server_info = f"📅 **Joined:** {target.joined_at.strftime('%Y-%m-%d')}\n"
        server_info += f"🎭 **Roles:** {', '.join(roles) if roles else 'None'}\n"
        
        embed.add_field(name="🏰 Server Info", value=server_info, inline=False)
        
        # Personal info
        personal_info = f"🎂 **Account Created:** {target.created_at.strftime('%Y-%m-%d')}\n"
        
        if profile_data.get("birthday"):
            personal_info += f"🎉 **Birthday:** {profile_data['birthday']}\n"
        
        if profile_data.get("favorite_color"):
            personal_info += f"🎨 **Favorite Color:** {profile_data['favorite_color']}\n"
        
        embed.add_field(name="🌟 Personal Info", value=personal_info, inline=False)
        
        # Roblox info
        if profile_data.get("roblox_username") or profile_data.get("roblox_id"):
            roblox_info = ""
            if profile_data.get("roblox_username"):
                roblox_info += f"👤 **Username:** {profile_data['roblox_username']}\n"
            if profile_data.get("roblox_id"):
                roblox_info += f"🆔 **ID:** {profile_data['roblox_id']}\n"
            
            embed.add_field(name="🎮 Roblox Info", value=roblox_info, inline=False)
        
        embed.set_footer(text=f"User ID: {target.id}")
        
        # Add view with edit button (only for own profile)
        view = ProfileView(target.id) if target.id == interaction.user.id else None
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
        
        # Update tracking message in background
        if target.id == interaction.user.id:
            try:
                await update_tracking_message(target, profile_data)
            except:
                pass
    
    # ═══════════════════════════════════════════════════════════════
    # SETTINGS COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="settings", description="View and change your settings")
    async def settings(interaction: discord.Interaction):
        """View user settings"""
        from ui.settings import SettingsView
        
        user_lang = get_user_language(interaction.user.id)
        user_tz = get_user_timezone(interaction.user.id)
        
        embed = discord.Embed(
            title="⚙️ Your Settings",
            description="Use the dropdowns below to change your settings",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🌐 Language",
            value=f"Current: **{SUPPORTED_LANGUAGES.get(user_lang, 'English')}**",
            inline=True
        )
        
        embed.add_field(
            name="🕐 Timezone",
            value=f"Current: **{SUPPORTED_TIMEZONES.get(user_tz, 'UTC')}**",
            inline=True
        )
        
        await interaction.response.send_message(embed=embed, view=SettingsView(), ephemeral=True)
    
    @bot.tree.command(name="setlanguage", description="Change your language")
    @app_commands.describe(language="Choose your preferred language")
    @app_commands.choices(language=[
        app_commands.Choice(name=name, value=code)
        for code, name in list(SUPPORTED_LANGUAGES.items())[:25]
    ])
    async def setlanguage(interaction: discord.Interaction, language: str):
        """Set user language"""
        if set_user_language(interaction.user.id, language):
            lang_name = SUPPORTED_LANGUAGES[language]
            await interaction.response.send_message(
                f"✅ Language set to **{lang_name}**!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to save language setting",
                ephemeral=True
            )
    
    @bot.tree.command(name="settimezone", description="Change your timezone")
    @app_commands.describe(timezone="Choose your timezone")
    @app_commands.choices(timezone=[
        app_commands.Choice(name=name, value=code)
        for code, name in list(SUPPORTED_TIMEZONES.items())[:25]
    ])
    async def settimezone(interaction: discord.Interaction, timezone: str):
        """Set user timezone"""
        if set_user_timezone(interaction.user.id, timezone):
            tz_name = SUPPORTED_TIMEZONES[timezone]
            await interaction.response.send_message(
                f"✅ Timezone set to **{tz_name}**!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to save timezone setting",
                ephemeral=True
            )
    
    # ═══════════════════════════════════════════════════════════════
    # WIKI COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="wikisearch", description="Search SBOR and Blox Fruits wikis")
    @app_commands.describe(query="What to search for")
    async def wikisearch(interaction: discord.Interaction, query: str):
        """Search wikis"""
        await interaction.response.defer()
        
        results = search_wikis(query, limit=5)
        
        if not results:
            await interaction.followup.send(
                f"❌ No results found for **{query}**",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"🔍 Wiki Search: {query}",
            description=f"Found {len(results)} results",
            color=discord.Color.blue()
        )
        
        for result in results:
            embed.add_field(
                name=f"📄 {result['title']}",
                value=f"**Wiki:** {result['wiki']}\n"
                      f"{result['snippet']}\n"
                      f"[Read More]({result['url']})",
                inline=False
            )
        
        await interaction.followup.send(embed=embed)
    
    @bot.tree.command(name="wikiinfo", description="View wiki scraper statistics")
    async def wikiinfo(interaction: discord.Interaction):
        """View wiki stats"""
        stats = get_wiki_stats()
        
        embed = discord.Embed(
            title="📚 Wiki Information",
            description=f"Total pages cached: **{stats['total_pages']}**",
            color=discord.Color.blue()
        )
        
        for wiki_name, wiki_stats in stats['wikis'].items():
            embed.add_field(
                name=f"📖 {wiki_name}",
                value=f"Pages: **{wiki_stats['pages']}**\n"
                      f"Last Update: {wiki_stats['last_update'][:10] if wiki_stats['last_update'] != 'Never' else 'Never'}",
                inline=True
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ═══════════════════════════════════════════════════════════════
    # SUGGESTIONS COMMAND
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="suggestions", description="Send a suggestion to staff")
    @app_commands.describe(suggestion="Your suggestion")
    async def suggestions(interaction: discord.Interaction, suggestion: str):
        """Send suggestion to staff"""
        
        # Get suggestions channel
        channel = interaction.guild.get_channel(SUGGESTIONS_CHANNEL_ID)
        
        if not channel:
            await interaction.response.send_message(
                "❌ Suggestions channel not found!",
                ephemeral=True
            )
            return
        
        # Create embed
        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_author(
            name=f"{interaction.user.display_name}",
            icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        )
        
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        
        # Send to suggestions channel
        msg = await channel.send(embed=embed)
        
        # Add reaction emojis for voting
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        
        await interaction.response.send_message(
            "✅ Your suggestion has been sent to staff!",
            ephemeral=True
        )
    
    # ═══════════════════════════════════════════════════════════════
    # BASIC INFO COMMANDS
    # ═══════════════════════════════════════════════════════════════
    
    @bot.tree.command(name="ping", description="Check bot latency")
    async def ping(interaction: discord.Interaction):
        """Check bot latency"""
        latency = round(bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=discord.Color.green() if latency < 200 else discord.Color.orange()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="about", description="About the bot")
    async def about(interaction: discord.Interaction):
        """Bot info"""
        embed = discord.Embed(
            title=f"🤖 CSR Bot v{BOT_VERSION}",
            description="Multi-language moderation + AI chat + Wiki search",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="👨‍💻 Creator", value=BOT_AUTHOR, inline=True)
        embed.add_field(name="🧪 Tester", value="flasharrow2003", inline=True)
        embed.add_field(name="📊 Servers", value=str(len(bot.guilds)), inline=True)
        
        features = [
            "✅ Multi-language moderation",
            "✅ AI-powered chat",
            "✅ Wiki search (SBOR + Blox Fruits)",
            "✅ Profile system",
            "✅ Verification system",
            "✅ Birthday tracking"
        ]
        
        embed.add_field(
            name="🎯 Features",
            value="\n".join(features),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="modstatus", description="Check moderation status")
    async def modstatus(interaction: discord.Interaction):
        """Check moderation status"""
        embed = discord.Embed(
            title="🛡️ Moderation Status",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Status",
            value=get_moderation_status(),
            inline=False
        )
        
        embed.add_field(
            name="Badwords Loaded",
            value=str(get_badword_count()),
            inline=True
        )
        
        # Check AI APIs
        apis = []
        if PERSPECTIVE_API_KEY:
            apis.append("✅ Perspective API")
        if OPENAI_API_KEY:
            apis.append("✅ OpenAI")
        if GROK_API_KEY:
            apis.append("✅ Grok")
        if GROQ_API_KEY:
            apis.append("✅ Groq")
        if ANTHROPIC_API_KEY:
            apis.append("✅ Claude")
        
        if apis:
            embed.add_field(
                name="AI APIs",
                value="\n".join(apis),
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="help", description="View all available commands")
    async def help_command(interaction: discord.Interaction):
        """Show help menu"""
        embed = discord.Embed(
            title="📚 CSR Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )
        
        # User commands
        user_cmds = [
            "`/profile` - View user profile",
            "`/settings` - Change language/timezone",
            "`/wikisearch` - Search wikis",
            "`/suggestions` - Send suggestion",
            "`/ping` - Check latency",
            "`/about` - Bot information",
            "`/modstatus` - Moderation status",
            "`/help` - This menu"
        ]
        
        embed.add_field(
            name="👤 User Commands",
            value="\n".join(user_cmds),
            inline=False
        )
        
        # Staff commands (if staff)
        if any(role.id in STAFF_ROLE_IDS + ADMIN_ROLE_IDS for role in interaction.user.roles):
            staff_cmds = [
                "`/addfaq` - Add FAQ",
                "`/listfaqs` - List FAQs",
                "`/removefaq` - Remove FAQ",
                "`/addbadword` - Add badword",
                "`/removebadword` - Remove badword",
                "`/testmod` - Test moderation",
                "`/forcefetch` - Update wiki cache",
                "`/kick` - Kick member",
                "`/ban` - Ban member",
                "`/mute` - Mute member",
                "`/announcement` - Send announcement"
            ]
            
            embed.add_field(
                name="👮 Staff Commands",
                value="\n".join(staff_cmds),
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    print("✅ User commands loaded!")
