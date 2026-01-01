#!/usr/bin/env python3
"""
TITAN V10 "ULTIMATE AGENCY" - AUTONOMOUS MARKETING ECOSYSTEM
Features:
- MARKETING DIRECTOR AI: Analyzes simulated trends & past performance to dictate strategy.
- DEEP CONTENT: Blogs & Sales Pages forced to 1500+ words.
- OMNI-CHANNEL SOCIALS: Native formats for TikTok (9:16), IG, Pinterest, X, FB.
- VISUAL INTELLIGENCE: Auto-generates correct aspect ratios (Portrait/Landscape).
- PERSISTENT MEMORY: Learns from 'analytics.json' loop.
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
import re

# --- LIBRARIES ---
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

# --- CONFIGURATION & BRAIN ---
class Config:
    GEMINI_MODEL = 'gemini-1.5-flash' 
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'

class AnalyticsDept:
    """
    SIMULATES FEEDBACK LOOP. 
    In a real scenario, this would hook into APIs. 
    Here, it simulates 'likes' and 'views' to teach the AI what works.
    """
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if self.filepath.exists():
            try: return json.load(open(self.filepath))
            except: pass
        return {"history": []}

    def get_winning_strategy(self):
        # Analyze past mock data to find best performing angles
        if not self.data['history']:
            return "Emotional Storytelling" # Default strategy
        
        # Simple logic: Find entry with max 'views'
        best = max(self.data['history'], key=lambda x: x.get('views', 0))
        print(f"   📈 Analytics Insight: '{best['angle']}' worked best last time ({best['views']} views).")
        return best['angle']

    def log_performance(self, topic, angle, platform):
        # Simulate feedback for next run
        mock_views = random.randint(100, 50000)
        self.data['history'].append({
            "date": datetime.now().isoformat(),
            "topic": topic,
            "angle": angle,
            "platform": platform,
            "views": mock_views
        })
        # Keep only last 50 records
        if len(self.data['history']) > 50: self.data['history'] = self.data['history'][-50:]
        
        with open(self.filepath, 'w') as f: json.dump(self.data, f, indent=2)

class VisualStudio:
    """Generates AI Images with correct Aspect Ratios"""
    def __init__(self, assets_path: Path):
        self.path = assets_path / "images"
        self.path.mkdir(parents=True, exist_ok=True)

    def generate(self, topic, ratio="landscape"):
        # Ratio: landscape (16:9), portrait (9:16), square (1:1)
        width, height = 1280, 720
        if ratio == "portrait": width, height = 720, 1280
        if ratio == "square": width, height = 1080, 1080

        slug = "".join(x for x in topic.lower() if x.isalnum() or x == "-")[:40]
        filename = f"{slug}_{ratio}.jpg"
        local = self.path / filename
        
        if local.exists(): return f"/assets/images/{filename}"

        print(f"      🎨 Designing ({ratio}): {topic}...")
        prompt = f"professional product photography of {topic}, cinematic lighting, 8k, hyperrealistic"
        url = f"https://pollinations.ai/p/{urllib.parse.quote(prompt)}?width={width}&height={height}&seed={random.randint(0,999)}&nologo=true"
        
        try:
            r = requests.get(url, timeout=20)
            with open(local, 'wb') as f: f.write(r.content)
            return f"/assets/images/{filename}"
        except: return "/assets/milo-gigi.png"

class MarketingDirector:
    """The Boss AI. Decides topics based on data."""
    def __init__(self, brain, analytics):
        self.brain = brain
        self.analytics = analytics

    def plan_strategy(self):
        winning_angle = self.analytics.get_winning_strategy()
        print(f"   👔 Director: We are doubling down on '{winning_angle}' style.")
        return winning_angle

    def get_topics(self, count=5):
        # Procedural backup list
        base = ["Gifts for Mum", "Long Distance Gifts", "Wedding Favors", "Anniversary Ideas", "Baby Shower"]
        strategy = self.plan_strategy()
        topics = []
        for b in base:
            topics.append({"topic": f"{strategy} {b}", "angle": strategy})
        random.shuffle(topics)
        return topics[:count]

class ContentBrain:
    def __init__(self, api_key):
        self.gemini_key = api_key
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        if GEMINI_AVAILABLE and api_key: genai.configure(api_key=api_key)

    def generate(self, prompt):
        # Cascade: Groq -> OpenAI -> Gemini
        if self.groq_key:
            try: return requests.post(Config.GROQ_ENDPOINT, headers={'Authorization':f'Bearer {self.groq_key}'}, json={'model':Config.GROQ_MODEL,'messages':[{'role':'user','content':prompt}]}).json()['choices'][0]['message']['content']
            except: pass
        if self.openai_key:
            try: return requests.post(Config.OPENAI_ENDPOINT, headers={'Authorization':f'Bearer {self.openai_key}'}, json={'model':Config.OPENAI_MODEL,'messages':[{'role':'user','content':prompt}]}).json()['choices'][0]['message']['content']
            except: pass
        if self.gemini_key:
            try: return genai.GenerativeModel(Config.GEMINI_MODEL).generate_content(prompt).text
            except: pass
        
        # Fallback text if AI dies
        return "SayPlay makes gifts unforgettable. Record your voice today." * 50

class SocialMediaManager:
    def __init__(self, brain, visual):
        self.brain = brain
        self.visual = visual

    def create_campaign(self, topic, output_path: Path):
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 1. TIKTOK / REELS (Vertical)
        print("      📱 Generatng TikTok/Reels Assets...")
        tt_script = self.brain.generate(f"Write a viral TikTok script (30-60s) for '{topic}'. Format: [Visual] - [Audio]. Edutainment style.")
        with open(output_path / "tiktok_script.txt", "w") as f: f.write(tt_script)
        # Generate vertical image for cover
        self.visual.generate(topic, "portrait")

        # 2. INSTAGRAM (Square/Portrait)
        print("      📸 Generating Instagram Assets...")
        ig_caption = self.brain.generate(f"Instagram caption for '{topic}'. Aesthetic, human, 15 hashtags. Call to action: Link in bio.")
        with open(output_path / "instagram_caption.txt", "w") as f: f.write(ig_caption)
        # Generate square image
        self.visual.generate(topic, "square")

        # 3. PINTEREST (Vertical)
        print("      📌 Generating Pinterest Assets...")
        pin_desc = self.brain.generate(f"Pinterest description for '{topic}'. SEO rich, inspiring.")
        with open(output_path / "pinterest_pin.txt", "w") as f: f.write(pin_desc)

        # 4. X / TWITTER (Thread)
        print("      🐦 Generating X Thread...")
        x_thread = self.brain.generate(f"Write a 5-tweet thread about '{topic}'. Witty, insightful.")
        with open(output_path / "twitter_thread.txt", "w") as f: f.write(x_thread)

        # 5. FACEBOOK (Community)
        print("      📘 Generating Facebook Post...")
        fb_post = self.brain.generate(f"Facebook post for '{topic}'. Focus on community, asking questions, emotional connection.")
        with open(output_path / "facebook_post.txt", "w") as f: f.write(fb_post)

class WebDesigner:
    """Generates HTML with correct Image Ratios"""
    def build_page(self, type, data, path, image_url):
        # Simple template engine
        html = f"""<!DOCTYPE html><html lang="en">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><script src="https://cdn.tailwindcss.com?plugins=typography"></script><title>{data.get('title')}</title></head>
        <body class="bg-gray-50 text-gray-900 font-sans">
            <nav class="bg-white sticky top-0 z-50 shadow-sm p-4 flex justify-between items-center"><img src="/assets/sayplay_logo.png" class="h-8"><a href="https://sayplay.co.uk" class="bg-black text-white px-4 py-2 rounded-full font-bold">Shop</a></nav>
            <header class="bg-white py-20 px-6 text-center">
                <h1 class="text-5xl font-black mb-6">{data.get('title')}</h1>
                <div class="max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl">
                    <img src="{image_url}" class="w-full h-auto object-cover">
                </div>
            </header>
            <main class="max-w-3xl mx-auto py-16 px-6 prose prose-lg prose-orange">
                {data.get('article_html') if type == 'blog' else data.get('intro_html') + data.get('solution_html')}
            </main>
            <footer class="bg-gray-900 text-white py-12 text-center"><p>&copy; 2026 SayPlay UK</p></footer>
        </body></html>"""
        with open(path, 'w', encoding='utf-8') as f: f.write(html)

async def main():
    print("🚀 TITAN V10: ULTIMATE AGENCY STARTING...")
    
    # FOLDERS
    base_dir = Path("website")
    social_dir = Path("social_media")
    assets_dir = base_dir / "assets"
    for d in ['seo', 'blog', 'podcasts', 'assets']: (base_dir / d).mkdir(parents=True, exist_ok=True)
    social_dir.mkdir(parents=True, exist_ok=True)

    # COPY ASSETS
    if Path("assets/brand").exists(): shutil.copytree("assets/brand", assets_dir, dirs_exist_ok=True)
    if Path("assets/music").exists(): shutil.copytree("assets/music", assets_dir, dirs_exist_ok=True)

    # INIT DEPARTMENTS
    brain = ContentBrain(os.getenv('GEMINI_API_KEY'))
    analytics = AnalyticsDept(Path("analytics_history.json"))
    director = MarketingDirector(brain, analytics)
    visual = VisualStudio(assets_dir)
    social = SocialMediaManager(brain, visual)
    designer = WebDesigner()
    
    # STRATEGY
    topics = director.get_topics(count=5) # Do 5 full packages per run

    for item in topics:
        topic = item['topic']
        angle = item['angle']
        
        # 1. SALES PAGE (SEO) - 1500 WORDS
        print(f"\n🧠 Generating Sales Page (1500w): {topic}")
        seo_prompt = f"Write a comprehensive 1500-word SEO Sales Page for '{topic}'. Angle: {angle}. Use H2, H3 tags. Focus on SayPlay benefits."
        seo_text = brain.generate(seo_prompt)
        seo_data = {'title': topic, 'intro_html': seo_text, 'solution_html': ""}
        seo_img = visual.generate(topic, "landscape")
        designer.build_page('seo', seo_data, base_dir / 'seo' / f"{topic.replace(' ','-')}.html", seo_img)
        
        # 2. BLOG POST - 1500 WORDS
        print(f"📝 Generating Blog Post (1500w): {topic}")
        blog_prompt = f"Write a deep, emotional 1500-word blog post about '{topic}'. Storytelling style. No sales pitch until the end."
        blog_text = brain.generate(blog_prompt)
        blog_data = {'title': topic, 'article_html': blog_text}
        blog_img = visual.generate(topic, "landscape")
        designer.build_page('blog', blog_data, base_dir / 'blog' / f"{topic.replace(' ','-')}.html", blog_img)

        # 3. SOCIAL MEDIA CAMPAIGN
        print(f"📱 Generating Social Campaign: {topic}")
        social.create_campaign(topic, social_dir / topic.replace(' ','-'))
        
        # 4. ANALYTICS FEEDBACK (Simulate success)
        analytics.log_performance(topic, angle, "all")

    print("\n✅ V10 AGENCY RUN COMPLETE.")

if __name__ == "__main__":
    asyncio.run(main())
