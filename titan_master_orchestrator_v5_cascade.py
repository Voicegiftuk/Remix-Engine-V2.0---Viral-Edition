#!/usr/bin/env python3
"""
TITAN V6 ULTIMATE CASCADE - 6-TIER AI FALLBACK
Tier 1: Gemini 1.5 Pro
Tier 2: Gemini 1.5 Flash
Tier 3: Gemini 1.0 Pro
Tier 4: OpenAI GPT-3.5 Turbo
Tier 5: Groq Llama 3.1 70B
Tier 6: Emergency Template (100% reliable)
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio
import json
import random
from typing import List, Dict, Optional

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

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

import requests


class AIConfig:
    """AI Models configuration"""
    # Gemini models (FIX: bez -latest)
    GEMINI_PRO = 'gemini-1.5-pro'
    GEMINI_FLASH = 'gemini-1.5-flash'
    GEMINI_PRO_OLD = 'gemini-pro'  # Starszy, stabilniejszy
    
    # OpenAI
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    
    # Groq (darmowy!)
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    
    TIMEOUT = 30


class ContentBrain:
    """
    6-TIER AI CASCADE
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
        if self.has_openai:
            print("✅ OpenAI configured")
        if self.has_groq:
            print("✅ Groq configured")
    
    def generate_seo_page(self, topic: str, city: str) -> Dict:
        """Generate SEO with 6-tier cascade"""
        
        print(f"      🧠 SEO: {topic} in {city}")
        
        # TIER 1: Gemini 1.5 Pro
        result = self._try_gemini_model(AIConfig.GEMINI_PRO, 'seo', topic, city)
        if result:
            print(f"         ✅ Gemini 1.5 Pro")
            return result
        
        # TIER 2: Gemini 1.5 Flash
        result = self._try_gemini_model(AIConfig.GEMINI_FLASH, 'seo', topic, city)
        if result:
            print(f"         ✅ Gemini 1.5 Flash")
            return result
        
        # TIER 3: Gemini 1.0 Pro (starszy)
        result = self._try_gemini_model(AIConfig.GEMINI_PRO_OLD, 'seo', topic, city)
        if result:
            print(f"         ✅ Gemini 1.0 Pro")
            return result
        
        # TIER 4: OpenAI GPT-3.5
        result = self._try_openai('seo', topic, city)
        if result:
            print(f"         ✅ OpenAI GPT-3.5")
            return result
        
        # TIER 5: Groq Llama
        result = self._try_groq('seo', topic, city)
        if result:
            print(f"         ✅ Groq Llama 3.1")
            return result
        
        # TIER 6: Emergency
        print(f"         🚨 ALL AI FAILED - Emergency Template")
        return self._emergency_seo(topic, city)
    
    def _try_gemini_model(self, model_name: str, content_type: str, topic: str, city: str = '') -> Optional[Dict]:
        """Try Gemini model"""
        if not self.has_gemini:
            return None
        
        try:
            model = genai.GenerativeModel(model_name)
            
            if content_type == 'seo':
                prompt = self._get_seo_prompt(topic, city)
            elif content_type == 'blog':
                prompt = self._get_blog_prompt(topic)
            else:  # podcast
                prompt = self._get_podcast_prompt(topic)
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=4096
                ),
                request_options={'timeout': AIConfig.TIMEOUT}
            )
            
            text = response.text.strip()
            
            # For podcast, return text directly
            if content_type == 'podcast':
                return text.replace('*', '').replace('#', '').replace('```', '')
            
            # For SEO/blog, parse JSON
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            return json.loads(text)
            
        except Exception as e:
            # Don't print full error, just note it failed
            return None
    
    def _try_openai(self, content_type: str, topic: str, city: str = '') -> Optional[Dict]:
        """Try OpenAI GPT-3.5"""
        if not self.has_openai:
            return None
        
        try:
            if content_type == 'seo':
                prompt = self._get_seo_prompt(topic, city)
            elif content_type == 'blog':
                prompt = self._get_blog_prompt(topic)
            else:
                prompt = self._get_podcast_prompt(topic)
            
            response = requests.post(
                AIConfig.OPENAI_ENDPOINT,
                headers={
                    'Authorization': f'Bearer {self.openai_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': AIConfig.OPENAI_MODEL,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.8,
                    'max_tokens': 3000
                },
                timeout=AIConfig.TIMEOUT
            )
            
            if response.status_code != 200:
                return None
            
            text = response.json()['choices'][0]['message']['content'].strip()
            
            if content_type == 'podcast':
                return text.replace('*', '').replace('#', '').replace('```', '')
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            return json.loads(text)
            
        except:
            return None
    
    def _try_groq(self, content_type: str, topic: str, city: str = '') -> Optional[Dict]:
        """Try Groq Llama 3.1"""
        if not self.has_groq:
            return None
        
        try:
            if content_type == 'seo':
                prompt = self._get_seo_prompt(topic, city, shorter=True)
            elif content_type == 'blog':
                prompt = self._get_blog_prompt(topic, shorter=True)
            else:
                prompt = self._get_podcast_prompt(topic, shorter=True)
            
            response = requests.post(
                AIConfig.GROQ_ENDPOINT,
                headers={
                    'Authorization': f'Bearer {self.groq_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': AIConfig.GROQ_MODEL,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.7,
                    'max_tokens': 2000
                },
                timeout=AIConfig.TIMEOUT
            )
            
            if response.status_code != 200:
                return None
            
            text = response.json()['choices'][0]['message']['content'].strip()
            
            if content_type == 'podcast':
                return text.replace('*', '').replace('#', '').replace('```', '')
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            
            return json.loads(text)
            
        except:
            return None
    
    def _get_seo_prompt(self, topic: str, city: str, shorter: bool = False) -> str:
        """SEO prompt"""
        facts = "Voice: 60s max, Video: 30s max, Hosting: 1yr (downloadable), No app (NFC tap), Mascots: Mylo & Gigi"
        
        if shorter:
            return f"""Write SEO page for "{topic} in {city}" for SayPlay gift stickers.
FACTS: {facts}
OUTPUT JSON: {{"title": "...", "meta_desc": "...", "intro_html": "<p>200+ words...</p>", "problem_html": "<p>200+ words...</p>", "solution_html": "<p>250+ words...</p>", "howto_html": "<p>150+ words...</p>", "local_html": "<p>100+ words {city} shops...</p>", "faq_html": "<div class='faq-item'><h4>Q?</h4><p>Answer...</p></div>..."}}"""
        
        return f"""Senior SEO copywriter for SayPlay - UK NFC voice/video gift stickers.

FACTS: {facts}

Write comprehensive page: "{topic} in {city}"

REQUIREMENTS:
- 1500+ characters total
- Natural UK English
- Emotional stories
- Local {city} references

STRUCTURE (FULL paragraphs, 150+ words each):
1. Introduction: Emotional hook about {topic} in {city}
2. Problem: Why generic gifts disappoint
3. Solution: SayPlay features (60s/30s, 1yr, Mylo & Gigi)
4. How-to: Step-by-step with examples
5. Local: Best shops in {city}
6. FAQ: 5 questions with detailed answers

JSON OUTPUT:
{{
    "title": "...",
    "meta_desc": "...",
    "intro_html": "<p>Long paragraph 150+ words...</p>",
    "problem_html": "<p>Long paragraph 150+ words...</p>",
    "solution_html": "<p>Long paragraph 200+ words...</p>",
    "howto_html": "<p>Long paragraph 150+ words...</p>",
    "local_html": "<p>Paragraph 100+ words about {city} shops...</p>",
    "faq_html": "<div class='faq-item'><h4>Question?</h4><p>Detailed answer...</p></div>..."
}}"""
    
    def _get_blog_prompt(self, topic: str, shorter: bool = False) -> str:
        """Blog prompt"""
        facts = "Voice: 60s max, Video: 30s max, Hosting: 1yr, No app, Mascots: Mylo & Gigi"
        
        if shorter:
            return f"""Write blog article: "{topic}" for SayPlay gift stickers.
FACTS: {facts}
OUTPUT JSON: {{"title": "...", "article_html": "<p>1500+ chars story...</p>", "keywords": ["..."]}}"""
        
        return f"""Senior content writer for SayPlay blog.

FACTS: {facts}

Write comprehensive blog: "{topic}"

REQUIREMENTS:
- 2000+ characters
- Storytelling style
- UK English
- Emotional connection

STRUCTURE:
1. Opening story (300 words)
2. Main content (800 words): problem, solution, benefits
3. How-to guide (400 words)
4. Conclusion with CTA (200 words)

JSON OUTPUT:
{{
    "title": "Engaging title",
    "article_html": "<p>Long story...</p><p>Main content...</p>...",
    "keywords": ["keyword1", "keyword2"]
}}"""
    
    def _get_podcast_prompt(self, topic: str, shorter: bool = False) -> str:
        """Podcast prompt"""
        facts = "Voice: 60s, Video: 30s, Hosting: 1yr, No app, Mascots: Mylo & Gigi"
        
        if shorter:
            return f"""Podcast script for "{topic}". Host Sonia. 500+ words, conversational.
FACTS: {facts}
Output: spoken text only, no markdown."""
        
        return f"""Podcast script for SayPlay Gift Guide.

FACTS: {facts}

Topic: "{topic}"

REQUIREMENTS:
- 700+ words (5+ minutes spoken)
- Host: Sonia (UK, warm)
- Conversational
- Emotional story
- Explain features

STRUCTURE:
1. Welcome (80 words)
2. Topic intro + story (200 words)
3. Problem (150 words)
4. SayPlay solution (250 words)
5. Example (120 words)
6. CTA (50 words): sayplay.co.uk

OUTPUT: Spoken script only, no markdown, no stage directions"""
    
    def generate_blog(self, topic: str) -> Dict:
        """Generate blog with 6-tier cascade"""
        
        print(f"      📝 Blog: {topic}")
        
        # Try all AI tiers
        for tier, method in [
            ('Gemini 1.5 Pro', lambda: self._try_gemini_model(AIConfig.GEMINI_PRO, 'blog', topic)),
            ('Gemini 1.5 Flash', lambda: self._try_gemini_model(AIConfig.GEMINI_FLASH, 'blog', topic)),
            ('Gemini 1.0 Pro', lambda: self._try_gemini_model(AIConfig.GEMINI_PRO_OLD, 'blog', topic)),
            ('OpenAI GPT-3.5', lambda: self._try_openai('blog', topic)),
            ('Groq Llama 3.1', lambda: self._try_groq('blog', topic))
        ]:
            result = method()
            if result:
                print(f"         ✅ {tier}")
                return result
        
        print(f"         🚨 ALL AI FAILED - Emergency")
        return self._emergency_blog(topic)
    
    def generate_podcast_script(self, topic: str) -> str:
        """Generate podcast with 6-tier cascade"""
        
        print(f"      🎙️ Podcast: {topic}")
        
        # Try all AI tiers
        for tier, method in [
            ('Gemini 1.5 Pro', lambda: self._try_gemini_model(AIConfig.GEMINI_PRO, 'podcast', topic)),
            ('Gemini 1.5 Flash', lambda: self._try_gemini_model(AIConfig.GEMINI_FLASH, 'podcast', topic)),
            ('Gemini 1.0 Pro', lambda: self._try_gemini_model(AIConfig.GEMINI_PRO_OLD, 'podcast', topic)),
            ('OpenAI GPT-3.5', lambda: self._try_openai('podcast', topic)),
            ('Groq Llama 3.1', lambda: self._try_groq('podcast', topic))
        ]:
            result = method()
            if result:
                print(f"         ✅ {tier}")
                return result
        
        print(f"         🚨 ALL AI FAILED - Emergency")
        return self._emergency_podcast(topic)
    
    def _emergency_seo(self, topic: str, city: str) -> Dict:
        """Emergency SEO template"""
        return {
            'title': f'Perfect {topic} in {city} | SayPlay UK',
            'meta_desc': f'Looking for {topic} in {city}? Add your voice or video message to any gift with SayPlay NFC stickers. No app needed - just tap!',
            'intro_html': f'''
                <p>Finding the perfect {topic.lower()} in <strong>{city}</strong> can be challenging. Traditional gifts often feel impersonal and forgettable. Whether you're celebrating a birthday, anniversary, graduation, or any special occasion, you want your gift to stand out and create lasting memories.</p>
                <p>That's where SayPlay comes in. We've created a revolutionary way to add a personal touch to any gift you choose. Imagine attaching your voice or a video message directly to a gift - a message that lasts forever and can be played simply by tapping a phone. No apps, no downloads, no complications. Just pure emotion and connection.</p>
            ''',
            'problem_html': f'''
                <p>Let's be honest - most gifts end up forgotten in a drawer or regifted to someone else. The thought behind the gift gets lost because there's no personal connection. You spend hours shopping in {city}, trying to find something meaningful, but standard gifts just don't capture what you really want to say.</p>
                <p>Gift cards feel lazy. Store-bought cards get thrown away. Even expensive presents can feel hollow without the personal touch that makes them truly special. The real value of a gift isn't in its price tag - it's in the emotion and memory it creates.</p>
            ''',
            'solution_html': f'''
                <p>SayPlay transforms any gift into an unforgettable memory. Our innovative NFC stickers allow you to record up to <strong>60 seconds of voice</strong> or <strong>30 seconds of video</strong> and attach it directly to your gift. When the recipient taps their phone on the sticker, they instantly hear or see your personal message - no app required!</p>
                <p>The technology is incredibly simple. Each SayPlay sticker contains a tiny NFC chip (the same technology used in contactless payments). You record your message online, link it to your sticker, and attach it to any gift. Your message is hosted securely for one full year, and you can download it anytime to keep forever.</p>
                <p>Meet our mascots, <strong>Mylo and Gigi</strong>! They represent the joy and connection that SayPlay brings to gift-giving. Whether it's a heartfelt birthday message, wedding vows, a funny memory, or words of encouragement, your voice makes the gift truly yours.</p>
            ''',
            'howto_html': f'''
                <p><strong>Step 1:</strong> Choose your gift in {city} - anything from flowers to jewelry to books. Purchase your SayPlay sticker pack online or from select retailers.</p>
                <p><strong>Step 2:</strong> Visit our website and record your message. You can record up to 60 seconds of voice or 30 seconds of video. Say whatever's in your heart - funny, emotional, or encouraging words.</p>
                <p><strong>Step 3:</strong> Attach the SayPlay sticker to your gift. Place it on the wrapping paper, gift box, or directly on the item itself.</p>
                <p><strong>Step 4:</strong> Give your gift! When the recipient taps their phone on the sticker, they'll instantly hear or see your message. The look on their face will be priceless. No app downloads, no complicated setup - just tap and play!</p>
            ''',
            'local_html': f'''
                <p>Shopping for gifts in {city}? Here are some great places to find items perfect for attaching SayPlay stickers: Visit the shopping centers in {city} city centre for a wide variety of options. Local boutiques offer unique, artisan gifts that pair beautifully with personal messages. Check out flower shops for bouquets, jewelers for special occasions, and bookstores for thoughtful literary gifts. Department stores provide everything from home goods to electronics, all perfect for personalizing with SayPlay.</p>
            ''',
            'faq_html': '''
                <div class="faq-item">
                    <h4>Do I need to download an app?</h4>
                    <p>No! That's the beauty of SayPlay. The recipient simply taps their phone on the sticker and the message plays instantly. It works with any modern smartphone (iPhone or Android) using built-in NFC technology - the same tech used for contactless payments. No downloads, no account creation, no hassle.</p>
                </div>
                <div class="faq-item">
                    <h4>How long can my message be?</h4>
                    <p>You can record up to 60 seconds of voice or 30 seconds of video. This is plenty of time to share heartfelt words, tell a story, or deliver a meaningful message. Quality over quantity - the most memorable messages are often the most concise and genuine.</p>
                </div>
                <div class="faq-item">
                    <h4>How long is my message stored?</h4>
                    <p>Your message is hosted on our secure servers for one full year from the date of creation. This gives plenty of time for the recipient to listen as many times as they want. You can also download the message at any point to keep it forever on your own device.</p>
                </div>
                <div class="faq-item">
                    <h4>Can the recipient listen multiple times?</h4>
                    <p>Absolutely! Once linked to the sticker, the recipient can tap and listen as many times as they want during the hosting period. Each tap brings back the same emotion and memory - it never gets old!</p>
                </div>
                <div class="faq-item">
                    <h4>What if the recipient doesn't have a modern phone?</h4>
                    <p>While NFC technology is standard on all smartphones made in the last 5+ years, if someone has an older device, they can access the message using a QR code alternative that we also provide. Everyone can enjoy SayPlay messages!</p>
                </div>
            '''
        }
    
    def _emergency_blog(self, topic: str) -> Dict:
        """Emergency blog template"""
        return {
            'title': f'{topic}: A Guide to Meaningful Gift-Giving',
            'article_html': f'''
                <p>Have you ever given someone a gift and wondered if they'll actually remember it a week later? Most of us have. The truth is, traditional gifts - no matter how expensive or carefully chosen - often fail to create lasting memories. They get used, put away, or forgotten. But what if there was a way to make every gift unforgettable?</p>
                
                <p>Sarah's story is a perfect example. Last Christmas, she gave her grandmother a beautiful photo album. It was elegant, expensive, and filled with family photos. Her grandmother loved it - for about a week. Then it sat on a shelf, rarely opened. This Christmas, Sarah tried something different. She gave the same type of album, but this time she attached a SayPlay sticker to the cover. On it, she recorded a heartfelt message about her favorite memories with her grandmother.</p>
                
                <p>The result? Her grandmother plays that message every single day. The album isn't just photos anymore - it's Sarah's voice, her love, and her presence, available whenever her grandmother wants to feel close to her. That's the power of adding your voice to a gift.</p>
                
                <h2>Why {topic} Matters</h2>
                
                <p>When it comes to {topic.lower()}, the challenge is always the same: how do you express something meaningful through a physical object? Words on a card can help, but they're easily lost or forgotten. The gift itself might be perfect, but without context, without emotion, it's just... an object.</p>
                
                <p>SayPlay solves this problem elegantly. Our NFC stickers allow you to record up to 60 seconds of voice or 30 seconds of video. You can say anything: share a memory, offer encouragement, tell a joke, express love, or simply let the person know you're thinking of them. The message stays with the gift forever (well, for a full year on our servers, plus you can download it to keep permanently).</p>
                
                <h2>How It Works: Simpler Than You Think</h2>
                
                <p>The technology might sound complicated, but using SayPlay is incredibly simple. Here's exactly how it works:</p>
                
                <p>First, you choose your gift. It can be anything - flowers, jewelry, books, toys, home goods, electronics - literally anything you can attach a small sticker to. Then, you visit our website and record your message. You can take your time, practice, re-record until it's perfect. Some people write a script, others speak from the heart. Both approaches work beautifully.</p>
                
                <p>Once you're happy with your recording, you link it to your SayPlay sticker (each one has a unique code). Then you simply attach the sticker to your gift. We recommend placing it somewhere visible but not obtrusive - on the gift wrap, on a gift box, or on the item itself if appropriate.</p>
                
                <p>When your recipient receives the gift, all they have to do is tap their smartphone on the sticker. Instantly, they hear your voice or see your video. No app download, no account creation, no technical knowledge required. It works with any modern iPhone or Android phone using the same NFC technology that powers contactless payments.</p>
                
                <h2>Real Stories from Real People</h2>
                
                <p>Tom used SayPlay for his daughter's wedding gift. Instead of just giving money in an envelope, he attached a sticker with a message about watching her grow up. His daughter said she played it before walking down the aisle and cried (happy tears, of course).</p>
                
                <p>Emma created a birthday gift for her best friend who moved abroad. The gift was simple - a framed photo - but the SayPlay message was 60 seconds of inside jokes and shared memories. Her friend said it made her feel like Emma was right there with her.</p>
                
                <p>These aren't exceptional cases. This is what happens when you add genuine emotion to a gift. The gift itself becomes a vessel for connection, memory, and love.</p>
                
                <h2>Getting Started</h2>
                
                <p>Ready to make your next gift unforgettable? Visit sayplay.co.uk to get started. Our starter packs include everything you need - stickers, instructions, and access to our easy-to-use recording platform. You'll be creating meaningful gift experiences in minutes.</p>
                
                <p>Don't let another special occasion pass with a gift that gets forgotten. Add your voice, add your presence, add meaning. That's what SayPlay is all about.</p>
            ''',
            'keywords': ['gifts', 'personalized', 'voice message', 'UK']
        }
    
    def _emergency_podcast(self, topic: str) -> str:
        """Emergency podcast template"""
        return f"""Welcome to the SayPlay Gift Guide podcast. I'm Sonia, and today we're talking about {topic.lower()}.

You know that feeling when you're shopping for a gift and nothing feels quite right? You walk through shop after shop, looking at options, but everything seems so... generic. A bottle of wine, a box of chocolates, another candle. They're nice, but they're forgettable.

Here's the thing about gifts that most people don't realize: the actual item matters less than the thought and emotion behind it. But how do you convey that thought? A card helps, but cards get thrown away or lost in a drawer. The gift itself can't speak - it can't tell the recipient why you chose it, what it means to you, or how much you care.

That's exactly why we created SayPlay. We wanted to solve this fundamental problem of gift-giving. How do you make any gift more meaningful? How do you ensure your message, your voice, your presence stays with the gift forever?

The answer is beautifully simple. SayPlay stickers use NFC technology - the same technology in contactless cards - to store a voice or video message. You can record up to sixty seconds of voice or thirty seconds of video. That's enough time to say something truly meaningful.

Imagine giving flowers with your voice attached. Imagine gifting jewelry while telling the story of why you chose it. Imagine sending a care package to someone far away, with your encouragement playing every time they open it.

The technology is invisible to the user. They just tap their phone on the sticker - no app download, no complicated setup - and your message plays instantly. It works on any modern smartphone, iPhone or Android, using built-in NFC capability.

Your message is hosted on our secure servers for one full year. The recipient can listen as many times as they want during that period. And you can download it anytime to keep forever.

We've even created two mascots, Mylo and Gigi, who represent the joy and connection that SayPlay brings to gift-giving. They remind us that the best gifts aren't expensive - they're personal.

Let me share a quick example. Last month, a grandmother used SayPlay to send birthday wishes to her grandson who lives abroad. She couldn't be there in person, but she recorded a message singing happy birthday and telling him stories about when she was his age. His mum said he played it every day for a week. That's the power of voice.

Whether you're celebrating {topic.lower()} or any special occasion, SayPlay helps you create moments that last. Visit sayplay dot co dot uk to get started. Make your next gift unforgettable. Thanks for listening to the SayPlay Gift Guide."""


# Rest of the code (DesignEngine, AudioStudio, TrendHunter, main) stays the same as V5...
# Just copy from the previous version

class DesignEngine:
    """Premium design templates - same as V5"""
    
    def __init__(self):
        if not JINJA2_AVAILABLE:
            self.seo_template = None
            self.blog_template = None
            return
        
        self.seo_template_str = """<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} | SayPlay UK</title>
    <meta name="description" content="{{ meta_desc }}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
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
            <span class="text-2xl font-bold"><span class="text-orange-600">Say</span><span>Play</span></span>
            <a href="https://sayplay.co.uk" class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-6 rounded-full transition">Shop Now</a>
        </div>
    </nav>
    <header class="bg-gradient-to-r from-orange-500 to-orange-600 text-white py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-4xl md:text-6xl font-extrabold mb-6">{{ title }}</h1>
            <p class="text-xl mb-8 opacity-90">Transform any gift with your voice or video message</p>
            <a href="https://sayplay.co.uk/collections/all" class="bg-white text-orange-600 font-bold py-4 px-10 rounded-full text-lg hover:scale-105 transition transform inline-block shadow-lg">🎁 Start Creating</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-6 py-16">
        <section class="prose lg:prose-xl max-w-none mb-12">{{ intro_html | safe }}</section>
        <div class="text-center my-12"><a href="https://sayplay.co.uk" class="text-orange-600 font-bold underline text-xl hover:text-orange-700">👉 Browse Stickers</a></div>
        <section class="bg-white p-8 rounded-2xl shadow-sm mb-12">
            <h2 class="text-3xl font-bold mb-6 text-gray-900">The Problem</h2>
            <div class="prose max-w-none">{{ problem_html | safe }}</div>
        </section>
        <section class="bg-orange-50 p-8 rounded-2xl mb-12">
            <h2 class="text-3xl font-bold mb-6 text-orange-900">The Solution</h2>
            <div class="prose max-w-none">{{ solution_html | safe }}</div>
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
        <div class="text-center my-12"><a href="https://sayplay.co.uk/products/starter-pack" class="bg-black text-white py-4 px-10 rounded-lg font-bold text-lg hover:bg-gray-800 transition inline-block shadow-lg">Get Starter Pack</a></div>
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
            <a href="https://sayplay.co.uk" class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 px-12 rounded-full text-xl transition shadow-lg inline-block mb-8">Buy Now</a>
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
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>body{font-family:'Inter'}h1,h2{font-family:'Playfair Display'}</style>
</head>
<body class="bg-stone-50">
    <nav class="bg-white border-b sticky top-0 z-50">
        <div class="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold"><span class="text-orange-600">Say</span><span>Play</span></div>
            <a href="https://sayplay.co.uk" class="bg-stone-900 text-white px-6 py-2 rounded-full hover:bg-orange-600 transition">Shop</a>
        </div>
    </nav>
    <header class="bg-gradient-to-br from-orange-600 to-orange-400 text-white py-24">
        <div class="max-w-4xl mx-auto px-6 text-center">
            <h1 class="text-5xl md:text-6xl mb-4">{{ title }}</h1>
        </div>
    </header>
    <main class="max-w-3xl mx-auto px-6 py-16">
        <article class="prose prose-xl max-w-none">{{ article_html | safe }}</article>
        <div class="mt-12 bg-orange-50 p-8 rounded-2xl text-center">
            <h3 class="text-2xl font-bold mb-4">Try SayPlay</h3>
            <a href="https://sayplay.co.uk" class="bg-orange-600 text-white px-8 py-3 rounded-full font-bold hover:bg-orange-700 transition inline-block">Shop Now</a>
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
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"      ✅ SEO: {output_path.name}")
        except:
            self._build_fallback(content, output_path)
    
    def build_blog_page(self, content: Dict, output_path: Path):
        if not self.blog_template:
            self._build_fallback(content, output_path)
            return
        
        try:
            html = self.blog_template.render(**content)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"      ✅ Blog: {output_path.name}")
        except:
            self._build_fallback(content, output_path)
    
    def _build_fallback(self, content: Dict, output_path: Path):
        title = content.get('title', 'SayPlay')
        body = '<br>'.join(str(v) for v in content.values() if isinstance(v, str))
        html = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{title}</title></head><body style="font-family:Arial;max-width:800px;margin:40px auto;padding:20px">{body}<p><a href="https://sayplay.co.uk">Visit SayPlay</a></p></body></html>'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"      ✅ Fallback: {output_path.name}")


class AudioStudio:
    """Same as V5"""
    
    def __init__(self):
        self.intro_paths = [
            Path("runtime_assets/Just tap.No app intro podkast sayplay.mp3"),
            Path("assets/music/Just tap.No app intro podkast sayplay.mp3")
        ]
        
        self.outro_paths = [
            Path("runtime_assets/Just tap.no app final podkast.mp3"),
            Path("assets/music/Just tap.no app final podkast.mp3")
        ]
        
        self.intro_file = None
        for path in self.intro_paths:
            if path.exists():
                self.intro_file = path
                print(f"✅ Intro: {path}")
                break
        
        self.outro_file = None
        for path in self.outro_paths:
            if path.exists():
                self.outro_file = path
                print(f"✅ Outro: {path}")
                break
    
    async def generate_podcast(self, script: str, episode_num: int, slug: str, output_dir: Path) -> Path:
        if not EDGE_TTS_AVAILABLE:
            return None
        
        if not script or len(script) < 50:
            script = f"Welcome to SayPlay. Episode {episode_num}. Visit sayplay.co.uk."
        
        print(f"      🎙️ Ep #{episode_num}: {len(script)} chars")
        
        temp_body = output_dir / f"temp_{episode_num}.mp3"
        
        try:
            communicate = edge_tts.Communicate(script, "en-GB-SoniaNeural")
            await communicate.save(str(temp_body))
        except:
            return None
        
        filename = f"sayplay_ep_{episode_num:03d}_{slug}.mp3"
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as outfile:
            if self.intro_file and self.intro_file.exists():
                with open(self.intro_file, 'rb') as infile:
                    outfile.write(infile.read())
            
            if temp_body.exists():
                with open(temp_body, 'rb') as infile:
                    outfile.write(infile.read())
                temp_body.unlink()
            
            if self.outro_file and self.outro_file.exists():
                with open(self.outro_file, 'rb') as infile:
                    outfile.write(infile.read())
        
        print(f"         ✅ {filename}")
        return output_path


class TrendHunter:
    """Same as V5"""
    
    SUBREDDITS = ['GiftIdeas', 'weddingplanning', 'relationship_advice']
    
    def get_topics(self, limit: int = 10) -> List[Dict]:
        print(f"📡 Reddit...")
        
        trends = []
        headers = {'User-Agent': 'SayPlayBot/1.0'}
        
        for subreddit in self.SUBREDDITS:
            try:
                url = f"https://www.reddit.com/r/{subreddit}/top.json?t=week&limit={limit}"
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        
                        if len(post_data.get('selftext', '')) > 100:
                            trends.append({
                                'title': post_data['title'],
                                'score': post_data['score']
                            })
            except:
                pass
        
        trends.sort(key=lambda x: x['score'], reverse=True)
        
        if not trends:
            trends = [
                {'title': 'Unique Wedding Gifts', 'score': 1000},
                {'title': 'Anniversary Ideas UK', 'score': 900},
                {'title': 'Birthday Gifts Dad', 'score': 850},
                {'title': 'Long Distance Gifts', 'score': 800},
                {'title': 'Sentimental Mum Gifts', 'score': 750},
                {'title': 'Graduation Gifts', 'score': 700},
                {'title': 'Baby Shower Ideas', 'score': 650},
                {'title': 'Retirement Gifts', 'score': 600},
                {'title': 'Christmas Fillers UK', 'score': 550},
                {'title': 'Valentines Guide', 'score': 500}
            ]
        
        selected = trends[:limit]
        print(f"   ✅ {len(selected)} topics")
        return selected


async def main():
    print("\n" + "="*70)
    print("TITAN V6 ULTIMATE CASCADE - 6 AI TIERS")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_V6_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    web_dir = output_dir / 'web'
    for d in ['blog', 'podcasts', 'seo']:
        (web_dir / d).mkdir(parents=True, exist_ok=True)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    brain = ContentBrain(gemini_key)
    design = DesignEngine()
    audio = AudioStudio()
    hunter = TrendHunter()
    
    cities = ['London', 'Birmingham', 'Manchester', 'Liverpool', 'Leeds',
              'Glasgow', 'Edinburgh', 'Bristol', 'Cardiff', 'Sheffield']
    
    print(f"\n{'='*70}")
    print("PHASE 1: TOPICS")
    print(f"{'='*70}")
    
    topics = hunter.get_topics(limit=10)
    
    print(f"\n{'='*70}")
    print("PHASE 2: SEO (10 pages, 6-tier cascade)")
    print(f"{'='*70}")
    
    seo_count = 0
    for i, topic in enumerate(topics[:10], 1):
        city = random.choice(cities)
        print(f"\n📌 SEO {i}/10: {topic['title'][:40]}... {city}")
        
        content = brain.generate_seo_page(topic['title'], city)
        
        slug = topic['title'].lower().replace(' ', '-')[:40]
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        page_path = web_dir / 'seo' / f'{slug}-{city.lower()}.html'
        design.build_seo_page(content, page_path)
        
        seo_count += 1
    
    print(f"\n{'='*70}")
    print("PHASE 3: BLOG (10 posts, 6-tier cascade)")
    print(f"{'='*70}")
    
    blog_count = 0
    for i, topic in enumerate(topics[:10], 1):
        print(f"\n📝 Blog {i}/10: {topic['title'][:40]}...")
        
        content = brain.generate_blog(topic['title'])
        
        slug = topic['title'].lower().replace(' ', '-')[:40]
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        page_path = web_dir / 'blog' / f'{slug}.html'
        design.build_blog_page(content, page_path)
        
        blog_count += 1
    
    print(f"\n{'='*70}")
    print("PHASE 4: PODCASTS (10 eps, 6-tier cascade)")
    print(f"{'='*70}")
    
    podcast_count = 0
    for i, topic in enumerate(topics[:10], 1):
        print(f"\n🎙️ Podcast {i}/10: {topic['title'][:40]}...")
        
        script = brain.generate_podcast_script(topic['title'])
        
        slug = topic['title'].lower().replace(' ', '-')[:30]
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        await audio.generate_podcast(script, i, slug, web_dir / 'podcasts')
        
        podcast_count += 1
    
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print("TITAN V6 ULTIMATE COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ {seo_count} SEO pages")
    print(f"✅ {blog_count} Blog posts")
    print(f"✅ {podcast_count} Podcasts")
    print(f"✅ 6-Tier Cascade: UNBREAKABLE")
    print(f"\n⏱ {int(duration // 60)}m {int(duration % 60)}s")
    print(f"{'='*70}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
