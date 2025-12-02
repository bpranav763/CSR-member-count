"""
═══════════════════════════════════════════════════════════════
🛠️ Utils Package - Helper Functions & Utilities
═══════════════════════════════════════════════════════════════
"""
import json
import os
from typing import Optional, Dict, Any

print("🛠️ Loading utils package...")

# ═══════════════════════════════════════════════════════════════
# JSON FILE OPERATIONS
# ═══════════════════════════════════════════════════════════════

def load_json(filepath: str, default=None) -> Any:
    """Load JSON file, return default if not found"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load {filepath}: {e}")
    return default if default is not None else {}

def save_json(filepath: str, data: Any) -> bool:
    """Save data to JSON file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️ Failed to save {filepath}: {e}")
        return False

# ═══════════════════════════════════════════════════════════════
# PERMISSION CHECKS
# ═══════════════════════════════════════════════════════════════

def is_admin(interaction) -> bool:
    """Check if user is admin"""
    from config import ADMIN_ROLE_IDS
    return any(role.id in ADMIN_ROLE_IDS for role in interaction.user.roles)

def is_staff(interaction) -> bool:
    """Check if user is staff or admin"""
    from config import STAFF_ROLE_IDS, ADMIN_ROLE_IDS
    user_role_ids = [role.id for role in interaction.user.roles]
    return any(rid in STAFF_ROLE_IDS + ADMIN_ROLE_IDS for rid in user_role_ids)

def staff_or_admin():
    """Decorator for staff/admin only commands"""
    async def predicate(interaction):
        return is_staff(interaction) or is_admin(interaction)
    return predicate

# ═══════════════════════════════════════════════════════════════
# USER SETTINGS
# ═══════════════════════════════════════════════════════════════

SETTINGS_FILE = "data/user_settings.json"

def get_user_language(user_id: int) -> str:
    """Get user's language preference"""
    settings = load_json(SETTINGS_FILE, {})
    return settings.get(str(user_id), {}).get('language', 'en')

def set_user_language(user_id: int, language: str) -> bool:
    """Set user's language preference"""
    settings = load_json(SETTINGS_FILE, {})
    if str(user_id) not in settings:
        settings[str(user_id)] = {}
    settings[str(user_id)]['language'] = language
    return save_json(SETTINGS_FILE, settings)

def get_user_timezone(user_id: int) -> str:
    """Get user's timezone"""
    settings = load_json(SETTINGS_FILE, {})
    return settings.get(str(user_id), {}).get('timezone', 'UTC')

def set_user_timezone(user_id: int, timezone: str) -> bool:
    """Set user's timezone"""
    settings = load_json(SETTINGS_FILE, {})
    if str(user_id) not in settings:
        settings[str(user_id)] = {}
    settings[str(user_id)]['timezone'] = timezone
    return save_json(SETTINGS_FILE, settings)

# ═══════════════════════════════════════════════════════════════
# PROFILE SYSTEM
# ═══════════════════════════════════════════════════════════════

PROFILES_FILE = "data/profiles.json"

def get_user_profile(user_id: int) -> dict:
    """Get user profile data"""
    profiles = load_json(PROFILES_FILE, {})
    return profiles.get(str(user_id), {
        "bio": None,
        "birthday": None,
        "favorite_color": None,
        "roblox_username": None,
        "roblox_id": None,
        "discord_usernames": [],
        "roblox_usernames": [],
        "tracking_message_id": None,
        "last_updated": None
    })

def update_user_profile(user_id: int, data: dict) -> bool:
    """Update user profile"""
    profiles = load_json(PROFILES_FILE, {})
    user_id_str = str(user_id)
    
    if user_id_str not in profiles:
        profiles[user_id_str] = get_user_profile(user_id)
    
    profiles[user_id_str].update(data)
    return save_json(PROFILES_FILE, profiles)

# ═══════════════════════════════════════════════════════════════
# BADWORDS MANAGEMENT
# ═══════════════════════════════════════════════════════════════

BADWORDS_FILE = "data/badwords.txt"

def load_badwords() -> set:
    """Load badwords from file"""
    try:
        if os.path.exists(BADWORDS_FILE):
            with open(BADWORDS_FILE, 'r', encoding='utf-8') as f:
                return set(line.strip().lower() for line in f if line.strip())
    except Exception as e:
        print(f"⚠️ Failed to load badwords: {e}")
    return set()

def save_badwords(words: set) -> bool:
    """Save badwords to file"""
    try:
        os.makedirs(os.path.dirname(BADWORDS_FILE), exist_ok=True)
        with open(BADWORDS_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(words)))
        return True
    except Exception as e:
        print(f"⚠️ Failed to save badwords: {e}")
        return False

def add_badword(word: str) -> bool:
    """Add word to badwords list"""
    words = load_badwords()
    words.add(word.lower())
    return save_badwords(words)

def remove_badword(word: str) -> bool:
    """Remove word from badwords list"""
    words = load_badwords()
    words.discard(word.lower())
    return save_badwords(words)

def get_badword_count() -> int:
    """Get count of badwords"""
    return len(load_badwords())

# ═══════════════════════════════════════════════════════════════
# MODERATION SYSTEM
# ═══════════════════════════════════════════════════════════════

async def check_message_toxicity(content: str) -> tuple:
    """
    Check message for toxicity
    Returns: (is_toxic: bool, category: str, confidence: float)
    """
    from config import CHAT_FILTER_ENABLED, AI_MODERATION_ENABLED
    import re
    
    # Check badwords first
    if CHAT_FILTER_ENABLED:
        badwords = load_badwords()
        content_lower = content.lower()
        
        for word in badwords:
            # Use word boundaries to avoid false positives
            if re.search(r'\b' + re.escape(word) + r'\b', content_lower):
                return (True, "Inappropriate Language", 1.0)
    
    # TODO: Add AI moderation API calls here if enabled
    if AI_MODERATION_ENABLED:
        pass  # Implement Perspective API / OpenAI Moderation
    
    return (False, None, 0.0)

def get_moderation_status() -> str:
    """Get moderation system status"""
    from config import CHAT_FILTER_ENABLED, AI_MODERATION_ENABLED
    
    if CHAT_FILTER_ENABLED and AI_MODERATION_ENABLED:
        return "Full Protection (Badwords + AI)"
    elif CHAT_FILTER_ENABLED:
        return "Badwords Filter Only"
    elif AI_MODERATION_ENABLED:
        return "AI Moderation Only"
    else:
        return "Disabled"

# ═══════════════════════════════════════════════════════════════
# WIKI SYSTEM
# ═══════════════════════════════════════════════════════════════

WIKI_DATA_FILE = "data/wiki_data.json"

def search_wiki(query: str) -> list:
    """Search wiki data"""
    wiki_data = load_json(WIKI_DATA_FILE, {})
    results = []
    query_lower = query.lower()
    
    for wiki_name, pages in wiki_data.items():
        for page_title, page_data in pages.items():
            if query_lower in page_title.lower():
                results.append({
                    "wiki": wiki_name,
                    "title": page_title,
                    "url": page_data.get("url"),
                    "content": page_data.get("content", "")[:200]
                })
    
    return results[:5]  # Return top 5 results

def fetch_wiki_page(page_name: str, wiki: str = "sbor") -> Optional[str]:
    """Fetch specific wiki page"""
    wiki_data = load_json(WIKI_DATA_FILE, {})
    
    if wiki in wiki_data and page_name in wiki_data[wiki]:
        return wiki_data[wiki][page_name].get("content")
    
    return None

# ═══════════════════════════════════════════════════════════════
# FAQ SYSTEM
# ═══════════════════════════════════════════════════════════════

FAQ_FILE = "data/faqs.json"

def get_all_faqs() -> dict:
    """Get all FAQs"""
    return load_json(FAQ_FILE, {})

def add_faq(question: str, answer: str, keywords: str) -> str:
    """Add new FAQ, return FAQ ID"""
    faqs = load_json(FAQ_FILE, {})
    
    # Generate ID
    faq_id = f"faq_{len(faqs) + 1}"
    
    faqs[faq_id] = {
        "question": question,
        "answer": answer,
        "keywords": [k.strip().lower() for k in keywords.split(',')]
    }
    
    save_json(FAQ_FILE, faqs)
    return faq_id

def remove_faq(faq_id: str) -> bool:
    """Remove FAQ"""
    faqs = load_json(FAQ_FILE, {})
    
    if faq_id in faqs:
        del faqs[faq_id]
        save_json(FAQ_FILE, faqs)
        return True
    
    return False

def search_faq(query: str) -> Optional[dict]:
    """Search FAQs by keywords"""
    faqs = load_json(FAQ_FILE, {})
    query_lower = query.lower()
    
    for faq_id, faq_data in faqs.items():
        for keyword in faq_data.get("keywords", []):
            if keyword in query_lower:
                return {
                    "id": faq_id,
                    "question": faq_data["question"],
                    "answer": faq_data["answer"]
                }
    
    return None

# ═══════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════

__all__ = [
    # JSON operations
    'load_json',
    'save_json',
    
    # Permissions
    'is_admin',
    'is_staff',
    'staff_or_admin',
    
    # User settings
    'get_user_language',
    'set_user_language',
    'get_user_timezone',
    'set_user_timezone',
    
    # Profile system
    'get_user_profile',
    'update_user_profile',
    
    # Badwords
    'load_badwords',
    'save_badwords',
    'add_badword',
    'remove_badword',
    'get_badword_count',
    
    # Moderation
    'check_message_toxicity',
    'get_moderation_status',
    
    # Wiki
    'search_wiki',
    'fetch_wiki_page',
    
    # FAQ
    'get_all_faqs',
    'add_faq',
    'remove_faq',
    'search_faq'
]

print("✅ Utils package loaded successfully!")
