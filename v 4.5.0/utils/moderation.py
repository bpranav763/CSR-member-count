"""
═══════════════════════════════════════════════════════════════
🛡️ Multi-Language Moderation System
Supports 100+ languages with badwords.txt + AI APIs
═══════════════════════════════════════════════════════════════
"""

import aiohttp
import re
import os
from typing import Tuple, Set

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
BADWORDS_FILE = "badwords.txt"

# ═══════════════════════════════════════════════════════════════
# LOAD BADWORDS
# ═══════════════════════════════════════════════════════════════

def load_badwords() -> Set[str]:
    """Load badwords from file"""
    badwords = set()
    try:
        if os.path.exists(BADWORDS_FILE):
            with open(BADWORDS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word and not word.startswith('#'):
                        badwords.add(word)
            print(f"✅ Loaded {len(badwords)} badwords")
        else:
            print(f"⚠️ {BADWORDS_FILE} not found - creating empty file")
            with open(BADWORDS_FILE, 'w', encoding='utf-8') as f:
                f.write("# CSR Bot Badwords\n# Add one word per line\n")
    except Exception as e:
        print(f"⚠️ Error loading badwords: {e}")
    return badwords

BADWORDS = load_badwords()

def check_badwords(text: str) -> Tuple[bool, str, float]:
    """Check if text contains badwords"""
    if not BADWORDS:
        return False, "N/A", 0.0
    
    text_lower = text.lower()
    for badword in BADWORDS:
        pattern = r'\b' + re.escape(badword) + r'\b'
        if re.search(pattern, text_lower, re.UNICODE):
            return True, f"Badword: {badword}", 0.95
    
    return False, "Clean", 0.0

# ═══════════════════════════════════════════════════════════════
# LANGUAGE DETECTION
# ═══════════════════════════════════════════════════════════════

def detect_language(text: str) -> str:
    """Detect language from text"""
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return 'zh'
    elif any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in text):
        return 'ja'
    elif any('\uac00' <= char <= '\ud7af' for char in text):
        return 'ko'
    elif any('\u0400' <= char <= '\u04ff' for char in text):
        return 'ru'
    elif any('\u0600' <= char <= '\u06ff' for char in text):
        return 'ar'
    return 'en'

# ═══════════════════════════════════════════════════════════════
# PERSPECTIVE API
# ═══════════════════════════════════════════════════════════════

async def check_perspective_api(text: str) -> Tuple[bool, str, float]:
    """Check text using Perspective API"""
    if not PERSPECTIVE_API_KEY:
        return False, "N/A", 0.0
    
    try:
        language = detect_language(text)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                params={"key": PERSPECTIVE_API_KEY},
                json={
                    "comment": {"text": text},
                    "languages": [language],
                    "requestedAttributes": {
                        "TOXICITY": {},
                        "SEVERE_TOXICITY": {},
                        "THREAT": {}
                    },
                    "doNotStore": True
                },
                timeout=aiohttp.ClientTimeout(total=8)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    scores = data.get('attributeScores', {})
                    
                    # AGGRESSIVE THRESHOLDS - Catches more!
                    severe = scores.get('SEVERE_TOXICITY', {}).get('summaryScore', {}).get('value', 0)
                    if severe > 0.5:  # Lowered from 0.7
                        return True, f"Severe toxicity ({language})", severe
                    
                    threat = scores.get('THREAT', {}).get('summaryScore', {}).get('value', 0)
                    if threat > 0.6:  # Lowered from 0.8
                        return True, f"Threat ({language})", threat
                    
                    toxicity = scores.get('TOXICITY', {}).get('summaryScore', {}).get('value', 0)
                    if toxicity > 0.75:  # Lowered from 0.85
                        return True, f"Toxicity ({language})", toxicity
    except Exception as e:
        print(f"⚠️ Perspective error: {e}")
    
    return False, "Clean", 0.0

# ═══════════════════════════════════════════════════════════════
# OPENAI MODERATION
# ═══════════════════════════════════════════════════════════════

async def check_openai_moderation(text: str) -> Tuple[bool, str, float]:
    """Check text using OpenAI Moderation API"""
    if not OPENAI_API_KEY:
        return False, "N/A", 0.0
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/moderations",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={"input": text},
                timeout=aiohttp.ClientTimeout(total=8)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data['results'][0]
                    
                    if result['flagged']:
                        categories = result['categories']
                        scores = result['category_scores']
                        flagged = [c for c, f in categories.items() if f]
                        
                        if flagged:
                            highest = max(flagged, key=lambda x: scores[x])
                            score = scores[highest]
                            lang = detect_language(text)
                            return True, f"{highest} ({lang})", score
    except Exception as e:
        print(f"⚠️ OpenAI error: {e}")
    
    return False, "Clean", 0.0

# ═══════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ═══════════════════════════════════════════════════════════════

async def check_message_toxicity(text: str) -> Tuple[bool, str, float]:
    """Multi-layer moderation check"""
    
    # Layer 1: badwords.txt (instant)
    is_toxic, category, confidence = check_badwords(text)
    if is_toxic:
        return is_toxic, category, confidence
    
    # Layer 2: Perspective API
    if PERSPECTIVE_API_KEY:
        is_toxic, category, confidence = await check_perspective_api(text)
        if is_toxic:
            return is_toxic, category, confidence
    
    # Layer 3: OpenAI
    if OPENAI_API_KEY:
        is_toxic, category, confidence = await check_openai_moderation(text)
        if is_toxic:
            return is_toxic, category, confidence
    
    return False, "Clean", 0.0

# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def reload_badwords() -> int:
    """Reload badwords from file"""
    global BADWORDS
    BADWORDS = load_badwords()
    return len(BADWORDS)

def add_badword(word: str) -> bool:
    """Add a word to badwords list"""
    try:
        with open(BADWORDS_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n{word.lower()}")
        BADWORDS.add(word.lower())
        return True
    except:
        return False

def remove_badword(word: str) -> bool:
    """Remove a word from badwords list"""
    try:
        with open(BADWORDS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(BADWORDS_FILE, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip().lower() != word.lower():
                    f.write(line)
        BADWORDS.discard(word.lower())
        return True
    except:
        return False

def get_badword_count() -> int:
    """Get count of loaded badwords"""
    return len(BADWORDS)

def get_moderation_status() -> str:
    """Get current moderation status"""
    parts = []
    if BADWORDS:
        parts.append(f"✅ {len(BADWORDS)} badwords")
    if PERSPECTIVE_API_KEY:
        parts.append("✅ Perspective API")
    if OPENAI_API_KEY:
        parts.append("✅ OpenAI")
    return " | ".join(parts) if parts else "❌ Not configured"
