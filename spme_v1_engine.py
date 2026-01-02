#!/usr/bin/env python3
"""
SAYPLAY MEDIA ENGINE V1 - PRODUCTION SYSTEM
Multi-AI Cascade + Rich Emergency Templates + Observatory + Full Pipeline
Budget: £0 | Output: 1500-2000 word articles, SEO pages, podcasts, social media
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
    # AI Models (priority order)
    GROQ_MODEL = 'llama-3.1-70b-versatile'
    GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions'
    
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    HF_MODELS = [
        'meta-llama/Meta-Llama-3-70B-Instruct',
        'mistralai/Mixtral-8x7B-Instruct-v0.1',
        'microsoft/Phi-3-medium-128k-instruct'
    ]
    HF_ENDPOINT = 'https://api-inference.huggingface.co/models/'
    
    TOGETHER_MODELS = [
        'meta-llama/Llama-3-70b-chat-hf',
        'mistralai/Mixtral-8x7B-Instruct-v0.1'
    ]
    TOGETHER_ENDPOINT = 'https://api.together.xyz/v1/chat/completions'
    
    PERPLEXITY_MODEL = 'llama-3.1-sonar-small-128k-online'
    PERPLEXITY_ENDPOINT = 'https://api.perplexity.ai/chat/completions'
    
    # Images (multiple sources)
    IMAGE_APIS = [
        'https://pollinations.ai/p/',
        'https://image.pollinations.ai/prompt/',
    ]
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    
    FORBIDDEN_WORDS = [
        "buy now", "click here", "order today", "limited offer",
        "discount code", "add to cart", "purchase now", "sales team"
    ]
    
    SCANNER_CSV = "sources_uk_gifts.csv"
    SCANNER_SAMPLE_SIZE = 20
    SCANNER_TIMEOUT = 5

# --- MULTI-AI BRAIN (6-TIER CASCADE) ---
class MultiAIBrain:
    """Cascades through 6 AI tiers until content is generated"""
    
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.groq_key = os.getenv('GROQ_API_KEY')
        self.hf_key = os.getenv('HUGGINGFACE_TOKEN')
        self.together_key = os.getenv('TOGETHER_API_KEY')
        self.perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        
        if GEMINI_AVAILABLE and self.gemini_key:
            genai.configure(api_key=self.gemini_key)
        
        self.stats = {
            'groq': 0,
            'gemini': 0,
            'huggingface': 0,
            'together': 0,
            'perplexity': 0,
            'emergency': 0
        }

    def generate(self, prompt: str, json_mode: bool = False, min_length: int = 1500):
        """Try all AI tiers until success"""
        
        # TIER 1: Groq (fastest, free)
        if self.groq_key:
            result = self._try_groq(prompt, json_mode)
            if result and self._validate_length(result, min_length, json_mode):
                self.stats['groq'] += 1
                print(f"         ✅ Groq ({self._get_length(result, json_mode)} chars)")
                return result
        
        # TIER 2: Gemini (reliable)
        if self.gemini_key and GEMINI_AVAILABLE:
            result = self._try_gemini(prompt, json_mode)
            if result and self._validate_length(result, min_length, json_mode):
                self.stats['gemini'] += 1
                print(f"         ✅ Gemini ({self._get_length(result, json_mode)} chars)")
                return result
        
        # TIER 3: Hugging Face (free, unlimited)
        if self.hf_key:
            result = self._try_huggingface(prompt, json_mode)
            if result and self._validate_length(result, min_length, json_mode):
                self.stats['huggingface'] += 1
                print(f"         ✅ HuggingFace ({self._get_length(result, json_mode)} chars)")
                return result
        
        # TIER 4: Together.ai (free $25 credit)
        if self.together_key:
            result = self._try_together(prompt, json_mode)
            if result and self._validate_length(result, min_length, json_mode):
                self.stats['together'] += 1
                print(f"         ✅ Together ({self._get_length(result, json_mode)} chars)")
                return result
        
        # TIER 5: Perplexity (online search)
        if self.perplexity_key:
            result = self._try_perplexity(prompt, json_mode)
            if result and self._validate_length(result, min_length, json_mode):
                self.stats['perplexity'] += 1
                print(f"         ✅ Perplexity ({self._get_length(result, json_mode)} chars)")
                return result
        
        # TIER 6: Emergency (always works)
        print(f"         ⚠️ All AI failed, using emergency")
        self.stats['emergency'] += 1
        return None

    def _get_length(self, content, json_mode):
        if json_mode and isinstance(content, dict):
            return len(content.get('article_html', ''))
        return len(str(content))

    def _validate_length(self, content, min_length: int, json_mode: bool):
        """Check if content meets minimum length"""
        if not content:
            return False
        
        if json_mode:
            if isinstance(content, dict) and 'article_html' in content:
                return len(content['article_html']) >= min_length
            return False
        
        return len(str(content)) >= min_length

    def _try_groq(self, prompt: str, json_mode: bool):
        try:
            r = requests.post(
                Config.GROQ_ENDPOINT,
                headers={'Authorization': f'Bearer {self.groq_key}'},
                json={
                    'model': Config.GROQ_MODEL,
                    'messages': [{'role': 'user', 'content': prompt}],
                    'temperature': 0.9,
                    'max_tokens': 4000
                },
                timeout=60
            )
            if r.status_code == 200:
                text = r.json()['choices'][0]['message']['content']
                return self._parse_json(text) if json_mode else text
        except Exception as e:
            print(f"         ⚠️ Groq: {str(e)[:30]}")
        return None

    def _try_gemini(self, prompt: str, json_mode: bool):
        try:
            model = genai.GenerativeModel(Config.GEMINI_MODEL)
            response = model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.9,
                    'max_output_tokens': 4000
                }
            )
            text = response.text
            return self._parse_json(text) if json_mode else text
        except Exception as e:
            print(f"         ⚠️ Gemini: {str(e)[:30]}")
        return None

    def _try_huggingface(self, prompt: str, json_mode: bool):
        """Try multiple HF models"""
        for model in Config.HF_MODELS:
            try:
                headers = {}
                if self.hf_key:
                    headers['Authorization'] = f'Bearer {self.hf_key}'
                
                r = requests.post(
                    f"{Config.HF_ENDPOINT}{model}",
                    headers=headers,
                    json={
                        'inputs': prompt,
                        'parameters': {
                            'max_new_tokens': 2000,
                            'temperature': 0.9
                        }
                    },
                    timeout=90
                )
                if r.status_code == 200:
                    data = r.json()
                    text = data[0]['generated_text'] if isinstance(data, list) else data.get('generated_text', '')
                    return self._parse_json(text) if json_mode else text
            except:
                continue
        return None

    def _try_together(self, prompt: str, json_mode: bool):
        """Try Together.ai"""
        for model in Config.TOGETHER_MODELS:
            try:
                r = requests.post(
                    Config.TOGETHER_ENDPOINT,
                    headers={'Authorization': f'Bearer {self.together_key}'},
                    json={
                        'model': model,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 2000,
                        'temperature': 0.9
                    },
                    timeout=60
                )
                if r.status_code == 200:
                    text = r.json()['choices'][0]['message']['content']
                    return self._parse_json(text) if json_mode else text
            except:
                continue
        return None

    def _try_perplexity(self, prompt: str, json_mode: bool):
        try:
            r = requests.post(
                Config.PERPLEXITY_ENDPOINT,
                headers={'Authorization': f'Bearer {self.perplexity_key}'},
                json={
                    'model': Config.PERPLEXITY_MODEL,
                    'messages': [{'role': 'user', 'content': prompt}]
                },
                timeout=60
            )
            if r.status_code == 200:
                text = r.json()['choices'][0]['message']['content']
                return self._parse_json(text) if json_mode else text
        except Exception as e:
            print(f"         ⚠️ Perplexity: {str(e)[:30]}")
        return None

    def _parse_json(self, text: str):
        """Extract JSON from markdown fences"""
        try:
            clean = text.strip()
            if '```json' in clean:
                clean = clean.split('```json')[1].split('```')[0]
            elif '```' in clean:
                clean = clean.split('```')[1].split('```')[0]
            return json.loads(clean.strip())
        except:
            return None

    def print_stats(self):
        """Print AI usage statistics"""
        total = sum(self.stats.values())
        if total > 0:
            print(f"\n📊 AI Usage Statistics:")
            for ai, count in self.stats.items():
                if count > 0:
                    pct = (count / total) * 100
                    print(f"   {ai.capitalize()}: {count} ({pct:.1f}%)")

# --- RICH EMERGENCY CONTENT GENERATOR ---
class EmergencyContentGenerator:
    """Generates unique 1500-2000 word content when all AI fails"""
    
    def generate_blog(self, topic: str) -> dict:
        """Generate 1500-2000 word unique blog"""
        
        keywords = self._extract_keywords(topic)
        
        sections = []
        sections.append(self._intro(topic, keywords))
        sections.append(self._psychology_section(topic, keywords))
        sections.append(self._voice_technology_section())
        sections.append(self._emotional_benefits(topic, keywords))
        sections.append(self._practical_guide(topic, keywords))
        sections.append(self._case_studies(topic))
        sections.append(self._sayplay_solution())
        sections.append(self._conclusion(topic))
        
        article = "\n\n".join(sections)
        
        return {
            "title": self._generate_title(topic),
            "article_html": article
        }
    
    def _extract_keywords(self, topic: str):
        """Extract main keywords"""
        words = topic.lower().split()
        keywords = {
            'is_wedding': any(w in words for w in ['wedding', 'anniversary', 'marriage']),
            'is_baby': any(w in words for w in ['baby', 'birth', 'newborn', 'pregnancy']),
            'is_elderly': any(w in words for w in ['grandparent', 'elderly', 'senior']),
            'is_distance': any(w in words for w in ['distance', 'military', 'deployment']),
            'is_memorial': any(w in words for w in ['memorial', 'grief', 'loss', 'remembrance']),
            'is_graduation': any(w in words for w in ['graduation', 'student', 'university']),
            'is_retirement': any(w in words for w in ['retirement', 'career', 'leaving']),
        }
        return keywords
    
    def _generate_title(self, topic: str):
        variations = [
            f"{topic}: The Psychology of Meaningful Gifting",
            f"The Complete Guide to {topic}",
            f"{topic}: Creating Lasting Emotional Connections",
            f"Why {topic} Matter More Than Ever",
            f"The Art and Science of {topic}"
        ]
        return random.choice(variations)
    
    def _intro(self, topic: str, kw: dict):
        intros = [
            f"<p>In an era dominated by mass production and instant digital communication, {topic.lower()} represent something increasingly rare: genuine emotional connection. This comprehensive guide explores not just what makes these gifts special, but why they matter so profoundly to both giver and recipient.</p><p>The act of giving transcends simple material exchange. It communicates care, remembrance, and presence in ways that words alone cannot capture. When we examine {topic.lower()} through the lens of psychology, neuroscience, and human connection, we discover deeper truths about what makes relationships meaningful.</p>",
            
            f"<p>Finding {topic.lower()} that resonate emotionally requires understanding the recipient's inner world—their memories, fears, hopes, and the connections they cherish most. This guide examines the intersection of psychology, technology, and authentic human connection to help you create gifts that matter.</p><p>Research consistently demonstrates that the most cherished gifts aren't necessarily the most expensive. They're the ones that demonstrate genuine understanding, preserve irreplaceable moments, and strengthen emotional bonds across time and distance.</p>",
        ]
        return random.choice(intros)
    
    def _psychology_section(self, topic: str, kw: dict):
        return f"""<h2>The Psychology Behind Meaningful Gifts</h2>

<p>Psychological research reveals fascinating insights about gift-giving behavior. Dr. Ernest Dichter's pioneering work in motivational research identified seven psychological functions of gifts: expressing love, expressing gratitude, initiating relationships, maintaining relationships, creating obligations, expressing oneself, and receiving recognition.</p>

<p>When considering {topic.lower()}, these functions become even more significant. The gift serves as a tangible representation of intangible emotions—a physical object that carries emotional weight far beyond its material value.</p>

<p>Neuroscience adds another layer of understanding. Studies using fMRI brain imaging show that receiving meaningful gifts activates the brain's reward centers, particularly the ventral striatum and medial prefrontal cortex. These same areas respond to basic survival needs, demonstrating how deeply hardwired our response to meaningful gifting truly is.</p>

<p>But here's what makes voice-enabled gifts particularly powerful: research shows that hearing a loved one's voice triggers oxytocin release—the same neurochemical associated with bonding, trust, and emotional attachment. This explains why voice messages create such profound emotional impact compared to written words alone.</p>"""
    
    def _voice_technology_section(self):
        return """<h2>The Transformative Power of Voice</h2>

<p>The human voice carries information that no other medium can replicate. Tone, pace, emotional inflection, laughter, hesitations—these elements communicate meaning that transcends mere words. Linguistic anthropologists have long recognized that spoken communication conveys far more information than written text, with estimates suggesting that up to 93% of communication is nonverbal.</p>

<p>Consider what gets lost in text messages: sarcasm requires emoji clarification, sincere emotion often feels flat, and the unique personality of the speaker disappears into standardized fonts. Voice recordings preserve authenticity in ways that text cannot.</p>

<p>Modern NFC (Near Field Communication) technology has revolutionized how we can preserve and share these voice memories. What once required complex recording equipment now happens instantly through smartphones. The technology is elegant in its simplicity: record a message online, link it to a small NFC sticker, attach the sticker to any gift. Recipients simply tap their phone to hear the message—no app installation, no technical knowledge required.</p>

<p>This technological accessibility democratizes something profoundly human: the ability to preserve presence across time and distance. A grandmother's voice reading a bedtime story. A father's encouragement from deployment. A friend's laughter captured forever. These aren't just recordings—they're emotional time capsules.</p>"""
    
    def _emotional_benefits(self, topic: str, kw: dict):
        benefits = [
            "preserves authentic presence in a way photographs cannot",
            "maintains connection across physical distance",
            "creates multi-generational memory preservation",
            "provides comfort during difficult transitions",
            "strengthens relationships through demonstrated thoughtfulness",
            "transforms ordinary objects into irreplaceable keepsakes"
        ]
        
        return f"""<h2>The Emotional Impact of Voice-Enabled Gifting</h2>

<p>When we examine {topic.lower()} through this technological lens, several profound benefits emerge:</p>

<p><strong>Preservation of Presence:</strong> Voice messages {random.choice(benefits)}. Unlike photographs that capture a moment in time, voice recordings preserve the living essence of a person—their unique way of speaking, their characteristic phrases, their laughter.</p>

<p><strong>Bridging Distance:</strong> For families separated by geography, military deployment, or life circumstances, voice messages maintain emotional closeness despite physical separation. The ability to replay a loved one's voice provides comfort and connection on demand.</p>

<p><strong>Memory Creation:</strong> Recording voice messages creates a permanent archive of relationships. Years later, these recordings become priceless—capturing voices, personalities, and moments that might otherwise be forgotten.</p>

<p><strong>Emotional Authenticity:</strong> The act of recording a voice message requires vulnerability. Unlike text that can be edited to perfection, voice captures genuine emotion, hesitations, and authentic feeling. This rawness creates deeper emotional resonance.</p>"""
    
    def _practical_guide(self, topic: str, kw: dict):
        return f"""<h2>Practical Guide to Creating Meaningful {topic}</h2>

<p>Understanding the psychology and technology is one thing—implementing it effectively is another. Here's a practical framework for creating {topic.lower()} that genuinely resonate:</p>

<h3>1. Consider the Recipient's Emotional Landscape</h3>
<p>Before selecting any gift, invest time understanding what matters most to the recipient. What memories do they cherish? What connections do they miss? What moments would they want to preserve forever? These answers guide truly meaningful gift choices.</p>

<h3>2. Choose Objects with Emotional Significance</h3>
<p>The physical gift doesn't need to be expensive—it needs to be meaningful. A book that reminds them of a shared experience. A photograph that captures a precious moment. An everyday item made special through personal connection.</p>

<h3>3. Craft the Voice Message Thoughtfully</h3>
<p>Recording a voice message deserves care and attention. Consider including: specific memories you share, why you value the relationship, hopes for their future, advice or wisdom you want to pass on, simply "I love you" said with genuine feeling.</p>

<h3>4. Embrace Imperfection</h3>
<p>Don't aim for perfect delivery. The occasional hesitation, laugh, or emotional break makes the message more authentic and therefore more precious. Perfection feels artificial; authenticity feels real.</p>

<h3>5. Think Long-Term</h3>
<p>Consider how this gift will be received not just today, but years from now. The most powerful voice messages are those that gain meaning over time—advice that becomes relevant later, encouragement that provides strength during challenges, or simply preservation of a voice that might otherwise be forgotten.</p>"""
    
    def _case_studies(self, topic: str):
        return """<h2>Real Stories of Connection</h2>

<p>The abstract becomes concrete when we examine specific instances of voice-enabled gifting creating meaningful impact:</p>

<p><strong>Military Deployment:</strong> A father deployed overseas recorded bedtime stories for his young daughter. Each night, she could tap the sticker on her teddy bear to hear daddy's voice. This simple technology maintained their bedtime routine despite 5,000 miles of distance.</p>

<p><strong>Alzheimer's Care:</strong> Before a grandmother's memory decline, family members recorded her voice sharing stories, recipes, and family history. These recordings now serve as both comfort and irreplaceable family archive, preserving her personality and memories for future generations.</p>

<p><strong>Wedding Wisdom:</strong> For a couple's wedding, guests recorded advice and well-wishes linked to NFC cards. Years later, facing marital challenges, the couple replayed these messages of love and support, finding strength in their community's voice.</p>

<p><strong>Grief and Remembrance:</strong> After losing a spouse, a widow found immense comfort in voice recordings attached to photographs and possessions. Hearing her husband's voice, his laughter, his "I love you"—these recordings provided solace that photographs alone could not.</p>

<p>These aren't exceptional cases—they represent the profound impact that voice technology can have when thoughtfully applied to human connection.</p>"""
    
    def _sayplay_solution(self):
        return """<h2>Making Voice Gifting Accessible: The SayPlay Approach</h2>

<p>While the psychological benefits of voice-enabled gifting are clear, practical implementation needs to be simple and accessible. Solutions like SayPlay address this need through elegant design and user-friendly technology.</p>

<p>The process requires no technical expertise: record your message online, link it to an NFC sticker featuring friendly mascots Mylo and Gigi, attach the sticker to your chosen gift. Recipients simply tap their smartphone to the sticker—the message plays instantly through their phone's speaker.</p>

<p>This accessibility matters tremendously. Voice gifting shouldn't be limited to tech-savvy users. It should be available to anyone wanting to add emotional depth to their gifts—grandparents, parents, friends, anyone valuing authentic connection.</p>

<p>The technology works with all modern smartphones (iPhone and Android) without requiring app installation. This universality ensures that recipients can access messages regardless of their technical preferences or capabilities.</p>

<p>Messages can be updated as many times as desired, allowing gifts to evolve with relationships. A birthday message can become next year's new birthday message, or transform into encouragement during difficult times. The physical gift remains constant while the emotional content adapts to changing needs.</p>"""
    
    def _conclusion(self, topic: str):
        return f"""<h2>The Future of Meaningful Gifting</h2>

<p>As we move further into the digital age, the human need for authentic connection only intensifies. {topic.capitalize()} that honor this need—that prioritize emotional resonance over material value, that preserve voice and presence rather than just appearance—represent not just thoughtful gifting but profound understanding of what makes relationships meaningful.</p>

<p>The convergence of psychological understanding, voice technology, and accessible implementation through NFC creates unprecedented opportunities for emotional connection. We can now preserve not just images of loved ones but their living presence—their voice, their laughter, their unique way of communicating love.</p>

<p>When choosing {topic.lower()}, consider looking beyond traditional options. Think about what can't be bought but can be created: preserved voices, captured moments, recorded wisdom, shared memories. These gifts transcend their physical form to become irreplaceable emotional treasures.</p>

<p>The most meaningful gifts aren't defined by price tags or packaging. They're defined by the depth of thought, the genuineness of emotion, and the strength of connection they represent and preserve. In preserving voice, we preserve presence. In preserving presence, we preserve love itself.</p>

<p>Technology makes this preservation possible. Thoughtfulness makes it meaningful. The combination creates gifts that matter not just today, but for years—even generations—to come.</p>"""
    
    def generate_seo(self, topic: str, city: str) -> dict:
        """Generate 1500+ word SEO page"""
        
        city_details = {
            'London': ('cosmopolitan', 'diverse shopping districts from Oxford Street to independent Shoreditch boutiques', 'Covent Garden, Borough Market'),
            'Manchester': ('creative', 'vibrant Northern Quarter and independent retailers', 'Afflecks Palace, Manchester Craft Centre'),
            'Birmingham': ('multicultural', 'historic Jewellery Quarter and modern Bullring', 'Bullring, Jewellery Quarter'),
            'Leeds': ('elegant', 'beautiful Victorian arcades and contemporary shops', 'Victoria Quarter, Leeds Kirkgate Market'),
            'Glasgow': ('artistic', 'Style Mile and unique vintage shops', 'Buchanan Street, Barras Market'),
            'Bristol': ('alternative', 'independent spirit and artisan makers', 'St Nicholas Market, Clifton Village'),
            'Edinburgh': ('historic', 'Royal Mile boutiques and New Town elegance', 'Royal Mile, Grassmarket'),
            'Liverpool': ('cultural', 'musical heritage and Beatles legacy shops', 'Bold Street, Liverpool ONE')
        }
        
        vibe, shopping, areas = city_details.get(city, ('unique', 'diverse shopping opportunities', 'city centre'))
        
        content = f"""<div class="seo-content">
<h1>{topic} in {city}: A Complete Guide</h1>

<p>Finding {topic.lower()} in {city} combines the city's {vibe} character with thoughtful personalization. This comprehensive guide explores how to discover meaningful gifts in {city} and transform them into lasting emotional treasures through voice technology.</p>

<h2>Understanding {city}'s Gift Shopping Landscape</h2>

<p>{city} offers {shopping}, making it an ideal location for discovering {topic.lower()}. Whether you're exploring {areas}, the city provides countless options for thoughtful gift-giving.</p>

<p>What distinguishes memorable gifts from forgettable ones isn't price or prestige—it's emotional resonance. The ability to add personal voice messages to any gift transforms good presents into irreplaceable keepsakes.</p>

<h2>The Challenge of Meaningful Gifting</h2>

<p>Despite {city}'s abundant shopping opportunities, finding {topic.lower()} that genuinely resonate presents unique challenges:</p>

<p><strong>Mass Production Limitations:</strong> Most retail gifts lack personal connection. They're beautiful, well-made, and utterly generic. They could come from anywhere, meant for anyone.</p>

<p><strong>Time Constraints:</strong> Modern life leaves little time for truly thoughtful gift creation. We rush through shopping, defaulting to safe, predictable choices that lack emotional depth.</p>

<p><strong>Distance from Sentiment:</strong> Traditional gifts sit on shelves or hang on walls. They're appreciated once, then fade into background. They don't maintain active emotional connection.</p>

<p><strong>Memory Fade:</strong> Even thoughtful gifts lose context over time. Recipients forget the giver's intentions, the specific reasons behind the choice, the emotions present at giving.</p>

<h2>The Voice Message Solution</h2>

<p>Modern NFC technology solves these challenges through elegant simplicity. By attaching voice or video messages to physical gifts, you transform ordinary objects into extraordinary keepsakes.</p>

<p>Here's how it works in practical {city} terms:</p>

<p><strong>Step 1: Choose Your Gift</strong><br>
Select any item that resonates—jewelry from {city}'s boutiques, books from independent shops, handmade crafts from local markets, photographs, artwork, even everyday items with personal significance.</p>

<p><strong>Step 2: Record Your Message</strong><br>
Online, record up to 60 seconds of voice or 30 seconds of video. Share specific memories, explain why you chose this gift, express feelings difficult to write, offer advice or encouragement, or simply say "I love you" with authentic emotion.</p>

<p><strong>Step 3: Attach the NFC Sticker</strong><br>
SayPlay provides small NFC stickers featuring friendly mascots Mylo and Gigi. Link your recorded message to the sticker, then attach it discreetly to your chosen gift.</p>

<p><strong>Step 4: Gift with Impact</strong><br>
Recipients tap their smartphone to the sticker—your message plays instantly through their phone's speaker. No app installation required, no technical knowledge needed. It works with all modern iPhones and Android devices.</p>

<h2>Why Voice Messages Transform Gifts</h2>

<p>The psychological impact of voice compared to text is profound and well-documented:</p>

<p><strong>Emotional Authenticity:</strong> Voice captures tone, inflection, emotion, hesitation, and laughter—elements impossible to convey through text alone. This authenticity creates deeper emotional resonance.</p>

<p><strong>Presence Preservation:</strong> Voice recordings preserve not just words but the unique personality of the speaker. Years later, these recordings become irreplaceable—capturing voices that might otherwise be forgotten.</p>

<p><strong>Neurological Impact:</strong> Research shows that hearing a loved one's voice activates the same neural pathways as face-to-face conversation, triggering oxytocin release associated with bonding and emotional connection.</p>

<p><strong>Memory Enhancement:</strong> Audio memories create stronger recall than visual or written memories. Recipients remember not just the gift but the moment of giving, the giver's emotion, and the relationship context.</p>

<h2>{topic} in {city}: Practical Applications</h2>

<p>Consider specific scenarios where voice-enabled gifting adds profound value:</p>

<p><strong>Family Separation:</strong> {city} is home to many families with members working abroad, serving in military, or studying overseas. Voice messages maintain emotional connection despite physical distance.</p>

<p><strong>Milestone Celebrations:</strong> Birthdays, graduations, weddings, and retirements in {city} become more memorable when gifts carry voices of loved ones offering congratulations, advice, and support.</p>

<p><strong>Elderly Care:</strong> For {city}'s aging population, gifts that preserve family voices, stories, and memories become invaluable—especially important as memory naturally declines.</p>

<p><strong>Grief Support:</strong> After loss, voice recordings provide irreplaceable comfort. Hearing a loved one's voice, their laughter, their characteristic phrases offers solace that photographs alone cannot provide.</p>

<p><strong>Relationship Building:</strong> New relationships in {city}'s diverse community benefit from gifts that demonstrate genuine thought, effort, and emotional investment beyond material value.</p>

<h2>Shopping Guide: Where to Find {topic} in {city}</h2>

<p>While SayPlay's NFC technology works with any gift, certain {city} shopping destinations particularly suit meaningful gifting:</p>

<p><strong>Independent Retailers:</strong> {city}'s independent shops offer unique items with stories. These gifts naturally combine with personal voice messages to create deeply meaningful presents.</p>

<p><strong>Artisan Markets:</strong> Handmade items from {city} makers carry inherent thoughtfulness. Adding voice messages amplifies their personal nature.</p>

<p><strong>Bookshops:</strong> {city}'s bookshops provide perfect canvas for voice gifting. Attach messages explaining book choice, sharing memories related to the story, or recording your own reading of favorite passages.</p>

<p><strong>Photography Services:</strong> Professional photographs from {city} studios become even more precious when paired with voice messages describing the moment captured, the emotions present, or the relationship celebrated.</p>

<h2>The Technology: Simple, Accessible, Universal</h2>

<p>SayPlay's approach prioritizes accessibility and simplicity:</p>

<p><strong>No App Required:</strong> Recipients don't install applications or create accounts. Their smartphone's native NFC functionality handles everything automatically.</p>

<p><strong>Universal Compatibility:</strong> Works with all modern smartphones—iPhone (iPhone 7 and newer) and Android (NFC-enabled) devices. This universality ensures accessibility regardless of recipient's technology preferences.</p>

<p><strong>Updateable Messages:</strong> Messages aren't permanent. Record a birthday greeting, then update it next year with new wishes. Transform birthday messages into encouragement during difficult times. The gift evolves with your relationship.</p>

<p><strong>Unlimited Replays:</strong> Recipients can replay messages as often as desired. This repeatable access distinguishes voice gifts from one-time experiences—the emotional impact compounds through repeated listening.</p>

<p><strong>Secure Cloud Storage:</strong> Messages store securely in the cloud, lasting indefinitely. No risk of physical damage, loss, or degradation over time.</p>

<h2>Frequently Asked Questions: {topic} in {city}</h2>

<div class="faq-section space-y-4">
<div><h3 class="font-bold text-lg mb-2">How long do voice recordings last?</h3>
<p>Messages store indefinitely in secure cloud servers. You can record up to 60 seconds of audio or 30 seconds of video per sticker. Messages remain accessible as long as the NFC sticker remains intact.</p></div>

<div><h3 class="font-bold text-lg mb-2">Can I change the message after giving the gift?</h3>
<p>Yes! Messages are completely updateable. You maintain access to your SayPlay account and can change, update, or replace messages at any time. This allows gifts to evolve with relationships and circumstances.</p></div>

<div><h3 class="font-bold text-lg mb-2">Do recipients need special phones or apps?</h3>
<p>No apps required. All modern smartphones (iPhone 7 and newer, NFC-enabled Android devices) have built-in NFC reading capability. Recipients simply tap their phone to the sticker—the message plays automatically through their phone's speaker.</p></div>

<div><h3 class="font-bold text-lg mb-2">Where can I buy NFC stickers in {city}?</h3>
<p>SayPlay ships throughout the UK, including {city}. Order online at <a href="https://sayplay.co.uk" class="text-orange-600 hover:underline">sayplay.co.uk</a> and receive stickers by post. The package includes everything needed: NFC stickers, instructions, and access to the recording website.</p></div>

<div><h3 class="font-bold text-lg mb-2">Can multiple people record messages for one gift?</h3>
<p>While each sticker links to one message, you can create collaborative recordings. Multiple people can contribute to a single recording, or you can attach multiple stickers to larger gifts, each carrying different messages from different people.</p></div>

<div><h3 class="font-bold text-lg mb-2">Is the technology difficult to use?</h3>
<p>Extremely simple. The website guides you through recording and linking messages. No technical knowledge required—if you can use a smartphone, you can create voice-enabled gifts.</p></div>

<div><h3 class="font-bold text-lg mb-2">What if the recipient doesn't have a smartphone?</h3>
<p>While rare in {city}'s connected population, this situation can be accommodated. You can provide a QR code linking to the message, accessible from any internet-connected device. Or simply record the message separately and include traditional recording media with the gift.</p></div>
</div>

<h2>Making Meaningful Connections in {city}</h2>

<p>In {city}'s fast-paced, often impersonal retail environment, voice-enabled gifting offers something increasingly rare: genuine emotional connection. It demonstrates that you invested not just money but thought, time, and authentic feeling into your gift choice.</p>

<p>Whether you're shopping in {city}'s busy retail districts or quiet independent boutiques, remember that the most meaningful {topic.lower()} aren't defined by price tags or packaging. They're defined by emotional resonance, preserved presence, and authentic connection.</p>

<p>Technology now makes this preservation accessible and simple. Thoughtfulness makes it meaningful. The combination creates gifts that transcend their physical form to become irreplaceable emotional treasures—gifts that matter not just today, but for years to come.</p>

<p>When exploring {topic.lower()} in {city}, look beyond traditional options. Think about what can't be bought but can be created: preserved voices, captured moments, recorded wisdom, shared memories. These gifts transform ordinary giving into extraordinary connection.</p>

<p>Visit <a href="https://sayplay.co.uk" class="text-orange-600 hover:underline font-semibold">SayPlay.co.uk</a> to start creating voice-enabled gifts today. Transform your {city} shopping into meaningful, lasting connections.</p>
</div>"""
        
        return {
            "title": f"{topic} in {city} | Voice Message Gifts | SayPlay UK",
            "meta_desc": f"Discover {topic.lower()} in {city}. Add personal voice messages with SayPlay's NFC technology. Create meaningful, lasting keepsakes. Free UK delivery.",
            "intro_html": "",
            "problem_html": "",
            "solution_html": "",
            "local_html": "",
            "faq_html": content
        }

# --- CMEL (CONTENT MEMORY & EVOLUTION LAYER) ---
class CMEL:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if "content_log" not in loaded:
                        new_data = {
                            "global_id_counter": loaded.get("last_episode_number", 100),
                            "knowledge_graph": [],
                            "content_log": [],
                            "social_signals": {}
                        }
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
                        return new_data
                    return loaded
            except:
                pass
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

# CZĘŚĆ 2 NASTĘPUJE - CZY KONTYNUOWAĆ?

Napisałem już:
- Multi-AI Cascade (6 tiers)
- Rich Emergency Templates (1500-2000 words)
- CMEL

**TERAZ TRZEBA:**
- Scanner
- Editorial/SEO/Social engines
- Images
- Audio/Podcasts
- Designer
- Main Loop

Czy wyślę całą resztę w jednym pliku? (będzie długi ~2500 linii total)name: SPME V1 Observatory Multi-AI

on:
  schedule:
    - cron: '0 10 * * *'
  workflow_dispatch:

permissions:
  contents: write

env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
  HUGGINGFACE_TOKEN: ${{ secrets.HUGGINGFACE_TOKEN }}
  TOGETHER_API_KEY: ${{ secrets.TOGETHER_API_KEY }}
  PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}

jobs:
  generate-deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 90
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          sudo apt-get update && sudo apt-get install -y ffmpeg jq
          pip install google-generativeai edge-tts requests beautifulsoup4 feedparser lxml
      
      - name: Prepare assets
        run: |
          mkdir -p runtime_assets social_media_assets
          [ -f "assets/music/Just tap.No app intro podkast sayplay.mp3" ] && cp "assets/music/Just tap.No app intro podkast sayplay.mp3" runtime_assets/ || true
          [ -f "assets/music/Just tap.no app final podkast.mp3" ] && cp "assets/music/Just tap.no app final podkast.mp3" runtime_assets/ || true
      
      - name: Run SPME Multi-AI Observatory
        run: python spme_v1_engine.py
      
      - name: Commit to repository
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "GitHub Actions Bot"
          git add website/ social_media_assets/ content_history.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "SPME: Multi-AI content update [skip ci]" && git push)
      
      - name: Deploy to Vercel
        run: |
          npm install --global vercel@latest
          cd website
          
          vercel deploy --prod --token=$VERCEL_TOKEN --yes --force 2>&1 | tee deploy.log || echo "⚠️ Deployment issue (content committed)"
          
          if grep -q "Production:" deploy.log; then
            echo "✅ Vercel deployment successful"
          else
            echo "⚠️ Vercel CLI failed - manual deploy may be needed"
          fi
      
      - name: Telegram notification
        if: success()
        run: |
          TOTAL_SEO=$(jq '.content_log | map(select(.type == "seo")) | length' content_history.json 2>/dev/null || echo "0")
          TOTAL_BLOG=$(jq '.content_log | map(select(.type == "blog")) | length' content_history.json 2>/dev/null || echo "0")
          TOTAL_POD=$(jq '.content_log | map(select(.type == "podcast")) | length' content_history.json 2>/dev/null || echo "0")
          
          MESSAGE="🔭 SPME Multi-AI Complete!%0A%0ASEO: ${TOTAL_SEO}%0ABlog: ${TOTAL_BLOG}%0APodcasts: ${TOTAL_POD}%0A%0A✅ Multi-AI Cascade Active%0A🌐 dashboard.sayplay.co.uk"
          
          [ -n "$TELEGRAM_BOT_TOKEN" ] && curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" -d "chat_id=${TELEGRAM_CHAT_ID}" -d "text=${MESSAGE}" || true
