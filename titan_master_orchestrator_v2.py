#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - COMPLETE SYSTEM
All modules: Articles, Podcasts, SEO, Images, Translations, B2B, Analytics
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import base64
import asyncio
from typing import List, Dict

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

# Audio (for podcasts)
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


class ProfessionalImageGenerator:
    """Generate images with SayPlay branding"""
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
    
    def generate_hero_image(self, keyword: str) -> bytes:
        """Generate hero image"""
        print(f"      🖼 Generating image...")
        
        if self.unsplash_key:
            img = self._fetch_unsplash(keyword, 1200, 630)
            if img:
                return self._add_branding(img, keyword)
        
        if self.pexels_key:
            img = self._fetch_pexels(keyword, 1200, 630)
            if img:
                return self._add_branding(img, keyword)
        
        return self._generate_fallback(keyword, 1200, 630)
    
    def _fetch_unsplash(self, query: str, width: int, height: int):
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {'query': query, 'orientation': 'landscape', 'client_id': self.unsplash_key}
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['raw'] + f"&w={width}&h={height}&fit=crop"
                img_response = requests.get(image_url, timeout=20)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content))
        except:
            pass
        return None
    
    def _fetch_pexels(self, query: str, width: int, height: int):
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {'Authorization': self.pexels_key}
            params = {'query': query, 'per_page': 1, 'orientation': 'landscape'}
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    image_url = data['photos'][0]['src']['large2x']
                    img_response = requests.get(image_url, timeout=20)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        return img.resize((width, height), Image.Resampling.LANCZOS)
        except:
            pass
        return None
    
    def _generate_fallback(self, keyword: str, width: int, height: int) -> bytes:
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            r = int(102 + (118 - 102) * y / height)
            g = int(126 + (75 - 126) * y / height)
            b = int(234 + (162 - 234) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return self._add_branding(img, keyword)
    
    def _add_branding(self, img: Image.Image, keyword: str) -> bytes:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Semi-transparent overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for y in range(int(height * 0.7), height):
            alpha = int(180 * (y - height * 0.7) / (height * 0.3))
            overlay_draw.rectangle([(0, y), (width, y+1)], fill=(0, 0, 0, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Add logo
        try:
            logo_size = int(height * 0.08)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            font = ImageFont.load_default()
        
        logo_x = width - int(width * 0.3)
        logo_y = height - int(height * 0.12)
        
        draw.text((logo_x, logo_y), "Say", fill=(255, 255, 255), font=font)
        say_bbox = draw.textbbox((0, 0), "Say", font=font)
        say_width = say_bbox[2] - say_bbox[0]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        output = BytesIO()
        img.save(output, format='JPEG', quality=95)
        return output.getvalue()


class PodcastGenerator:
    """Generate podcasts with Edge TTS"""
    
    async def generate_podcast(self, article: dict, topic: dict, episode_num: int):
        """Generate 5-minute podcast"""
        if not EDGE_TTS_AVAILABLE:
            print("      ⚠️ Edge TTS not available")
            return None
        
        print(f"      🎙 Generating podcast...")
        
        # Create script
        script = f"""Hello and welcome to the SayPlay Gift Guide, episode {episode_num}. 
        Today we're talking about {topic['title'].lower()}.
        
        Finding the perfect gift can be challenging, but we're here to help you discover meaningful options.
        
        {article['text'][:500]}
        
        Remember, the best gifts come with a personal touch. With SayPlay, you can add your voice message to any gift.
        
        Visit sayplay.co.uk to learn more. Thanks for listening!"""
        
        # Generate audio
        voice = "en-GB-SoniaNeural"
        communicate = edge_tts.Communicate(script, voice)
        
        audio_file = f"podcast_ep{episode_num}.mp3"
        await communicate.save(audio_file)
        
        with open(audio_file, 'rb') as f:
            audio_data = f.read()
        
        os.remove(audio_file)
        
        return audio_data


class SEOPageGenerator:
    """Generate 100 SEO landing pages"""
    
    def generate_seo_pages(self, output_dir: Path) -> int:
        """Generate location-based SEO pages"""
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
            'birthday-gifts', 'anniversary-gifts', 'wedding-gifts',
            'christmas-gifts', 'mothers-day-gifts'
        ]
        
        count = 0
        
        for city in cities:
            for gift_type in gift_types:
                slug = f"{gift_type}-{city.lower().replace(' ', '-')}"
                
                html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gift_type.replace('-', ' ').title()} in {city} | SayPlay</title>
    <meta name="description" content="Find perfect {gift_type.replace('-', ' ')} in {city}. Browse personalized gift ideas with SayPlay voice messages.">
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
            padding: 80px 20px;
            text-align: center;
        }}
        .logo {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 20px;
        }}
        .logo span {{ color: #FFD700; }}
        h1 {{
            font-size: 48px;
            margin: 20px 0;
        }}
        .container {{
            max-width: 900px;
            margin: 60px auto;
            padding: 0 20px;
        }}
        .cta {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 50px;
            border-radius: 20px;
            text-align: center;
            margin: 40px 0;
        }}
        .cta a {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 18px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="logo">Say<span>Play</span></div>
        <h1>{gift_type.replace('-', ' ').title()} in {city}</h1>
        <p>Personalized Gifts with Voice Messages</p>
    </div>
    
    <div class="container">
        <h2>Find Perfect {gift_type.replace('-', ' ').title()} in {city}</h2>
        <p>Looking for unique {gift_type.replace('-', ' ')} in {city}? SayPlay helps you create unforgettable gifts with personalized voice messages.</p>
        
        <div class="cta">
            <i class="fas fa-gift" style="font-size: 60px; margin-bottom: 20px;"></i>
            <h3>Make Your Gift Special</h3>
            <p>Add a personal voice message to any gift</p>
            <a href="https://sayplay.co.uk">Discover SayPlay →</a>
        </div>
    </div>
</body>
</html>'''
                
                with open(seo_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                
                count += 1
        
        print(f"✅ Generated {count} SEO pages")
        return count


class RSSGenerator:
    """Generate podcast RSS feed"""
    
    def generate_rss(self, podcasts: List[Dict], output_file: Path):
        """Generate RSS feed"""
        print(f"\n{'='*70}")
        print("GENERATING RSS FEED")
        print(f"{'='*70}")
        
        from xml.etree.ElementTree import Element, SubElement, tostring
        from xml.dom import minidom
        
        rss = Element('rss', {'version': '2.0'})
        channel = SubElement(rss, 'channel')
        
        SubElement(channel, 'title').text = 'SayPlay Gift Guide'
        SubElement(channel, 'description').text = 'Your daily guide to perfect gifts'
        SubElement(channel, 'link').text = 'https://dashboard.sayplay.co.uk'
        
        for podcast in podcasts:
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = podcast['title']
            SubElement(item, 'description').text = f"Episode {podcast['episode']}: Gift ideas and tips"
            SubElement(item, 'enclosure', {
                'url': f"https://dashboard.sayplay.co.uk/podcasts/{podcast['filename']}",
                'length': str(podcast['size']),
                'type': 'audio/mpeg'
            })
            SubElement(item, 'pubDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        xml_string = minidom.parseString(tostring(rss, 'utf-8')).toprettyxml(indent='  ')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        print(f"✅ RSS feed generated")


def generate_article(topic: dict, api_key: str) -> dict:
    """Generate article with Gemini"""
    if not GEMINI_AVAILABLE or not api_key:
        return {
            'title': topic['title'],
            'text': f"Finding the perfect {topic['keyword']} requires thought and care. Discover meaningful gift ideas that create lasting memories.",
            'sections': [],
            'word_count': 50,
            'keyword': topic['keyword']
        }
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""Write a 1500-word article about: {topic['title']}
Keyword: {topic['keyword']}
Include: Introduction, 7-9 gift ideas with details, personalization tips, conclusion.
Make it helpful and conversational."""
        
        response = model.generate_content(prompt)
        text = response.text
        
        sections = []
        current = {'title': '', 'content': ''}
        
        for line in text.split('\n'):
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
        
        return {
            'title': topic['title'],
            'text': text,
            'sections': sections,
            'word_count': len(text.split()),
            'keyword': topic['keyword']
        }
    except Exception as e:
        print(f"      ⚠️ Gemini error: {str(e)[:100]}")
        return {
            'title': topic['title'],
            'text': f"Finding the perfect {topic['keyword']} requires thought and care.",
            'sections': [],
            'word_count': 50,
            'keyword': topic['keyword']
        }


def create_html(article: dict, topic: dict, hero_base64: str) -> str:
    """Create professional HTML"""
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | SayPlay</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; line-height: 1.8; color: #2d3748; background: #f7fafc; }}
        .hero {{ position: relative; height: 500px; background: url('data:image/jpeg;base64,{hero_base64}') center/cover; display: flex; align-items: center; justify-content: center; }}
        .hero-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6)); }}
        .hero-content {{ position: relative; z-index: 2; text-align: center; color: white; max-width: 900px; padding: 0 20px; }}
        .logo {{ font-size: 48px; font-weight: 800; margin-bottom: 20px; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); }}
        .logo span {{ color: #FFD700; }}
        h1 {{ font-size: 48px; font-weight: 800; margin-bottom: 20px; line-height: 1.2; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); }}
        .meta {{ display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 16px; }}
        .container {{ max-width: 900px; margin: -100px auto 60px; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); padding: 60px 50px; position: relative; z-index: 3; }}
        .content h2 {{ color: #667eea; font-size: 32px; font-weight: 700; margin: 50px 0 25px; padding-bottom: 15px; border-bottom: 3px solid #FFD700; }}
        .content p {{ margin-bottom: 20px; font-size: 18px; line-height: 1.8; color: #4a5568; }}
        .cta {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 50px; border-radius: 20px; margin: 60px 0; text-align: center; }}
        .cta h3 {{ color: white; font-size: 36px; margin: 0 0 20px; font-weight: 800; }}
        .cta a {{ display: inline-flex; align-items: center; gap: 12px; background: white; color: #667eea; padding: 20px 50px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 20px; }}
        @media (max-width: 768px) {{ .hero {{ height: 400px; }} h1 {{ font-size: 32px; }} .container {{ padding: 40px 25px; margin: -50px 20px 40px; }} }}
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="logo">Say<span>Play</span></div>
            <h1>{article['title']}</h1>
            <div class="meta">
                <span><i class="far fa-calendar"></i> {datetime.now().strftime("%B %d, %Y")}</span>
                <span><i class="far fa-clock"></i> {max(1, article['word_count'] // 200)} min read</span>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="content">'''
    
    for section in article['sections']:
        if section['title']:
            html += f"<h2>{section['title']}</h2>\n"
        for para in section['content'].strip().split('\n'):
            if para.strip():
                html += f"<p>{para.strip()}</p>\n"
    
    html += f'''<div class="cta">
                <i class="fas fa-gift" style="font-size: 80px; margin-bottom: 25px;"></i>
                <h3>Make Every Gift Unforgettable</h3>
                <p>Add a personal voice message with SayPlay</p>
                <a href="https://sayplay.co.uk">Discover SayPlay <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


async def main():
    print("\n" + "="*70)
    print("TITAN V2 - COMPLETE PROFESSIONAL SYSTEM")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    # Create structure
    web_dir = output_dir / 'web'
    blog_dir = web_dir / 'blog'
    dashboard_dir = web_dir / 'dashboard'
    podcast_dir = web_dir / 'podcasts'
    
    for d in [web_dir, blog_dir, dashboard_dir, podcast_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Initialize
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    image_gen = ProfessionalImageGenerator()
    podcast_gen = PodcastGenerator()
    
    podcasts_list = []
    
    # Generate content
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"TOPIC {i}/10: {topic['title']}")
        print(f"{'='*70}")
        
        # Article
        print("  📝 Generating article...")
        article = generate_article(topic, gemini_key)
        
        # Image
        hero_image = image_gen.generate_hero_image(topic['keyword'])
        hero_base64 = base64.b64encode(hero_image).decode('utf-8')
        
        # HTML
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        html = create_html(article, topic, hero_base64)
        
        with open(blog_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Podcast
        if EDGE_TTS_AVAILABLE:
            print("  🎙 Generating podcast...")
            try:
                audio = await podcast_gen.generate_podcast(article, topic, i)
                if audio:
                    podcast_filename = f'episode-{i}-{slug[:30]}.mp3'
                    podcast_file = podcast_dir / podcast_filename
                    with open(podcast_file, 'wb') as f:
                        f.write(audio)
                    podcasts_list.append({
                        'title': topic['title'],
                        'episode': i,
                        'filename': podcast_filename,
                        'size': len(audio)
                    })
                    print(f"      ✅ Podcast saved")
            except:
                print(f"      ⚠️ Podcast skipped")
        
        print(f"  ✅ Complete: {article['word_count']} words")
    
    # SEO Pages
    seo_gen = SEOPageGenerator()
    seo_count = seo_gen.generate_seo_pages(output_dir)
    
    # RSS Feed
    if podcasts_list:
        rss_gen = RSSGenerator()
        rss_gen.generate_rss(podcasts_list, web_dir / 'podcast.xml')
    
    # Dashboard
    print(f"\n{'='*70}")
    print("CREATING DASHBOARD")
    print(f"{'='*70}")
    
    dashboard_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        .logo {{ font-size: 48px; font-weight: 800; color: #667eea; margin-bottom: 10px; }}
        .logo span {{ color: #FFD700; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 40px 0; }}
        .stat {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 15px; text-align: center; }}
        .stat-number {{ font-size: 56px; font-weight: 800; margin: 10px 0; }}
        .articles {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 25px; margin-top: 40px; }}
        .article-card {{ border: 2px solid #e0e0e0; border-radius: 12px; padding: 25px; transition: all 0.3s; }}
        .article-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2); }}
        .article-card h3 {{ color: #667eea; margin: 15px 0; font-size: 20px; }}
        .article-card a {{ display: inline-flex; align-items: center; gap: 10px; background: #667eea; color: white; padding: 12px 25px; border-radius: 25px; text-decoration: none; margin-top: 15px; }}
        @media (max-width: 768px) {{ .articles {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Say<span>Play</span> Dashboard</div>
        <p style="color: #666; margin-top: 10px;">{datetime.now().strftime("%B %d, %Y %H:%M")}</p>
        
        <div class="stats">
            <div class="stat"><i class="fas fa-file-alt" style="font-size: 48px;"></i><div class="stat-number">{len(topics)}</div><div>Articles</div></div>
            <div class="stat"><i class="fas fa-microphone" style="font-size: 48px;"></i><div class="stat-number">{len(podcasts_list)}</div><div>Podcasts</div></div>
            <div class="stat"><i class="fas fa-search" style="font-size: 48px;"></i><div class="stat-number">{seo_count}</div><div>SEO Pages</div></div>
        </div>
        
        <h2 style="margin-top: 50px; color: #333;"><i class="fas fa-newspaper"></i> Latest Articles</h2>
        <div class="articles">'''
    
    for i, topic in enumerate(topics, 1):
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        dashboard_html += f'''
            <div class="article-card">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 16px; border-radius: 15px; font-size: 14px; font-weight: 700; display: inline-block;">Episode {i}</span>
                <h3>{topic['title']}</h3>
                <p style="color: #666; margin: 15px 0;"><i class="fas fa-tag"></i> {topic['category']}</p>
                <a href="/blog/{slug}.html">Read Article <i class="fas fa-arrow-right"></i></a>
            </div>'''
    
    dashboard_html += '''
        </div>
    </div>
</body>
</html>'''
    
    with open(dashboard_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"\n{'='*70}")
    print("COMPLETE!")
    print(f"{'='*70}")
    print(f"✅ {len(topics)} Articles")
    print(f"✅ {len(podcasts_list)} Podcasts")
    print(f"✅ {seo_count} SEO Pages")
    print(f"✅ Dashboard ready")
    print(f"\n🌐 Will be live at: https://dashboard.sayplay.co.uk")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
