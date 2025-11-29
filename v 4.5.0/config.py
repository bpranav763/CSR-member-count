"""
═══════════════════════════════════════════════════════════════
🔧 CSR Bot v4.0 - CONFIG MODULE (COMPLETE)
Update ONLY this file to change settings!
═══════════════════════════════════════════════════════════════
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# BOT INFO
# ═══════════════════════════════════════════════════════════════

BOT_VERSION = "4.0.0"
BOT_AUTHOR = "kikusuka"
BOT_CREATED = "October 24, 2025"

# ═══════════════════════════════════════════════════════════════
# API TOKENS - Set in .env file!
# ═══════════════════════════════════════════════════════════════

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GROK_API_KEY = os.getenv('GROK_API_KEY', '')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
HF_TOKEN = os.getenv('HF_TOKEN', '')

if not TOKEN:
    raise ValueError("❌ DISCORD_BOT_TOKEN not found in .env!")

# ═══════════════════════════════════════════════════════════════
# CHANNEL IDS - UPDATE THESE!
# ═══════════════════════════════════════════════════════════════

MODLOG_CHANNEL_ID = 1429402899649134664
VERIFICATION_CHANNEL_ID = 1433909897749073931
ALLIANCE_CHANNEL_ID = 1429402899649134664
AI_CHAT_CHANNEL_ID = 1429402899649134664
HELP_CHANNEL_ID = 1434121366008889457
DAILYCHECKS_CHANNEL_ID = 1433403158612279327
MEMBER_COUNT_CHANNEL_ID = 1432803218919919666

# ═══════════════════════════════════════════════════════════════
# ROLE IDS - UPDATE THESE!
# ═══════════════════════════════════════════════════════════════

CSR_STAFF_ROLE_ID = 1430084386837102673
TESTER_ROLE_ID = 1433887090621284393
VISITOR_ROLE_ID = 1433907795593531513
MUTED_ROLE_ID = 1433893267816054844
VERIFICATION_PENDING_ROLE_ID = 1425155127530225767
MEMBER_APPROVED_ROLE_ID = 1425144091762495631

# ═══════════════════════════════════════════════════════════════
# ROBLOX
# ═══════════════════════════════════════════════════════════════

GROUP_ID = '1003228779'
GUILD_IMAGE = 'https://tr.rbxcdn.com/180DAY-929c99c9ad05b139c8851f873606876e/150/150/Image/Webp/noFilter'
CSR_EMOJI = "<:CSR:1432804739447263333>"

# ═══════════════════════════════════════════════════════════════
# FEATURES
# ═══════════════════════════════════════════════════════════════

CHAT_FILTER_ENABLED = True
AI_MODERATION_ENABLED = True
UPDATE_INTERVAL = 300

# ═══════════════════════════════════════════════════════════════
# LANGUAGES
# ═══════════════════════════════════════════════════════════════

SUPPORTED_LANGUAGES = {
    'en': '🇺🇸 English', 'es': '🇪🇸 Español', 'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch', 'pt': '🇵🇹 Português', 'ja': '🇯🇵 日本語',
    'ko': '🇰🇷 한국어', 'zh-cn': '🇨🇳 中文', 'hi': '🇮🇳 हिन्दी',
    'ar': '🇸🇦 العربية', 'ru': '🇷🇺 Русский', 'tr': '🇹🇷 Türkçe',
    'nl': '🇳🇱 Nederlands', 'pl': '🇵🇱 Polski', 'id': '🇮🇩 Indonesia',
    'th': '🇹🇭 ภาษาไทย', 'ms': '🇲🇾 Bahasa Melayu', 'vi': '🇻🇳 Tiếng Việt',
    'it': '🇮🇹 Italiano'
}

SUPPORTED_TIMEZONES = {
    'UTC': 'UTC',
    'America/New_York': 'EST/EDT (US East)',
    'America/Chicago': 'CST/CDT (US Central)',
    'America/Denver': 'MST/MDT (US Mountain)',
    'America/Los_Angeles': 'PST/PDT (US West)',
    'Europe/London': 'GMT/BST (UK)',
    'Europe/Paris': 'CET/CEST (Europe)',
    'Europe/Berlin': 'CET/CEST (Germany)',
    'Europe/Moscow': 'MSK (Russia)',
    'Asia/Tokyo': 'JST (Japan)',
    'Asia/Seoul': 'KST (Korea)',
    'Asia/Shanghai': 'CST (China)',
    'Asia/Singapore': 'SGT (Singapore)',
    'Asia/Dubai': 'GST (UAE)',
    'Australia/Sydney': 'AEDT/AEST (Australia)',
    'Pacific/Auckland': 'NZDT/NZST (New Zealand)'
}

# ═══════════════════════════════════════════════════════════════
# FILE PATHS
# ═══════════════════════════════════════════════════════════════

DATA_DIR = "data"
CUSTOM_KNOWLEDGE_FILE = f"{DATA_DIR}/custom_knowledge.json"
GUILD_FAQS_FILE = f"{DATA_DIR}/guild_faqs.json"
USER_SETTINGS_FILE = f"{DATA_DIR}/user_settings.json"
BADWORDS_FILE = "badwords.txt"

os.makedirs(DATA_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# ALLIANCE SYSTEM
# ═══════════════════════════════════════════════════════════════
# Alliance thread ID
ALLIANCE_THREAD_ID = 1435975636916109322
