#!/usr/bin/env python3
"""
SAYPLAY MEDIA ENGINE (SPME) V1.3 - CRASH PROOF
Fixes:
- KeyError 'file' (Handles mixed legacy data structure automatically).
- API Reliability (Improved timeouts).
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

# Dummy Dashboard
try:
    from dashboard_index_generator import DashboardIndexGenerator
except ImportError:
    class DashboardIndexGenerator:
        def generate_main_dashboard(self, p, d): pass
        def generate_seo_index(self, p, d): pass
        def generate_blog_index(self, p, d): pass
        def generate_podcast_index(self, p, d): pass

# --- CONFIG ---
class Config:
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    GEMINI_MODEL = 'gemini-1.5-flash'
    HF_MODELS = ['meta-llama/Meta-Llama-3-70B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1']
    HF_ENDPOINT = 'https://api-inference.huggingface.co/models/'
    SCANNER_CSV = "sources.csv"

# --- 1. BRAIN ---
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
        if self.keys['groq']:
            res = self._req_groq(prompt)
            if self._valid(res, min_len): return self._parse(res, json_mode)
        if self.keys['gemini'] and GEMINI_AVAILABLE:
            res = self._req_gemini(prompt)
            if self._valid(res, min_len): return self._parse(res, json_mode)
        print("      ⚠️ AI Failed. Using Template.")
        return None

    def _valid(self, text, min_len): return text and len(str(text)) > min_len * 0.5
    def _parse(self, text, json_mode):
        if not json_mode: return text
        try: return json.loads(text.replace('```json','').replace('```','').strip())
        except: return text

    def _req_groq(self, p):
        try:
            r = requests.post(Config.GROQ_ENDPOINT, headers={'Authorization':f"Bearer {self.keys['groq']}"}, json={'model':Config.GROQ_MODEL,'messages':[{'role':'user','content':p}]}, timeout=20)
            return r.json()['choices'][0]['message']['content']
        except: return None

    def _req_gemini(self, p):
        try: return genai.GenerativeModel(Config.GEMINI_MODEL).generate_content(p).text
        except: return None

# --- 2. EMERGENCY ---
class EmergencyContentGenerator:
    def generate_blog(self, topic):
        return {"title": f"{topic} Guide", "article_html": f"<p>Ultimate guide to <strong>{topic}</strong>. Voice gifts change everything.</p>"}
    def generate_seo(self, topic, city):
        return {"title": f"{topic} in {city}", "intro_html": f"<p>Find {topic} here.</p>", "problem_html":"", "solution_html":"", "local_html":"", "faq_html":""}

# --- 3. SCANNER ---
class UniversalScanner:
    def __init__(self, csv_path): self.csv_path = csv_path
    def scan(self):
        trends = []
        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, 'r') as f:
                    for row in csv.DictReader(f):
                        if random.random() < 0.2: trends.append(row.get('temat', 'Gift Idea'))
            except: pass
        return list(set(trends + ["Personalized Gifts"]))[:10]

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
        try:
            url = f"https://pollinations.ai/p/{urllib.parse.quote(topic)}?width=1280&height=720&nologo=true"
            r = requests.get(url, timeout=10)
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
        res = self.brain.generate(f"Write 1500w HTML blog about '{topic}'", min_len=1500)
        return {"title": topic, "article_html": res} if res else self.emer.generate_blog(topic)
    def create_seo(self, topic, city):
        res = self.brain.generate(f"SEO JSON for '{topic} in {city}': title, intro_html, problem_html, solution_html, local_html, faq_html", json_mode=True)
        return res if res else self.emer.generate_seo(topic, city)

class SocialGenerator:
    def __init__(self, brain): self.brain = brain
    def generate(self, topic, folder):
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder/"tiktok.txt", "w") as f: f.write(str(self.brain.generate(f"TikTok for {topic}") or "Draft"))

class AudioStudio:
    async def create(self, text, path):
        if EDGE_TTS_AVAILABLE:
            try: await edge_tts.Communicate(text[:2000], "en-GB-SoniaNeural").save(str(path))
            except: pass

class ChameleonDesigner:
    def build(self, type, data, path, img):
        body = data.get('article_html') if type == 'blog' else "".join([str(v) for k,v in data.items() if 'html' in k])
        html = f"<html><head><title>{data.get('title')}</title></head><body><img src='{img}' style='width:100%;height:300px;object-fit:cover'><h1>{data.get('title')}</h1>{body}</body></html>"
        with open(path, 'w', encoding='utf-8') as f: f.write(html)

# --- 5. ROBUST CMEL ---
class CMEL:
    def __init__(self, path):
        self.path = path
        self.data = self._load()
    def _load(self):
        defaults = {"content_log": [], "id_counter": 100}
        if self.path.exists():
            try:
                loaded = json.load(open(self.path))
                # Auto-repair missing keys
                if "global_id_counter" in loaded: loaded["id_counter"] = loaded.pop("global_id_counter")
                if "id_counter" not in loaded: loaded["id_counter"] = 100
                if "content_log" not in loaded: loaded["content_log"] = []
                return loaded
            except: pass
        return defaults
    def save(self): json.dump(self.data, open(self.path, 'w'), indent=2)
    def register(self, type, topic, file):
        self.data["id_counter"] += 1
        self.data["content_log"].append({"id": self.data["id_counter"], "type": type, "topic": topic, "file": file, "date": str(datetime.now())})
        self.save()

async def main():
    print("🚀 SPME V1.3 CRASH PROOF START")
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
        designer.build('blog', editor.create_blog(clean), root/'blog'/f"{slug}.html", img)
        cmel.register('blog', clean, f"{slug}.html")
        
        # SEO
        designer.build('seo', editor.create_seo(clean, "London"), root/'seo'/f"{slug}-london.html", img)
        cmel.register('seo', clean, f"{slug}-london.html")
        
        # Assets
        social.generate(clean, Path("social_media_assets")/slug)
        await audio.create(f"Podcast: {clean}", root/'podcasts'/f"{slug}.mp3")
        cmel.register('podcast', clean, f"{slug}.mp3")

    # FIX: SAFE DATA MAPPING FOR DASHBOARD
    legacy = {"seo_pages":[], "blog_posts":[], "podcasts":[]}
    for i in cmel.data["content_log"]:
        # Handles both 'file' (new) and 'filename' (old) keys safely
        fname = i.get('file') or i.get('filename') or 'unknown.html'
        topic = i.get('topic') or 'Unknown Topic'
        date = i.get('date') or str(datetime.now())
        
        entry = {'topic': topic, 'filename': fname, 'created': date}
        
        if i.get('type') == 'blog': legacy['blog_posts'].append(entry)
        if i.get('type') == 'seo': legacy['seo_pages'].append(entry)
        if i.get('type') == 'podcast': legacy['podcasts'].append(entry)

    dash.generate_main_dashboard(root/'index.html', {"seo": len(legacy['seo_pages']), "blog": len(legacy['blog_posts'])})
    dash.generate_blog_index(root/'blog'/'index.html', legacy['blog_posts'])
    dash.generate_seo_index(root/'seo'/'index.html', legacy['seo_pages'])
    dash.generate_podcast_index(root/'podcasts'/'index.html', legacy['podcasts'])

    print("✅ DONE")

if __name__ == "__main__":
    asyncio.run(main())
