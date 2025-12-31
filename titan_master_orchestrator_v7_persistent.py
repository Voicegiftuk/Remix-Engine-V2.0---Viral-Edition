#!/usr/bin/env python3
"""
TITAN V9 "ULTIMA" - PERSISTENT LIBRARY & ROBUST GENERATION
Features:
- PERSISTENCE: Works in 'website/' folder to build a massive library (Snowball Effect).
- SMART ASSETS: Auto-renames complex file names to simple 'milo-gigi.png' for HTML safety.
- FALLBACK ENGINE: If AI fails (404), generates professional content procedurally (No more "...").
- AUDIO MIXING: FFmpeg with absolute paths to ensure Music + Voice + Music.
- LAYOUT GUARD: CSS classes that prevent images from breaking the site.
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio
import json
import random
from typing import List, Dict, Optional
import shutil
import subprocess
import time

# Import metadata managers
from content_metadata_manager import ContentMetadataManager
from dashboard_index_generator import DashboardIndexGenerator

# --- LIBRARIES SAFETY CHECK ---
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

class AIConfig:
    # Using the most stable models. If one fails, the code auto-switches.
    GEMINI_MODEL = 'gemini-1.5-flash' 
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'

class FallbackGenerator:
    """
    SAFETY NET: If AI APIs crash (404/Quota), this writes the content locally.
    Ensures no page ever looks empty or broken.
    """
    def generate_seo(self, topic, city):
        return {
            'title': f"The Ultimate Guide to {topic} in {city}",
            'meta_desc': f"Looking for {topic} in {city}? Make your gift unforgettable with SayPlay video messages. The perfect personal touch.",
            'intro_html': f"<p>Finding the perfect <strong>{topic}</strong> in <strong>{city}</strong> can be a challenge. You want something meaningful, personal, and lasting. In a world of mass-produced items, how do you make your gift stand out?</p><p>That is where SayPlay comes in. We bridge the gap between physical gifts and digital emotion.</p>",
            'problem_html': f"<p>We have all been there. You scour the shops in {city}, but nothing feels quite 'enough'. A card gets read once and thrown away. A text message is forgotten in seconds. The gift needs a voice.</p>",
            'solution_html': f"<p><strong>SayPlay is the solution.</strong> Our NFC stickers allow you to attach a real voice or video message to any gift. <br><br>Meet <strong>Mylo & Gigi</strong>, our mascots! They represent the joy of connection. Whether it's a birthday, anniversary, or just because, your voice makes it special.</p>",
            'howto_html': "<ul><li><strong>1. Record:</strong> Use your phone to record a message (no app needed).</li><li><strong>2. Stick:</strong> Place the SayPlay sticker on the gift or card.</li><li><strong>3. Give:</strong> Watch them smile as they tap and listen.</li></ul>",
            'local_html': f"<p>{city} is a wonderful place for shopping. Whether you are visiting the high street or local boutiques, pairing your find with a SayPlay sticker elevates it to a memory they will keep forever.</p>",
            'faq_html': "<div class='faq-item'><strong>Do they need an app?</strong><br>No! It works natively on smartphones.</div><div class='faq-item'><strong>How long is it stored?</strong><br>We keep your message safe for a full year.</div>"
        }

    def generate_blog(self, topic):
        return {
            'title': topic,
            'article_html': f"""
                <p>When we think about <strong>{topic}</strong>, we often focus on the object itself. But the true value of a gift lies in the emotion behind it.</p>
                <h2>The Problem with Modern Gifting</h2>
                <p>In our fast-paced world, gifts have become transactional. We click 'buy', it arrives, we hand it over. Where is the heart? Where is the connection?</p>
                <h2>Enter SayPlay</h2>
                <p>Imagine giving {topic}, but when they open it, they hear your voice telling them exactly why you chose it. That is the power of SayPlay NFC stickers.</p>
                <h2>Approved by Mylo & Gigi</h2>
                <p>Our mascots know that memories are the best treats. Mylo (the dog) digs for the best moments, and Gigi (the cat) ensures everything looks perfect. Join the revolution of personalized gifting.</p>
            """,
            'keywords': ["Gifts", "SayPlay", "Memories", "UK"]
        }

    def generate_podcast(self, topic):
        # Generates a long script to ensure audio isn't 10 seconds
        t = f"Welcome to the Say Play Gift Guide. I am Sonia. Today we are talking about {topic}. "
        t += "Gift giving is an art form that is slowly being lost. We buy things, but we forget to infuse them with meaning. "
        t += f"That is why {topic} is such a great starting point for a conversation about connection. "
        t += "At Say Play, we have solved this with technology. Our NFC stickers let you attach sixty seconds of audio or thirty seconds of video to anything. "
        t += "No app is required. You just tap your phone, and the message plays. It is magic. "
        t += "Meet Mylo and Gigi, our mascots who remind us that playfulness is key to a good gift. "
        t += f"So if you are looking for {topic}, do not just give the item. Give a piece of yourself with it. "
        t += "Visit Say Play dot co dot U K. Make your next gift unforgettable. "
        # Repeat once to ensure length > 3 minutes with intro/outro
        return t + " " + t

class ContentBrain:
    def __init__(self, api_key: str):
        self.gemini_key = api_key
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.fallback = FallbackGenerator()
        if GEMINI_AVAILABLE and api_key:
            genai.configure(api_key=api_key)

    def generate_seo_page(self, topic: str, city: str) -> Dict:
        print(f"      🧠 SEO ({city}): {topic}")
        data = self._generate_with_retry('seo', topic, city)
        if not data: 
            print("         ⚠️ AI Failed. Switching to Procedural Engine.")
            return self.fallback.generate_seo(topic, city)
        return data

    def generate_blog(self, topic: str) -> Dict:
        print(f"      📝 Blog: {topic}")
        data = self._generate_with_retry('blog', topic)
        if not data:
            print("         ⚠️ AI Failed. Switching to Procedural Engine.")
            return self.fallback.generate_blog(topic)
        return data

    def generate_podcast_script(self, topic: str) -> str:
        print(f"      🎙️ Scripting: {topic}")
        script = self._generate_with_retry('podcast', topic)
        if not script or len(script) < 500:
            print("         ⚠️ AI Script too short/failed. Using Procedural Script.")
            return self.fallback.generate_podcast(topic)
        return script

    def _generate_with_retry(self, type: str, topic: str, city: str = '') -> any:
        # Cascade: Groq -> OpenAI -> Gemini
        if self.groq_key:
            res = self._try_groq(type, topic, city)
            if res: return res
        if self.openai_key:
            res = self._try_openai(type, topic, city)
            if res: return res
        if self.gemini_key:
            res = self._try_gemini(AIConfig.GEMINI_MODEL, type, topic, city)
            if res: return res
        return None

    def _get_prompt(self, type, topic, city):
        facts = "Product: SayPlay NFC Stickers. Features: 60s voice/30s video, 1yr hosting, No App needed. Mascots: Mylo (dog) & Gigi (cat)."
        if type == 'seo':
            return f"""Generate JSON for SEO Page: "{topic} in {city}". Facts: {facts}. Output JSON keys: title, meta_desc, intro_html, problem_html, solution_html, howto_html, local_html, faq_html. Content: Emotional, local {city} details."""
        if type == 'blog':
            return f"""Generate JSON for Blog Post: "{topic}". Facts: {facts}. Output JSON keys: title, article_html (use <h2>, <p>, <ul>), keywords. Content: Story-driven."""
        if type == 'podcast':
            return f"""Write a 4-MINUTE Podcast Script (approx 1000 words) about "{topic}". Host: Sonia. Structure: Intro -> Story -> Problem -> SayPlay Solution -> Outro. Spoken text only."""

    def _try_gemini(self, model, type, topic, city):
        try:
            m = genai.GenerativeModel(model)
            res = m.generate_content(self._get_prompt(type, topic, city))
            return self._parse(type, res.text)
        except: return None

    def _try_groq(self, type, topic, city):
        try:
            res = requests.post(AIConfig.GROQ_ENDPOINT, headers={'Authorization':f'Bearer {self.groq_key}'}, json={'model':AIConfig.GROQ_MODEL,'messages':[{'role':'user','content':self._get_prompt(type, topic, city)}]})
            return self._parse(type, res.json()['choices'][0]['message']['content'])
        except: return None

    def _try_openai(self, type, topic, city):
        try:
            res = requests.post(AIConfig.OPENAI_ENDPOINT, headers={'Authorization':f'Bearer {self.openai_key}'}, json={'model':AIConfig.OPENAI_MODEL,'messages':[{'role':'user','content':self._get_prompt(type, topic, city)}]})
            return self._parse(type, res.json()['choices'][0]['message']['content'])
        except: return None

    def _parse(self, type, text):
        text = text.replace('```json', '').replace('```', '').strip()
        if type == 'podcast': return text
        try: return json.loads(text)
        except: return None

class ChameleonDesigner:
    """
    Ensures layout stability with hardcoded CSS dimensions.
    Randomizes designs to keep it fresh.
    """
    def __init__(self):
        self.nav = """<nav class="bg-white shadow-sm sticky top-0 z-50"><div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center"><a href="https://sayplay.co.uk"><img src="/assets/sayplay_logo.png" class="h-10 w-auto object-contain"></a><a href="https://sayplay.co.uk/collections/all" class="bg-black text-white px-6 py-2 rounded-full font-bold hover:bg-orange-600 transition">SHOP</a></div></nav>"""
        self.footer = """<footer class="bg-gray-900 text-white py-12 mt-12 text-center"><img src="/assets/sayplay_logo.png" class="h-8 mx-auto mb-4 brightness-200 grayscale"><p>&copy; 2025 SayPlay UK</p></footer>"""

    def build_page(self, type: str, data: Dict, path: Path):
        content = data.get('article_html') if type == 'blog' else f"{data.get('intro_html')}{data.get('problem_html')}{data.get('solution_html')}{data.get('local_html')}{data.get('faq_html')}"
        
        # HERO SECTION - Hardcoded height to prevent layout shifts
        hero = f"""
        <div class="bg-orange-50 py-16 px-4 text-center">
            <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">{data.get('title')}</h1>
            <div class="max-w-3xl mx-auto h-64 md:h-80 rounded-2xl overflow-hidden shadow-xl">
                <img src="/assets/milo-gigi.png" class="w-full h-full object-cover object-center" alt="Milo and Gigi">
            </div>
        </div>
        """
        
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{data.get('title')}</title><script src="https://cdn.tailwindcss.com"></script><script src="https://cdn.tailwindcss.com?plugins=typography"></script></head><body class="bg-white font-sans text-gray-800">{self.nav}{hero}<div class="max-w-3xl mx-auto py-12 px-6 prose prose-lg prose-orange max-w-none">{content}</div>{self.footer}</body></html>"""
        
        with open(path, 'w', encoding='utf-8') as f: f.write(html)

class OmniSourceHunter:
    """Generates topics procedurally if AI fails"""
    def __init__(self, brain):
        self.brain = brain
        
    def get_topics(self) -> List[str]:
        topics = []
        # AI Simulation
        try:
            prompt = "Generate 10 UNIQUE UK gifting topics (recipients, occasions, hobbies)."
            if self.brain.gemini_key:
                m = genai.GenerativeModel('gemini-1.5-flash')
                r = m.generate_content(prompt)
                for l in r.text.split('\n'):
                    if len(l) > 10: topics.append(l.strip().strip('1234567890.-* '))
        except: pass

        # Procedural Backup (Guaranteed 10 topics)
        recipients = ["Mum", "Dad", "Partner", "Friend", "Grandparent", "Teacher", "Colleague"]
        occasions = ["Birthday", "Anniversary", "Wedding", "New Job", "Baby Shower", "Retirement"]
        interests = ["Garden", "Tech", "Cooking", "Travel", "Wellness", "Music", "Reading"]
        while len(topics) < 20:
            topics.append(f"{random.choice(interests)} Gifts for {random.choice(recipients)} {random.choice(occasions)} UK")
        
        random.shuffle(topics)
        return topics[:10]

class AudioStudio:
    def __init__(self):
        # Check multiple paths for assets to ensure we find them
        self.intro = self._find_file("Just tap.No app intro podkast sayplay.mp3")
        self.outro = self._find_file("Just tap.no app final podkast.mp3")

    def _find_file(self, name):
        # Logic: Check runtime_assets, then repo assets, then website assets
        paths = [
            Path("runtime_assets") / name,
            Path("assets/music") / name,
            Path("website/assets") / name
        ]
        for p in paths:
            if p.exists(): return p.resolve()
        return None

    async def generate(self, script, ep_num, slug, out_dir):
        temp = out_dir / f"temp_{ep_num}.mp3"
        try:
            # Slower rate for longer audio
            comm = edge_tts.Communicate(script, "en-GB-SoniaNeural", rate="-5%") 
            await comm.save(str(temp))
        except: return None

        final = out_dir / f"sayplay_ep_{ep_num:03d}_{slug}.mp3"
        cmd = ['ffmpeg', '-y']
        inputs = []
        if self.intro: inputs.extend(['-i', str(self.intro)])
        inputs.extend(['-i', str(temp)])
        if self.outro: inputs.extend(['-i', str(self.outro)])
        
        # Concat filter
        filter_str = f"concat=n={len(inputs)//2}:v=0:a=1[out]"
        cmd.extend(['-filter_complex', filter_str, '-map', '[out]', str(final)])
        
        try: subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except: shutil.copy(temp, final) # Fallback to just voice if ffmpeg fails
        
        if temp.exists(): temp.unlink()
        return final

async def main():
    print("🚀 TITAN V9 STARTING (Persistent Mode)")
    
    # 1. SETUP PERSISTENT FOLDER
    web_dir = Path('website')
    assets_dir = web_dir / 'assets'
    for d in ['seo', 'blog', 'podcasts', 'assets']: 
        (web_dir / d).mkdir(parents=True, exist_ok=True)

    # 2. ASSET SYNCHRONIZATION (RENAMING COMPLEX FILES FOR HTML SAFETY)
    print("📂 Syncing Assets...")
    
    # Music
    if Path("assets/music").exists():
        for f in Path("assets/music").glob("*.mp3"): shutil.copy(f, assets_dir / f.name)
    
    # Images - SPECIFIC RENAMING FOR MILO & GIGI
    # Your repo has "milo&gigi-razem-z-logo-sayplay.png" -> map to "milo-gigi.png"
    brand_src = Path("assets/brand")
    if brand_src.exists():
        # Copy Logo
        if (brand_src / "sayplay_logo.png").exists():
            shutil.copy(brand_src / "sayplay_logo.png", assets_dir / "sayplay_logo.png")
        
        # Copy & Rename Mascot (Handles the '&' issue in URLs)
        mascot_src = brand_src / "milo&gigi-razem-z-logo-sayplay.png"
        if mascot_src.exists():
            shutil.copy(mascot_src, assets_dir / "milo-gigi.png")
            print("   ✅ Mascots synced as milo-gigi.png")

    # 3. INIT MANAGERS
    history_file = Path('content_history.json')
    meta = ContentMetadataManager(history_file)
    dash = DashboardIndexGenerator()
    brain = ContentBrain(os.getenv('GEMINI_API_KEY'))
    designer = ChameleonDesigner()
    audio = AudioStudio()
    hunter = OmniSourceHunter(brain)

    topics = hunter.get_topics()
    cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Liverpool', 'Bristol']

    # 4. GENERATION LOOP (With Safety Saves)
    # SEO
    count = 0
    for topic in topics:
        if count >= 10: break
        city = random.choice(cities)
        if meta.is_duplicate_seo(topic, city): continue
        
        data = brain.generate_seo_page(topic, city)
        slug = "".join(x for x in topic.lower() if x.isalnum() or x == "-")[:30]
        fname = f"{slug}-{city.lower()}.html"
        designer.build_page('seo', data, web_dir / 'seo' / fname)
        meta.add_seo_page(topic, city, fname, data.get('title', topic))
        meta.save()
        count += 1

    # BLOG
    count = 0
    for topic in topics:
        if count >= 10: break
        if meta.is_duplicate_blog(topic): continue
        data = brain.generate_blog(topic)
        slug = "".join(x for x in topic.lower() if x.isalnum() or x == "-")[:30]
        fname = f"{slug}.html"
        designer.build_page('blog', data, web_dir / 'blog' / fname)
        meta.add_blog_post(topic, fname, data.get('title', topic))
        meta.save()
        count += 1

    # PODCAST
    count = 0
    for topic in topics:
        if count >= 10: break
        if meta.is_duplicate_podcast(topic): continue
        ep = meta.get_next_episode_number()
        script = brain.generate_podcast_script(topic)
        slug = "".join(x for x in topic.lower() if x.isalnum() or x == "-")[:30]
        path = await audio.generate(script, ep, slug, web_dir / 'podcasts')
        if path:
            meta.add_podcast(topic, path.name, ep)
            meta.save()
            count += 1

    # 5. FINALIZE
    shutil.copy(history_file, assets_dir / 'content_history.json')
    stats = meta.get_stats()
    
    # Generate Indexes based on FULL HISTORY
    dash.generate_main_dashboard(web_dir / 'index.html', stats)
    dash.generate_seo_index(web_dir / 'seo' / 'index.html', meta.get_all_seo_pages())
    dash.generate_blog_index(web_dir / 'blog' / 'index.html', meta.get_all_blog_posts())
    dash.generate_podcast_index(web_dir / 'podcasts' / 'index.html', meta.get_all_podcasts())
    
    print(f"✅ DONE. Library Updated.")

if __name__ == "__main__":
    asyncio.run(main())
