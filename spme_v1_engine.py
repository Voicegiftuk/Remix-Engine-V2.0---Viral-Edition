#!/usr/bin/env python3
"""
SAYPLAY MEDIA ENGINE (SPME) V1 - WITH TITAN OBSERVATORY
Real-time trend intelligence from 100 UK gift sources
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio
import json
import random
import urllib.parse
import shutil
import subprocess
import csv
import time

from dashboard_index_generator import DashboardIndexGenerator

# Libraries
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

import requests

try:
    from bs4 import BeautifulSoup
    import feedparser
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False

# --- CONFIG ---
class Config:
    GEMINI_MODEL = 'gemini-1.5-flash'
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    
    # Anti-Marketing Validator
    FORBIDDEN_WORDS = [
        "buy now", "click here", "order today", "limited offer",
        "discount code", "add to cart", "purchase now", "sales team"
    ]
    
    # Trend Scanner
    SCANNER_CSV = "sources_uk_gifts.csv"
    SCANNER_SAMPLE_SIZE = 20  # Scan 20/100 sources per run
    SCANNER_TIMEOUT = 5  # seconds per request

# --- UNIVERSAL SCANNER (TITAN OBSERVATORY) ---
class UniversalScanner:
    """Scans 100 UK gift sources for real-time trends"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.found_trends = []

    def scan(self):
        print("\n📡 TITAN OBSERVATORY: Scanning trend sources...")
        
        if not os.path.exists(self.csv_path):
            print(f"   ⚠️ CSV not found: {self.csv_path}")
            return []
        
        if not SCANNER_AVAILABLE:
            print(f"   ⚠️ Scanner libraries not available")
            return []

        # Load sources
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                sources = list(reader)
        except Exception as e:
            print(f"   ⚠️ Error reading CSV: {e}")
            return []
        
        # Random sample
        selection = random.sample(sources, min(len(sources), Config.SCANNER_SAMPLE_SIZE))
        print(f"   🔭 Scanning {len(selection)} random sources...")
        
        for site in selection:
            stype = site.get('typ', 'blog')
            url = site.get('url', '')
            name = site.get('nazwa', '')
            topic_hint = site.get('temat', 'gift ideas')

            try:
                # Social media - use signals from CSV
                if stype == 'social' or any(x in url for x in ['tiktok', 'instagram', 'twitter', 'pinterest', 'youtube']):
                    signal = f"{topic_hint} trending"
                    self.found_trends.append({
                        "topic": signal, 
                        "source": name, 
                        "type": "social_signal"
                    })
                    print(f"   📱 Social: {signal[:40]}")

                # Reddit (via RSS)
                elif 'reddit.com' in url:
                    self._scan_reddit(url)

                # RSS feeds
                elif stype == 'katalog' or url.endswith('xml') or url.endswith('rss'):
                    self._scan_rss(url, name)

                # Blogs (HTML scraping)
                else:
                    self._scan_blog_html(url, name)
                
                # Small delay to be polite
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                # Silently skip failed sources
                pass

        print(f"   ✅ Found {len(self.found_trends)} trends")
        return self.found_trends

    def _scan_rss(self, url, source_name):
        try:
            f = feedparser.parse(url)
            for e in f.entries[:2]:  # Get 2 latest
                if len(e.title) > 15:
                    self.found_trends.append({
                        "topic": e.title, 
                        "source": source_name, 
                        "type": "real_data"
                    })
                    print(f"   📰 RSS: {e.title[:40]}")
        except:
            pass

    def _scan_reddit(self, url):
        # Reddit RSS hack
        if not url.endswith('.rss'): 
            url = url.rstrip('/') + '/.rss'
        self._scan_rss(url, "Reddit")

    def _scan_blog_html(self, url, source_name):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(url, headers=headers, timeout=Config.SCANNER_TIMEOUT)
            soup = BeautifulSoup(r.text, 'lxml')
            
            # Find article titles (h2, h3)
            titles = soup.find_all(['h2', 'h3'], limit=3)
            for t in titles:
                text = t.get_text().strip()
                if 15 < len(text) < 100:
                    self.found_trends.append({
                        "topic": text, 
                        "source": source_name, 
                        "type": "real_data"
                    })
                    print(f"   🖊️ Blog: {text[:40]}")
        except:
            pass

# --- CMEL (Content Memory & Evolution Layer) ---
class CMEL:
    """Brain - remembers topics, angles, prevents duplicates"""
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    
                    # MIGRATION: Old format to new format
                    if "content_log" not in loaded:
                        print("   🔄 Migrating old format to CMEL v1...")
                        
                        new_data = {
                            "global_id_counter": loaded.get("last_episode_number", 100),
                            "knowledge_graph": [],
                            "content_log": [],
                            "social_signals": {}
                        }
                        
                        # Migrate old seo_pages
                        for page in loaded.get("seo_pages", []):
                            new_data["content_log"].append({
                                "id": new_data["global_id_counter"],
                                "date": page.get("created", datetime.now().isoformat()),
                                "type": "seo",
                                "topic": page.get("topic", "Unknown"),
                                "angle": "legacy",
                                "filename": page.get("filename", "")
                            })
                            new_data["global_id_counter"] += 1
                        
                        # Migrate old blog_posts
                        for post in loaded.get("blog_posts", []):
                            new_data["content_log"].append({
                                "id": new_data["global_id_counter"],
                                "date": post.get("created", datetime.now().isoformat()),
                                "type": "blog",
                                "topic": post.get("topic", "Unknown"),
                                "angle": "legacy",
                                "filename": post.get("filename", "")
                            })
                            new_data["global_id_counter"] += 1
                        
                        # Migrate old podcasts
                        for pod in loaded.get("podcasts", []):
                            new_data["content_log"].append({
                                "id": new_data["global_id_counter"],
                                "date": pod.get("created", datetime.now().isoformat()),
                                "type": "podcast",
                                "topic": pod.get("topic", "Unknown"),
                                "angle": "legacy",
                                "filename": pod.get("filename", "")
                            })
                            new_data["global_id_counter"] += 1
                        
                        print(f"   ✅ Migrated {len(new_data['content_log'])} items")
                        return new_data
                    
                    return loaded
            except Exception as e:
                print(f"   ⚠️ Error loading: {e}")
        
        # Fresh start
        return {
            "global_id_counter": 100,
            "knowledge_graph": [],
            "content_log": [],
            "social_signals": {}
        }

    def save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get_next_id(self):
        self.data["global_id_counter"] += 1
        return self.data["global_id_counter"]

    def is_topic_exhausted(self, topic):
        """Check if topic used >3 times"""
        count = sum(1 for item in self.data["content_log"] if item.get("topic") == topic)
        return count > 3

    def register_content(self, c_type, topic, angle, filename):
        entry = {
            "id": self.get_next_id(),
            "date": datetime.now().isoformat(),
            "type": c_type,
            "topic": topic,
            "angle": angle,
            "filename": filename
        }
        self.data["content_log"].append(entry)
        self.save()
        return entry["id"]

    def get_stats(self):
        return {
            "seo": sum(1 for x in self.data["content_log"] if x.get("type") == "seo"),
            "blog": sum(1 for x in self.data["content_log"] if x.get("type") == "blog"),
            "podcasts": sum(1 for x in self.data["content_log"] if x.get("type") == "podcast"),
            "last_id": self.data["global_id_counter"]
        }

# --- BLOCK 1: TREND INTELLIGENCE (WITH OBSERVATORY) ---
class TrendIntelligence:
    """Harvests topics from real-time scanner + fallback"""
    def __init__(self, brain):
        self.brain = brain
        self.scanner = UniversalScanner(Config.SCANNER_CSV)
        
        # Backup topics if scanner fails
        self.backup_topics = [
            "Long distance relationship gifts",
            "Gifts for grandparents who have everything",
            "Meaningful wedding favors",
            "Baby shower messages that last",
            "Comforting gifts for grief",
            "Graduation keepsakes UK",
            "First birthday time capsule ideas",
            "Anniversary gifts beyond flowers",
            "Retirement gifts with meaning",
            "New parent survival gifts",
            "Gifts for homesick students",
            "Voice messages for military families",
            "Memorial gifts for loss",
            "Wedding vows preservation",
            "Birthday wishes that last forever"
        ]

    def harvest_trends(self, cmel: CMEL):
        print("\n📡 BLOCK 1: Trend Intelligence")
        
        # Try scanner first
        scanned = self.scanner.scan()
        
        candidates = []
        
        if scanned:
            # Use real trends from scanner
            print(f"   🎯 Processing {len(scanned)} scanned trends...")
            for item in scanned:
                topic = item['topic']
                if not cmel.is_topic_exhausted(topic):
                    angle = self.brain.get_angle(topic)
                    candidates.append({"topic": topic, "angle": angle, "source": item.get('source', 'Unknown')})
                    print(f"   ✅ {topic[:50]}")
        else:
            # Fallback to backup topics
            print(f"   ⚠️ Scanner returned no results, using backup topics...")
            for topic in self.backup_topics:
                if not cmel.is_topic_exhausted(topic):
                    angle = self.brain.get_angle(topic)
                    candidates.append({"topic": topic, "angle": angle, "source": "backup"})
                    print(f"   ✅ {topic[:50]}")
        
        random.shuffle(candidates)
        selected = candidates[:10]
        print(f"   📊 Selected: {len(selected)} topics for production")
        return selected

# --- BLOCK 2: EDITORIAL ENGINE ---
class EditorialEngine:
    """Writes editorial blog posts with quality validation"""
    def __init__(self, brain):
        self.brain = brain

    def create_blog_post(self, topic, angle):
        print(f"\n✍️  BLOCK 2: Editorial Blog")
        print(f"   Topic: {topic}")
        print(f"   Angle: {angle}")
        
        persona = "Relationship Psychologist writing for The Atlantic. Empathetic, deep."
        
        prompt = f"""
{persona}

Write a deep essay about "{topic}".
ANGLE: {angle}
Focus on psychology of memory and voice.

RULES:
- NO sales pitch
- British English
- 1500+ characters
- Structure: Hook → Analysis → Voice Role → Subtle Solution

Mention SayPlay ONCE neutrally at end: "Solutions like SayPlay..."

JSON output:
{{
  "title": "...",
  "article_html": "<p>...</p>"
}}
"""
        
        for attempt in range(3):
            print(f"      Attempt {attempt + 1}/3...")
            content = self.brain.generate(prompt, json_mode=True)
            
            if self._validate(content):
                print(f"      ✅ Validated")
                return content
            
            print(f"      ⚠️  Failed validation")
        
        return self._emergency_blog(topic)

    def _validate(self, content):
        if not content:
            print(f"         ❌ No content returned")
            return False
        
        if not isinstance(content, dict):
            print(f"         ❌ Not a dict")
            return False
        
        if 'article_html' not in content:
            print(f"         ❌ Missing article_html")
            return False
        
        article_html = content.get('article_html', '')
        
        if len(article_html) < 1500:
            print(f"         ❌ Too short ({len(article_html)} chars, need 1500+)")
            return False
        
        article_lower = article_html.lower()
        for bad in Config.FORBIDDEN_WORDS:
            if bad in article_lower:
                print(f"         ❌ Forbidden: '{bad}'")
                return False
        
        print(f"         ✅ Valid ({len(article_html)} chars)")
        return True

    def _emergency_blog(self, topic):
        return {
            "title": f"{topic}: A Thoughtful Guide",
            "article_html": f"<p>Exploring {topic.lower()} through the lens of emotional connection and meaningful gift-giving. The psychology behind presents extends far beyond their material value, reaching into the realm of memory, presence, and emotional resonance.</p><p>When we consider {topic.lower()}, we're really contemplating how to bridge distance, preserve moments, and create lasting emotional connections. Voice messages and video recordings preserve not just words, but tone, emotion, laughter, and the unique essence of a person's presence.</p><p>Research in psychology shows that hearing a loved one's voice activates the same neural pathways as being with them in person. This neurological connection explains why voice messages carry such profound emotional weight. Solutions like SayPlay enable this through simple NFC technology, allowing anyone to attach personal voice or video messages to physical gifts.</p><p>The act of recording a message requires thoughtfulness and vulnerability. Unlike text, which can be edited and perfected, voice captures authenticity. This rawness creates deeper connections and more meaningful memories that last far beyond the moment of gift-giving itself.</p>"
        }

# --- BLOCK 3: SEO ENGINE ---
class SEOEngine:
    """Creates SEO pages with local targeting"""
    def __init__(self, brain):
        self.brain = brain

    def create_seo_page(self, topic, city):
        print(f"\n🌐 BLOCK 3: SEO Page")
        print(f"   Topic: {topic} in {city}")
        
        prompt = f"""
Senior SEO Specialist. Intent: Informational.

Create guide: "{topic} in {city}"

Include:
- Local {city} references (vibes, NOT spam)
- Mention Mylo & Gigi mascots
- British English
- 1800+ characters
- NO sales language

JSON:
{{
  "title": "...",
  "meta_desc": "...",
  "intro_html": "<p>...</p>",
  "problem_html": "<p>...</p>",
  "solution_html": "<p>...</p>",
  "local_html": "<p>...</p>",
  "faq_html": "<div>...</div>"
}}
"""
        
        content = self.brain.generate(prompt, json_mode=True)
        
        if content and len(str(content)) > 1500:
            print(f"      ✅ SEO generated")
            return content
        
        print(f"      🚨 Emergency template")
        return self._emergency_seo(topic, city)

    def _emergency_seo(self, topic, city):
        return {
            "title": f"{topic} in {city} | SayPlay UK",
            "meta_desc": f"Discover {topic.lower()} in {city}. Add voice messages with SayPlay.",
            "intro_html": f"<p>Finding {topic.lower()} in {city} requires personalization and thoughtful consideration. Whether you're shopping in the city centre or browsing local boutiques, adding a personal touch makes all the difference.</p>",
            "problem_html": "<p>Generic gifts often lack emotional connection and fail to convey the depth of your feelings. Mass-produced items, while convenient, rarely capture the unique bond you share with the recipient.</p>",
            "solution_html": f"<p>SayPlay's NFC stickers attach voice or video messages to any gift. Record up to 60 seconds of voice or 30 seconds of video. Recipients simply tap their phone - no app needed. The technology features adorable mascots Mylo and Gigi, making it approachable for all ages.</p>",
            "local_html": f"<p>Shopping in {city} offers diverse options from independent retailers to high street favourites. Personalize any purchase with a voice message that preserves your authentic voice, laughter, and emotion - creating a keepsake that lasts forever.</p>",
            "faq_html": "<div><h4>How does it work?</h4><p>Record your message online, link it to the NFC sticker, attach to your gift. When the recipient taps their phone to the sticker, your message plays instantly.</p><h4>Is it reusable?</h4><p>Yes, messages can be updated and changed as many times as you like.</p></div>"
        }

# --- BLOCK 4: SOCIAL MEDIA GENERATOR ---
class SocialGenerator:
    """Creates social media assets in folders"""
    def __init__(self, brain):
        self.brain = brain

    def generate_assets(self, topic, angle, output_path: Path):
        print(f"\n📱 BLOCK 4: Social Assets")
        print(f"   Folder: {output_path.name}")
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # TikTok
        tt_prompt = f"TikTok script (60s) about '{topic}'. Hook in 3s. Emotional. [Visual cues]. British."
        tt_script = self.brain.generate(tt_prompt) or f"[Hook] {topic}. Here's why it matters... [Show emotion] The power of voice... [Product] SayPlay NFC stickers make it simple..."
        (output_path / "tiktok_script.txt").write_text(tt_script, encoding='utf-8')
        print(f"      ✅ TikTok")
        
        # Instagram
        ig_prompt = f"Instagram caption for '{topic}'. Aesthetic lifestyle. 15 hashtags. British."
        ig_content = self.brain.generate(ig_prompt) or f"{topic} ✨\n\nThe power of voice in gift-giving.\n\n#gifts #personalized #sayplay #voice #meaningful #nfc #giftideas #thoughtful #voicemessage #uk #relationships #memory #keepsake #emotional #connection"
        (output_path / "instagram_post.txt").write_text(ig_content, encoding='utf-8')
        print(f"      ✅ Instagram")
        
        # X/Twitter
        x_prompt = f"3-tweet thread about '{topic}'. Hook, psychology, insight. <280 chars each."
        x_content = self.brain.generate(x_prompt) or f"1/ {topic} isn't about the object.\n\n2/ It's about preserving a voice, a laugh, a moment that might otherwise be forgotten.\n\n3/ Voice messages activate the same neural pathways as being together. That's the science of connection."
        (output_path / "twitter_thread.txt").write_text(x_content, encoding='utf-8')
        print(f"      ✅ Twitter/X")
        
        # Pinterest
        p_prompt = f"Pinterest description for '{topic}'. Visual, aesthetic, inspirational."
        p_content = self.brain.generate(p_prompt) or f"Beautiful {topic.lower()} ideas. Preserve memories with voice messages. Thoughtful, emotional, lasting."
        (output_path / "pinterest_description.txt").write_text(p_content, encoding='utf-8')
        print(f"      ✅ Pinterest")

# --- VISUAL ENGINE ---
class VisualEngine:
    """Generates AI images"""
    def __init__(self, assets_path: Path):
        self.library_path = assets_path / "images"
        self.library_path.mkdir(parents=True, exist_ok=True)

    def get_image(self, topic: str) -> str:
        slug = "".join(x for x in topic.lower() if x.isalnum() or x == "-")[:50]
        filename = f"{slug}.jpg"
        local_path = self.library_path / filename
        web_path = f"/assets/images/{filename}"

        if local_path.exists():
            return web_path

        print(f"      🎨 Image: {topic[:40]}...")
        
        prompt = f"cinematic photo of {topic}, emotional, aesthetic, soft lighting"
        url = f"https://pollinations.ai/p/{urllib.parse.quote(prompt)}?width={Config.IMAGE_WIDTH}&height={Config.IMAGE_HEIGHT}&seed={random.randint(0,999)}&nologo=true"
        
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                local_path.write_bytes(r.content)
                return web_path
        except:
            pass
        
        return "/assets/milo-gigi.png"

# --- DESIGNER ---
class ChameleonDesigner:
    def build_page(self, page_type, data, path, image_url):
        title = data.get('title', 'SayPlay')
        
        if page_type == 'blog':
            content = data.get('article_html', '')
        else:
            content = f"{data.get('intro_html', '')}{data.get('problem_html', '')}{data.get('solution_html', '')}{data.get('local_html', '')}{data.get('faq_html', '')}"
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{data.get('meta_desc', '')}">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow sticky top-0">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="https://sayplay.co.uk" class="bg-orange-600 text-white px-6 py-2 rounded-full">Shop</a>
        </div>
    </nav>
    
    <div class="max-w-4xl mx-auto py-12 px-6">
        <h1 class="text-5xl font-bold mb-8">{title}</h1>
        <img src="{image_url}" class="w-full h-96 object-cover rounded-xl mb-8">
        <div class="prose prose-lg max-w-none">
            {content}
        </div>
    </div>
</body>
</html>"""
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding='utf-8')

# --- AUDIO STUDIO ---
class AudioStudio:
    def __init__(self):
        self.intro = self._find("Just tap.No app intro podkast sayplay.mp3")
        self.outro = self._find("Just tap.no app final podkast.mp3")

    def _find(self, name):
        for p in [Path("runtime_assets") / name, Path("assets/music") / name]:
            if p.exists():
                return p.resolve()
        return None

    async def generate(self, script, ep, slug, out_dir):
        if not EDGE_TTS_AVAILABLE:
            return None
        
        if len(script) < 200:
            script = f"Welcome to SayPlay podcast episode {ep}. {script}" * 3
        
        temp = out_dir / f"temp_{ep}.mp3"
        
        try:
            communicate = edge_tts.Communicate(script, "en-GB-SoniaNeural")
            await communicate.save(str(temp))
        except:
            return None
        
        final = out_dir / f"sayplay_ep_{ep:03d}_{slug}.mp3"
        
        inputs = []
        if self.intro:
            inputs.append(str(self.intro))
        inputs.append(str(temp))
        if self.outro:
            inputs.append(str(self.outro))
        
        if len(inputs) > 1:
            try:
                cmd = ['ffmpeg', '-y']
                for inp in inputs:
                    cmd.extend(['-i', inp])
                
                filter_str = f"concat=n={len(inputs)}:v=0:a=1[out]"
                cmd.extend(['-filter_complex', filter_str, '-map', '[out]', str(final)])
                
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except:
                shutil.copy(temp, final)
        else:
            shutil.copy(temp, final)
        
        if temp.exists():
            temp.unlink()
        
        return final

# --- AI BRAIN ---
class ContentBrain:
    def __init__(self, api_key):
        self.gemini_key = api_key
        self.groq_key = os.getenv('GROQ_API_KEY')
        
        if GEMINI_AVAILABLE and api_key:
            genai.configure(api_key=api_key)

    def get_angle(self, topic):
        """AI determines unique angle"""
        prompt = f"Give ONE unique emotional angle for '{topic}'. Example: 'The pain of forgetting a voice'. Output ONLY the angle."
        return self.generate(prompt) or "Emotional value of voice"

    def generate(self, prompt, json_mode=False):
        res = None
        
        # Try Groq first (free)
        if self.groq_key:
            try:
                r = requests.post(
                    Config.GROQ_ENDPOINT,
                    headers={'Authorization': f'Bearer {self.groq_key}'},
                    json={'model': Config.GROQ_MODEL, 'messages': [{'role': 'user', 'content': prompt}]},
                    timeout=30
                )
                if r.status_code == 200:
                    res = r.json()['choices'][0]['message']['content']
            except:
                pass
        
        # Try Gemini
        if not res and self.gemini_key and GEMINI_AVAILABLE:
            try:
                model = genai.GenerativeModel(Config.GEMINI_MODEL)
                response = model.generate_content(prompt)
                res = response.text
            except:
                pass
        
        if json_mode and res:
            try:
                clean = res.strip()
                if '```json' in clean:
                    clean = clean.split('```json')[1].split('```')[0]
                elif '```' in clean:
                    clean = clean.split('```')[1].split('```')[0]
                return json.loads(clean.strip())
            except:
                return None
        
        return res

# --- MAIN ORCHESTRATOR ---
async def main():
    print("\n" + "="*70)
    print("🚀 SAYPLAY MEDIA ENGINE V1 - WITH TITAN OBSERVATORY")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    # Setup
    web_dir = Path("website")
    social_dir = Path("social_media_assets")
    assets_dir = web_dir / "assets"
    
    for d in ['seo', 'blog', 'podcasts']:
        (web_dir / d).mkdir(parents=True, exist_ok=True)
    
    social_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy assets
    print("📂 Syncing assets...")
    if Path("assets/brand").exists():
        for f in Path("assets/brand").glob("*"):
            if f.is_file():
                shutil.copy(f, assets_dir / f.name)
                print(f"   ✅ {f.name}")
    
    # Initialize modules
    print("\n🧠 Initializing modules...")
    cmel = CMEL(Path("content_history.json"))
    brain = ContentBrain(os.getenv('GEMINI_API_KEY'))
    
    trend_module = TrendIntelligence(brain)
    editorial_module = EditorialEngine(brain)
    seo_module = SEOEngine(brain)
    social_module = SocialGenerator(brain)
    
    visual = VisualEngine(assets_dir)
    designer = ChameleonDesigner()
    audio = AudioStudio()
    dashboard = DashboardIndexGenerator()
    
    print(f"   ✅ CMEL loaded (ID: {cmel.get_stats()['last_id']})")
    
    # Harvest topics
    topics = trend_module.harvest_trends(cmel)
    
    if not topics:
        print("\n⚠️ No new topics")
        return
    
    cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Bristol', 'Edinburgh', 'Liverpool']
    
    # Production loop
    print(f"\n{'='*70}")
    print("⚙️  CONTENT PRODUCTION CYCLE")
    print(f"{'='*70}")
    
    for idx, item in enumerate(topics, 1):
        topic = item['topic']
        angle = item['angle']
        city = random.choice(cities)
        
        print(f"\n[{idx}/{len(topics)}] {topic}")
        
        # Image
        img = visual.get_image(topic)
        
        # Blog (Block 2)
        blog_data = editorial_module.create_blog_post(topic, angle)
        if blog_data:
            slug = "".join(c for c in topic.lower() if c.isalnum() or c == '-')[:40]
            blog_file = f"{slug}.html"
            
            designer.build_page('blog', blog_data, web_dir / 'blog' / blog_file, img)
            cmel.register_content('blog', topic, angle, blog_file)
            
            # Social assets for blog
            social_module.generate_assets(topic, angle, social_dir / f"{slug}_social")
        
        # SEO Page (Block 3)
        seo_data = seo_module.create_seo_page(topic, city)
        if seo_data:
            slug = "".join(c for c in topic.lower() if c.isalnum() or c == '-')[:40]
            seo_file = f"{slug}-{city.lower()}.html"
            
            designer.build_page('seo', seo_data, web_dir / 'seo' / seo_file, img)
            cmel.register_content('seo', topic, angle, seo_file)
        
        # Podcast
        script_prompt = f"Podcast script about {topic}. 800 words. Conversational British. Intro, Story, Insight, Outro."
        script = brain.generate(script_prompt)
        
        if script and len(script) > 300:
            ep_id = cmel.get_stats()['last_id']
            slug = "".join(c for c in topic.lower() if c.isalnum() or c == '-')[:30]
            
            podcast_path = await audio.generate(script, ep_id, slug, web_dir / 'podcasts')
            
            if podcast_path:
                cmel.register_content('podcast', topic, angle, podcast_path.name)
                print(f"      ✅ Podcast")
    
    # Finalize
    print(f"\n{'='*70}")
    print("📊 FINALIZING")
    print(f"{'='*70}\n")
    
    cmel.save()
    shutil.copy(Path("content_history.json"), assets_dir / "content_history.json")
    
    # Legacy format for dashboard
    legacy = {"seo_pages": [], "blog_posts": [], "podcasts": []}
    
    for item in cmel.data["content_log"]:
        if item['type'] == 'seo':
            legacy['seo_pages'].append({
                'topic': item['topic'],
                'city': 'UK',
                'filename': item['filename'],
                'title': item['topic'],
                'created': item['date']
            })
        elif item['type'] == 'blog':
            legacy['blog_posts'].append({
                'topic': item['topic'],
                'filename': item['filename'],
                'title': item['topic'],
                'created': item['date']
            })
        elif item['type'] == 'podcast':
            legacy['podcasts'].append({
                'episode': item['id'],
                'topic': item['topic'],
                'filename': item['filename'],
                'created': item['date']
            })
    
    stats = cmel.get_stats()
    
    # Generate dashboards
    dashboard.generate_main_dashboard(web_dir / 'index.html', stats)
    dashboard.generate_seo_index(web_dir / 'seo' / 'index.html', legacy['seo_pages'])
    dashboard.generate_blog_index(web_dir / 'blog' / 'index.html', legacy['blog_posts'])
    dashboard.generate_podcast_index(web_dir / 'podcasts' / 'index.html', legacy['podcasts'])
    
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print("✅ SPME V1 WITH OBSERVATORY COMPLETE")
    print(f"{'='*70}")
    print(f"📊 Generated:")
    print(f"   • SEO Pages: {stats['seo']}")
    print(f"   • Blog Posts: {stats['blog']}")
    print(f"   • Podcasts: {stats['podcasts']}")
    print(f"   • ID: {stats['last_id']}")
    print(f"\n⏱  Time: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"📁 Social: social_media_assets/")
    print(f"🌐 Dashboard: website/index.html")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(main())
