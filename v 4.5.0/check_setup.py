"""
═══════════════════════════════════════════════════════════════
🔍 Setup Checker - Verify bot configuration
Run this to check if everything is set up correctly
═══════════════════════════════════════════════════════════════
"""

import os
import sys

def check_env_file():
    """Check .env file"""
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("  ❌ .env file not found!")
        print("     Create a .env file with:")
        print("     DISCORD_BOT_TOKEN=your_token_here")
        print("     GROQ_API_KEY=your_groq_key_here")
        return False
    
    print("  ✅ .env file exists")
    
    # Load .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check DISCORD_BOT_TOKEN
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("  ❌ DISCORD_BOT_TOKEN not set in .env")
        return False
    print(f"  ✅ DISCORD_BOT_TOKEN: {token[:20]}...")
    
    # Check GROQ_API_KEY
    groq = os.getenv('GROQ_API_KEY')
    if not groq:
        print("  ⚠️ GROQ_API_KEY not set (AI chat won't work)")
        print("     Get free key: https://console.groq.com")
    else:
        print(f"  ✅ GROQ_API_KEY: {groq[:20]}...")
    
    return True

def check_file_structure():
    """Check file structure"""
    print("\n🔍 Checking file structure...")
    
    required_files = {
        'bot.py': 'Main bot file',
        'config.py': 'Configuration',
        'requirements.txt': 'Dependencies',
        'utils/__init__.py': 'Utils package',
        'utils/ai_chat.py': 'AI chat system',
        'commands/__init__.py': 'Commands package',
        'commands/ai_commands.py': 'AI commands',
        'events/__init__.py': 'Events package',
        'events/on_message.py': 'Message handler',
    }
    
    missing = []
    for file, desc in required_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file} - {desc}")
        else:
            print(f"  ❌ {file} - {desc} (MISSING)")
            missing.append(file)
    
    if missing:
        print(f"\n  ⚠️ Missing {len(missing)} files!")
        return False
    
    return True

def check_dependencies():
    """Check Python dependencies"""
    print("\n🔍 Checking dependencies...")
    
    required = {
        'discord': 'discord.py',
        'aiohttp': 'aiohttp',
        'dotenv': 'python-dotenv',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n  ⚠️ Missing {len(missing)} packages!")
        print(f"  📦 Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def test_ai_import():
    """Test AI chat import"""
    print("\n🔍 Testing AI chat system...")
    
    try:
        from utils.ai_chat import chat_with_groq, get_ai_status
        print("  ✅ AI chat module imports successfully")
        
        status = get_ai_status()
        print(f"\n{status}")
        
        return True
    except Exception as e:
        print(f"  ❌ AI chat failed to import: {e}")
        return False

def main():
    """Run all checks"""
    print("═" * 60)
    print("🔍 CSR Bot Setup Checker")
    print("═" * 60)
    
    checks = [
        check_env_file(),
        check_file_structure(),
        check_dependencies(),
        test_ai_import(),
    ]
    
    print("\n" + "═" * 60)
    
    if all(checks):
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 Your bot is ready to run!")
        print("   Run: python bot.py")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("\n📝 Fix the issues above and try again")
        sys.exit(1)
    
    print("═" * 60)

if __name__ == "__main__":
    main()
