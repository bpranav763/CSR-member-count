# 🤖 CSR Bot v4.0

**Advanced Discord Bot for Champions of the Shattered Realm**

Multi-language moderation • AI Chat • Wiki Integration • Roblox Verification

---

## ✨ Features

### 🛡️ **Multi-Language Moderation**
- Supports **100+ languages**
- 4-layer protection system
- Custom badwords.txt (1000+ words included!)
- Perspective API + OpenAI Moderation
- Auto-delete toxic messages
- Modlog integration

### 🤖 **AI Chat System**
- **Grok** (xAI) - Primary AI
- **Groq** (Llama 3.3) - Fast backup
- **Claude** (Anthropic) - Fallback
- Knowledge base integration
- FAQ system
- Multi-language responses

### 📚 **Wiki Integration**
- SBOR Wiki (Sword Blox Online Rebirth)
- Blox Fruits Wiki
- Smart search
- Auto-caching

### 🌍 **Multi-Language Support**
- 20+ languages supported
- Auto-translation
- User language preferences

### ⏰ **Timezone Support**
- 16 timezones
- User timezone preferences
- Formatted timestamps

### 🎮 **Roblox Integration**
- Verification system
- Group linking
- Role management

---

## 📂 File Structure

```
csr_bot/
├── main.py                  # Main bot runner
├── config.py                # All configuration
├── requirements.txt         # Python dependencies
├── .env                     # API keys (create this!)
├── badwords.txt             # Custom badwords
│
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── helpers.py          # Helper functions
│   ├── translation.py      # Translation system
│   ├── moderation.py       # Multi-language moderation
│   ├── ai_chat.py          # AI chat system
│   └── wiki_fetcher.py     # Wiki integration
│
├── commands/                # Command modules
│   ├── __init__.py
│   ├── user_commands.py    # User commands
│   ├── staff_commands.py   # Staff commands
│   └── admin_commands.py   # Admin commands
│
├── events/                  # Event handlers
│   ├── __init__.py
│   ├── on_ready.py         # Startup events
│   ├── on_message.py       # Message handling
│   └── on_member_join.py   # Welcome system
│
└── ui/                      # UI components
    ├── __init__.py
    ├── verification.py     # Verification buttons
    ├── moderation.py       # Moderation review
    └── settings.py         # Settings menus
```

---

## 🚀 Quick Setup

### 1. **Install Python 3.11+**
Download from: https://www.python.org/downloads/

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Get API Keys**

#### Discord Bot Token (Required)
1. Go to: https://discord.com/developers/applications
2. Create Application → Bot → Copy Token

#### Perspective API (For Moderation - FREE!)
1. Go to: https://developers.perspectiveapi.com/s/
2. Sign up → Get API key
3. Limit: 1M requests/day

#### Grok API (For AI Chat)
1. Go to: https://console.x.ai/
2. Sign up → Create API key
3. You should have received this via email!

#### Groq API (Backup AI - FREE!)
1. Go to: https://console.groq.com/keys
2. Sign up → Create key
3. Limit: 14.4K requests/day

### 4. **Configure Bot**

#### Create `.env` file:
```env
# Discord Bot Token (Required)
DISCORD_BOT_TOKEN=your_discord_token_here

# Moderation API (pick at least one)
PERSPECTIVE_API_KEY=AIza_your_key_here
OPENAI_API_KEY=sk_your_key_here

# AI Chat (pick at least one)
GROK_API_KEY=xai_your_key_here
GROQ_API_KEY=gsk_your_key_here
```

#### Update `config.py` (lines 35-60):
```python
# Channel IDs (Right-click channel → Copy ID)
MODLOG_CHANNEL_ID = YOUR_CHANNEL_ID
VERIFICATION_CHANNEL_ID = YOUR_CHANNEL_ID
AI_CHAT_CHANNEL_ID = YOUR_CHANNEL_ID
# ... etc

# Role IDs (Right-click role → Copy ID)
CSR_STAFF_ROLE_ID = YOUR_ROLE_ID
# ... etc

# Roblox Group
GROUP_ID = 'YOUR_GROUP_ID'
```

### 5. **Run Bot**
```bash
python main.py
```

---

## 📋 Commands

### User Commands
- `/ping` - Check bot latency
- `/about` - Bot information
- `/aistatus` - Check AI system status
- `/modstatus` - Check moderation status
- `/wikisearch <game> <query>` - Search wiki
- `/settings` - View your settings
- `/setlanguage <lang>` - Set language
- `/settimezone <tz>` - Set timezone

### Staff Commands
- `/reloadbadwords` - Reload badwords.txt
- `/addbadword <word>` - Add badword
- `/removebadword <word>` - Remove badword
- `/testmod <text>` - Test moderation
- `/addknowledge <key> <info>` - Add knowledge
- `/addfaq <question> <answer> <keywords>` - Add FAQ

### Admin Commands
- `/forcefetch` - Force fetch wikis
- `/kick <member> [reason]` - Kick member
- `/ban <member> [reason]` - Ban member

---

## 🎯 Configuration

### Moderation Settings
Edit `config.py`:
```python
CHAT_FILTER_ENABLED = True
AI_MODERATION_ENABLED = True
```

### Supported Languages
```python
SUPPORTED_LANGUAGES = {
    'en': '🇺🇸 English',
    'es': '🇪🇸 Español',
    'fr': '🇫🇷 Français',
    # ... 20+ more!
}
```

### Supported Timezones
```python
SUPPORTED_TIMEZONES = {
    'UTC': 'UTC',
    'America/New_York': 'EST/EDT (US East)',
    'Europe/London': 'GMT/BST (UK)',
    # ... 16 total!
}
```

---

## 🛡️ Badwords.txt

The bot includes a comprehensive badwords list with 1000+ words across 20+ languages!

**Format:**
```txt
# Comments start with #
badword1
badword2
phrase with spaces
```

**Manage:**
- `/addbadword <word>` - Add word
- `/removebadword <word>` - Remove word
- `/reloadbadwords` - Reload file

---

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Bot not responding
1. Check bot has proper permissions
2. Enable "Message Content Intent" in Discord Developer Portal
3. Check bot token is correct

### Commands not showing
1. Wait 1 hour for global sync
2. Or kick/re-invite bot

### Moderation not working
1. Check API keys in `.env`
2. Check `CHAT_FILTER_ENABLED = True` in config
3. Check bot can delete messages

### AI chat not working
1. Check you have at least one AI API key
2. Check bot is mentioned correctly
3. Check `/aistatus` for API status

---

## 📊 System Requirements

- **Python:** 3.11 or higher
- **RAM:** 256MB minimum
- **Storage:** 100MB
- **Network:** Stable internet connection

---

## 🎉 Credits

- **Created by:** kikusuka
- **Tester:** flasharrow2003
- **Version:** 4.0.0
- **Released:** October 24, 2025

---

## 📝 License

Made with ❤️ for **Champions of the Shattered Realm**

---

## 🆘 Support

Need help? Ask in the support channel or DM kikusuka!

---

## 🔄 Updates

### v4.0.0 (Current)
- ✅ Multi-language moderation (100+ languages)
- ✅ AI chat with Grok, Groq, and Claude
- ✅ Wiki integration (SBOR + Blox Fruits)
- ✅ Modular architecture
- ✅ Complete documentation

---

**Made with ❤️ for CSR - Champions of the Shattered Realm**
