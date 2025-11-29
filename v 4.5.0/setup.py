"""
═══════════════════════════════════════════════════════════════
🔧 CSR Bot Setup Script
Auto-creates folder structure and template files
═══════════════════════════════════════════════════════════════
"""

import os
import sys

def create_folder_structure():
    """Create all necessary folders"""
    folders = [
        'utils',
        'commands',
        'events',
        'ui',
        'data'
    ]
    
    print("📁 Creating folder structure...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"   ✅ {folder}/")
    
    print("✅ Folders created!")

def create_init_files():
    """Create __init__.py files"""
    packages = ['utils', 'commands', 'events', 'ui']
    
    print("\n📝 Creating __init__.py files...")
    for package in packages:
        init_file = os.path.join(package, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f'"""\n{package.capitalize()} package\n"""\n')
            print(f"   ✅ {package}/__init__.py")
    
    print("✅ Init files created!")

def create_env_template():
    """Create .env.template file"""
    print("\n📝 Creating .env.template...")
    
    template = """# ═══════════════════════════════════════════════════════════════
# CSR Bot v4.0 - Environment Variables
# RENAME THIS FILE TO: .env (remove .template)
# ═══════════════════════════════════════════════════════════════

# Discord Bot Token (Required)
DISCORD_BOT_TOKEN=your_discord_token_here

# Moderation APIs (Pick at least ONE!)
PERSPECTIVE_API_KEY=AIza_your_key_here
# OPENAI_API_KEY=sk_your_key_here

# AI Chat APIs (Pick at least ONE!)
GROK_API_KEY=xai_your_key_here
# GROQ_API_KEY=gsk_your_key_here
# ANTHROPIC_API_KEY=sk-ant_your_key_here
"""
    
    with open('.env.template', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("   ✅ .env.template")
    print("✅ Template created!")

def create_badwords_template():
    """Create badwords.txt template"""
    if os.path.exists('badwords.txt'):
        print("\n⚠️  badwords.txt already exists, skipping...")
        return
    
    print("\n📝 Creating badwords.txt template...")
    
    template = """# ═══════════════════════════════════════════════════════════════
# CSR Bot - Badwords List
# Add one word per line
# Lines starting with # are comments
# ═══════════════════════════════════════════════════════════════

# Add your badwords here!
# Example:
# badword1
# badword2
# phrase with spaces
"""
    
    with open('badwords.txt', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("   ✅ badwords.txt")
    print("✅ Template created!")

def check_files():
    """Check which files are missing"""
    required_files = {
        'main.py': 'Main bot runner',
        'config.py': 'Configuration file',
        'requirements.txt': 'Python dependencies',
        'utils/moderation.py': 'Moderation module',
        'utils/helpers.py': 'Helper functions',
        'utils/translation.py': 'Translation system',
        'utils/ai_chat.py': 'AI chat system',
        'utils/wiki_fetcher.py': 'Wiki fetcher'
    }
    
    print("\n📊 Checking for required files...")
    missing = []
    
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"   ✅ {file} - {description}")
        else:
            print(f"   ❌ {file} - {description} (MISSING!)")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} files!")
        print("📝 You need to copy these files from the artifacts!")
    else:
        print("\n✅ All required files present!")
    
    return missing

def main():
    """Main setup function"""
    print("═" * 60)
    print("🚀 CSR Bot v4.0 - Setup Script")
    print("═" * 60)
    
    # Create folders
    create_folder_structure()
    
    # Create __init__ files
    create_init_files()
    
    # Create templates
    create_env_template()
    create_badwords_template()
    
    # Check for missing files
    missing = check_files()
    
    print("\n" + "═" * 60)
    if not missing:
        print("✅ Setup complete! Your bot structure is ready!")
        print("\n📝 Next steps:")
        print("   1. Copy all module files from artifacts")
        print("   2. Rename .env.template to .env")
        print("   3. Add your API keys to .env")
        print("   4. Update config.py with your channel/role IDs")
        print("   5. Run: python main.py")
    else:
        print("⚠️  Setup incomplete!")
        print("\n📝 Next steps:")
        print("   1. Copy the missing files from artifacts")
        print("   2. Run this script again to verify")
    print("═" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
