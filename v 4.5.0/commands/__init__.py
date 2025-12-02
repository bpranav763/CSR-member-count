"""
═══════════════════════════════════════════════════════════════
📦 Commands Package - Load all command modules
═══════════════════════════════════════════════════════════════
"""

def setup_all_commands(bot):
    """Setup all command modules"""
    
    # User commands
    try:
        from .user_commands import setup
        setup(bot)
        print("  ✅ User commands")
    except Exception as e:
        print(f"  ⚠️ User commands failed: {e}")
    
    # Staff commands
    try:
        from .staff_commands import setup
        setup(bot)
        print("  ✅ Staff commands")
    except Exception as e:
        print(f"  ⚠️ Staff commands failed: {e}")
    
    # Admin commands
    try:
        from .admin_commands import setup
        setup(bot)
        print("  ✅ Admin commands")
    except Exception as e:
        print(f"  ⚠️ Admin commands failed: {e}")
    
    # AI commands
    try:
        from .ai_commands import setup
        setup(bot)
        print("  ✅ AI commands")
    except Exception as e:
        print(f"  ⚠️ AI commands failed: {e}")
    
    # Statistics commands (NEW)
    try:
        from .stats_commands import setup
        setup(bot)
        print("  ✅ Statistics commands")
    except Exception as e:
        print(f"  ⚠️ Statistics commands failed: {e}")
    
    # Help command (NEW)
    try:
        from .help_command import setup
        setup(bot)
        print("  ✅ Help command")
    except Exception as e:
        print(f"  ⚠️ Help command failed: {e}")
