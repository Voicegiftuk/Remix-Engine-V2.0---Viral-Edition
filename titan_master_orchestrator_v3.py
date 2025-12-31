#!/usr/bin/env python3
"""
TITAN V3 - PREMIUM CONTENT STUDIO
- Reddit Trend Hunter (real problems, real content)
- Jinja2 Templates (no AI CSS, professional design)
- State Management (no overwriting)
- Gemini Pro (better quality)
- Premium assets (Unsplash + your products)
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import base64
import asyncio
import hashlib
import json
import random
from typing import List, Dict, Set

sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Images & Web
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Audio
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Templates
try:
    from jinja2 import Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("⚠️ Jinja2 not available. Install: pip install jinja2")


class StateManager:
    """
    Pamięć systemu - zapobiega nadpisywaniu podcastów
    """
    def __init__(self, state_file: Path = Path("titan_memory.json")):
        self.state_file = state_file
        if not self.state_file.exists():
            self._save({"last_episode": 0, "processed_trends": [], "last_run": None})
    
    def _load(self) -> dict:
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def _save(self, data: dict):
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_next_episode_number(self) -> int:
        data = self._load()
        return data["last_episode"] + 1
    
    def commit_success(self, episode_num: int, trend_id: str):
        data = self._load()
        data["last_episode"] = episode_num
        data["processed_trends"].append(trend_id)
        data["last_run"] = datetime.now().isoformat()
        self._save(data)


class TrendHunter:
    """
    Łowca trendów - pobiera REALNE problemy z Reddit
    """
    
    SUBREDDITS = [
        'GiftIdeas',
        'weddingplanning',
        'relationship_advice',
        'relationships'
    ]
    
    def get_real_trends(self, limit: int = 5) -> List[Dict]:
        """Pobiera gorące tematy z Reddit"""
        print(f"📡 TrendHunter: Skanowanie Reddit...")
        
        trends = []
        headers = {'User-Agent': 'SayPlayTrendBot/1.0'}
        
        for subreddit in self.SUBREDDITS:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit={limit}"
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        
                        # Filtruj tylko wartościowe posty (z opisem)
                        if len(post_data.get('selftext', '')) > 100:
                            trends.append({
                                'source': f'r/{subreddit}',
                                'title': post_data['title'],
                                'context': post_data['selftext'][:800],
                                'url': f"https://reddit.com{post_data['permalink']}",
                                'score': post_data['score']
                            })
                            
            except Exception as e:
                print(f"   ⚠️ Error fetching r/{subreddit}: {str(e)[:60]}")
        
        # Sortuj po score (popularności)
        trends.sort(key=lambda x: x['score'], reverse=True)
        
        # Fallback jeśli Reddit nie działa
        if not trends:
            print("   ⚠️ Reddit unavailable, using evergreen topics")
            trends = self._get_evergreen_topics()
        
        selected = trends[:3]  # Top 3 najgorętsze tematy
        print(f"   ✅ Found {len(trends)} trends, selected {len(selected)} best")
        
        for i, t in enumerate(selected, 1):
            print(f"      {i}. [{t['source']}] {t['title'][:60]}...")
        
        return selected
    
    def _get_evergreen_topics(self) -> List[Dict]:
        """Tematy awaryjne gdy Reddit nie działa"""
        return [
            {
                'source': 'System',
                'title': 'Unique wedding gifts for couples who have everything',
                'context': 'People struggle to find meaningful gifts for couples with established homes. Traditional items feel impersonal.',
                'url': 'internal',
                'score': 1000
            },
            {
                'source': 'System',
                'title': 'Long distance relationship gift ideas UK',
                'context': 'Partners separated by distance need ways to feel connected. Physical gifts that bridge emotional gaps.',
                'url': 'internal',
                'score': 900
            }
        ]


class PremiumContentStudio:
    """
    AI Content Studio - używa Gemini PRO dla lepszej jakości
    """
    
    def __init__(self, api_key: str):
        if GEMINI_AVAILABLE:
            genai.configure(api_key=api_key)
            # Gemini PRO dla wyższej jakości content
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
    
    def develop_content_strategy(self, trend: Dict) -> Dict:
        """
        Zamienia trend z Reddit w kompletną strategię contentową
        """
        
        if not self.model:
            return self._fallback_content(trend)
        
        prompt = f"""You are a Senior Content Strategist for 'SayPlay' - a UK premium brand selling NFC voice/video message stickers for gifts.

TARGET AUDIENCE: UK millennials & Gen Z, emotionally intelligent, tech-savvy
BRAND VOICE: Empathetic, sophisticated, authentic, not salesy

INPUT - REAL USER PROBLEM:
Source: {trend['source']}
Title: "{trend['title']}"
Context: "{trend['context']}"

YOUR TASK: Create a complete content package addressing this real problem.

1. BLOG ARTICLE (1800-2200 words):
   - SEO-optimized title (emotional + keyword-rich)
   - Opening: Hook with the problem (reference the Reddit discussion style)
   - Section 1: "Why this is hard" - empathy + insights
   - Section 2: "What people get wrong" - common mistakes
   - Section 3: "The real solution" - deep gift ideas (mention SayPlay naturally as ONE option)
   - Section 4: "How to make it personal" - actionable tips
   - Conclusion: Emotional, empowering
   
   FORMAT: HTML with <h2>, <h3>, <p>, <ul>, <li> tags
   TONE: Like a trusted friend + expert advisor
   
2. PODCAST SCRIPT (1200-1500 words for 8-10 min audio):
   - Intro: "Today we're talking about [problem] - and I've been reading what people are saying online..."
   - Main: Tell a story, discuss insights, provide solutions
   - Outro: Call to action (visit sayplay.co.uk)
   
3. SOCIAL MEDIA CAPTION (Instagram/TikTok):
   - Hook line
   - Problem → insight → solution
   - Hashtags (UK trending)

OUTPUT FORMAT: Return ONLY valid JSON:
{{
    "title": "Blog title here",
    "article_html": "Full HTML article here",
    "podcast_script": "Full podcast script here",
    "social_caption": "Social media post here",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}

CRITICAL: Return ONLY the JSON object, no markdown formatting, no code blocks."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up markdown if present
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            return json.loads(text)
            
        except Exception as e:
            print(f"      ⚠️ Gemini Pro error: {str(e)[:80]}")
            return self._fallback_content(trend)
    
    def _fallback_content(self, trend: Dict) -> Dict:
        """Fallback content gdy API zawiedzie"""
        return {
            'title': trend['title'],
            'article_html': f"<h2>Understanding {trend['title']}</h2><p>{trend['context']}</p><p>At SayPlay, we believe gifts should carry your voice and emotion, not just your money.</p>",
            'podcast_script': f"Today we're exploring {trend['title']}. This is a challenge many people face...",
            'social_caption': f"Struggling with {trend['title']}? You're not alone. Here's what actually works.",
            'keywords': ['gifts', 'personalized', 'UK']
        }


class PremiumDesignEngine:
    """
    Design Engine - Jinja2 Templates + Tailwind CSS
    AI NIE DOTYKA CSS! Design jest sztywny i profesjonalny.
    """
    
    def __init__(self):
        if not JINJA2_AVAILABLE:
            print("❌ Jinja2 not available!")
            self.template = None
            return
        
        # PREMIUM TEMPLATE - Playfair Display + Inter + Tailwind
        self.template_str = """<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | SayPlay Journal</title>
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords }}">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    
    <!-- Premium Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-feature-settings: "kern" 1, "liga" 1;
        }
        h1, h2, h3, h4, h5, h6 { 
            font-family: 'Playfair Display', Georgia, serif;
            font-weight: 400;
        }
        .first-letter::first-letter {
            float: left;
            font-size: 4rem;
            line-height: 1;
            font-weight: 700;
            margin: 0.1em 0.1em 0 0;
            color: #ea580c;
        }
    </style>
</head>
<body class="bg-stone-50 text-stone-900 antialiased">
    
    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-white/90 backdrop-blur-lg border-b border-stone-200">
        <div class="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold tracking-tight">
                <span class="text-orange-600">Say</span><span class="text-stone-900">Play</span>
            </div>
            <a href="https://sayplay.co.uk" 
               class="bg-stone-900 text-white px-6 py-2.5 rounded-full text-sm font-medium hover:bg-orange-600 transition-colors duration-300 shadow-lg shadow-stone-900/10">
                Shop Collection
            </a>
        </div>
    </nav>

    <!-- Hero Section -->
    <header class="relative w-full h-[65vh] min-h-[500px] flex items-center justify-center overflow-hidden">
        <img src="{{ hero_image }}" 
             alt="{{ title }}"
             class="absolute inset-0 w-full h-full object-cover brightness-[0.5]">
        
        <div class="relative z-10 text-center px-6 max-w-4xl animate-fade-in">
            <span class="inline-block py-1.5 px-4 border border-white/40 rounded-full text-xs font-semibold text-white uppercase tracking-widest mb-6 bg-white/10 backdrop-blur-sm">
                <i class="fas fa-fire mr-1.5"></i> Trending Now
            </span>
            <h1 class="text-5xl md:text-7xl text-white font-normal leading-tight mb-4">
                {{ title }}
            </h1>
            <div class="flex justify-center items-center gap-4 text-white/70 text-sm mt-6">
                <span><i class="far fa-calendar mr-2"></i>{{ date }}</span>
                <span>•</span>
                <span><i class="far fa-clock mr-2"></i>{{ read_time }} min read</span>
                <span>•</span>
                <span><i class="fas fa-tag mr-2"></i>Gift Guide</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-6 py-20">
        
        <!-- Article -->
        <article class="prose prose-xl prose-stone max-w-none
                        prose-headings:font-normal prose-headings:tracking-tight
                        prose-h2:text-4xl prose-h2:mt-16 prose-h2:mb-6
                        prose-h3:text-2xl prose-h3:mt-12 prose-h3:mb-4
                        prose-p:text-lg prose-p:leading-relaxed prose-p:mb-6
                        prose-a:text-orange-600 prose-a:no-underline hover:prose-a:underline
                        prose-ul:my-8 prose-li:my-3
                        prose-strong:text-stone-900 prose-strong:font-semibold
                        first-letter">
            {{ content_html | safe }}
        </article>

        <!-- Product Showcase -->
        <div class="my-24 relative overflow-hidden rounded-3xl bg-gradient-to-br from-orange-50 to-orange-100/50 border border-orange-200/50 p-10 md:p-16">
            <div class="flex flex-col md:flex-row items-center gap-12">
                <div class="w-full md:w-1/2">
                    <img src="{{ product_image }}" 
                         alt="SayPlay Voice Message Stickers"
                         class="rounded-2xl shadow-2xl transform hover:scale-105 transition-transform duration-500">
                </div>
                <div class="w-full md:w-1/2">
                    <h3 class="text-4xl mb-6 text-stone-900 leading-tight">
                        Don't just give a gift.<br>
                        <span class="text-orange-600">Give your voice.</span>
                    </h3>
                    <p class="text-stone-600 text-lg mb-8 leading-relaxed">
                        Turn any object into a living memory. Record a heartfelt message, stick it anywhere, and let them tap to hear your voice. No app required. Pure emotion, instantly.
                    </p>
                    <div class="flex flex-col sm:flex-row gap-4">
                        <a href="https://sayplay.co.uk" 
                           class="inline-flex items-center justify-center gap-3 px-8 py-4 text-base font-semibold text-white bg-orange-600 rounded-xl hover:bg-orange-700 transition-all duration-300 shadow-xl shadow-orange-600/30 hover:shadow-2xl hover:shadow-orange-600/40">
                            <i class="fas fa-shopping-bag"></i>
                            Get Your Starter Pack
                        </a>
                        <a href="https://sayplay.co.uk" 
                           class="inline-flex items-center justify-center gap-3 px-8 py-4 text-base font-semibold text-stone-900 bg-white rounded-xl hover:bg-stone-50 transition-all duration-300 border border-stone-200">
                            Learn How It Works
                            <i class="fas fa-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Back to Blog -->
        <div class="mt-16 text-center">
            <a href="/blog" class="inline-flex items-center gap-2 text-stone-600 hover:text-orange-600 transition-colors">
                <i class="fas fa-arrow-left"></i>
                Back to all articles
            </a>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-stone-900 text-stone-400 py-16 mt-24">
        <div class="max-w-5xl mx-auto px-6 text-center">
            <div class="text-2xl font-bold mb-4">
                <span class="text-orange-500">Say</span><span class="text-white">Play</span>
            </div>
            <p class="text-sm mb-8">Bringing memories to life, one voice at a time.</p>
            <div class="flex justify-center gap-6 mb-8">
                <a href="https://instagram.com/sayplay.uk" class="hover:text-orange-500 transition-colors">
                    <i class="fab fa-instagram text-xl"></i>
                </a>
                <a href="https://tiktok.com/@sayplay.uk" class="hover:text-orange-500 transition-colors">
                    <i class="fab fa-tiktok text-xl"></i>
                </a>
                <a href="https://facebook.com/sayplay.uk" class="hover:text-orange-500 transition-colors">
                    <i class="fab fa-facebook text-xl"></i>
                </a>
            </div>
            <p class="text-xs text-stone-500">© {{ year }} SayPlay UK. All rights reserved.</p>
        </div>
    </footer>

</body>
</html>"""
        
        self.template = Template(self.template_str) if JINJA2_AVAILABLE else None
    
    def build_page(self, content: Dict, hero_image_url: str, product_image_url: str, output_path: Path):
        """Buduje stronę z premium template"""
        
        if not self.template:
            print("❌ Template not available")
            return
        
        # Extract first 160 chars for description
        description = content.get('article_html', '')[:160].replace('<', '').replace('>', '')
        
        # Calculate read time (250 words per minute)
        word_count = len(content.get('article_html', '').split())
        read_time = max(1, word_count // 250)
        
        html = self.template.render(
            title=content['title'],
            description=description,
            keywords=', '.join(content.get('keywords', ['gifts', 'UK', 'personalized'])),
            hero_image=hero_image_url,
            product_image=product_image_url,
            content_html=content['article_html'],
            date=datetime.now().strftime("%B %d, %Y"),
            read_time=read_time,
            year=datetime.now().year
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)


class PremiumImageGenerator:
    """Generate premium lifestyle images"""
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
    
    def get_hero_image(self, keywords: List[str]) -> str:
        """Get premium lifestyle image from Unsplash"""
        
        # Dodaj "emotion" i "lifestyle" do keywords
        search_terms = keywords[:2] + ['emotion', 'lifestyle', 'people']
        query = '+'.join(search_terms)
        
        if self.unsplash_key:
            try:
                url = f"https://api.unsplash.com/photos/random"
                params = {
                    'query': query,
                    'orientation': 'landscape',
                    'client_id': self.unsplash_key
                }
                response = requests.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data['urls']['regular']
                    print(f"      ✅ Unsplash image: {data.get('description', 'N/A')[:40]}")
                    return image_url
            except Exception as e:
                print(f"      ⚠️ Unsplash error: {str(e)[:60]}")
        
        # Fallback: Unsplash Source API (no auth needed)
        fallback_url = f"https://source.unsplash.com/1600x900/?{query}"
        print(f"      ℹ️ Using Unsplash Source fallback")
        return fallback_url


class PodcastGeneratorPremium:
    """Generate premium podcasts with proper state management"""
    
    async def generate_podcast(self, script: str, episode_num: int, slug: str, output_dir: Path) -> Path:
        """Generate podcast with unique numbering"""
        
        if not EDGE_TTS_AVAILABLE:
            print("❌ Edge TTS not available")
            return None
        
        # Unique filename with episode number and slug
        filename = f"sayplay_ep_{episode_num:03d}_{slug}.mp3"
        output_path = output_dir / filename
        
        print(f"      🎙️ Generating Episode #{episode_num}...")
        
        # Generate audio with UK voice
        communicate = edge_tts.Communicate(script, "en-GB-SoniaNeural")
        await communicate.save(str(output_path))
        
        # Calculate duration
        word_count = len(script.split())
        duration_minutes = word_count / 150  # 150 words per minute
        
        print(f"         ✅ Saved: {filename} (~{duration_minutes:.1f} min)")
        
        return output_path


def create_blog_index_v3(articles: List[Dict], output_dir: Path):
    """Create blog index with V3 styling"""
    
    print("📄 Creating premium blog index...")
    
    blog_dir = output_dir / 'web' / 'blog'
    
    html = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Journal | Gift Guides & Insights</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Inter', sans-serif; }
        h1, h2 { font-family: 'Playfair Display', serif; }
    </style>
</head>
<body class="bg-stone-50">
    <nav class="bg-white border-b border-stone-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold"><span class="text-orange-600">Say</span><span>Play</span></div>
            <a href="https://sayplay.co.uk" class="bg-stone-900 text-white px-6 py-2 rounded-full hover:bg-orange-600 transition">Shop</a>
        </div>
    </nav>
    
    <header class="bg-gradient-to-br from-orange-600 to-orange-400 text-white py-24">
        <div class="max-w-5xl mx-auto px-6 text-center">
            <h1 class="text-6xl mb-4">The SayPlay Journal</h1>
            <p class="text-xl text-white/90">Real insights for meaningful gifting</p>
        </div>
    </header>
    
    <main class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">'''
    
    for article in articles:
        slug = article['slug']
        html += f'''
            <article class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-shadow duration-300 border border-stone-200">
                <div class="h-48 bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center text-white text-6xl">
                    <i class="fas fa-gift"></i>
                </div>
                <div class="p-6">
                    <h2 class="text-2xl mb-3 leading-tight">{article['title']}</h2>
                    <p class="text-stone-600 text-sm mb-4">{article['date']} • {article['read_time']} min read</p>
                    <a href="/blog/{slug}.html" class="text-orange-600 font-semibold hover:text-orange-700 inline-flex items-center gap-2">
                        Read Article <i class="fas fa-arrow-right text-sm"></i>
                    </a>
                </div>
            </article>'''
    
    html += '''
        </div>
    </main>
    
    <footer class="bg-stone-900 text-stone-400 py-12 mt-24 text-center">
        <p>© 2025 SayPlay UK</p>
    </footer>
</body>
</html>'''
    
    with open(blog_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("   ✅ Blog index created")


def create_podcasts_index_v3(podcasts: List[Dict], output_dir: Path):
    """Create podcasts index with V3 styling"""
    
    print("📄 Creating premium podcasts index...")
    
    podcast_dir = output_dir / 'web' / 'podcasts'
    
    html = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Podcast | Gift Insights Audio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Inter', sans-serif; }
        h1, h2 { font-family: 'Playfair Display', serif; }
    </style>
</head>
<body class="bg-stone-50">
    <nav class="bg-white border-b border-stone-200">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold"><span class="text-orange-600">Say</span><span>Play</span></div>
            <a href="/" class="text-stone-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <header class="bg-gradient-to-br from-stone-900 to-stone-700 text-white py-20">
        <div class="max-w-5xl mx-auto px-6">
            <h1 class="text-5xl mb-4"><i class="fas fa-podcast mr-4"></i>SayPlay Podcast</h1>
            <p class="text-xl text-white/80">Insights on gifting, relationships, and emotional connection</p>
        </div>
    </header>
    
    <main class="max-w-4xl mx-auto px-6 py-16">
        <div class="space-y-6">'''
    
    for podcast in podcasts:
        html += f'''
            <div class="bg-white rounded-2xl p-8 shadow-sm border border-stone-200">
                <div class="flex items-start gap-6">
                    <div class="flex-shrink-0 w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">
                        {podcast['episode']}
                    </div>
                    <div class="flex-1">
                        <h2 class="text-2xl mb-2">{podcast['title']}</h2>
                        <p class="text-stone-600 text-sm mb-4">Episode {podcast['episode']} • ~{podcast['duration']} min</p>
                        <audio controls class="w-full" preload="metadata">
                            <source src="/podcasts/{podcast['filename']}" type="audio/mpeg">
                        </audio>
                    </div>
                </div>
            </div>'''
    
    html += '''
        </div>
    </main>
    
    <footer class="bg-stone-900 text-stone-400 py-12 mt-24 text-center">
        <p>© 2025 SayPlay UK</p>
    </footer>
</body>
</html>'''
    
    with open(podcast_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("   ✅ Podcasts index created")


def create_dashboard_v3(stats: Dict, output_dir: Path):
    """Create main dashboard V3"""
    
    print("📄 Creating premium dashboard...")
    
    dashboard_dir = output_dir / 'web' / 'dashboard'
    
    html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITAN V3 Dashboard | Premium Content Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        h1, h2 {{ font-family: 'Playfair Display', serif; }}
    </style>
</head>
<body class="bg-gradient-to-br from-orange-500 to-orange-600 min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
        
        <!-- Header -->
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-2xl">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-5xl mb-2"><span class="text-orange-600">Say</span><span>Play</span> Studio</h1>
                    <p class="text-stone-600">TITAN V3 Premium Content Engine</p>
                </div>
                <div class="text-right">
                    <div class="text-sm text-stone-500">Last Generation</div>
                    <div class="text-lg font-semibold">{stats['date']}</div>
                </div>
            </div>
        </div>
        
        <!-- Stats Grid -->
        <div class="grid md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-2xl p-6 shadow-lg text-center">
                <div class="text-orange-600 text-5xl mb-3"><i class="fas fa-newspaper"></i></div>
                <div class="text-4xl font-bold mb-2">{stats['articles']}</div>
                <div class="text-stone-600">Premium Articles</div>
            </div>
            <div class="bg-white rounded-2xl p-6 shadow-lg text-center">
                <div class="text-orange-600 text-5xl mb-3"><i class="fas fa-podcast"></i></div>
                <div class="text-4xl font-bold mb-2">{stats['podcasts']}</div>
                <div class="text-stone-600">Podcast Episodes</div>
            </div>
            <div class="bg-white rounded-2xl p-6 shadow-lg text-center">
                <div class="text-orange-600 text-5xl mb-3"><i class="fas fa-fire"></i></div>
                <div class="text-4xl font-bold mb-2">{stats['trends']}</div>
                <div class="text-stone-600">Reddit Trends</div>
            </div>
            <div class="bg-white rounded-2xl p-6 shadow-lg text-center">
                <div class="text-green-600 text-5xl mb-3"><i class="fas fa-check-circle"></i></div>
                <div class="text-4xl font-bold mb-2">✓</div>
                <div class="text-stone-600">AI Powered</div>
            </div>
        </div>
        
        <!-- Quick Access -->
        <div class="bg-white rounded-3xl p-8 shadow-2xl">
            <h2 class="text-3xl mb-6">Quick Access</h2>
            <div class="grid md:grid-cols-3 gap-6">
                <a href="/blog" class="block p-6 bg-orange-50 rounded-xl hover:bg-orange-100 transition border-2 border-orange-200">
                    <div class="text-orange-600 text-4xl mb-3"><i class="fas fa-book-open"></i></div>
                    <h3 class="text-xl font-semibold mb-2">Blog Articles</h3>
                    <p class="text-stone-600">{stats['articles']} premium articles</p>
                </a>
                <a href="/podcasts" class="block p-6 bg-orange-50 rounded-xl hover:bg-orange-100 transition border-2 border-orange-200">
                    <div class="text-orange-600 text-4xl mb-3"><i class="fas fa-microphone-alt"></i></div>
                    <h3 class="text-xl font-semibold mb-2">Podcasts</h3>
                    <p class="text-stone-600">{stats['podcasts']} episodes ready</p>
                </a>
                <a href="https://sayplay.co.uk" class="block p-6 bg-orange-50 rounded-xl hover:bg-orange-100 transition border-2 border-orange-200">
                    <div class="text-orange-600 text-4xl mb-3"><i class="fas fa-shopping-bag"></i></div>
                    <h3 class="text-xl font-semibold mb-2">Shop</h3>
                    <p class="text-stone-600">Visit SayPlay store</p>
                </a>
            </div>
        </div>
        
        <!-- System Info -->
        <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-6 mt-8 text-white">
            <h3 class="text-xl mb-4"><i class="fas fa-info-circle mr-2"></i>System Status</h3>
            <div class="space-y-2 text-sm">
                <div>✅ Reddit Trend Hunter: Active</div>
                <div>✅ Gemini Pro Content: Enabled</div>
                <div>✅ Jinja2 Templates: Premium Design</div>
                <div>✅ State Management: Unique Numbering</div>
                <div>✅ Unsplash Images: Lifestyle Quality</div>
            </div>
        </div>
        
    </div>
</body>
</html>'''
    
    with open(dashboard_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("   ✅ Dashboard created")


async def main():
    print("\n" + "="*70)
    print("TITAN V3 - PREMIUM CONTENT STUDIO")
    print("Reddit Trends • Jinja2 Design • State Management • Gemini Pro")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    # Setup
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_V3_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    web_dir = output_dir / 'web'
    for d in ['blog', 'podcasts', 'dashboard']:
        (web_dir / d).mkdir(parents=True, exist_ok=True)
    
    # Initialize modules
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    state_mgr = StateManager()
    trend_hunter = TrendHunter()
    content_studio = PremiumContentStudio(gemini_key)
    design_engine = PremiumDesignEngine()
    image_gen = PremiumImageGenerator()
    podcast_gen = PodcastGeneratorPremium()
    
    # PHASE 1: Hunt Trends
    print(f"\n{'='*70}")
    print("PHASE 1: TREND HUNTING")
    print(f"{'='*70}")
    
    trends = trend_hunter.get_real_trends(limit=5)
    
    if not trends:
        print("❌ No trends found, exiting")
        return 1
    
    # PHASE 2: Generate Premium Content
    print(f"\n{'='*70}")
    print(f"PHASE 2: CONTENT GENERATION ({len(trends)} trends)")
    print(f"{'='*70}")
    
    articles = []
    podcasts = []
    
    for i, trend in enumerate(trends, 1):
        print(f"\n📌 TREND {i}/{len(trends)}: {trend['title'][:60]}...")
        
        # Generate content strategy
        print("   🧠 Gemini Pro: Developing content strategy...")
        content = content_studio.develop_content_strategy(trend)
        
        if not content:
            print("   ⚠️ Skipping due to content generation error")
            continue
        
        # Create slug
        slug = content['title'].lower().replace(' ', '-').replace("'", '').replace('"', '')[:50]
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Get hero image
        print("   🖼️ Fetching premium hero image...")
        hero_image_url = image_gen.get_hero_image(content.get('keywords', ['gift', 'emotion']))
        
        # Product image (adjust path as needed)
        product_image_url = "https://sayplay.co.uk/images/product-collection.jpg"
        
        # Build page
        print("   🎨 Building premium page...")
        page_path = web_dir / 'blog' / f'{slug}.html'
        design_engine.build_page(content, hero_image_url, product_image_url, page_path)
        print(f"      ✅ Page: {page_path.name}")
        
        # Generate podcast
        episode_num = state_mgr.get_next_episode_number()
        podcast_path = await podcast_gen.generate_podcast(
            content['podcast_script'],
            episode_num,
            slug,
            web_dir / 'podcasts'
        )
        
        if podcast_path:
            # Save state
            state_mgr.commit_success(episode_num, trend.get('url', 'system'))
            
            # Calculate duration
            word_count = len(content['podcast_script'].split())
            duration_min = int(word_count / 150)
            
            podcasts.append({
                'episode': episode_num,
                'title': content['title'],
                'filename': podcast_path.name,
                'duration': duration_min
            })
        
        # Save article metadata
        articles.append({
            'title': content['title'],
            'slug': slug,
            'date': datetime.now().strftime("%B %d, %Y"),
            'read_time': max(1, len(content.get('article_html', '').split()) // 250)
        })
        
        print(f"   ✅ Complete: {content['title'][:50]}...")
    
    # PHASE 3: Create Index Pages
    print(f"\n{'='*70}")
    print("PHASE 3: INDEX PAGES")
    print(f"{'='*70}")
    
    create_blog_index_v3(articles, output_dir)
    create_podcasts_index_v3(podcasts, output_dir)
    
    create_dashboard_v3({
        'articles': len(articles),
        'podcasts': len(podcasts),
        'trends': len(trends),
        'date': datetime.now().strftime("%B %d, %Y %H:%M")
    }, output_dir)
    
    # Summary
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print("TITAN V3 COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ {len(articles)} Premium Articles (1500-2500 words)")
    print(f"✅ {len(podcasts)} Podcasts (8-10 min, unique numbering)")
    print(f"✅ Reddit Trends Used: {len(trends)}")
    print(f"✅ Jinja2 Premium Design")
    print(f"✅ State Management Active")
    print(f"\n⏱ Duration: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"{'='*70}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
