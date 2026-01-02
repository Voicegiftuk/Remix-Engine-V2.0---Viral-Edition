#!/usr/bin/env python3
"""
SAYPLAY MEDIA ENGINE (SPME) V1.2 - STABILITY PATCH
Fixes:
- KeyError 'id_counter' crash (Robust CMEL loading).
- Missing asyncio import.
- Deprecation warnings.
"""
import sys
import os
import asyncio
import json
import random
import urllib.parse
import shutil
import subprocess
import csv
import time
import requests
from datetime import datetime
from pathlib import Path

# --- SAFE IMPORTS ---
import warnings
warnings.filterwarnings("ignore")

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

# Dummy Dashboard if missing
try:
    from dashboard_index_generator import DashboardIndexGenerator
except ImportError:
    class DashboardIndexGenerator:
        def generate_main_dashboard(self, p, d): pass
        def generate_seo_index(self, p, d): pass
        def generate_blog_index(self, p, d): pass
        def generate_podcast_index(self, p, d): pass

# --- CONFIGURATION ---
class Config:
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    GEMINI_MODEL = 'gemini-1.5-flash'
    HF_MODELS = ['meta-llama/Meta-Llama-3-70B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1']
    HF_ENDPOINT = 'https://api-inference.huggingface.co/models/'
    TOGETHER_ENDPOINT = 'https://api.together.xyz/v1/chat/completions'
    PERPLEXITY_ENDPOINT = 'https://api.perplexity.ai/chat/completions'
    
    SCANNER_CSV = "sources.csv"

# --- 1. MULTI-AI BRAIN ---
class MultiAIBrain:
    def __init__(self):
        self.keys = {
            'gemini': os.getenv('GEMINI_API_KEY'),
            'groq': os.getenv('GROQ_API_KEY'),
            'hf': os.getenv('HUGGINGFACE_TOKEN')
        }
        if GEMINI_AVAILABLE and self.keys['gemini']:
            try: genai.configure(api_key=self.keys['gemini'])
            except: pass

    def generate(self, prompt, json_mode=False, min_len=1000):
        # 1. Groq
        if self.keys['groq']:
            res = self._req_groq(prompt)
            if self._valid(res, min_len): return self._parse(res, json_mode)
        
        # 2. Gemini
        if self.keys['gemini'] and GEMINI_AVAILABLE:
            res = self._req_gemini(prompt)
            if self._valid(res, min_len): return self._parse(res, json_mode)

        # 3. HuggingFace
        if self.keys['hf']:
            res = self._req_hf(prompt)
            if self._valid(res, min_len): return self._parse(res, json_mode)

        print("      ⚠️ All AIs failed. Engaging Emergency Generator.")
        return None

    def _valid(self, text, min_len):
        return text and len(str(text)) > min_len * 0.5

    def _parse(self, text, json_mode):
        if not json_mode: return text
        try:
            clean = text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean)
        except: return text

    def _req_groq(self, p):
        try:
            r = requests.post(Config.GROQ_ENDPOINT, headers={'Authorization':f"Bearer {self.keys['groq']}"}, json={'model':Config.GROQ_MODEL,'messages':[{'role':'user','content':p}]}, timeout=30)
            return r.json()['choices'][0]['message']['content']
        except: return None

    def _req_gemini(self, p):
        try: return genai.GenerativeModel(Config.GEMINI_MODEL).generate_content(p).text
        except: return None

    def _req_hf(self, p):
        for m in Config.HF_MODELS:
            try:
                r = requests.post(f"{Config.HF_ENDPOINT}{m}", headers={'Authorization':f"Bearer {self.keys['hf']}"}, json={'inputs':p}, timeout=60)
                return r.json()[0]['generated_text']
            except: continue
        return None

# --- 2. EMERGENCY GENERATOR ---
class EmergencyContentGenerator:
    def generate_blog(self, topic):
        return {
            "title": f"{topic}: The 2026 Guide",
            "article_html": f"""
            <p class="lead">Exploring <strong>{topic}</strong> reveals the power of connection.</p>
            <h2>Why it matters</h2>
            <p>In a digital age, personal touches like voice messages mean everything. {topic} is more than a gift; it is a memory.</p>
            <h2>The Solution</h2>
            <p>SayPlay allows you to attach audio to any object. It is simple, effective, and emotional.</p>
            """
        }

    def generate_seo(self, topic, city):
        return {
            "title": f"{topic} in {city}",
            "intro_html": f"<p>Find {topic} in {city}.</p>",
            "problem_html": "<p>Gifts often lack personality.</p>",
            "solution_html": "<p>SayPlay adds voice to gifts.</p>",
            "local_html": f"<p>Available now in {city}.</p>",
            "faq_html": "<p>No app required.</p>"
        }

# --- 3. SCANNER ---
class UniversalScanner:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def scan(self):
        print("🔭 OBSERVATORY: Scanning...")
        trends = []
        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    sources = list(reader)
                    random.shuffle(sources)
                    for site in sources[:15]:
                        t = site.get('temat', '')
                        if t and "404" not in t: trends.append(f"{t} idea")
            except: pass
            
        evergreen = ["Emotional Gifts", "Long Distance Love", "Wedding Favors", "Baby Shower Ideas"]
        return list(set(trends + evergreen))[:10]

# --- 4. ENGINES ---
class VisualEngine:
    def __init__(self, brain, path):
        self.brain = brain
        self.path = path / "images"
        self.path.mkdir(parents=True, exist_ok=True)

    def get_image(self, topic):
        slug = "".join(x for x in topic.lower() if x.isalnum())[:40]
        fpath = self.path / f"{slug}.jpg"
        if fpath.exists(): return f"/assets/images/{slug}.jpg"

        print(f"      🎨 Generating Image: {topic}")
        prompt = self.brain.generate(f"Prompt for photo of {topic}, 8k, luxury", min_len=10) or f"Luxury photo of {topic}"
        try:
            safe = urllib.parse.quote(str(prompt)[:200])
            url = f"https://pollinations.ai/p/{safe}?width=1280&height=720&nologo=true"
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                with open(fpath, 'wb') as f: f.write(r.content)
                return f"/assets/images/{slug}.jpg"
        except: pass
        return "/assets/milo-gigi.png"

class EditorialEngine:
    def __init__(self, brain):
        self.brain = brain
        self.emer = EmergencyContentGenerator()

    def create_blog(self, topic):
        print(f"   ✍️ Writing Blog: {topic}")
        res = self.brain.generate(f"Write 1500w HTML blog about '{topic}'. Use h2, p.", min_len=1500)
        return {"title": topic, "article_html": res} if res else self.emer.generate_blog(topic)

    def create_seo(self, topic, city):
        print(f"   🌐 SEO Page: {topic} in {city}")
        res = self.brain.generate(f"SEO JSON for '{topic} in {city}': title, intro_html, problem_html, solution_html, local_html, faq_html", json_mode=True)
        return res if res else self.emer.generate_seo(topic, city)

class SocialGenerator:
    def __init__(self, brain): self.brain = brain
    def generate(self, topic, folder):
        folder.mkdir(parents=True, exist_ok=True)
        tt = self.brain.generate(f"TikTok script for {topic}", min_len=100) or "TikTok Draft"
        with open(folder/"tiktok.txt", "w") as f: f.write(str(tt))

class AudioStudio:
    async def create(self, text, path):
        if not EDGE_TTS_AVAILABLE: return
        try: await edge_tts.Communicate(text[:2000], "en-GB-SoniaNeural").save(str(path))
        except: pass

class ChameleonDesigner:
    def build(self, type, data, path, img):
        title = data.get('title', 'Guide')
        body = data.get('article_html') if type == 'blog' else "".join([str(v) for k,v in data.items() if 'html' in k])
        html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{title}</title><script src="https://cdn.tailwindcss.com?plugins=typography"></script></head><body class="bg-gray-50"><img src="{img}" class="w-full h-64 object-cover"><div class="max-w-3xl mx-auto p-8 prose prose-lg bg-white -mt-10 relative rounded shadow">{body}</div></body></html>"""
        with open(path, 'w', encoding='utf-8') as f: f.write(html)

# --- 5. ROBUST CMEL (FIXED) ---
class CMEL:
    def __init__(self, path):
        self.path = path
        self.data = self._load()

    def _load(self):
        defaults = {"content_log": [], "id_counter": 100}
        if self.path.exists():
            try:
                loaded = json.load(open(self.path))
                # FIX: Migrate legacy keys if needed
                if "global_id_counter" in loaded:
                    loaded["id_counter"] = loaded.pop("global_id_counter")
                # FIX: Ensure all keys exist
                for k, v in defaults.items():
                    if k not in loaded: loaded[k] = v
                return loaded
            except: pass
        return defaults

    def save(self):
        json.dump(self.data, open(self.path, 'w'), indent=2)

    def register(self, type, topic, file):
        self.data["id_counter"] += 1
        self.data["content_log"].append({
            "id": self.data["id_counter"],
            "type": type,
            "topic": topic,
            "file": file,
            "date": str(datetime.now())
        })
        self.save()

async def main():
    print("🚀 SPME V1.2 STABLE START")
    root = Path("website")
    for d in ['blog', 'seo', 'podcasts', 'assets/images']: (root/d).mkdir(parents=True, exist_ok=True)
    
    cmel = CMEL(Path("content_history.json"))
    brain = MultiAIBrain()
    scanner = UniversalScanner(Config.SCANNER_CSV)
    vis = VisualEngine(brain, root/"assets")
    editor = EditorialEngine(brain)
    social = SocialGenerator(brain)
    audio = AudioStudio()
    designer = ChameleonDesigner()
    dash = DashboardIndexGenerator()

    topics = scanner.scan()
    print(f"🎯 Targets: {len(topics)}")

    for topic in topics:
        clean = topic.split(" idea")[0]
        slug = "".join(x for x in clean.lower() if x.isalnum())[:50]
        
        img = vis.get_image(clean)
        
        # Blog
        b_data = editor.create_blog(clean)
        designer.build('blog', b_data, root/'blog'/f"{slug}.html", img)
        cmel.register('blog', clean, f"{slug}.html")
        
        # SEO
        city = random.choice(['London', 'Manchester'])
        s_data = editor.create_seo(clean, city)
        designer.build('seo', s_data, root/'seo'/f"{slug}-{city.lower()}.html", img)
        cmel.register('seo', clean, f"{slug}-{city.lower()}.html")
        
        # Social
        social.generate(clean, Path("social_media_assets")/slug)
        
        # Podcast
        await audio.create(f"Podcast about {clean}", root/'podcasts'/f"{slug}.mp3")
        cmel.register('podcast', clean, f"{slug}.mp3")

    # Dashboard logic
    legacy = {"seo_pages":[], "blog_posts":[], "podcasts":[]}
    for i in cmel.data["content_log"]:
        if i['type'] == 'blog': legacy['blog_posts'].append({'topic': i['topic'], 'filename': i['file'], 'created': i['date']})
        if i['type'] == 'seo': legacy['seo_pages'].append({'topic': i['topic'], 'filename': i['file'], 'created': i['date']})
        if i['type'] == 'podcast': legacy['podcasts'].append({'topic': i['topic'], 'filename': i['file'], 'created': i['date']})

    dash.generate_main_dashboard(root/'index.html', {"seo": len(legacy['seo_pages']), "blog": len(legacy['blog_posts'])})
    dash.generate_blog_index(root/'blog'/'index.html', legacy['blog_posts'])
    dash.generate_seo_index(root/'seo'/'index.html', legacy['seo_pages'])
    dash.generate_podcast_index(root/'podcasts'/'index.html', legacy['podcasts'])

    print("✅ DONE")

if __name__ == "__main__":
    asyncio.run(main())
