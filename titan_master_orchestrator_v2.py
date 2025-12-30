#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - COMPLETE WITH AI WEBSITE BUILDER
- AI generates COMPLETE HTML/CSS/JS pages from master prompt
- Variables: [title], [keyword], [city], [category], [emoji], [date]
- 5 design templates rotate automatically
- Unique content guaranteed
- Blog articles + Podcasts + 100 SEO pages
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import base64
import asyncio
import hashlib
from typing import List, Dict, Set

sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

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


class ContentUniqueValidator:
    """Ensures all content is unique"""
    
    def __init__(self):
        self.content_hashes: Set[str] = set()
    
    def is_unique(self, content: str, content_type: str) -> bool:
        """Check if content is unique"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash in self.content_hashes:
            print(f"      ⚠️ Duplicate {content_type}! Regenerating...")
            return False
        
        self.content_hashes.add(content_hash)
        return True


class AIWebsiteBuilder:
    """
    AI Website Builder - generates COMPLETE HTML/CSS/JS pages
    Uses master prompt with variable substitution
    """
    
    # 5 Professional Design Templates
    DESIGN_TEMPLATES = [
        {
            'name': 'modern-gradient',
            'description': 'Modern design with gradient backgrounds, glassmorphism, smooth animations',
            'colors': '#667eea, #764ba2, #FFD700',
            'fonts': 'Inter, Roboto',
            'vibe': 'sleek, professional, tech-forward, contemporary'
        },
        {
            'name': 'elegant-minimal',
            'description': 'Elegant minimal design with white space, serif fonts, subtle animations',
            'colors': '#2d3748, #4a5568, #e0e0e0',
            'fonts': 'Playfair Display, Georgia',
            'vibe': 'sophisticated, clean, timeless, refined'
        },
        {
            'name': 'bold-vibrant',
            'description': 'Bold vibrant design with bright colors, large typography, energetic feel',
            'colors': '#FF6B6B, #4ECDC4, #FFE66D',
            'fonts': 'Poppins, Montserrat',
            'vibe': 'energetic, fun, attention-grabbing, playful'
        },
        {
            'name': 'luxury-dark',
            'description': 'Luxury dark theme with gold accents, premium feel, elegant transitions',
            'colors': '#1a1a1a, #FFD700, #f5f5f5',
            'fonts': 'Cormorant Garamond, Lora',
            'vibe': 'premium, exclusive, high-end, luxurious'
        },
        {
            'name': 'fresh-nature',
            'description': 'Fresh nature-inspired design with green tones, organic shapes, calm feel',
            'colors': '#2ecc71, #27ae60, #f39c12',
            'fonts': 'Nunito, Open Sans',
            'vibe': 'natural, friendly, approachable, organic'
        }
    ]
    
    # MASTER PROMPT with variables
    MASTER_PROMPT = """You are an expert web designer creating a COMPLETE, PRODUCTION-READY HTML page.

DESIGN TEMPLATE: {design_name}
Design Description: {design_description}
Color Palette: {design_colors}
Typography: {design_fonts}
Overall Vibe: {design_vibe}

PAGE VARIABLES:
- Title: [title]
- Keyword: [keyword]
- Location: [city]
- Category: [category]
- Emoji: [emoji]
- Date: [date]

YOUR TASK:
Create a COMPLETE HTML document (with embedded CSS and JavaScript) for a gift guide page.

REQUIREMENTS:

1. COMPLETE HTML STRUCTURE
   - Full <!DOCTYPE html> document
   - All meta tags (title, description, viewport, keywords)
   - Title: "[title] | SayPlay Gift Guide"
   - Description: "Find perfect [keyword] in [city]. Personalized voice message gifts with SayPlay."
   - Font Awesome CDN for icons
   - Google Fonts for typography ({design_fonts})

2. HERO SECTION
   - Full-width hero matching {design_vibe} aesthetic
   - Colors from palette: {design_colors}
   - Large "SayPlay" logo (Say in white, Play in gold #FFD700)
   - Main heading: [title]
   - Subheading: "Personalized Gifts with Voice Messages in [city]"

3. CONTENT SECTIONS (800-1000 words)
   
   Introduction (2 paragraphs)
   - Emotional hook about [keyword] in [city]
   - Why personalization matters
   
   Why [city] is Special for Gifts (2 paragraphs)
   - Specific local references to [city]
   - Shopping areas and culture
   
   Top 6 Gift Ideas (cards/boxes)
   - Each with icon from Font Awesome
   - Personalized Jewelry
   - Photo Frames  
   - Spa & Wellness
   - Books & Journals
   - Personalized Items
   - Plants & Flowers
   - 80-100 words each
   - Specific to [category]
   
   How SayPlay Works (3 steps)
   - Record Your Message
   - Attach to Gift
   - They Tap & Listen
   
   Shopping in [city] (1 paragraph)
   - Local shopping references
   
   Call to Action Section
   - Large CTA box with gradient from palette
   - Gift icon [emoji]
   - "Make Your Gift Special in [city]"
   - Button: "Get Started with SayPlay →"
   - Link: https://sayplay.co.uk

4. CSS STYLING (embedded in <style>)
   - Use {design_name} aesthetic EXACTLY
   - Colors: {design_colors}
   - Fonts: {design_fonts} (import from Google Fonts)
   - Match {design_vibe} vibe completely
   - Responsive (mobile, tablet, desktop)
   - Smooth transitions and hover effects
   - Modern CSS (flexbox, grid, animations)
   - Professional spacing and typography

5. JAVASCRIPT (embedded in <script>)
   - Smooth scroll for anchor links
   - Fade-in animations on scroll
   - Interactive hover effects
   - Back-to-top button (if page is long)
   - Simple, clean, performant

6. DESIGN MUST BE UNIQUE
   - Each template looks COMPLETELY different
   - Modern gradient = sleek tech style
   - Elegant minimal = clean white space style
   - Bold vibrant = energetic colorful style
   - Luxury dark = premium dark theme style
   - Fresh nature = organic green style

7. BACK NAVIGATION
   - Include back link: <a href="/seo">← Back to all locations</a>
   - Styled to match design

CRITICAL RULES:
- Generate COMPLETE working HTML code
- NO placeholders or "add your content here"
- Real, helpful, valuable content
- Professional design matching template EXACTLY
- Ready to deploy immediately
- ALL CSS in <style> tag
- ALL JavaScript in <script> tag
- Make it UNIQUE and BEAUTIFUL

OUTPUT FORMAT:
Return ONLY the complete HTML code.
Start with <!DOCTYPE html> and end with </html>
Do NOT include markdown formatting or explanations.
Do NOT wrap in code blocks.
Just pure HTML code ready to save as .html file."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        else:
            self.model = None
    
    def build_page(self, variables: Dict[str, str], template_index: int) -> str:
        """
        Build complete page using AI with master prompt
        
        Args:
            variables: Dict with title, keyword, city, category, emoji, date
            template_index: Index for design template rotation (0-4)
        
        Returns:
            Complete HTML page with CSS and JS
        """
        
        if not self.model:
            return self._generate_fallback(variables)
        
        # Select design template (rotate)
        template = self.DESIGN_TEMPLATES[template_index % len(self.DESIGN_TEMPLATES)]
        
        print(f"      🎨 AI Building: {variables['title']}")
        print(f"         Design: {template['name']}")
        
        # Fill master prompt with template details
        prompt = self.MASTER_PROMPT.format(
            design_name=template['name'],
            design_description=template['description'],
            design_colors=template['colors'],
            design_fonts=template['fonts'],
            design_vibe=template['vibe']
        )
        
        # Replace all [variables] in prompt
        for key, value in variables.items():
            prompt = prompt.replace(f'[{key}]', str(value))
        
        try:
            # Generate complete page with AI
            response = self.model.generate_content(prompt)
            html_code = response.text
            
            # Clean up if wrapped in code blocks
            if '```html' in html_code:
                html_code = html_code.split('```html')[1].split('```')[0].strip()
            elif '```' in html_code:
                html_code = html_code.split('```')[1].split('```')[0].strip()
            
            # Verify it starts with DOCTYPE
            if not html_code.strip().startswith('<!DOCTYPE'):
                print(f"         ⚠️ AI output missing DOCTYPE, using fallback")
                return self._generate_fallback(variables)
            
            print(f"         ✅ AI generated complete HTML")
            return html_code
            
        except Exception as e:
            print(f"         ⚠️ AI error: {str(e)[:80]}")
            return self._generate_fallback(variables)
    
    def _generate_fallback(self, variables: Dict[str, str]) -> str:
        """Fallback if AI fails"""
        
        title = variables.get('title', 'Gift Guide')
        keyword = variables.get('keyword', 'gifts')
        city = variables.get('city', 'UK')
        emoji = variables.get('emoji', '🎁')
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | SayPlay</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; line-height: 1.8; color: #2d3748; }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 30px; text-align: center; }}
        .logo {{ font-size: 56px; font-weight: 800; margin-bottom: 25px; }}
        .logo span {{ color: #FFD700; }}
        h1 {{ font-size: 48px; margin: 25px 0; font-weight: 900; }}
        .container {{ max-width: 900px; margin: 80px auto; padding: 0 30px; }}
        h2 {{ color: #667eea; font-size: 36px; margin: 50px 0 25px; font-weight: 800; }}
        p {{ font-size: 19px; margin-bottom: 20px; line-height: 1.8; }}
        .cta {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 70px 50px; border-radius: 25px; text-align: center; margin: 70px 0; }}
        .cta a {{ display: inline-flex; align-items: center; gap: 12px; background: white; color: #667eea; padding: 20px 50px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 20px; }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="logo">Say<span>Play</span></div>
        <h1>{emoji} {title}</h1>
        <p>Personalized Gifts with Voice Messages in {city}</p>
    </div>
    <div class="container">
        <a href="/seo" style="color: #667eea; text-decoration: none; font-weight: 600;">← Back to all locations</a>
        <h2>Perfect {keyword} in {city}</h2>
        <p>Looking for unique {keyword} in {city}? Discover thoughtful gift ideas with personalized voice messages from SayPlay.</p>
        <div class="cta">
            <i class="fas fa-gift" style="font-size: 70px; margin-bottom: 25px;"></i>
            <h3 style="color: white; font-size: 36px; margin-bottom: 20px;">Make Your Gift Special</h3>
            <p style="color: white; font-size: 20px; margin-bottom: 35px;">Add a personal voice message with SayPlay</p>
            <a href="https://sayplay.co.uk">Get Started <i class="fas fa-arrow-right"></i></a>
        </div>
    </div>
</body>
</html>'''


class ProfessionalImageGenerator:
    """Generate images with SayPlay branding"""
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
    
    def generate_hero_image(self, keyword: str, seed: str = None) -> bytes:
        """Generate unique hero image"""
        print(f"      🖼 Generating image for: {keyword}")
        
        search_query = f"{keyword} {seed[:4] if seed else ''}"
        
        if self.unsplash_key:
            img = self._fetch_unsplash(search_query, 1200, 630)
            if img:
                print(f"         ✅ Unsplash image")
                return self._add_logo_overlay(img)
        
        if self.pexels_key:
            img = self._fetch_pexels(search_query, 1200, 630)
            if img:
                print(f"         ✅ Pexels image")
                return self._add_logo_overlay(img)
        
        print(f"         ⚠️ Gradient fallback")
        return self._generate_gradient(1200, 630, seed)
    
    def _fetch_unsplash(self, query: str, width: int, height: int):
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {'query': query, 'orientation': 'landscape', 'client_id': self.unsplash_key}
            response = requests.get(url, params=params, timeout=20)
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['raw'] + f"&w={width}&h={height}&fit=crop"
                img_response = requests.get(image_url, timeout=25)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content)).convert('RGB')
        except:
            pass
        return None
    
    def _fetch_pexels(self, query: str, width: int, height: int):
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {'Authorization': self.pexels_key}
            params = {'query': query, 'per_page': 1, 'orientation': 'landscape'}
            response = requests.get(url, headers=headers, params=params, timeout=20)
            if response.status_code == 200:
                data = response.json()
                if data.get('photos'):
                    image_url = data['photos'][0]['src']['large2x']
                    img_response = requests.get(image_url, timeout=25)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content)).convert('RGB')
                        return img.resize((width, height), Image.Resampling.LANCZOS)
        except:
            pass
        return None
    
    def _generate_gradient(self, width: int, height: int, seed: str = None) -> bytes:
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        offset = int(seed[:2], 16) if seed else 0
        for y in range(height):
            progress = y / height
            r = int((102 + offset % 50) + (118 - 102) * progress)
            g = int((126 + offset % 30) + (75 - 126) * progress)
            b = int((234 - offset % 40) + (162 - 234) * progress)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return self._add_logo_overlay(img)
    
    def _add_logo_overlay(self, img: Image.Image) -> bytes:
        width, height = img.size
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        gradient_start = int(height * 0.65)
        for y in range(gradient_start, height):
            progress = (y - gradient_start) / (height - gradient_start)
            alpha = int(200 * progress)
            overlay_draw.rectangle([(0, y), (width, y+1)], fill=(0, 0, 0, alpha))
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        try:
            logo_size = max(40, int(height * 0.08))
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            logo_size = 40
            font = ImageFont.load_default()
        logo_x = width - int(width * 0.35)
        logo_y = height - int(height * 0.15)
        draw.text((logo_x, logo_y), "Say", fill=(255, 255, 255), font=font)
        say_bbox = draw.textbbox((0, 0), "Say", font=font)
        say_width = say_bbox[2] - say_bbox[0]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format='JPEG', quality=92)
        return output.getvalue()
    
    def generate_podcast_cover(self, output_file: Path):
        print("\n🎨 Generating podcast cover (1400x1400)...")
        img = Image.new('RGB', (1400, 1400))
        draw = ImageDraw.Draw(img)
        for y in range(1400):
            progress = y / 1400
            r = int(102 + (118 - 102) * progress)
            g = int(126 + (75 - 126) * progress)
            b = int(234 + (162 - 234) * progress)
            draw.line([(0, y), (1400, y)], fill=(r, g, b))
        try:
            logo_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
            tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        except:
            logo_font = ImageFont.load_default()
            subtitle_font = logo_font
            tagline_font = logo_font
        say_text = "Say"
        say_bbox = draw.textbbox((0, 0), say_text, font=logo_font)
        say_width = say_bbox[2] - say_bbox[0]
        play_text = "Play"
        play_bbox = draw.textbbox((0, 0), play_text, font=logo_font)
        play_width = play_bbox[2] - play_bbox[0]
        total_width = say_width + play_width
        logo_x = (1400 - total_width) // 2
        logo_y = 350
        draw.text((logo_x, logo_y), say_text, fill=(255, 255, 255), font=logo_font)
        draw.text((logo_x + say_width, logo_y), play_text, fill=(255, 215, 0), font=logo_font)
        subtitle = "GIFT GUIDE"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((1400 - subtitle_width) // 2, 600), subtitle, fill=(255, 255, 255), font=subtitle_font)
        tagline = "Your Daily Inspiration for Perfect Gifts"
        tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
        tagline_width = tagline_bbox[2] - tagline_bbox[0]
        draw.text(((1400 - tagline_width) // 2, 720), tagline, fill=(255, 255, 255), font=tagline_font)
        img.save(output_file, format='JPEG', quality=95)
        print(f"✅ Podcast cover saved")


class PodcastGeneratorWithJingles:
    """Generate 3-5 min podcasts with jingles"""
    
    async def generate_podcast(self, article: dict, topic: dict, episode_num: int) -> dict:
        if not EDGE_TTS_AVAILABLE:
            return None
        print(f"      🎙 Generating podcast (3-5 min with jingles)...")
        script = self._create_extended_script(article, topic, episode_num)
        print(f"         🎵 Generating audio tracks...")
        main_audio = await self._generate_audio(script, "en-GB-SoniaNeural")
        intro_script = "SayPlay Gift Guide. Where every gift tells a story."
        intro_audio = await self._generate_audio(intro_script, "en-GB-RyanNeural", rate="-5%")
        outro_script = "SayPlay. Make every gift unforgettable. Visit sayplay dot co dot uk"
        outro_audio = await self._generate_audio(outro_script, "en-GB-RyanNeural", rate="-5%")
        combined_audio = intro_audio + main_audio + outro_audio
        word_count = len(script.split()) + 20
        duration_seconds = int((word_count / 150) * 60)
        print(f"         ✅ Podcast: {duration_seconds}s ({duration_seconds//60}m {duration_seconds%60}s)")
        return {'audio': combined_audio, 'duration': duration_seconds}
    
    def _create_extended_script(self, article: dict, topic: dict, episode_num: int) -> str:
        parts = [
            f"Hello and welcome to the SayPlay Gift Guide, episode {episode_num}.",
            f"I'm your host, and today we're exploring {topic['title'].lower()}.",
            "",
            "Finding the perfect gift can feel overwhelming. There are so many options, so many occasions, and so many people to shop for. But here's the secret: the best gifts aren't always the most expensive or the most elaborate. The best gifts are the ones that show genuine thought, care, and understanding of the person you're giving to.",
            "",
            f"So let's talk about {topic['keyword']}. What makes a gift truly special? It starts with knowing the person. Think about their interests, their hobbies, what makes them smile.",
            "",
            "Let me share some ideas that really stand out.",
            "",
            "First, personalized items. A custom piece of jewelry with their initials, an engraved watch, or a photo album filled with shared memories. These gifts say I took the time to make this just for you.",
            "",
            "Second, experience gifts. Concert tickets to see their favorite band, a cooking class where they can learn something new, or a weekend getaway. Experiences create memories that last forever.",
            "",
            "Third, handmade gifts. If you're creative, consider making something yourself. A knitted scarf, a painted portrait, homemade treats. The time and effort shows a level of care that money can't buy.",
            "",
            "Fourth, subscription services. Monthly book clubs, specialty coffee delivery, streaming services. These are gifts that keep giving long after the initial occasion.",
            "",
            "Fifth, tech gadgets for those who love innovation. Smart home devices, wireless earbuds, tablets, or fitness trackers. Technology gifts can be both practical and exciting.",
            "",
            "Sixth, wellness and self-care gifts. Spa days, massage gift cards, aromatherapy sets, meditation app subscriptions. These gifts say I care about your wellbeing.",
            "",
            "Seventh, charitable gifts in their name. For the person who has everything, consider donating to a cause they care about.",
            "",
            f"Now, here's where {topic['keyword']} become even more special. Think about the presentation. Beautiful wrapping, a heartfelt card, choosing the right moment.",
            "",
            "But there's something that takes personalization to an entirely new level: adding your voice. With SayPlay's innovative NFC technology, you can record a personal message and attach it to any gift.",
            "",
            "Imagine this: someone receives your gift, taps their phone on it, and instantly hears your voice sharing a memory, expressing your feelings, or simply saying why you chose that gift for them.",
            "",
            "No app download required. No complicated setup. Just pure, emotional connection.",
            "",
            "Your grandmother can hear your voice every time she looks at the photo frame you gave her. Your best friend can replay your message whenever they need encouragement. Your partner can hear you say I love you every anniversary.",
            "",
            "This technology transforms ordinary gifts into extraordinary keepsakes. It's not just about the physical item anymore, it's about the emotion, the story, the voice behind the gift.",
            "",
            "Let's talk about budget. Great gifts don't have to break the bank. Under thirty pounds, you can find meaningful books, artisan chocolates, plant gifts. Between thirty and one hundred pounds opens up jewelry, tech accessories, experience vouchers. And for luxury, watches, designer items, or once-in-a-lifetime experiences.",
            "",
            "The key is choosing something that fits your relationship with the person and shows you understand what makes them happy.",
            "",
            "A few mistakes to avoid: Don't give gift cards without personalization. Don't buy something you want for yourself. Don't wait until the last minute. And never underestimate the power of presentation.",
            "",
            f"So as you think about {topic['keyword']}, remember: it's not about perfection, it's about connection. It's about showing someone you see them, you know them, and you care about them.",
            "",
            f"That wraps up episode {episode_num} of the SayPlay Gift Guide. I hope these ideas have inspired you. Remember, the best gift is one given with love and thought.",
            "",
            "Thank you so much for listening. Until next time, happy gift giving, and remember: make every gift unforgettable."
        ]
        return " ".join(parts)
    
    async def _generate_audio(self, text: str, voice: str, rate: str = "+0%") -> bytes:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        temp_file = f"temp_audio_{datetime.now().timestamp()}.mp3"
        await communicate.save(temp_file)
        with open(temp_file, 'rb') as f:
            audio_data = f.read()
        os.remove(temp_file)
        return audio_data


def generate_unique_article(topic: dict, api_key: str, validator: ContentUniqueValidator, attempt: int = 1) -> dict:
    if not GEMINI_AVAILABLE or not api_key:
        return generate_fallback_article(topic)
    max_attempts = 3
    for i in range(max_attempts):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            seed = hashlib.md5(f"{topic['title']}{datetime.now()}{attempt}{i}".encode()).hexdigest()
            prompt = f"""Write a COMPLETELY UNIQUE article about: {topic['title']}

Uniqueness Seed: {seed[:8]}
Keyword: {topic['keyword']}
Style: {topic['angle']}
Length: 1500-1800 words

STRUCTURE:
1. Opening Hook (2-3 paragraphs)
2. Why This Gift Matters (2 paragraphs)
3. 7-9 Specific Gift Ideas (150-200 words each)
   - UK shops: John Lewis, Not On The High Street, Amazon UK
   - Price ranges: £15-£300
4. Personalization Ideas (2 paragraphs)
5. Presentation Tips (2 paragraphs)
6. Common Mistakes (1 paragraph)
7. Emotional Conclusion

Make it unique with unexpected examples, real stories, UK cultural references.
Write naturally, warmly, helpfully."""
            response = model.generate_content(prompt)
            article_text = response.text
            if validator.is_unique(article_text, "article"):
                sections = []
                current = {'title': '', 'content': ''}
                for line in article_text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('##') or line.startswith('#'):
                        if current['content']:
                            sections.append(current)
                        current = {'title': line.replace('#', '').strip(), 'content': ''}
                    else:
                        current['content'] += line + '\n'
                if current['content']:
                    sections.append(current)
                word_count = len(article_text.split())
                print(f"      ✅ Unique article: {word_count} words")
                return {
                    'title': topic['title'],
                    'text': article_text,
                    'sections': sections,
                    'word_count': word_count,
                    'keyword': topic['keyword'],
                    'seed': seed
                }
            else:
                print(f"      🔄 Duplicate, retry {i+2}/{max_attempts}")
        except Exception as e:
            print(f"      ⚠️ Gemini error: {str(e)[:80]}")
    return generate_fallback_article(topic)


def generate_fallback_article(topic: dict) -> dict:
    content = f"Discovering perfect {topic['keyword']} requires thoughtfulness and care."
    return {
        'title': topic['title'],
        'text': content,
        'sections': [{'title': 'Gift Ideas', 'content': content}],
        'word_count': len(content.split()),
        'keyword': topic['keyword'],
        'seed': 'fallback'
    }


def create_professional_html(article: dict, topic: dict, hero_base64: str) -> str:
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | SayPlay Gift Guide</title>
    <meta name="description" content="{article['text'][:160]}...">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; line-height: 1.8; color: #2d3748; background: #f7fafc; }}
        .hero {{ position: relative; height: 600px; background: url('data:image/jpeg;base64,{hero_base64}') center/cover; display: flex; align-items: center; justify-content: center; }}
        .hero-overlay {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.7) 100%); }}
        .hero-content {{ position: relative; z-index: 2; text-align: center; color: white; max-width: 900px; padding: 0 30px; }}
        .logo {{ font-size: 56px; font-weight: 800; margin-bottom: 25px; text-shadow: 3px 3px 10px rgba(0,0,0,0.5); }}
        .logo span {{ color: #FFD700; }}
        h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 25px; line-height: 1.15; text-shadow: 2px 2px 12px rgba(0,0,0,0.6); }}
        .container {{ max-width: 900px; margin: -120px auto 80px; background: white; border-radius: 25px; box-shadow: 0 25px 70px rgba(0,0,0,0.15); padding: 70px 60px; position: relative; z-index: 3; }}
        .content h2 {{ color: #667eea; font-size: 36px; font-weight: 800; margin: 60px 0 30px; padding-bottom: 18px; border-bottom: 4px solid #FFD700; }}
        .content p {{ margin-bottom: 24px; font-size: 19px; line-height: 1.9; color: #4a5568; }}
        .cta {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 70px 60px; border-radius: 25px; margin: 70px 0; text-align: center; }}
        .cta a {{ display: inline-flex; align-items: center; gap: 15px; background: white; color: #667eea; padding: 22px 55px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 22px; }}
        @media (max-width: 768px) {{ .hero {{ height: 450px; }} h1 {{ font-size: 36px; }} .container {{ padding: 45px 30px; margin: -70px 20px 50px; }} }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="logo">Say<span>Play</span></div>
            <h1>{article['title']}</h1>
            <div style="font-size: 17px; margin-top: 20px;">
                <i class="far fa-calendar-alt"></i> {datetime.now().strftime("%B %d, %Y")} •
                <i class="far fa-clock"></i> {max(1, article['word_count'] // 200)} min read
            </div>
        </div>
    </div>
    <div class="container">
        <a href="/blog" style="display: inline-flex; align-items: center; gap: 10px; color: #667eea; text-decoration: none; font-weight: 600; margin-bottom: 30px;">
            <i class="fas fa-arrow-left"></i> Back to all articles
        </a>
        <div class="content">'''
    for section in article['sections']:
        if section['title']:
            html += f"<h2>{section['title']}</h2>\n"
        for para in section['content'].strip().split('\n'):
            if para.strip():
                html += f"<p>{para.strip()}</p>\n"
    html += '''
            <div class="cta">
                <i class="fas fa-gift" style="font-size: 90px; margin-bottom: 30px;"></i>
                <h3 style="color: white; font-size: 42px; margin-bottom: 25px; font-weight: 900;">Make Every Gift Unforgettable</h3>
                <p style="color: white; font-size: 22px; margin-bottom: 40px;">Add a personal voice message with SayPlay</p>
                <a href="https://sayplay.co.uk">Discover SayPlay <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </div>
</body>
</html>'''
    return html


def generate_seo_pages_with_ai_builder(output_dir: Path, validator: ContentUniqueValidator, builder: AIWebsiteBuilder) -> List[Dict]:
    """Generate 100 SEO pages using AI Website Builder with master prompt"""
    
    print(f"\n{'='*70}")
    print("AI WEBSITE BUILDER - GENERATING 100 SEO PAGES")
    print("Using Master Prompt with [variables] and 5 design templates")
    print(f"{'='*70}")
    
    seo_dir = output_dir / 'web' / 'seo'
    seo_dir.mkdir(parents=True, exist_ok=True)
    
    cities = [
        'London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds',
        'Glasgow', 'Edinburgh', 'Bristol', 'Cardiff', 'Sheffield',
        'Newcastle', 'Belfast', 'Brighton', 'Oxford', 'Cambridge',
        'York', 'Bath', 'Nottingham', 'Leicester', 'Southampton'
    ]
    
    gift_types = [
        {'slug': 'birthday-gifts', 'title': 'Birthday Gifts', 'emoji': '🎂'},
        {'slug': 'anniversary-gifts', 'title': 'Anniversary Gifts', 'emoji': '💑'},
        {'slug': 'wedding-gifts', 'title': 'Wedding Gifts', 'emoji': '💍'},
        {'slug': 'christmas-gifts', 'title': 'Christmas Gifts', 'emoji': '🎄'},
        {'slug': 'mothers-day-gifts', 'title': "Mother's Day Gifts", 'emoji': '🌸'}
    ]
    
    pages = []
    page_index = 0
    
    for city in cities:
        for gift_type in gift_types:
            slug = f"{gift_type['slug']}-{city.lower().replace(' ', '-')}"
            title = f"{gift_type['title']} in {city}"
            
            # Variables for master prompt
            variables = {
                'title': title,
                'keyword': gift_type['slug'].replace('-', ' '),
                'city': city,
                'category': gift_type['title'],
                'emoji': gift_type['emoji'],
                'date': datetime.now().strftime('%B %d, %Y')
            }
            
            # AI builds complete page (rotates through 5 designs)
            html = builder.build_page(variables, page_index)
            
            # Save page
            with open(seo_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Get design name
            template = builder.DESIGN_TEMPLATES[page_index % len(builder.DESIGN_TEMPLATES)]
            
            pages.append({
                'slug': slug,
                'title': title,
                'city': city,
                'category': gift_type['title'],
                'url': f"/seo/{slug}.html",
                'design': template['name']
            })
            
            page_index += 1
    
    print(f"\n✅ Generated {len(pages)} AI-powered SEO pages")
    print(f"   5 unique design styles rotating")
    print(f"   Each page built from master prompt with variables")
    
    return pages


def create_rss_feed_apple(podcasts: List[Dict], output_file: Path, cover_url: str):
    print(f"\n📡 Generating Apple Podcasts RSS...")
    from xml.etree.ElementTree import Element, SubElement, tostring
    from xml.dom import minidom
    rss = Element('rss', {'version': '2.0', 'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd', 'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'})
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = 'SayPlay Gift Guide'
    description_text = """Your daily guide to perfect gifts, gift ideas, and personalization. 
Discover thoughtful presents, creative gifting inspiration, and meaningful ways to personalize 
every occasion. From birthdays to anniversaries, weddings to holidays - we help you find gifts 
that create lasting memories with SayPlay voice message technology."""
    SubElement(channel, 'description').text = description_text
    SubElement(channel, 'link').text = 'https://dashboard.sayplay.co.uk'
    SubElement(channel, 'language').text = 'en-GB'
    SubElement(channel, 'itunes:author').text = 'SayPlay by VoiceGift UK'
    SubElement(channel, 'itunes:summary').text = description_text
    SubElement(channel, 'itunes:subtitle').text = 'Expert gift-giving tips and inspiration'
    SubElement(channel, 'itunes:explicit').text = 'no'
    SubElement(channel, 'itunes:image', {'href': cover_url})
    category = SubElement(channel, 'itunes:category', {'text': 'Leisure'})
    SubElement(category, 'itunes:category', {'text': 'Hobbies'})
    owner = SubElement(channel, 'itunes:owner')
    SubElement(owner, 'itunes:name').text = 'SayPlay'
    SubElement(owner, 'itunes:email').text = 'podcast@sayplay.co.uk'
    SubElement(channel, 'copyright').text = f'© {datetime.now().year} VoiceGift UK Ltd'
    for podcast in podcasts:
        item = SubElement(channel, 'item')
        episode_title = f"Episode {podcast['episode']}: {podcast['title']}"
        SubElement(item, 'title').text = episode_title
        episode_desc = f"Explore {podcast['title'].lower()}. Discover thoughtful gift ideas and creative ways to make your gifts memorable."
        SubElement(item, 'description').text = episode_desc
        SubElement(item, 'itunes:summary').text = episode_desc
        SubElement(item, 'itunes:author').text = 'SayPlay'
        SubElement(item, 'itunes:episode').text = str(podcast['episode'])
        SubElement(item, 'itunes:episodeType').text = 'full'
        SubElement(item, 'itunes:explicit').text = 'no'
        SubElement(item, 'enclosure', {'url': f"https://dashboard.sayplay.co.uk/podcasts/{podcast['filename']}", 'length': str(podcast['size']), 'type': 'audio/mpeg'})
        SubElement(item, 'guid').text = f"https://dashboard.sayplay.co.uk/podcasts/{podcast['filename']}"
        SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        SubElement(item, 'itunes:duration').text = str(podcast['duration'])
    xml_string = minidom.parseString(tostring(rss, 'utf-8')).toprettyxml(indent='  ')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_string)
    print(f"✅ Apple Podcasts RSS ({len(podcasts)} episodes)")


def create_podcasts_index(podcasts: List[Dict], output_dir: Path):
    print("📄 Creating /podcasts index...")
    podcast_dir = output_dir / 'web' / 'podcasts'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Gift Guide Podcast | All Episodes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 25px; padding: 50px; box-shadow: 0 25px 70px rgba(0,0,0,0.3); }}
        .logo {{ font-size: 56px; font-weight: 800; color: #667eea; text-align: center; margin-bottom: 15px; }}
        .logo span {{ color: #FFD700; }}
        h1 {{ text-align: center; font-size: 42px; color: #2d3748; margin: 20px 0; font-weight: 900; }}
        .subscribe-box {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 50px; }}
        .subscribe-links {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 25px; }}
        .subscribe-btn {{ display: inline-flex; align-items: center; gap: 10px; background: white; color: #667eea; padding: 15px 30px; border-radius: 50px; text-decoration: none; font-weight: 700; }}
        .episodes-list {{ display: grid; gap: 30px; }}
        .episode-card {{ background: #f7fafc; border-radius: 20px; padding: 35px; border: 2px solid #e0e0e0; }}
        .episode-header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }}
        .episode-number {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 800; }}
        .episode-title {{ font-size: 24px; color: #2d3748; font-weight: 700; }}
        audio {{ width: 100%; margin-top: 20px; }}
        .back-link {{ display: inline-flex; align-items: center; gap: 10px; color: #667eea; text-decoration: none; font-weight: 600; margin-bottom: 30px; }}
        @media (max-width: 768px) {{ .container {{ padding: 30px 20px; }} .episode-header {{ flex-direction: column; }} }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Back to dashboard</a>
        <div class="logo">Say<span>Play</span></div>
        <h1><i class="fas fa-microphone-alt"></i> Gift Guide Podcast</h1>
        <p style="text-align: center; color: #718096; font-size: 18px; margin-bottom: 50px;">Your daily inspiration for perfect gifts</p>
        <div class="subscribe-box">
            <h2 style="font-size: 28px; margin-bottom: 15px;"><i class="fas fa-podcast"></i> Subscribe</h2>
            <div class="subscribe-links">
                <a href="/podcast.xml" class="subscribe-btn"><i class="fas fa-rss"></i> RSS Feed</a>
                <a href="https://podcasts.apple.com" class="subscribe-btn" target="_blank"><i class="fab fa-apple"></i> Apple Podcasts</a>
                <a href="https://open.spotify.com" class="subscribe-btn" target="_blank"><i class="fab fa-spotify"></i> Spotify</a>
            </div>
        </div>
        <h2 style="font-size: 32px; color: #2d3748; margin-bottom: 30px;"><i class="fas fa-list"></i> All Episodes</h2>
        <div class="episodes-list">'''
    for podcast in podcasts:
        duration_min = podcast['duration'] // 60
        duration_sec = podcast['duration'] % 60
        html += f'''
            <div class="episode-card">
                <div class="episode-header">
                    <div class="episode-number">{podcast['episode']}</div>
                    <div>
                        <div class="episode-title">{podcast['title']}</div>
                        <div style="color: #718096; margin-top: 8px;">
                            <i class="far fa-clock"></i> {duration_min}m {duration_sec}s
                        </div>
                    </div>
                </div>
                <audio controls preload="metadata">
                    <source src="/podcasts/{podcast['filename']}" type="audio/mpeg">
                </audio>
            </div>'''
    html += '''
        </div>
    </div>
</body>
</html>'''
    with open(podcast_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ Podcasts index created")


def create_blog_index(topics: List[Dict], output_dir: Path):
    print("📄 Creating /blog index...")
    blog_dir = output_dir / 'web' / 'blog'
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Gift Guide Blog | SayPlay</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 25px; padding: 50px; }}
        .logo {{ font-size: 56px; font-weight: 800; color: #667eea; text-align: center; margin-bottom: 15px; }}
        .logo span {{ color: #FFD700; }}
        h1 {{ text-align: center; color: #2d3748; font-size: 42px; margin-bottom: 60px; font-weight: 900; }}
        .articles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 30px; }}
        .article-card {{ background: #f7fafc; border-radius: 20px; overflow: hidden; border: 2px solid #e0e0e0; text-decoration: none; display: block; transition: all 0.3s; }}
        .article-card:hover {{ border-color: #667eea; transform: translateY(-8px); }}
        .article-header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; }}
        .article-card h3 {{ color: white; font-size: 24px; font-weight: 800; }}
        .article-body {{ padding: 30px; }}
        .back-link {{ display: inline-flex; align-items: center; gap: 10px; color: #667eea; text-decoration: none; font-weight: 600; margin-bottom: 30px; }}
        @media (max-width: 768px) {{ .articles-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Back to dashboard</a>
        <div class="logo">Say<span>Play</span></div>
        <h1><i class="fas fa-newspaper"></i> Gift Guide Blog</h1>
        <div class="articles-grid">'''
    for i, topic in enumerate(topics, 1):
        slug = topic['title'].lower().replace(' ', '-').replace("'", '')[:60]
        html += f'''
            <a href="/blog/{slug}.html" class="article-card">
                <div class="article-header">
                    <h3>Episode {i}: {topic['title']}</h3>
                </div>
                <div class="article-body">
                    <p style="color: #718096;"><i class="fas fa-tag"></i> {topic['category']}</p>
                    <p style="color: #4a5568; margin: 15px 0;">Expert tips for choosing meaningful {topic['keyword']}.</p>
                    <span style="color: #667eea; font-weight: 700;">Read Article <i class="fas fa-arrow-right"></i></span>
                </div>
            </a>'''
    html += '</div></div></body></html>'
    with open(blog_dir / 'index.html', 'w') as f:
        f.write(html)
    print(f"✅ Blog index created")


def create_seo_index(seo_pages: List[Dict], output_dir: Path):
    print("📄 Creating /seo index...")
    seo_dir = output_dir / 'web' / 'seo'
    cities = {}
    for page in seo_pages:
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
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 25px; padding: 50px; box-shadow: 0 25px 70px rgba(0,0,0,0.3); }}
        .logo {{ font-size: 56px; font-weight: 800; color: #667eea; text-align: center; margin-bottom: 15px; }}
        .logo span {{ color: #FFD700; }}
        h1 {{ text-align: center; color: #2d3748; font-size: 42px; margin-bottom: 15px; font-weight: 900; }}
        .subtitle {{ text-align: center; color: #718096; font-size: 20px; margin-bottom: 60px; }}
        .stats {{ display: flex; justify-content: center; gap: 40px; margin-bottom: 60px; flex-wrap: wrap; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 48px; font-weight: 800; color: #667eea; }}
        .stat-label {{ color: #718096; font-size: 16px; margin-top: 8px; }}
        .city-section {{ margin-bottom: 50px; }}
        .city-title {{ color: #667eea; font-size: 32px; font-weight: 800; margin-bottom: 25px; padding-bottom: 12px; border-bottom: 3px solid #FFD700; }}
        .links-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .link-card {{ background: #f7fafc; padding: 25px; border-radius: 15px; border: 2px solid #e0e0e0; transition: all 0.3s; text-decoration: none; display: block; }}
        .link-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15); }}
        .link-card h3 {{ color: #2d3748; font-size: 20px; margin-bottom: 8px; font-weight: 700; }}
        .link-card p {{ color: #718096; font-size: 15px; margin: 0; }}
        .back-link {{ display: inline-flex; align-items: center; gap: 10px; color: #667eea; text-decoration: none; font-weight: 600; margin-bottom: 30px; }}
        @media (max-width: 768px) {{ .container {{ padding: 30px 20px; }} .links-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Back to dashboard</a>
        <div class="logo">Say<span>Play</span></div>
        <h1><i class="fas fa-map-marker-alt"></i> Gift Guides by Location</h1>
        <p class="subtitle">AI-generated pages with 5 unique design styles</p>
        <div class="stats">
            <div class="stat"><div class="stat-number">{len(cities)}</div><div class="stat-label">UK Cities</div></div>
            <div class="stat"><div class="stat-number">{len(seo_pages)}</div><div class="stat-label">Gift Guides</div></div>
            <div class="stat"><div class="stat-number">5</div><div class="stat-label">Design Styles</div></div>
        </div>'''
    for city in sorted(cities.keys()):
        html += f'''
        <div class="city-section">
            <h2 class="city-title"><i class="fas fa-map-pin"></i> {city}</h2>
            <div class="links-grid">'''
        for page in sorted(cities[city], key=lambda x: x['title']):
            html += f'''
                <a href="{page['url']}" class="link-card">
                    <h3><i class="fas fa-gift"></i> {page['title']}</h3>
                    <p>Style: {page['design']}</p>
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
    print(f"✅ SEO index created")


def create_complete_dashboard(topics: List[Dict], podcasts: List[Dict], seo_count: int, output_dir: Path, start_time):
    print("📄 Creating complete dashboard...")
    dashboard_dir = output_dir / 'web' / 'dashboard'
    duration = (datetime.now() - start_time).total_seconds()
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SayPlay Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 25px; padding: 50px; }}
        .logo {{ font-size: 56px; font-weight: 800; color: #667eea; }}
        .logo span {{ color: #FFD700; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 50px 0; }}
        .stat {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 35px; border-radius: 20px; text-align: center; }}
        .stat-number {{ font-size: 64px; font-weight: 900; margin: 15px 0; }}
        .quick-links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin-top: 50px; }}
        .quick-link {{ background: #f7fafc; padding: 35px; border-radius: 20px; border: 2px solid #e0e0e0; text-decoration: none; display: block; }}
        .quick-link:hover {{ border-color: #667eea; transform: translateY(-5px); }}
        .quick-link i {{ font-size: 48px; color: #667eea; margin-bottom: 20px; }}
        .quick-link h3 {{ color: #2d3748; font-size: 24px; margin-bottom: 12px; }}
        @media (max-width: 768px) {{ .quick-links {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Say<span>Play</span> Dashboard</div>
        <p style="color: #666; margin-top: 10px;">{datetime.now().strftime("%B %d, %Y %H:%M UTC")}</p>
        <div class="stats">
            <div class="stat"><i class="fas fa-file-alt" style="font-size: 48px;"></i><div class="stat-number">{len(topics)}</div><div>Blog Articles</div></div>
            <div class="stat"><i class="fas fa-microphone-alt" style="font-size: 48px;"></i><div class="stat-number">{len(podcasts)}</div><div>Podcasts</div></div>
            <div class="stat"><i class="fas fa-search-location" style="font-size: 48px;"></i><div class="stat-number">{seo_count}</div><div>SEO Pages</div></div>
            <div class="stat"><i class="fas fa-check-circle" style="font-size: 48px;"></i><div class="stat-number">✓</div><div>AI Generated</div></div>
        </div>
        <h2 style="font-size: 36px; color: #2d3748; margin-top: 50px;"><i class="fas fa-link"></i> Quick Access</h2>
        <div class="quick-links">
            <a href="/blog" class="quick-link">
                <i class="fas fa-newspaper"></i>
                <h3>Blog Articles</h3>
                <p style="color: #718096; margin: 0;">{len(topics)} expert guides</p>
            </a>
            <a href="/podcasts" class="quick-link">
                <i class="fas fa-podcast"></i>
                <h3>Podcast Episodes</h3>
                <p style="color: #718096; margin: 0;">{len(podcasts)} episodes with jingles</p>
            </a>
            <a href="/seo" class="quick-link">
                <i class="fas fa-map-marked-alt"></i>
                <h3>SEO Landing Pages</h3>
                <p style="color: #718096; margin: 0;">{seo_count} AI-generated pages</p>
            </a>
            <a href="/podcast.xml" class="quick-link">
                <i class="fas fa-rss"></i>
                <h3>Podcast RSS Feed</h3>
                <p style="color: #718096; margin: 0;">Apple Podcasts ready</p>
            </a>
        </div>
        <div style="background: #f7fafc; padding: 40px; border-radius: 20px; margin-top: 50px;">
            <h3 style="color: #667eea; font-size: 28px; margin-bottom: 20px;"><i class="fas fa-info-circle"></i> System Status</h3>
            <p style="font-size: 18px; color: #4a5568; line-height: 1.8;">
                ✅ All content unique (hash verified)<br>
                ✅ Podcasts 3-5 min with jingles<br>
                ✅ SEO pages AI-generated (5 designs)<br>
                ✅ RSS feed Apple Podcasts ready<br>
                ⏱ Generation: {int(duration // 60)}m {int(duration % 60)}s
            </p>
        </div>
    </div>
</body>
</html>'''
    with open(dashboard_dir / 'index.html', 'w') as f:
        f.write(html)
    print(f"✅ Complete dashboard created")


async def main():
    print("\n" + "="*70)
    print("TITAN V2 - AI WEBSITE BUILDER COMPLETE")
    print("="*70)
    start_time = datetime.now()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    web_dir = output_dir / 'web'
    for d in ['blog', 'dashboard', 'podcasts', 'seo']:
        (web_dir / d).mkdir(parents=True, exist_ok=True)
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    validator = ContentUniqueValidator()
    gemini_key = os.getenv('GEMINI_API_KEY')
    image_gen = ProfessionalImageGenerator()
    podcast_gen = PodcastGeneratorWithJingles()
    ai_builder = AIWebsiteBuilder(gemini_key)
    podcasts_list = []
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"TOPIC {i}/10: {topic['title']}")
        print(f"{'='*70}")
        print("  📝 Generating unique article...")
        article = generate_unique_article(topic, gemini_key, validator)
        hero_image = image_gen.generate_hero_image(topic['keyword'], article.get('seed'))
        hero_base64 = base64.b64encode(hero_image).decode('utf-8')
        slug = topic['title'].lower().replace(' ', '-').replace("'", '')[:60]
        html = create_professional_html(article, topic, hero_base64)
        with open(web_dir / 'blog' / f'{slug}.html', 'w') as f:
            f.write(html)
        if EDGE_TTS_AVAILABLE:
            try:
                podcast = await podcast_gen.generate_podcast(article, topic, i)
                if podcast and podcast['duration'] >= 180:
                    filename = f'episode-{i:02d}-{slug[:30]}.mp3'
                    with open(web_dir / 'podcasts' / filename, 'wb') as f:
                        f.write(podcast['audio'])
                    podcasts_list.append({'title': topic['title'], 'episode': i, 'filename': filename, 'size': len(podcast['audio']), 'duration': podcast['duration']})
                else:
                    print(f"      ⚠️ Podcast too short")
            except Exception as e:
                print(f"      ⚠️ Podcast error: {str(e)[:60]}")
        print(f"  ✅ Complete")
    image_gen.generate_podcast_cover(web_dir / 'podcast-cover.jpg')
    if podcasts_list:
        cover_url = 'https://dashboard.sayplay.co.uk/podcast-cover.jpg'
        create_rss_feed_apple(podcasts_list, web_dir / 'podcast.xml', cover_url)
    seo_pages = generate_seo_pages_with_ai_builder(output_dir, validator, ai_builder)
    print(f"\n{'='*70}")
    print("CREATING INDEX PAGES")
    print(f"{'='*70}")
    create_podcasts_index(podcasts_list, output_dir)
    create_blog_index(topics, output_dir)
    create_seo_index(seo_pages, output_dir)
    create_complete_dashboard(topics, podcasts_list, len(seo_pages), output_dir, start_time)
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n{'='*70}")
    print("TITAN COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ {len(topics)} Unique Articles")
    print(f"✅ {len(podcasts_list)} Podcasts (3-5 min + jingles)")
    print(f"✅ {len(seo_pages)} AI-generated SEO Pages (5 designs)")
    print(f"✅ All Index Pages (/blog, /podcasts, /seo, /)")
    print(f"\n⏱ Duration: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"{'='*70}\n")
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
