"""
═══════════════════════════════════════════════════════════════
🔧 Utils Package - Helper Functions & Utilities
═══════════════════════════════════════════════════════════════
"""

# Import and expose commonly used functions
try:
    from .moderation import (
        check_message_toxicity,
        get_moderation_status,
        reload_badwords,
        add_badword,
        remove_badword,
        get_badword_count
    )
except ImportError as e:
    print(f"⚠️ Failed to import moderation: {e}")

try:
    from .helpers import (
        load_json,
        save_json,
        get_user_language,
        get_user_timezone,
        set_user_language,
        set_user_timezone,
        format_time,
        staff_or_admin,
        is_admin,
        log_to_modlog,
        log_action
    )
except ImportError as e:
    print(f"⚠️ Failed to import helpers: {e}")

try:
    from .translation import translate_text
except ImportError as e:
    print(f"⚠️ Failed to import translation: {e}")
    # Fallback - no translation
    async def translate_text(text, lang='en'):
        return text

try:
    from .ai_chat import get_ai_response, get_ai_status
except ImportError as e:
    print(f"⚠️ Failed to import ai_chat: {e}")
    # Fallback - stub functions
    async def get_ai_response(message, user_id):
        return "AI chat is being configured!", False
    
    def get_ai_status():
        return "⚠️ AI not configured"

try:
    from .wiki_fetcher import (
        fetch_wiki_pages,
        search_wiki,
        get_wiki_status
    )
except ImportError as e:
    print(f"⚠️ Failed to import wiki_fetcher: {e}")
    # Fallback - stub functions
    async def fetch_wiki_pages(url, file, max_pages=50):
        return 0
    
    def search_wiki(query, wiki_file, max_results=5):
        return []
    
    def get_wiki_status():
        return {
            'sbor': {'pages': 0, 'last_fetch': 'Never'},
            'bloxfruits': {'pages': 0, 'last_fetch': 'Never'},
            'total_pages': 0
        }

__all__ = [
    # Moderation
    'check_message_toxicity',
    'get_moderation_status',
    'reload_badwords',
    'add_badword',
    'remove_badword',
    'get_badword_count',
    
    # Helpers
    'load_json',
    'save_json',
    'get_user_language',
    'get_user_timezone',
    'set_user_language',
    'set_user_timezone',
    'format_time',
    'staff_or_admin',
    'is_admin',
    'log_to_modlog',
    'log_action',
    
    # Translation
    'translate_text',
    
    # AI Chat
    'get_ai_response',
    'get_ai_status',
    
    # Wiki
    'fetch_wiki_pages',
    'search_wiki',
    'get_wiki_status'
]
