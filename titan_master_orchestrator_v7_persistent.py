#!/usr/bin/env python3
"""
TITAN V7 PERSISTENT - Dashboard + Metadata + 6-Tier AI Cascade
Version: 7.1 (Fixes: Images, Links, FFmpeg Audio)
Features:
- 6-tier AI cascade
- Real FFmpeg audio concatenation (fixes 6s bug)
- Logo and Mascot image integration
- Hardcoded production links
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
import subprocess  # Added for FFmpeg

# Import metadata managers
from content_metadata_manager import ContentMetadataManager
from dashboard_index_generator import DashboardIndexGenerator

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini not available")

# Audio
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ Edge TTS not available")

# Templates
try:
    from jinja2 import Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("⚠️ Jinja2 not available")

import requests


class AIConfig:
    """AI Models configuration"""
    # Gemini models
    GEMINI_PRO = 'gemini-1.5-pro'
    GEMINI_FLASH = 'gemini-1.5-flash'
    GEMINI_PRO_OLD = 'gemini-pro'
    
    # OpenAI
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    
    # Groq
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    
    TIMEOUT = 60  # Increased timeout for longer scripts


class ContentBrain:
    """
    6-TIER AI CASCADE with emergency fallback
    """
    
    def __init__(self, api_key: str):
        self.gemini_key = api_key
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        
        self.has_gemini = GEMINI_AVAILABLE and api_key
        self.has_openai = bool(self.openai_key)
        self.has_groq = bool(self.groq_key)
        
        if self.has_gemini:
            genai.configure(api_key=api_key)
            print("✅ Gemini configured")
    
    def generate_seo_page(self, topic: str, city: str) -> Dict:
        print(f"      🧠 SEO: {topic} in {city}")
        for tier_name, method in [
            ('Gemini 1.5 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO, 'seo', topic, city)),
            ('Gemini 1.5 Flash', lambda: self._try_gemini(AIConfig.GEMINI_FLASH, 'seo', topic, city)),
            ('Gemini 1.0 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO_OLD, 'seo', topic, city)),
            ('OpenAI GPT-3.5', lambda: self._try_openai('seo', topic, city)),
            ('Groq Llama 3.1', lambda: self._try_groq('seo', topic, city))
        ]:
            result = method()
            if result:
                print(f"         ✅ {tier_name}")
                return result
        print(f"         🚨 Emergency Template")
        return self._emergency_seo(topic, city)
    
    def generate_blog(self, topic: str) -> Dict:
        print(f"      📝 Blog: {topic}")
        for tier_name, method in [
            ('Gemini 1.5 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO, 'blog', topic)),
            ('Gemini 1.5 Flash', lambda: self._try_gemini(AIConfig.GEMINI_FLASH, 'blog', topic)),
            ('Gemini 1.0 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO_OLD, 'blog', topic)),
            ('OpenAI GPT-3.5', lambda: self._try_openai('blog', topic)),
            ('Groq Llama 3.1', lambda: self._try_groq('blog', topic))
        ]:
            result = method()
            if result:
                print(f"         ✅ {tier_name}")
                return result
        print(f"         🚨 Emergency Template")
        return self._emergency_blog(topic)
    
    def generate_podcast_script(self, topic: str) -> str:
        print(f"      🎙️ Podcast: {topic}")
        for tier_name, method in [
            ('Gemini 1.5 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO, 'podcast', topic)),
            ('Gemini 1.5 Flash', lambda: self._try_gemini(AIConfig.GEMINI_FLASH, 'podcast', topic)),
            ('Gemini 1.0 Pro', lambda: self._try_gemini(AIConfig.GEMINI_PRO_OLD, 'podcast', topic)),
            ('OpenAI GPT-3.5', lambda: self._try_openai('podcast', topic)),
            ('Groq Llama 3.1', lambda: self._try_groq('podcast', topic))
        ]:
            result = method()
            if result:
                print(f"         ✅ {tier_name}")
                return result
        print(f"         🚨 Emergency Template")
        return self._emergency_podcast(topic)
    
    def _try_gemini(self, model_name: str, content_type: str, topic: str, city: str = '') -> Optional:
        if not self.has_gemini: return None
        try:
            model = genai.GenerativeModel(model_name)
            if content_type == 'seo': prompt = self._get_seo_prompt(topic, city)
            elif content_type == 'blog': prompt = self._get_blog_prompt(topic)
            else: prompt = self._get_podcast_prompt(topic)
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.8, max_output_tokens=4096),
                request_options={'timeout': AIConfig.TIMEOUT}
            )
            text = response.text.strip()
            if content_type == 'podcast': return text.replace('*', '').replace('#', '').replace('```', '')
            if '```json' in text: text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text: text = text.split('```')[1].split('```')[0].strip()
            return json.loads(text)
        except Exception as e:
            return None
    
    def _try_openai(self, content_type: str, topic: str, city: str = '') -> Optional:
        if not self.has_openai: return None
        try:
            if content_type == 'seo': prompt = self._get_seo_prompt(topic, city)
            elif content_type == 'blog': prompt = self._get_blog_prompt(topic)
            else: prompt = self._get_podcast_prompt(topic)
            
            response = requests.post(
                AIConfig.OPENAI_ENDPOINT,
                headers={'Authorization': f'Bearer {self.openai_key}', 'Content-Type': 'application/json'},
                json={'model': AIConfig.OPENAI_MODEL, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.8, 'max_tokens': 3000},
                timeout=AIConfig.TIMEOUT
            )
            if response.status_code != 200: return None
            text = response.json()['choices'][0]['message']['content'].strip()
            if content_type == 'podcast': return text.replace('*', '').replace('#', '').replace('```', '')
            if '```json' in text: text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text: text = text.split('```')[1].split('```')[0].strip()
            return json.loads(text)
        except: return None

    def _try_groq(self, content_type: str, topic: str, city: str = '') -> Optional:
        if not self.has_groq: return None
        try:
            if content_type == 'seo': prompt = self._get_seo_prompt(topic, city, shorter=True)
            elif content_type == 'blog': prompt = self._get_blog_prompt(topic, shorter=True)
            else: prompt = self._get_podcast_prompt(topic, shorter=True)
            
            response = requests.post(
                AIConfig.GROQ_ENDPOINT,
                headers={'Authorization': f'Bearer {self.groq_key}', 'Content-Type': 'application/json'},
                json={'model': AIConfig.GROQ_MODEL, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.7, 'max_tokens': 3000},
                timeout=AIConfig.TIMEOUT
            )
            if response.status_code != 200: return None
            text = response.json()['choices'][0]['message']['content'].strip()
            if content_type == 'podcast': return text.replace('*', '').replace('#', '').replace('```', '')
            if '```json' in text: text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text: text = text.split('```')[1].split('```')[0].strip()
            return json.loads(text)
        except: return None

    def _get_seo_prompt(self, topic: str, city: str, shorter: bool = False) -> str:
        facts = "Voice: 60s max, Video: 30s max, Hosting: 1yr, No app (NFC tap), Mascots: Mylo & Gigi"
        if shorter:
            return f"""Write SEO page for "{topic} in {city}" for SayPlay gift stickers.
FACTS: {facts}
OUTPUT JSON: {{"title": "...", "meta_desc": "...", "intro_html": "<p>...</p>", "problem_html": "<p>...</p>", "solution_html": "<p>...</p>", "howto_html": "<p>...</p>", "local_html": "<p>...</p>", "faq_html": "<div class='faq-item'>...</div>"}}"""
        
        return f"""Senior SEO copywriter for SayPlay - UK NFC voice/video gift stickers.
FACTS: {facts}
Write comprehensive page: "{topic} in {city}"
REQUIREMENTS:
- 1500+ characters total
- Natural UK English
- Mention Mylo & Gigi mascots
- Local {city} references
JSON OUTPUT:
{{
    "title": "...",
    "meta_desc": "...",
    "intro_html": "<p>Long paragraph 150+ words...</p>",
    "problem_html": "<p>Long paragraph 150+ words...</p>",
    "solution_html": "<p>Long paragraph 200+ words highlighting Mylo and Gigi...</p>",
    "howto_html": "<p>Long paragraph 150+ words...</p>",
    "local_html": "<p>Paragraph 100+ words about {city} shops...</p>",
    "faq_html": "<div class='faq-item'><h4>Question?</h4><p>Detailed answer...</p></div>..."
}}"""

    def _get_blog_prompt(self, topic: str, shorter: bool = False) -> str:
        facts = "Voice: 60s max, Video: 30s max, Hosting: 1yr, No app, Mascots: Mylo & Gigi"
        if shorter:
            return f"""Write blog article: "{topic}" for SayPlay gift stickers.
OUTPUT JSON: {{"title": "...", "article_html": "<p>...</p>", "keywords": ["..."]}}"""
        
        return f"""Senior content writer for SayPlay blog.
FACTS: {facts}
Write comprehensive blog: "{topic}"
REQUIREMENTS:
- 2000+ characters
- UK English
- Mention Mylo & Gigi
JSON OUTPUT:
{{
    "title": "Engaging title",
    "article_html": "<p>Long story...</p><p>Main content...</p>...",
    "keywords": ["keyword1", "keyword2"]
}}"""

    def _get_podcast_prompt(self, topic: str, shorter: bool = False) -> str:
        facts = "Voice: 60s, Video: 30s, Hosting: 1yr, No app, Mascots: Mylo & Gigi"
        # Increased word count request to ensure ~4 mins
        return f"""Podcast script for SayPlay Gift Guide.
FACTS: {facts}
Topic: "{topic}"
REQUIREMENTS:
- **EXTREMELY IMPORTANT: LENGTH MUST BE 800-1000 WORDS (approx 4 minutes spoken)**
- Host: Sonia (UK, warm tone)
- Conversational, natural, storytelling
- Break it down into clear segments
- Mention Mylo and Gigi the mascots explicitly
OUTPUT: Spoken script only, no markdown, no stage directions."""

    def _emergency_seo(self, topic: str, city: str) -> Dict:
        return {
            'title': f'Perfect {topic} in {city} | SayPlay UK',
            'meta_desc': f'Looking for {topic} in {city}? Add voice/video messages to gifts with SayPlay NFC stickers. No app needed - just tap!',
            'intro_html': f'<p>Finding the perfect {topic.lower()} in <strong>{city}</strong> can be challenging.</p>',
            'problem_html': '<p>Most gifts end up forgotten in a drawer.</p>',
            'solution_html': '<p>SayPlay transforms any gift. Meet our mascots Mylo and Gigi!</p>',
            'howto_html': '<p>Step 1: Record. Step 2: Stick. Step 3: Give.</p>',
            'local_html': f'<p>Shopping in {city} is great.</p>',
            'faq_html': '<div class="faq-item"><h4>App needed?</h4><p>No!</p></div>'
        }

    def _emergency_blog(self, topic: str) -> Dict:
        return {
            'title': f'{topic}: Guide',
            'article_html': f'<p>Traditional gifts often fail to create lasting memories. SayPlay changes that with Mylo and Gigi.</p>',
            'keywords': ['gifts', 'SayPlay']
        }

    def _emergency_podcast(self, topic: str) -> str:
        return f"Welcome to SayPlay. Today we talk about {topic}. It is very important to give good gifts. Use SayPlay stickers. Mylo and Gigi love them. Visit sayplay.co.uk. Goodbye."


class DesignEngine:
    """Premium design templates with LOGO and IMAGES fixed"""
    
    def __init__(self):
        if not JINJA2_AVAILABLE:
            self.seo_template = None
            self.blog_template = None
            return
        
        # LOGO FIXED: Points to /assets/sayplay_logo.png
        # MASCOT FIXED: Points to /assets/milo-gigi.png
        # LINKS FIXED: Hardcoded to [https://sayplay.co.uk](https://sayplay.co.uk)
        
        self.seo_template_str = """<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | SayPlay UK</title>
    <meta name="description" content="{{ meta_desc }}">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Open+Sans:wght@400;600&display=swap](https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Open+Sans:wght@400;600&display=swap)" rel="stylesheet">
    <style>
        body{font-family:'Open Sans',sans-serif}
        h1,h2,h3,h4{font-family:'Poppins',sans-serif}
        .faq-item{background:#f8f9fa;padding:1.5rem;margin-bottom:1rem;border-radius:0.5rem}
        .faq-item h4{margin-bottom:0.5rem;font-weight:600}
    </style>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="[https://sayplay.co.uk](https://sayplay.co.uk)">
                <img src="/assets/sayplay_logo.png" alt="SayPlay Logo" class="h-12 w-auto object-contain">
            </a>
            <a href="[https://sayplay.co.uk/collections/all](https://sayplay.co.uk/collections/all)" class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-6 rounded-full transition">Shop Now</a>
        </div>
    </nav>
    <header class="bg-gradient-to-r from-orange-500 to-orange-600 text-white py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-4xl md:text-6xl font-extrabold mb-6">{{ title }}</h1>
            <p class="text-xl mb-8 opacity-90">Transform any gift with your voice or video message</p>
            <a href="[https://sayplay.co.uk/collections/all](https://sayplay.co.uk/collections/all)" class="bg-white text-orange-600 font-bold py-4 px-10 rounded-full text-lg hover:scale-105 transition transform inline-block shadow-lg">🎁 Start Creating</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-6 py-16">
        <section class="prose lg:prose-xl max-w-none mb-12">{{ intro_html | safe }}</section>
        
        <div class="text-center my-12"><a href="[https://sayplay.co.uk](https://sayplay.co.uk)" class="text-orange-600 font-bold underline text-xl hover:text-orange-700">👉 Browse Stickers</a></div>
        
        <section class="bg-white p-8 rounded-2xl shadow-sm mb-12">
            <h2 class="text-3xl font-bold mb-6 text-gray-900">The Problem</h2>
            <div class="prose max-w-none">{{ problem_html | safe }}</div>
        </section>
        
        <section class="bg-orange-50 p-8 rounded-2xl mb-12 border border-orange-100">
            <div class="flex flex-col md:flex-row items-center gap-8">
                <div class="flex-1">
                    <h2 class="text-3xl font-bold mb-6 text-orange-900">The Solution</h2>
                    <div class="prose max-w-none">{{ solution_html | safe }}</div>
                </div>
                <div class="w-full md:w-1/3">
                    <img src="/assets/milo-gigi.png" alt="Milo and Gigi" class="w-full h-auto rounded-lg shadow-md transform hover:scale-105 transition">
                </div>
            </div>
            <div class="mt-6 p-4 bg-white rounded-lg border-2 border-orange-200">
                <p class="font-bold text-orange-800 mb-2">✨ Specs:</p>
                <ul class="text-gray-700 space-y-1">
                    <li>🎤 Voice: 60 seconds</li>
                    <li>📹 Video: 30 seconds</li>
                    <li>☁️ Hosting: 1 year (downloadable)</li>
                    <li>📱 No app required</li>
                </ul>
            </div>
        </section>
        
        <section class="mb-12">
            <h2 class="text-3xl font-bold mb-6">How It Works</h2>
            <div class="prose max-w-none">{{ howto_html | safe }}</div>
        </section>
        
        <div class="text-center my-12"><a href="[https://sayplay.co.uk/products/starter-pack](https://sayplay.co.uk/products/starter-pack)" class="bg-black text-white py-4 px-10 rounded-lg font-bold text-lg hover:bg-gray-800 transition inline-block shadow-lg">Get Starter Pack</a></div>
        
        <section class="bg-blue-50 p-8 rounded-2xl mb-12">
            <h2 class="text-3xl font-bold mb-6 text-blue-900">Local Shopping</h2>
            <div class="prose max-w-none">{{ local_html | safe }}</div>
        </section>
        
        <section class="mb-12">
            <h2 class="text-3xl font-bold mb-8 text-center">FAQ</h2>
            <div class="space-y-4">{{ faq_html | safe }}</div>
        </section>
    </main>
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-4xl mx-auto px-6 text-center">
            <h3 class="text-3xl font-bold mb-6">Ready?</h3>
            <a href="[https://sayplay.co.uk](https://sayplay.co.uk)" class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 px-12 rounded-full text-xl transition shadow-lg inline-block mb-8">Buy Now</a>
            <p class="text-gray-400 text-sm">&copy; 2025 SayPlay UK</p>
        </div>
    </footer>
</body>
</html>"""
        
        self.blog_template_str = """<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} | SayPlay</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap](https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap)" rel="stylesheet">
    <style>body{font-family:'Inter'}h1,h2{font-family:'Playfair Display'}</style>
</head>
<body class="bg-stone-50">
    <nav class="bg-white border-b sticky top-0 z-50">
        <div class="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="[https://sayplay.co.uk](https://sayplay.co.uk)">
                <img src="/assets/sayplay_logo.png" alt="SayPlay Logo" class="h-10 w-auto">
            </a>
            <a href="[https://sayplay.co.uk/collections/all](https://sayplay.co.uk/collections/all)" class="bg-stone-900 text-white px-6 py-2 rounded-full hover:bg-orange-600 transition">Shop</a>
        </div>
    </nav>
    <header class="bg-gradient-to-br from-orange-600 to-orange-400 text-white py-24">
        <div class="max-w-4xl mx-auto px-6 text-center">
            <h1 class="text-5xl md:text-6xl mb-4">{{ title }}</h1>
        </div>
    </header>
    <main class="max-w-3xl mx-auto px-6 py-16">
        <article class="prose prose-xl max-w-none">
            {{ article_html | safe }}
        </article>
        
        <div class="my-12">
            <img src="/assets/milo-gigi.png" alt="Milo and Gigi" class="w-full rounded-xl shadow-lg">
        </div>

        <div class="mt-12 bg-orange-50 p-8 rounded-2xl text-center">
            <h3 class="text-2xl font-bold mb-4">Try SayPlay</h3>
            <a href="[https://sayplay.co.uk](https://sayplay.co.uk)" class="bg-orange-600 text-white px-8 py-3 rounded-full font-bold hover:bg-orange-700 transition inline-block">Shop Now</a>
        </div>
    </main>
    <footer class="bg-stone-900 text-stone-400 py-12 text-center"><p>&copy; 2025 SayPlay UK</p></footer>
</body>
</html>"""
        
        self.seo_template = Template(self.seo_template_str) if JINJA2_AVAILABLE else None
        self.blog_template = Template(self.blog_template_str) if JINJA2_AVAILABLE else None
    
    def build_seo_page(self, content: Dict, output_path: Path):
        if not self.seo_template:
            self._build_fallback(content, output_path)
            return
        try:
            html = self.seo_template.render(**content)
            with open(output_path, 'w', encoding='utf-8') as f: f.write(html)
            print(f"      ✅ SEO: {output_path.name}")
        except Exception as e:
            print(f"      ⚠️ Template error: {str(e)[:50]}")
            self._build_fallback(content, output_path)
    
    def build_blog_page(self, content: Dict, output_path: Path):
        if not self.blog_template:
            self._build_fallback(content, output_path)
            return
        try:
            html = self.blog_template.render(**content)
            with open(output_path, 'w', encoding='utf-8') as f: f.write(html)
            print(f"      ✅ Blog: {output_path.name}")
        except Exception as e:
            print(f"      ⚠️ Template error: {str(e)[:50]}")
            self._build_fallback(content, output_path)
    
    def _build_fallback(self, content: Dict, output_path: Path):
        title = content.get('title', 'SayPlay')
        body = '<br>'.join(str(v) for v in content.values() if isinstance(v, str))
        html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title}</title></head><body>{body}</body></html>'
        with open(output_path, 'w', encoding='utf-8') as f: f.write(html)


class AudioStudio:
    """Podcast generator using FFmpeg for correct 4-minute file composition"""
    
    def __init__(self):
        self.intro_paths = [
            Path("runtime_assets/Just tap.No app intro podkast sayplay.mp3"),
            Path("assets/music/Just tap.No app intro podkast sayplay.mp3")
        ]
        self.outro_paths = [
            Path("runtime_assets/Just tap.no app final podkast.mp3"),
            Path("assets/music/Just tap.no app final podkast.mp3")
        ]
        
        self.intro_file = next((p for p in self.intro_paths if p.exists()), None)
        self.outro_file = next((p for p in self.outro_paths if p.exists()), None)
        
        if self.intro_file: print(f"✅ Intro: {self.intro_file}")
        if self.outro_file: print(f"✅ Outro: {self.outro_file}")
    
    async def generate_podcast(self, script: str, episode_num: int, slug: str, output_dir: Path) -> Optional[Path]:
        if not EDGE_TTS_AVAILABLE:
            print("      ⚠️ Edge TTS not available")
            return None
        
        if not script or len(script) < 50:
            script = f"Welcome to SayPlay. Episode {episode_num}. Visit sayplay.co.uk."
        
        print(f"      🎙️ Ep #{episode_num}: {len(script)} chars")
        
        # 1. Generate Main Body
        temp_body = output_dir / f"temp_body_{episode_num}.mp3"
        try:
            communicate = edge_tts.Communicate(script, "en-GB-SoniaNeural")
            await communicate.save(str(temp_body))
        except Exception as e:
            print(f"          ❌ TTS failed: {str(e)[:50]}")
            return None
        
        # 2. Prepare Output
        filename = f"sayplay_ep_{episode_num:03d}_{slug}.mp3"
        output_path = output_dir / filename
        
        # 3. Concatenate using FFmpeg (The only reliable way)
        # We build a list of inputs: Intro (if exists) + Body + Outro (if exists)
        inputs = []
        if self.intro_file: inputs.append(str(self.intro_file))
        inputs.append(str(temp_body))
        if self.outro_file: inputs.append(str(self.outro_file))
        
        # Construct FFmpeg command
        # filter_complex "concat" ensures audio streams are merged properly
        cmd = ['ffmpeg', '-y']
        for inp in inputs:
            cmd.extend(['-i', inp])
        
        # Simple concat filter: n=number_of_inputs:v=0:a=1 (0 video, 1 audio)
        filter_str = f"concat=n={len(inputs)}:v=0:a=1[out]"
        cmd.extend(['-filter_complex', filter_str, '-map', '[out]', str(output_path)])
        
        try:
            # Run FFmpeg quietly
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"          ✅ {filename} (Merged {len(inputs)} parts)")
        except subprocess.CalledProcessError:
            print(f"          ⚠️ FFmpeg merge failed, fallback to body only")
            shutil.copy(temp_body, output_path)
        except FileNotFoundError:
             print(f"          ⚠️ FFmpeg not found, fallback to body only")
             shutil.copy(temp_body, output_path)

        # Cleanup temp
        if temp_body.exists(): temp_body.unlink()
        
        return output_path


class TrendHunter:
    """Reddit topic hunter"""
    SUBREDDITS = ['GiftIdeas', 'weddingplanning', 'relationship_advice']
    
    def get_topics(self, limit: int = 15) -> List[Dict]:
        print(f"📡 Scanning Reddit...")
        trends = []
        headers = {'User-Agent': 'SayPlayBot/1.0'}
        for subreddit in self.SUBREDDITS:
            try:
                url = f"[https://www.reddit.com/r/](https://www.reddit.com/r/){subreddit}/top.json?t=week&limit={limit}"
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for post in data['data']['children']:
                        if len(post['data'].get('selftext', '')) > 100:
                            trends.append({'title': post['data']['title'], 'score': post['data']['score']})
            except: pass
        trends.sort(key=lambda x: x['score'], reverse=True)
        if not trends:
            trends = [{'title': 'Unique Wedding Gifts', 'score': 1000}, {'title': 'Birthday Gifts Dad', 'score': 850}]
        return trends[:limit]


async def main():
    print("\n" + "="*70)
    print("TITAN V7.1 - FIXED: Images, Links & FFmpeg Audio")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_V7_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    web_dir = output_dir / 'web'
    assets_dir = web_dir / 'assets'
    
    for d in ['blog', 'podcasts', 'seo', 'assets']:
        (web_dir / d).mkdir(parents=True, exist_ok=True)
    
    # --- FIX: COPY IMAGE ASSETS TO OUTPUT ---
    print(f"\n📂 Copying visual assets...")
    runtime_assets = Path("runtime_assets")
    if runtime_assets.exists():
        for item in runtime_assets.glob("*.png"):
            shutil.copy(item, assets_dir / item.name)
            print(f"   ✅ Copied {item.name}")
    else:
        print("   ⚠️ runtime_assets not found, images might be missing")
    # ----------------------------------------
    
    # Initialize managers
    history_file = Path('content_history.json')
    metadata = ContentMetadataManager(history_file)
    dashboard_gen = DashboardIndexGenerator()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    brain = ContentBrain(gemini_key)
    design = DesignEngine()
    audio = AudioStudio()
    hunter = TrendHunter()
    
    cities = ['London', 'Birmingham', 'Manchester', 'Liverpool', 'Leeds', 'Glasgow', 'Bristol']
    
    # Phase 1: Hunt
    topics = hunter.get_topics(limit=15)
    
    # Phase 2: SEO
    print(f"\nPHASE 2: SEO PAGES")
    seo_count = 0
    for i, topic in enumerate(topics, 1):
        city = random.choice(cities)
        if metadata.is_duplicate_seo(topic['title'], city): continue
        print(f"\n📌 SEO {seo_count+1}: {topic['title'][:40]}... in {city}")
        content = brain.generate_seo_page(topic['title'], city)
        slug = ''.join(c for c in topic['title'].lower().replace(' ', '-')[:40] if c.isalnum() or c == '-')
        filename = f'{slug}-{city.lower()}.html'
        design.build_seo_page(content, web_dir / 'seo' / filename)
        metadata.add_seo_page(topic['title'], city, filename, content.get('title', topic['title']))
        seo_count += 1
        if seo_count >= 10: break
    
    # Phase 3: Blog
    print(f"\nPHASE 3: BLOG POSTS")
    blog_count = 0
    for i, topic in enumerate(topics, 1):
        if metadata.is_duplicate_blog(topic['title']): continue
        print(f"\n📝 Blog {blog_count+1}: {topic['title'][:40]}...")
        content = brain.generate_blog(topic['title'])
        slug = ''.join(c for c in topic['title'].lower().replace(' ', '-')[:40] if c.isalnum() or c == '-')
        filename = f'{slug}.html'
        design.build_blog_page(content, web_dir / 'blog' / filename)
        metadata.add_blog_post(topic['title'], filename, content.get('title', topic['title']))
        blog_count += 1
        if blog_count >= 10: break
    
    # Phase 4: Podcasts
    print(f"\nPHASE 4: PODCASTS")
    podcast_count = 0
    for i, topic in enumerate(topics, 1):
        if metadata.is_duplicate_podcast(topic['title']): continue
        episode_num = metadata.get_next_episode_number()
        print(f"\n🎙️  Ep #{episode_num}: {topic['title'][:40]}...")
        script = brain.generate_podcast_script(topic['title'])
        slug = ''.join(c for c in topic['title'].lower().replace(' ', '-')[:30] if c.isalnum() or c == '-')
        await audio.generate_podcast(script, episode_num, slug, web_dir / 'podcasts')
        filename = f'sayplay_ep_{episode_num:03d}_{slug}.mp3' # Logic repeated inside audio, but tracking here
        metadata.add_podcast(topic['title'], filename, episode_num)
        podcast_count += 1
        if podcast_count >= 10: break
    
    # Phase 5 & 6
    metadata.save()
    shutil.copy(history_file, web_dir / 'assets' / 'content_history.json')
    
    stats = metadata.get_stats()
    dashboard_gen.generate_main_dashboard(web_dir / 'index.html', stats)
    dashboard_gen.generate_seo_index(web_dir / 'seo' / 'index.html', metadata.get_all_seo_pages())
    dashboard_gen.generate_blog_index(web_dir / 'blog' / 'index.html', metadata.get_all_blog_posts())
    dashboard_gen.generate_podcast_index(web_dir / 'podcasts' / 'index.html', metadata.get_all_podcasts())
    
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\nSUCCESS! {seo_count} SEO, {blog_count} Blogs, {podcast_count} Podcasts. Time: {int(duration)}s")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
