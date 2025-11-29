"""
═══════════════════════════════════════════════════════════════
🛠️ Helper Functions - Reusable Utilities
═══════════════════════════════════════════════════════════════
"""

import json
import os
from datetime import datetime
import pytz
import discord
from config import *

# ═══════════════════════════════════════════════════════════════
# JSON UTILITIES
# ═══════════════════════════════════════════════════════════════

def load_json(filepath, default=None):
    """Load JSON file"""
    if default is None:
        default = {}
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {filepath}: {e}")
    return default

def save_json(filepath, data):
    """Save JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️ Failed to save {filepath}: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# USER SETTINGS
# ═══════════════════════════════════════════════════════════════

def get_user_language(user_id):
    """Get user's preferred language"""
    settings = load_json(USER_SETTINGS_FILE)
    return settings.get(str(user_id), {}).get('language', 'en')

def get_user_timezone(user_id):
    """Get user's timezone"""
    settings = load_json(USER_SETTINGS_FILE)
    return settings.get(str(user_id), {}).get('timezone', 'UTC')

def set_user_language(user_id, language):
    """Set user's language"""
    settings = load_json(USER_SETTINGS_FILE)
    if str(user_id) not in settings:
        settings[str(user_id)] = {}
    settings[str(user_id)]['language'] = language
    return save_json(USER_SETTINGS_FILE, settings)

def set_user_timezone(user_id, timezone):
    """Set user's timezone"""
    settings = load_json(USER_SETTINGS_FILE)
    if str(user_id) not in settings:
        settings[str(user_id)] = {}
    settings[str(user_id)]['timezone'] = timezone
    return save_json(USER_SETTINGS_FILE, settings)

# ═══════════════════════════════════════════════════════════════
# TIME FORMATTING
# ═══════════════════════════════════════════════════════════════

def format_time(dt, timezone='UTC'):
    """Format datetime with timezone"""
    try:
        tz = pytz.timezone(timezone)
        localized = dt.replace(tzinfo=pytz.UTC).astimezone(tz)
        return localized.strftime('%Y-%m-%d %H:%M:%S %Z')
    except:
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')

# ═══════════════════════════════════════════════════════════════
# PERMISSION CHECKS (FIXED!)
# ═══════════════════════════════════════════════════════════════

def staff_or_admin(interaction: discord.Interaction) -> bool:
    """Check if user is staff or admin - FIXED!"""
    member = interaction.user
    staff_role = interaction.guild.get_role(CSR_STAFF_ROLE_ID)
    
    # Check if staff role exists and user has it
    has_staff_role = staff_role and staff_role in member.roles
    # Check if user is admin
    is_admin_user = member.guild_permissions.administrator
    
    return has_staff_role or is_admin_user

def is_admin(interaction: discord.Interaction) -> bool:
    """Check if user is admin - FIXED!"""
    return interaction.user.guild_permissions.administrator

# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

async def log_to_modlog(bot, embed):
    """Send embed to modlog channel"""
    try:
        modlog = bot.get_channel(MODLOG_CHANNEL_ID)
        if modlog:
            await modlog.send(embed=embed)
    except Exception as e:
        print(f"⚠️ Failed to log to modlog: {e}")

async def log_action(bot, message):
    """Log a moderation action - SIMPLIFIED!"""
    try:
        modlog = bot.get_channel(MODLOG_CHANNEL_ID)
        if modlog:
            await modlog.send(message)
    except Exception as e:
        print(f"⚠️ Failed to log action: {e}")
