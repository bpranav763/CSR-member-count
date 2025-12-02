"""
═══════════════════════════════════════════════════════════════
📦 Events Package - Bot Event Handlers
═══════════════════════════════════════════════════════════════
"""

print("📦 Loading events package...")

try:
    from .on_ready import setup as setup_on_ready
    print("   ✅ on_ready loaded")
except Exception as e:
    print(f"   ⚠️ Failed to load on_ready: {e}")
    def setup_on_ready(bot):
        pass

try:
    from .on_message import setup as setup_on_message
    print("   ✅ on_message loaded")
except Exception as e:
    print(f"   ⚠️ Failed to load on_message: {e}")
    def setup_on_message(bot):
        pass

try:
    from .on_member_join import setup as setup_on_member_join
    print("   ✅ on_member_join loaded")
except Exception as e:
    print(f"   ⚠️ Failed to load on_member_join: {e}")
    def setup_on_member_join(bot):
        pass

def setup_all_events(bot):
    """Setup all event handlers"""
    print("\n🔧 Setting up events...")
    setup_on_ready(bot)
    setup_on_message(bot)
    setup_on_member_join(bot)
    print("✅ All events loaded!\n")

__all__ = [
    'setup_all_events',
    'setup_on_ready',
    'setup_on_message',
    'setup_on_member_join'
]
