"""
═══════════════════════════════════════════════════════════════
📚 Wiki Fetcher - Scrapes Fandom wikis
Fetches ALL pages from SBOR and Blox Fruits wikis
═══════════════════════════════════════════════════════════════
"""

import aiohttp
import asyncio
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

WIKIS = {
    "sbor": {
        "name": "Soul Blade Online Rebirth",
        "base_url": "https://soul-blade-online-rebirth.fandom.com",
        "api_url": "https://soul-blade-online-rebirth.fandom.com/api.php"
    },
    "bloxfruits": {
        "name": "Blox Fruits",
        "base_url": "https://blox-fruits.fandom.com",
        "api_url": "https://blox-fruits.fandom.com/api.php"
    }
}

WIKI_DATA_FILE = "data/wiki_data.json"
RATE_LIMIT_DELAY = 0.5  # Seconds between requests
CACHE_DURATION_DAYS = 30  # Re-scrape pages older than this

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def load_wiki_data() -> dict:
    """Load cached wiki data"""
    try:
        if os.path.exists(WIKI_DATA_FILE):
            with open(WIKI_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load wiki data: {e}")
    return {}

def save_wiki_data(data: dict) -> bool:
    """Save wiki data to file"""
    try:
        os.makedirs(os.path.dirname(WIKI_DATA_FILE), exist_ok=True)
        with open(WIKI_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"⚠️ Failed to save wiki data: {e}")
        return False

def should_update_page(page_data: dict) -> bool:
    """Check if page should be re-scraped"""
    if "last_updated" not in page_data:
        return True
    
    try:
        last_updated = datetime.fromisoformat(page_data["last_updated"])
        age = datetime.utcnow() - last_updated
        return age > timedelta(days=CACHE_DURATION_DAYS)
    except:
        return True

# ═══════════════════════════════════════════════════════════════
# WIKI SCRAPER
# ═══════════════════════════════════════════════════════════════

async def get_all_pages(wiki_key: str, session: aiohttp.ClientSession) -> List[str]:
    """Get list of all pages in wiki"""
    wiki = WIKIS[wiki_key]
    pages = []
    continue_param = None
    
    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "500",
            "format": "json"
        }
        
        if continue_param:
            params["apcontinue"] = continue_param
        
        try:
            async with session.get(wiki["api_url"], params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Add pages
                    for page in data.get("query", {}).get("allpages", []):
                        pages.append(page["title"])
                    
                    # Check if more pages exist
                    if "continue" in data:
                        continue_param = data["continue"]["apcontinue"]
                    else:
                        break
                else:
                    print(f"❌ Failed to fetch page list: HTTP {response.status}")
                    break
        except Exception as e:
            print(f"❌ Error fetching page list: {e}")
            break
        
        await asyncio.sleep(RATE_LIMIT_DELAY)
    
    return pages

async def scrape_page(wiki_key: str, page_title: str, session: aiohttp.ClientSession) -> Optional[dict]:
    """Scrape single wiki page"""
    wiki = WIKIS[wiki_key]
    
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text|images"
    }
    
    try:
        async with session.get(wiki["api_url"], params=params) as response:
            if response.status != 200:
                return None
            
            data = await response.json()
            
            if "parse" not in data:
                return None
            
            # Extract HTML content
            html = data["parse"]["text"]["*"]
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Get images
            images = data["parse"].get("images", [])
            
            return {
                "title": page_title,
                "content": text[:5000],  # Limit content length
                "url": f"{wiki['base_url']}/wiki/{page_title.replace(' ', '_')}",
                "images": images[:5],  # Top 5 images
                "last_updated": datetime.utcnow().isoformat()
            }
    
    except Exception as e:
        print(f"❌ Error scraping {page_title}: {e}")
        return None

async def fetch_wiki(wiki_key: str, force: bool = False, progress_callback=None) -> int:
    """
    Fetch entire wiki
    Returns number of pages scraped
    """
    print(f"\n🔍 Fetching {WIKIS[wiki_key]['name']} wiki...")
    
    # Load existing data
    all_data = load_wiki_data()
    if wiki_key not in all_data:
        all_data[wiki_key] = {}
    
    wiki_data = all_data[wiki_key]
    
    async with aiohttp.ClientSession() as session:
        # Get all pages
        pages = await get_all_pages(wiki_key, session)
        print(f"📄 Found {len(pages)} pages")
        
        if not pages:
            return 0
        
        # Filter pages that need updating
        if not force:
            pages_to_scrape = [
                p for p in pages 
                if p not in wiki_data or should_update_page(wiki_data[p])
            ]
        else:
            pages_to_scrape = pages
        
        print(f"🔄 Scraping {len(pages_to_scrape)} pages...")
        
        # Scrape pages
        scraped_count = 0
        for i, page_title in enumerate(pages_to_scrape, 1):
            page_data = await scrape_page(wiki_key, page_title, session)
            
            if page_data:
                wiki_data[page_title] = page_data
                scraped_count += 1
            
            # Progress update
            if progress_callback and i % 50 == 0:
                await progress_callback(f"Scraped {i}/{len(pages_to_scrape)} pages...")
            
            # Rate limiting
            await asyncio.sleep(RATE_LIMIT_DELAY)
        
        # Save data
        all_data[wiki_key] = wiki_data
        save_wiki_data(all_data)
        
        print(f"✅ Scraped {scraped_count} pages from {WIKIS[wiki_key]['name']}")
        return scraped_count

async def fetch_all_wikis(force: bool = False, progress_callback=None) -> Dict[str, int]:
    """
    Fetch all wikis
    Returns dict of wiki_key: pages_scraped
    """
    results = {}
    
    for wiki_key in WIKIS.keys():
        try:
            count = await fetch_wiki(wiki_key, force, progress_callback)
            results[wiki_key] = count
        except Exception as e:
            print(f"❌ Failed to fetch {wiki_key}: {e}")
            results[wiki_key] = 0
    
    return results

# ═══════════════════════════════════════════════════════════════
# SEARCH FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def search_wikis(query: str, limit: int = 5) -> List[dict]:
    """Search all wikis for query"""
    wiki_data = load_wiki_data()
    results = []
    query_lower = query.lower()
    
    for wiki_key, pages in wiki_data.items():
        wiki_name = WIKIS[wiki_key]["name"]
        
        for page_title, page_data in pages.items():
            # Check if query matches title or content
            if (query_lower in page_title.lower() or 
                query_lower in page_data.get("content", "").lower()):
                
                results.append({
                    "wiki": wiki_name,
                    "title": page_title,
                    "url": page_data.get("url"),
                    "snippet": page_data.get("content", "")[:200] + "...",
                    "relevance": (
                        100 if query_lower in page_title.lower() else 50
                    )
                })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    
    return results[:limit]

def get_wiki_stats() -> dict:
    """Get statistics about cached wiki data"""
    wiki_data = load_wiki_data()
    
    stats = {
        "total_pages": 0,
        "wikis": {}
    }
    
    for wiki_key, pages in wiki_data.items():
        wiki_name = WIKIS[wiki_key]["name"]
        page_count = len(pages)
        
        stats["wikis"][wiki_name] = {
            "pages": page_count,
            "last_update": max(
                (p.get("last_updated", "") for p in pages.values()),
                default="Never"
            )
        }
        stats["total_pages"] += page_count
    
    return stats

# ═══════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════

__all__ = [
    'fetch_wiki',
    'fetch_all_wikis',
    'search_wikis',
    'get_wiki_stats'
]
