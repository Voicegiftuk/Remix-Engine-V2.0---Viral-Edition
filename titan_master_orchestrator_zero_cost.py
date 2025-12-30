#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - PROFESSIONAL COMPLETE
- Real images from Unsplash/Pexels with logo
- 3-5 minute podcasts
- Unique 1500+ word articles
- Index pages for blog and SEO
- Professional design
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import base64
import asyncio
from typing import List, Dict
import hashlib

sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai not installed")

# Images
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Audio
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ edge-tts not installed")


class ProfessionalImageGenerator:
    """Generate professional images with SayPlay branding"""
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
    
    def generate_hero_image(self, keyword: str, width: int = 1200, height: int = 630) -> bytes:
        """Generate hero image with logo"""
        print(f"      🖼 Fetching image for: {keyword}")
        
        # Try Unsplash
        if self.unsplash_key:
            img = self._fetch_unsplash(keyword, width, height)
            if img:
                print(f"         ✅ Got Unsplash image")
                return self._add_logo_overlay(img)
        
        # Try Pexels
        if self.pexels_key:
            img = self._fetch_pexels(keyword, width, height)
            if img:
                print(f"         ✅ Got Pexels image")
                return self._add_logo_overlay(img)
        
        # Fallback gradient
        print(f"         ⚠️ Using gradient fallback")
        return self._generate_gradient(width, height)
    
    def _fetch_unsplash(self, query: str, width: int, height: int):
        """Fetch from Unsplash API"""
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {
                'query': query,
                'orientation': 'landscape',
                'client_id': self.unsplash_key
            }
            
            response = requests.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['raw'] + f"&w={width}&h={height}&fit=crop"
                
                img_response = requests.get(image_url, timeout=25)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content)).convert('RGB')
        except Exception as e:
            print(f"         Unsplash error: {str(e)[:80]}")
        
        return None
    
    def _fetch_pexels(self, query: str, width: int, height: int):
        """Fetch from Pexels API"""
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {'Authorization': self.pexels_key}
            params = {
                'query': query,
                'per_page': 1,
                'orientation': 'landscape'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('photos'):
                    image_url = data['photos'][0]['src']['large2x']
                    
                    img_response = requests.get(image_url, timeout=25)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content)).convert('RGB')
                        return img.resize((width, height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"         Pexels error: {str(e)[:80]}")
        
        return None
    
    def _generate_gradient(self, width: int, height: int) -> bytes:
        """Generate gradient background"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            r = int(102 + (118 - 102) * y / height)
            g = int(126 + (75 - 126) * y / height)
            b = int(234 + (162 - 234) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return self._add_logo_overlay(img)
    
    def _add_logo_overlay(self, img: Image.Image) -> bytes:
        """Add SayPlay logo to image"""
        width, height = img.size
        
        # Dark gradient overlay at bottom
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        gradient_start = int(height * 0.65)
        for y in range(gradient_start, height):
            progress = (y - gradient_start) / (height - gradient_start)
            alpha = int(200 * progress)
            overlay_draw.rectangle([(0, y), (width, y+1)], fill=(0, 0, 0, alpha))
        
        # Composite overlay
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        
        # Add logo text
        draw = ImageDraw.Draw(img)
        
        try:
            logo_size = max(40, int(height * 0.08))
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            logo_size = 40
            font = ImageFont.load_default()
        
        # Position logo
        logo_x = width - int(width * 0.35)
        logo_y = height - int(height * 0.15)
        
        # Draw "Say" in white
        draw.text((logo_x, logo_y), "Say", fill=(255, 255, 255), font=font)
        
        # Calculate "Say" width
        say_bbox = draw.textbbox((0, 0), "Say", font=font)
        say_width = say_bbox[2] - say_bbox[0]
        
        # Draw "Play" in gold
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        # Convert to bytes
        img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format='JPEG', quality=92)
        return output.getvalue()


class LongFormPodcastGenerator:
    """Generate 3-5 minute podcasts"""
    
    async def generate_podcast(self, article: dict, topic: dict, episode_num: int) -> dict:
        """Generate long-form podcast"""
        if not EDGE_TTS_AVAILABLE:
            print("      ⚠️ Edge TTS not available")
            return None
        
        print(f"      🎙 Generating podcast (3-5 min)...")
        
        # Create detailed script (800-1000 words for 3-5 minutes)
        script_parts = [
            f"Hello and welcome to the SayPlay Gift Guide, I'm your host, and this is episode {episode_num}.",
            f"Today, we're diving deep into {topic['title'].lower()}.",
            "",
            "Finding the perfect gift can feel overwhelming, but it doesn't have to be. Whether you're shopping for a milestone celebration or just want to show someone you care, the right gift can create a memory that lasts forever.",
            "",
            f"Let's talk about {topic['keyword']}. What makes a gift truly special? It's not just about the price tag or the packaging. It's about thoughtfulness, personalization, and showing that you truly understand the person you're giving to.",
            "",
            "Here are some ideas that really stand out:",
            "",
            "First, consider personalized items. A custom piece of jewelry, an engraved watch, or a photo album filled with memories can mean so much more than something generic off the shelf.",
            "",
            "Second, think about experiences. Concert tickets, a cooking class, or a weekend getaway can create new memories together. These are gifts that keep on giving.",
            "",
            "Third, handmade gifts show incredible thoughtfulness. Whether it's a knitted scarf, a painted portrait, or homemade treats, the time and effort you put in speaks volumes.",
            "",
            "Fourth, subscription services are perfect for ongoing joy. A monthly book club, coffee delivery, or streaming service shows you're thinking about them all year long.",
            "",
            "Fifth, tech gadgets for the person who loves innovation. Smart home devices, wireless earbuds, or the latest tablet can be both practical and exciting.",
            "",
            "Sixth, wellness gifts like a spa day, massage gift card, or meditation app subscription show you care about their wellbeing.",
            "",
            "And finally, don't underestimate the power of a heartfelt card with a personal message. Sometimes words matter most.",
            "",
            "But here's where SayPlay takes gift-giving to the next level. Imagine being able to record your voice, sharing a personal message, a favorite memory, or even singing happy birthday. With SayPlay's NFC technology, you can attach that voice message to any gift. The recipient simply taps their phone, and your voice plays instantly. No app needed, no complicated setup.",
            "",
            "Think about it - a grandmother hearing her grandchild's voice every time she looks at her gift. A long-distance friend feeling connected through your words. A spouse reliving your wedding vows on your anniversary. That's the magic of adding your voice.",
            "",
            "Whether you're giving jewelry, flowers, a photo frame, or any gift at all, SayPlay transforms it into something unforgettable. Your voice becomes part of the gift forever.",
            "",
            f"So as you think about {topic['keyword']}, remember - it's not just what you give, but how you give it. Add your personal touch, add your voice, and create a moment they'll treasure.",
            "",
            "Visit sayplay dot co dot uk to learn more about adding voice messages to your gifts. Make every gift unforgettable.",
            "",
            f"That's it for episode {episode_num} of the SayPlay Gift Guide. Thanks for listening, and happy gift giving!"
        ]
        
        full_script = " ".join(script_parts)
        
        # Generate audio with UK voice
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(full_script, voice, rate="+0%", volume="+0%")
        
        # Save to temp file
        temp_file = f"temp_podcast_{episode_num}.mp3"
        await communicate.save(temp_file)
        
        # Read audio data
        with open(temp_file, 'rb') as f:
            audio_data = f.read()
        
        # Cleanup
        os.remove(temp_file)
        
        duration = len(audio_data) / 3000  # Rough estimate
        
        print(f"         ✅ Podcast generated (~{int(duration)}s)")
        
        return {
            'audio': audio_data,
            'script': full_script,
            'duration': int(duration),
            'voice': voice
        }


def generate_article_with_gemini(topic: dict, api_key: str) -> dict:
    """Generate unique article with Gemini"""
    
    if not GEMINI_AVAILABLE or not api_key:
        return generate_fallback_article(topic)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Create unique seed for this topic
        seed = hashlib.md5(f"{topic['title']}{datetime.now().date()}".encode()).hexdigest()
        
        prompt = f"""Write a comprehensive, engaging blog article about: {topic['title']}

CRITICAL: Make this article UNIQUE and DIFFERENT from others. Use creative examples and fresh perspectives.

Keyword: {topic['keyword']}
Tone: {topic['angle']}
Length: 1500-1800 words
Article ID: {seed[:8]}

Structure:
1. Compelling introduction (3 paragraphs) - Hook readers emotionally
2. Why This Gift Matters (2 paragraphs) - Explain significance
3. Top 7-9 Specific Gift Ideas:
   - Each idea: 150-200 words
   - Include specific products/brands
   - Price ranges (budget to luxury)
   - Where to buy (UK shops/online)
   - Why it's meaningful
4. Personalization Ideas (2 paragraphs) - How to make it special
5. Presentation Tips (2 paragraphs) - How to give the gift
6. Common Mistakes to Avoid (1 paragraph)
7. Conclusion with emotional appeal (2 paragraphs)

IMPORTANT:
- Use real, specific examples (not generic)
- Include UK shopping references (John Lewis, Not On The High Street, Amazon UK, local shops)
- Make it conversational and warm
- Add personal anecdotes and scenarios
- Focus on emotional connection
- Each article MUST be completely different from others"""

        response = model.generate_content(prompt)
        article_text = response.text
        
        # Parse sections
        sections = []
        current_section = {'title': '', 'content': ''}
        
        for line in article_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('##'):
                if current_section['content']:
                    sections.append(current_section)
                current_section = {'title': line.replace('##', '').strip(), 'content': ''}
            elif line.startswith('#'):
                if current_section['content']:
                    sections.append(current_section)
                current_section = {'title': line.replace('#', '').strip(), 'content': ''}
            else:
                current_section['content'] += line + '\n'
        
        if current_section['content']:
            sections.append(current_section)
        
        word_count = len(article_text.split())
        
        print(f"      ✅ Article: {word_count} words, {len(sections)} sections")
        
        return {
            'title': topic['title'],
            'text': article_text,
            'sections': sections,
            'word_count': word_count,
            'keyword': topic['keyword']
        }
        
    except Exception as e:
        print(f"      ⚠️ Gemini error: {str(e)[:100]}")
        return generate_fallback_article(topic)


def generate_fallback_article(topic: dict) -> dict:
    """Fallback article if Gemini fails"""
    
    content = f"""Finding the perfect {topic['keyword']} requires thoughtfulness and care. Whether you're celebrating a special occasion or simply want to show someone you care, the right gift can create lasting memories.

## Understanding What Makes a Great Gift

The best gifts are those that show you truly know the recipient. Consider their interests, hobbies, and what brings them joy. A personalized approach always makes a difference.

## Top Gift Ideas

Here are some thoughtful {topic['keyword']} that stand out:

**Personalized Items**: Custom jewelry, engraved accessories, or photo gifts add a special touch that shows extra thought and care.

**Experience Gifts**: Concert tickets, cooking classes, or adventure days create memories that last far longer than physical items.

**Handmade Gifts**: Something crafted by hand, whether it's baked goods, knitted items, or artwork, carries emotional value.

**Tech Gadgets**: For the tech-savvy person, the latest devices or accessories can be both practical and exciting.

**Wellness Gifts**: Spa vouchers, massage sessions, or wellness subscriptions show you care about their wellbeing.

## Adding a Personal Touch

The key to making any gift special is personalization. Add a heartfelt card, include a meaningful message, or present it in a memorable way.

With SayPlay's voice message technology, you can add your voice to any gift. Simply record a personal message, and the recipient can play it with a tap of their phone. No app needed - just pure emotion and connection.

## Making It Memorable

Remember, it's not about how much you spend, but about the thought behind the gift. Choose something that reflects your relationship and shows genuine care."""

    sections = [
        {'title': 'Understanding What Makes a Great Gift', 'content': 'The best gifts are those that show you truly know the recipient.'},
        {'title': 'Top Gift Ideas', 'content': 'Here are some thoughtful options that stand out.'},
        {'title': 'Adding a Personal Touch', 'content': 'The key to making any gift special is personalization.'}
    ]
    
    return {
        'title': topic['title'],
        'text': content,
        'sections': sections,
        'word_count': len(content.split()),
        'keyword': topic['keyword']
    }


def create_professional_html(article: dict, topic: dict, hero_base64: str, slug: str) -> str:
    """Create professional HTML with hero image"""
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{article['text'][:160]}...">
    <meta name="keywords" content="{topic['keyword']}, personalized gifts, sayplay, voice messages">
    <title>{article['title']} | SayPlay Gift Guide</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #2d3748;
            background: #f7fafc;
        }}
        
        .hero {{
            position: relative;
            height: 600px;
            background: url('data:image/jpeg;base64,{hero_base64}') center/cover no-repeat;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .hero-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.7) 100%);
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            max-width: 900px;
            padding: 0 30px;
        }}
        
        .logo {{
            font-size: 56px;
            font-weight: 800;
            margin-bottom: 25px;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.5);
            letter-spacing: -1px;
        }}
        
        .logo span {{ color: #FFD700; }}
        
        h1 {{
            font-size: 56px;
            font-weight: 900;
            margin-bottom: 25px;
            line-height: 1.15;
            text-shadow: 2px 2px 12px rgba(0,0,0,0.6);
            letter-spacing: -0.5px;
        }}
        
        .meta {{
            display: flex;
            justify-content: center;
            gap: 35px;
            flex-wrap: wrap;
            font-size: 17px;
            opacity: 0.95;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .container {{
            max-width: 900px;
            margin: -120px auto 80px;
            background: white;
            border-radius: 25px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.15);
            padding: 70px 60px;
            position: relative;
            z-index: 3;
        }}
        
        .content h2 {{
            color: #667eea;
            font-size: 36px;
            font-weight: 800;
            margin: 60px 0 30px;
            padding-bottom: 18px;
            border-bottom: 4px solid #FFD700;
            letter-spacing: -0.5px;
        }}
        
        .content h3 {{
            color: #764ba2;
            font-size: 26px;
            font-weight: 700;
            margin: 40px 0 20px;
        }}
        
        .content p {{
            margin-bottom: 24px;
            font-size: 19px;
            line-height: 1.9;
            color: #4a5568;
        }}
        
        .content strong {{
            color: #2d3748;
            font-weight: 700;
        }}
        
        .cta-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 70px 60px;
            border-radius: 25px;
            margin: 70px 0;
            text-align: center;
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.35);
        }}
        
        .cta-icon {{
            font-size: 90px;
            margin-bottom: 30px;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-15px); }}
        }}
        
        .cta-section h3 {{
            color: white;
            font-size: 42px;
            margin: 0 0 25px;
            font-weight: 900;
            letter-spacing: -0.5px;
        }}
        
        .cta-section p {{
            color: rgba(255, 255, 255, 0.95);
            font-size: 22px;
            margin-bottom: 40px;
            line-height: 1.6;
        }}
        
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 15px;
            background: white;
            color: #667eea;
            padding: 22px 55px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 800;
            font-size: 22px;
            transition: all 0.3s ease;
            box-shadow: 0 12px 35px rgba(0,0,0,0.25);
        }}
        
        .cta-button:hover {{
            transform: translateY(-4px);
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 35px;
            margin: 60px 0;
        }}
        
        .feature {{
            text-align: center;
            padding: 35px;
            background: #f7fafc;
            border-radius: 20px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .feature:hover {{
            transform: translateY(-8px);
            border-color: #667eea;
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
        }}
        
        .feature i {{
            font-size: 56px;
            color: #667eea;
            margin-bottom: 25px;
        }}
        
        .feature h4 {{
            color: #2d3748;
            font-size: 22px;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .feature p {{
            color: #718096;
            font-size: 17px;
            margin: 0;
            line-height: 1.6;
        }}
        
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-size: 17px;
            margin-bottom: 30px;
            transition: gap 0.3s;
        }}
        
        .back-link:hover {{
            gap: 15px;
        }}
        
        @media (max-width: 768px) {{
            .hero {{ height: 450px; }}
            h1 {{ font-size: 36px; }}
            .logo {{ font-size: 42px; }}
            .container {{
                padding: 45px 30px;
                margin: -70px 20px 50px;
                border-radius: 20px;
            }}
            .content h2 {{ font-size: 28px; }}
            .content p {{ font-size: 17px; }}
            .cta-section {{ padding: 50px 35px; }}
            .cta-section h3 {{ font-size: 32px; }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="logo">Say<span>Play</span></div>
            <h1>{article['title']}</h1>
            <div class="meta">
                <span class="meta-item">
                    <i class="far fa-calendar-alt"></i>
                    {datetime.now().strftime("%B %d, %Y")}
                </span>
                <span class="meta-item">
                    <i class="far fa-clock"></i>
                    {max(1, article['word_count'] // 200)} min read
                </span>
                <span class="meta-item">
                    <i class="fas fa-tags"></i>
                    {topic['category']}
                </span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <a href="/blog" class="back-link">
            <i class="fas fa-arrow-left"></i>
            Back to all articles
        </a>
        
        <div class="content">
'''
    
    # Add article sections
    for section in article['sections']:
        if section['title']:
            html += f"<h2>{section['title']}</h2>\n"
        
        paragraphs = section['content'].strip().split('\n')
        for para in paragraphs:
            para = para.strip()
            if para:
                # Check if it's a bullet point
                if para.startswith('**') and para.endswith('**'):
                    html += f"<h3>{para.replace('**', '')}</h3>\n"
                elif para.startswith('-') or para.startswith('*'):
                    html += f"<p><strong>•</strong> {para[1:].strip()}</p>\n"
                else:
                    html += f"<p>{para}</p>\n"
    
    html += f'''
            <div class="cta-section">
                <div class="cta-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <h3>Make Every Gift Unforgettable</h3>
                <p>Transform any gift into a cherished memory with SayPlay's voice message technology. Record your heartfelt message and let it play with a simple tap. No app needed!</p>
                <a href="https://sayplay.co.uk" class="cta-button">
                    Discover SayPlay
                    <i class="fas fa-arrow-right"></i>
                </a>
            </div>
            
            <div class="features">
                <div class="feature">
                    <i class="fas fa-mobile-alt"></i>
                    <h4>Tap & Play</h4>
                    <p>No app needed. Just tap with any smartphone.</p>
                </div>
                <div class="feature">
                    <i class="fas fa-heart"></i>
                    <h4>Personal Touch</h4>
                    <p>Record your heartfelt message in seconds.</p>
                </div>
                <div class="feature">
                    <i class="fas fa-infinity"></i>
                    <h4>Lasts Forever</h4>
                    <p>Your voice message never expires.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


def generate_seo_pages(output_dir: Path) -> List[Dict]:
    """Generate 100 SEO landing pages with FULL content"""
    
    print(f"\n{'='*70}")
    print("GENERATING SEO LANDING PAGES")
    print(f"{'='*70}")
    
    seo_dir = output_dir / 'web' / 'seo'
    seo_dir.mkdir(parents=True, exist_ok=True)
    
    # UK Cities
    cities = [
        'London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds',
        'Glasgow', 'Edinburgh', 'Bristol', 'Cardiff', 'Sheffield',
        'Newcastle', 'Belfast', 'Brighton', 'Oxford', 'Cambridge',
        'York', 'Bath', 'Nottingham', 'Leicester', 'Southampton'
    ]
    
    # Gift types
    gift_types = [
        {'slug': 'birthday-gifts', 'title': 'Birthday Gifts', 'emoji': '🎂'},
        {'slug': 'anniversary-gifts', 'title': 'Anniversary Gifts', 'emoji': '💑'},
        {'slug': 'wedding-gifts', 'title': 'Wedding Gifts', 'emoji': '💍'},
        {'slug': 'christmas-gifts', 'title': 'Christmas Gifts', 'emoji': '🎄'},
        {'slug': 'mothers-day-gifts', 'title': "Mother's Day Gifts", 'emoji': '🌸'}
    ]
    
    pages = []
    
    for city in cities:
        for gift_type in gift_types:
            slug = f"{gift_type['slug']}-{city.lower().replace(' ', '-')}"
            
            # Create FULL content page
            html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gift_type['title']} in {city} | SayPlay Gift Guide</title>
    <meta name="description" content="Find perfect {gift_type['title'].lower()} in {city}. Personalized voice message gifts that create lasting memories. Browse unique gift ideas with SayPlay.">
    <meta name="keywords" content="{gift_type['slug']}, {city}, personalized gifts, voice messages, sayplay">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            line-height: 1.8;
            color: #2d3748;
        }}
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 30px;
            text-align: center;
        }}
        .logo {{
            font-size: 56px;
            font-weight: 800;
            margin-bottom: 25px;
            letter-spacing: -1px;
        }}
        .logo span {{ color: #FFD700; }}
        h1 {{
            font-size: 48px;
            margin: 25px 0;
            font-weight: 900;
            letter-spacing: -0.5px;
        }}
        .hero p {{
            font-size: 22px;
            opacity: 0.95;
        }}
        .container {{
            max-width: 1000px;
            margin: 80px auto;
            padding: 0 30px;
        }}
        h2 {{
            color: #667eea;
            font-size: 36px;
            margin: 50px 0 25px;
            font-weight: 800;
        }}
        p {{
            font-size: 19px;
            margin-bottom: 20px;
            line-height: 1.8;
            color: #4a5568;
        }}
        .gift-ideas {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 50px 0;
        }}
        .gift-card {{
            background: #f7fafc;
            padding: 35px;
            border-radius: 20px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s;
        }}
        .gift-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
        }}
        .gift-card i {{
            font-size: 48px;
            color: #667eea;
            margin-bottom: 20px;
        }}
        .gift-card h3 {{
            color: #2d3748;
            font-size: 22px;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        .cta {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 70px 50px;
            border-radius: 25px;
            text-align: center;
            margin: 70px 0;
            box-shadow: 0 20px 50px rgba(102, 126, 234, 0.35);
        }}
        .cta i {{
            font-size: 80px;
            margin-bottom: 25px;
        }}
        .cta h3 {{
            color: white;
            font-size: 38px;
            margin-bottom: 20px;
            font-weight: 900;
        }}
        .cta p {{
            color: white;
            font-size: 20px;
            margin-bottom: 35px;
        }}
        .cta a {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: white;
            color: #667eea;
            padding: 20px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 800;
            font-size: 20px;
            transition: all 0.3s;
        }}
        .cta a:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-size: 17px;
            margin-bottom: 30px;
        }}
        @media (max-width: 768px) {{
            .hero {{ padding: 70px 20px; }}
            h1 {{ font-size: 36px; }}
            .logo {{ font-size: 42px; }}
            .container {{ padding: 0 20px; }}
            .gift-ideas {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="logo">Say<span>Play</span></div>
        <h1>{gift_type['emoji']} {gift_type['title']} in {city}</h1>
        <p>Personalized Gifts with Voice Messages</p>
    </div>
    
    <div class="container">
        <a href="/seo" class="back-link">
            <i class="fas fa-arrow-left"></i>
            Back to all locations
        </a>
        
        <h2>Find Perfect {gift_type['title']} in {city}</h2>
        
        <p>Looking for unique {gift_type['title'].lower()} in {city}? You're in the right place. Whether you're shopping in the city center or browsing online, finding a gift that truly resonates can transform a special occasion into an unforgettable memory.</p>
        
        <p>At SayPlay, we believe the best gifts combine thoughtfulness with personalization. That's why we've created a way to add your voice to any gift, making it truly one-of-a-kind.</p>
        
        <h2>Why Personalized Gifts Matter</h2>
        
        <p>In {city}, you have access to countless shops and gift options. But what makes a gift truly special isn't just what you buy—it's how you present it and the personal touch you add.</p>
        
        <p>A voice message transforms any gift into something extraordinary. Imagine your loved one hearing your voice every time they look at their gift. Whether it's a heartfelt message, a favorite memory, or even a song, your voice adds emotion that lasts forever.</p>
        
        <h2>Popular Gift Ideas in {city}</h2>
        
        <div class="gift-ideas">
            <div class="gift-card">
                <i class="fas fa-gem"></i>
                <h3>Personalized Jewelry</h3>
                <p>Add a voice message to a beautiful necklace or bracelet. Perfect for creating lasting memories.</p>
            </div>
            <div class="gift-card">
                <i class="fas fa-image"></i>
                <h3>Photo Frames</h3>
                <p>Combine cherished photos with your personal message. Great for any occasion.</p>
            </div>
            <div class="gift-card">
                <i class="fas fa-spa"></i>
                <h3>Spa & Wellness</h3>
                <p>Pair a relaxing experience with an encouraging voice message for extra thoughtfulness.</p>
            </div>
            <div class="gift-card">
                <i class="fas fa-book"></i>
                <h3>Books & Journals</h3>
                <p>Add your voice to a meaningful book or journal for a truly personal touch.</p>
            </div>
            <div class="gift-card">
                <i class="fas fa-mug-hot"></i>
                <h3>Personalized Items</h3>
                <p>From mugs to keepsakes, add your voice to make everyday items extraordinary.</p>
            </div>
            <div class="gift-card">
                <i class="fas fa-seedling"></i>
                <h3>Plants & Flowers</h3>
                <p>Living gifts with a voice message create memories that grow over time.</p>
            </div>
        </div>
        
        <h2>How SayPlay Works</h2>
        
        <p><strong>1. Record Your Message:</strong> Use your phone to record a heartfelt message, memory, or greeting—up to 3 minutes long.</p>
        
        <p><strong>2. Attach to Your Gift:</strong> Place the SayPlay NFC sticker anywhere on your gift. It works with any present, any packaging.</p>
        
        <p><strong>3. They Tap & Listen:</strong> When they receive their gift, they simply tap their phone on the sticker. Your voice plays instantly—no app needed.</p>
        
        <h2>Shopping in {city}</h2>
        
        <p>Whether you're browsing local {city} shops or ordering online, SayPlay works with any gift you choose. Visit boutiques, department stores, or craft markets—then add your personal voice message to make it unforgettable.</p>
        
        <p>Popular shopping areas in {city} offer countless gift options, but the real magic happens when you add your voice. It's the difference between giving a gift and creating a memory.</p>
        
        <div class="cta">
            <i class="fas fa-gift"></i>
            <h3>Make Your Gift Special</h3>
            <p>Add a personal voice message to any gift in {city}</p>
            <a href="https://sayplay.co.uk">
                Get Started with SayPlay
                <i class="fas fa-arrow-right"></i>
            </a>
        </div>
        
        <h2>Why Choose SayPlay</h2>
        
        <p><strong>No App Required:</strong> Works with any smartphone—iPhone or Android. Just tap and play.</p>
        
        <p><strong>Your Voice, Forever:</strong> Messages never expire. They can hear your voice whenever they want.</p>
        
        <p><strong>Perfect for Any Occasion:</strong> {gift_type['title']}, anniversaries, celebrations, or "just because" moments.</p>
        
        <p><strong>Privacy Protected:</strong> Your message is secure and can only be accessed by tapping the NFC sticker.</p>
        
        <p>Transform your next gift in {city} into an unforgettable memory. With SayPlay, you're not just giving a present—you're giving your voice, your emotion, and a moment that lasts forever.</p>
    </div>
</body>
</html>'''
            
            # Save page
            with open(seo_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            pages.append({
                'slug': slug,
                'title': f"{gift_type['title']} in {city}",
                'city': city,
                'category': gift_type['title'],
                'url': f"/seo/{slug}.html"
            })
    
    print(f"✅ Generated {len(pages)} SEO pages with full content")
    
    return pages


def create_seo_index(pages: List[Dict], output_dir: Path):
    """Create index page for all SEO pages"""
    
    print("📄 Creating SEO index page...")
    
    seo_dir = output_dir / 'web' / 'seo'
    
    # Group by city
    cities = {}
    for page in pages:
        city = page['city']
        if city not in cities:
            cities[city] = []
        cities[city].append(page)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gift Guides by Location | SayPlay</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.3);
        }}
        .logo {{
            font-size: 56px;
            font-weight: 800;
            color: #667eea;
            text-align: center;
            margin-bottom: 15px;
        }}
        .logo span {{ color: #FFD700; }}
        h1 {{
            text-align: center;
            color: #2d3748;
            font-size: 42px;
            margin-bottom: 15px;
            font-weight: 900;
        }}
        .subtitle {{
            text-align: center;
            color: #718096;
            font-size: 20px;
            margin-bottom: 50px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-bottom: 60px;
            flex-wrap: wrap;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 48px;
            font-weight: 800;
            color: #667eea;
        }}
        .stat-label {{
            color: #718096;
            font-size: 16px;
            margin-top: 8px;
        }}
        .city-section {{
            margin-bottom: 50px;
        }}
        .city-title {{
            color: #667eea;
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid #FFD700;
        }}
        .links-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        .link-card {{
            background: #f7fafc;
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s;
            text-decoration: none;
            display: block;
        }}
        .link-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
        }}
        .link-card h3 {{
            color: #2d3748;
            font-size: 20px;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        .link-card p {{
            color: #718096;
            font-size: 15px;
            margin: 0;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 30px 20px; }}
            .logo {{ font-size: 42px; }}
            h1 {{ font-size: 32px; }}
            .links-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Say<span>Play</span></div>
        <h1><i class="fas fa-map-marker-alt"></i> Gift Guides by Location</h1>
        <p class="subtitle">Find perfect personalized gifts in your city</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(cities)}</div>
                <div class="stat-label">UK Cities</div>
            </div>
            <div class="stat">
                <div class="stat-number">{len(pages)}</div>
                <div class="stat-label">Gift Guides</div>
            </div>
            <div class="stat">
                <div class="stat-number">5</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
'''
    
    # Add city sections
    for city in sorted(cities.keys()):
        html += f'''
        <div class="city-section">
            <h2 class="city-title">{city}</h2>
            <div class="links-grid">'''
        
        for page in sorted(cities[city], key=lambda x: x['category']):
            html += f'''
                <a href="{page['url']}" class="link-card">
                    <h3><i class="fas fa-gift"></i> {page['title']}</h3>
                    <p>Personalized voice message gifts</p>
                </a>'''
        
        html += '''
            </div>
        </div>'''
    
    html += '''
    </div>
</body>
</html>'''
    
    with open(seo_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ SEO index created at /seo")


def create_blog_index(topics: List[Dict], output_dir: Path):
    """Create index page for all blog articles"""
    
    print("📄 Creating blog index page...")
    
    blog_dir = output_dir / 'web' / 'blog'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gift Guide Blog | SayPlay</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 25px;
            padding: 50px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.3);
        }}
        .logo {{
            font-size: 56px;
            font-weight: 800;
            color: #667eea;
            text-align: center;
            margin-bottom: 15px;
        }}
        .logo span {{ color: #FFD700; }}
        h1 {{
            text-align: center;
            color: #2d3748;
            font-size: 42px;
            margin-bottom: 15px;
            font-weight: 900;
        }}
        .subtitle {{
            text-align: center;
            color: #718096;
            font-size: 20px;
            margin-bottom: 60px;
        }}
        .articles-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
        }}
        .article-card {{
            background: #f7fafc;
            border-radius: 20px;
            overflow: hidden;
            border: 2px solid #e0e0e0;
            transition: all 0.3s;
            text-decoration: none;
            display: block;
        }}
        .article-card:hover {{
            border-color: #667eea;
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        }}
        .article-header {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            position: relative;
        }}
        .episode-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(255,255,255,0.25);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 700;
        }}
        .article-card h3 {{
            color: white;
            font-size: 24px;
            margin: 0;
            font-weight: 800;
            line-height: 1.3;
        }}
        .article-body {{
            padding: 30px;
        }}
        .article-meta {{
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            font-size: 15px;
            color: #718096;
        }}
        .article-meta span {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .article-excerpt {{
            color: #4a5568;
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 20px;
        }}
        .read-more {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: #667eea;
            font-weight: 700;
            font-size: 16px;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 30px 20px; }}
            .articles-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Say<span>Play</span></div>
        <h1><i class="fas fa-newspaper"></i> Gift Guide Blog</h1>
        <p class="subtitle">Expert tips and ideas for perfect personalized gifts</p>
        
        <div class="articles-grid">'''
    
    for i, topic in enumerate(topics, 1):
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        
        excerpt = f"Discover the best {topic['keyword']} that create lasting memories. Learn how to choose meaningful gifts and add a personal touch."
        
        html += f'''
            <a href="/blog/{slug}.html" class="article-card">
                <div class="article-header">
                    <div class="episode-badge">Episode {i}</div>
                    <h3>{topic['title']}</h3>
                </div>
                <div class="article-body">
                    <div class="article-meta">
                        <span><i class="fas fa-tag"></i> {topic['category']}</span>
                        <span><i class="far fa-clock"></i> 8 min read</span>
                    </div>
                    <p class="article-excerpt">{excerpt}</p>
                    <span class="read-more">
                        Read Full Article
                        <i class="fas fa-arrow-right"></i>
                    </span>
                </div>
            </a>'''
    
    html += '''
        </div>
    </div>
</body>
</html>'''
    
    with open(blog_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Blog index created at /blog")


def create_rss_feed(podcasts: List[Dict], output_file: Path):
    """Generate RSS feed for podcasts"""
    
    if not podcasts:
        return
    
    print(f"\n📡 Generating RSS feed...")
    
    from xml.etree.ElementTree import Element, SubElement, tostring
    from xml.dom import minidom
    
    rss = Element('rss', {'version': '2.0', 'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'})
    channel = SubElement(rss, 'channel')
    
    SubElement(channel, 'title').text = 'SayPlay Gift Guide Podcast'
    SubElement(channel, 'description').text = 'Your daily guide to finding perfect personalized gifts with expert tips and ideas.'
    SubElement(channel, 'link').text = 'https://dashboard.sayplay.co.uk'
    SubElement(channel, 'language').text = 'en-GB'
    SubElement(channel, 'itunes:author').text = 'SayPlay - VoiceGift UK'
    SubElement(channel, 'itunes:summary').text = 'Expert gift-giving advice and inspiration'
    
    for podcast in podcasts:
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = podcast['title']
        SubElement(item, 'description').text = f"Episode {podcast['episode']}: {podcast['title']}"
        SubElement(item, 'enclosure', {
            'url': f"https://dashboard.sayplay.co.uk/podcasts/{podcast['filename']}",
            'length': str(podcast['size']),
            'type': 'audio/mpeg'
        })
        SubElement(item, 'itunes:duration').text = str(podcast['duration'])
        SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    xml_string = minidom.parseString(tostring(rss, 'utf-8')).toprettyxml(indent='  ')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_string)
    
    print(f"✅ RSS feed generated ({len(podcasts)} episodes)")


async def main():
    print("\n" + "="*70)
    print("TITAN V2 - COMPLETE PROFESSIONAL SYSTEM")
    print("="*70)
    
    start_time = datetime.now()
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    # Create structure
    web_dir = output_dir / 'web'
    blog_dir = web_dir / 'blog'
    dashboard_dir = web_dir / 'dashboard'
    podcast_dir = web_dir / 'podcasts'
    seo_dir = web_dir / 'seo'
    
    for d in [web_dir, blog_dir, dashboard_dir, podcast_dir, seo_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Initialize
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    image_gen = ProfessionalImageGenerator()
    podcast_gen = LongFormPodcastGenerator()
    
    podcasts_list = []
    
    # Generate content for each topic
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"TOPIC {i}/10: {topic['title']}")
        print(f"{'='*70}")
        
        # Generate article
        print("  📝 Generating article...")
        article = generate_article_with_gemini(topic, gemini_key)
        
        # Generate hero image
        hero_image = image_gen.generate_hero_image(topic['keyword'])
        hero_base64 = base64.b64encode(hero_image).decode('utf-8')
        
        # Create HTML
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        html = create_professional_html(article, topic, hero_base64, slug)
        
        with open(blog_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Generate podcast
        if EDGE_TTS_AVAILABLE:
            try:
                podcast = await podcast_gen.generate_podcast(article, topic, i)
                if podcast:
                    podcast_filename = f'episode-{i:02d}-{slug[:30]}.mp3'
                    podcast_file = podcast_dir / podcast_filename
                    
                    with open(podcast_file, 'wb') as f:
                        f.write(podcast['audio'])
                    
                    podcasts_list.append({
                        'title': topic['title'],
                        'episode': i,
                        'filename': podcast_filename,
                        'size': len(podcast['audio']),
                        'duration': podcast['duration']
                    })
            except Exception as e:
                print(f"      ⚠️ Podcast error: {str(e)[:100]}")
        
        print(f"  ✅ Complete")
    
    # Generate SEO pages
    seo_pages = generate_seo_pages(output_dir)
    
    # Create index pages
    create_blog_index(topics, output_dir)
    create_seo_index(seo_pages, output_dir)
    
    # Create RSS feed
    if podcasts_list:
        create_rss_feed(podcasts_list, web_dir / 'podcast.xml')
    
    # Create dashboard
    print(f"\n{'='*70}")
    print("CREATING DASHBOARD")
    print(f"{'='*70}")
    
    dashboard_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Content Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 25px; padding: 50px; box-shadow: 0 25px 70px rgba(0,0,0,0.3); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 50px; padding-bottom: 25px; border-bottom: 3px solid #e0e0e0; }}
        .logo {{ font-size: 56px; font-weight: 800; color: #667eea; }}
        .logo span {{ color: #FFD700; }}
        .date {{ color: #718096; font-size: 18px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 50px 0; }}
        .stat {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 35px; border-radius: 20px; text-align: center; transition: transform 0.3s; }}
        .stat:hover {{ transform: translateY(-8px); }}
        .stat i {{ font-size: 56px; margin-bottom: 20px; }}
        .stat-number {{ font-size: 64px; font-weight: 900; margin: 15px 0; }}
        .stat-label {{ font-size: 18px; opacity: 0.95; }}
        .section {{ margin: 60px 0; }}
        .section-title {{ color: #2d3748; font-size: 36px; font-weight: 900; margin-bottom: 30px; display: flex; align-items: center; gap: 15px; }}
        .quick-links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }}
        .quick-link {{ background: #f7fafc; padding: 30px; border-radius: 20px; border: 2px solid #e0e0e0; text-decoration: none; display: block; transition: all 0.3s; }}
        .quick-link:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15); }}
        .quick-link h3 {{ color: #2d3748; font-size: 22px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }}
        .quick-link p {{ color: #718096; font-size: 16px; margin: 0; }}
        @media (max-width: 768px) {{ .container {{ padding: 30px 20px; }} .header {{ flex-direction: column; gap: 20px; text-align: center; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Say<span>Play</span> Dashboard</div>
            <div class="date">{datetime.now().strftime("%B %d, %Y %H:%M UTC")}</div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <i class="fas fa-file-alt"></i>
                <div class="stat-number">{len(topics)}</div>
                <div class="stat-label">Blog Articles</div>
            </div>
            <div class="stat">
                <i class="fas fa-microphone-alt"></i>
                <div class="stat-number">{len(podcasts_list)}</div>
                <div class="stat-label">Podcasts</div>
            </div>
            <div class="stat">
                <i class="fas fa-search-location"></i>
                <div class="stat-number">{len(seo_pages)}</div>
                <div class="stat-label">SEO Pages</div>
            </div>
            <div class="stat">
                <i class="fas fa-check-circle"></i>
                <div class="stat-number">✓</div>
                <div class="stat-label">System Active</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">
                <i class="fas fa-link"></i>
                Quick Links
            </h2>
            <div class="quick-links">
                <a href="/blog" class="quick-link">
                    <h3><i class="fas fa-newspaper"></i> View All Articles</h3>
                    <p>{len(topics)} professional blog posts</p>
                </a>
                <a href="/seo" class="quick-link">
                    <h3><i class="fas fa-map-marked-alt"></i> View SEO Pages</h3>
                    <p>{len(seo_pages)} location-based landing pages</p>
                </a>
                <a href="/podcast.xml" class="quick-link">
                    <h3><i class="fas fa-rss"></i> Podcast RSS Feed</h3>
                    <p>{len(podcasts_list)} episodes available</p>
                </a>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">
                <i class="fas fa-chart-line"></i>
                Performance
            </h2>
            <div style="background: #f7fafc; padding: 40px; border-radius: 20px;">
                <p style="font-size: 18px; color: #4a5568; line-height: 1.8; margin: 0;">
                    <strong>Content generated:</strong> {len(topics)} unique articles with professional images<br>
                    <strong>Podcasts created:</strong> {len(podcasts_list)} episodes (3-5 min each)<br>
                    <strong>SEO coverage:</strong> {len(seo_pages)} location-specific pages<br>
                    <strong>Total files:</strong> {len(topics) + len(podcasts_list) + len(seo_pages) + 3}<br>
                    <strong>Generation time:</strong> {int((datetime.now() - start_time).total_seconds() / 60)} minutes
                </p>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open(dashboard_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    # Final summary
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print("TITAN COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ {len(topics)} Articles (full content with images)")
    print(f"✅ {len(podcasts_list)} Podcasts (3-5 min each)")
    print(f"✅ {len(seo_pages)} SEO Pages (full content)")
    print(f"✅ 3 Index Pages (blog, seo, dashboard)")
    print(f"✅ 1 RSS Feed")
    print(f"\n⏱ Duration: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"\n🌐 Will be live at: https://dashboard.sayplay.co.uk")
    print(f"{'='*70}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
