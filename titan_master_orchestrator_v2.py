#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - PROFESSIONAL EDITION
Full article generation with images and premium design
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio
import json

sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator

# Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai not installed")

# Image imports
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class ProfessionalImageGenerator:
    """Generate professional images with SayPlay branding"""
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
    
    def generate_hero_image(self, keyword: str) -> bytes:
        """Generate hero image for article"""
        print(f"    Generating hero image for: {keyword}")
        
        # Try Unsplash first
        if self.unsplash_key:
            img = self._fetch_unsplash(keyword, 1200, 630)
            if img:
                return self._add_branding(img, keyword)
        
        # Fallback to Pexels
        if self.pexels_key:
            img = self._fetch_pexels(keyword, 1200, 630)
            if img:
                return self._add_branding(img, keyword)
        
        # Fallback to generated gradient
        return self._generate_fallback(keyword, 1200, 630)
    
    def _fetch_unsplash(self, query: str, width: int, height: int):
        """Fetch from Unsplash"""
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {
                'query': query,
                'orientation': 'landscape',
                'client_id': self.unsplash_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['raw'] + f"&w={width}&h={height}&fit=crop"
                
                img_response = requests.get(image_url, timeout=20)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content))
        except Exception as e:
            print(f"      Unsplash error: {str(e)[:50]}")
        
        return None
    
    def _fetch_pexels(self, query: str, width: int, height: int):
        """Fetch from Pexels"""
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
        except Exception as e:
            print(f"      Pexels error: {str(e)[:50]}")
        
        return None
    
    def _generate_fallback(self, keyword: str, width: int, height: int) -> bytes:
        """Generate gradient background as fallback"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        for y in range(height):
            r = int(102 + (118 - 102) * y / height)
            g = int(126 + (75 - 126) * y / height)
            b = int(234 + (162 - 234) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return self._add_branding(img, keyword)
    
    def _add_branding(self, img: Image.Image, keyword: str) -> bytes:
        """Add SayPlay logo overlay"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Add semi-transparent overlay at bottom
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        for y in range(int(height * 0.7), height):
            alpha = int(180 * (y - height * 0.7) / (height * 0.3))
            overlay_draw.rectangle([(0, y), (width, y+1)], fill=(0, 0, 0, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Add SayPlay logo
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
        
        # Convert to bytes
        output = BytesIO()
        img.save(output, format='JPEG', quality=95)
        return output.getvalue()


def generate_article_with_gemini(topic: dict, api_key: str) -> dict:
    """Generate full professional article"""
    if not GEMINI_AVAILABLE:
        return generate_fallback_article(topic)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""Write a comprehensive, engaging blog article about: {topic['title']}

Target keyword: {topic['keyword']}
Tone: {topic['angle']}
Length: 1500-1800 words

Structure:
1. Compelling introduction (2-3 paragraphs)
2. Why This Gift Matters (1 section)
3. Top 7-9 Gift Ideas (detailed descriptions, 150-200 words each)
   - Each with specific product suggestions
   - Price ranges
   - Where to buy
   - Why it's special
4. How to Personalize Your Gift (1 section)
5. Budget-Friendly vs Luxury Options (1 section)
6. Presentation Tips (1 section)
7. Conclusion with call-to-action

Make it conversational, helpful, and inspiring. Include specific examples and real scenarios.
Focus on emotional connection and meaningful gift-giving."""

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
        
        print(f"    ✅ Article generated: {word_count} words")
        
        return {
            'title': topic['title'],
            'text': article_text,
            'sections': sections,
            'word_count': word_count,
            'keyword': topic['keyword']
        }
        
    except Exception as e:
        print(f"    ⚠️ Gemini error: {e}")
        return generate_fallback_article(topic)


def generate_fallback_article(topic: dict) -> dict:
    """Generate basic article as fallback"""
    sections = [
        {
            'title': 'Discover Perfect Gift Ideas',
            'content': f"Finding the right {topic['keyword']} can be challenging, but we're here to help you discover meaningful options that will be cherished for years to come."
        },
        {
            'title': 'Why Personalization Matters',
            'content': f"The best {topic['keyword']} are those that show genuine thought and care. Adding a personal touch transforms an ordinary gift into something truly special."
        },
        {
            'title': 'Our Top Recommendations',
            'content': f"We've curated a selection of {topic['keyword']} that combine quality, thoughtfulness, and lasting value. Each option has been chosen for its ability to create memorable moments."
        }
    ]
    
    article_text = '\n\n'.join([f"## {s['title']}\n{s['content']}" for s in sections])
    
    return {
        'title': topic['title'],
        'text': article_text,
        'sections': sections,
        'word_count': len(article_text.split()),
        'keyword': topic['keyword']
    }


def create_professional_html(article: dict, topic: dict, hero_image_base64: str) -> str:
    """Create professional HTML with premium design"""
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{article['text'][:160]}...">
    <meta name="keywords" content="{topic['keyword']}, gifts, sayplay, personalized gifts">
    <title>{article['title']} | SayPlay</title>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.8;
            color: #2d3748;
            background: #f7fafc;
        }}
        
        .hero {{
            position: relative;
            height: 500px;
            background: url('data:image/jpeg;base64,{hero_image_base64}') center/cover;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .hero-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.6));
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            max-width: 900px;
            padding: 0 20px;
        }}
        
        .logo {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        }}
        
        .logo span {{
            color: #FFD700;
        }}
        
        h1 {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 20px;
            line-height: 1.2;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        }}
        
        .meta {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            font-size: 16px;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .container {{
            max-width: 900px;
            margin: -100px auto 60px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            padding: 60px 50px;
            position: relative;
            z-index: 3;
        }}
        
        .content h2 {{
            color: #667eea;
            font-size: 32px;
            font-weight: 700;
            margin: 50px 0 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #FFD700;
        }}
        
        .content h3 {{
            color: #764ba2;
            font-size: 24px;
            font-weight: 600;
            margin: 35px 0 20px;
        }}
        
        .content p {{
            margin-bottom: 20px;
            font-size: 18px;
            line-height: 1.8;
            color: #4a5568;
        }}
        
        .cta-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 50px;
            border-radius: 20px;
            margin: 60px 0;
            text-align: center;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .cta-icon {{
            font-size: 80px;
            margin-bottom: 25px;
        }}
        
        .cta-section h3 {{
            color: white;
            font-size: 36px;
            margin: 0 0 20px;
            font-weight: 800;
        }}
        
        .cta-section p {{
            color: rgba(255, 255, 255, 0.95);
            font-size: 20px;
            margin-bottom: 35px;
            line-height: 1.6;
        }}
        
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: white;
            color: #667eea;
            padding: 20px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 50px 0;
        }}
        
        .feature {{
            text-align: center;
            padding: 30px;
            background: #f7fafc;
            border-radius: 15px;
            transition: transform 0.3s;
        }}
        
        .feature:hover {{
            transform: translateY(-5px);
        }}
        
        .feature i {{
            font-size: 48px;
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .feature h4 {{
            color: #2d3748;
            font-size: 20px;
            margin-bottom: 15px;
        }}
        
        .feature p {{
            color: #718096;
            font-size: 16px;
            margin: 0;
        }}
        
        @media (max-width: 768px) {{
            .hero {{
                height: 400px;
            }}
            
            h1 {{
                font-size: 32px;
            }}
            
            .container {{
                padding: 40px 25px;
                margin: -50px 20px 40px;
            }}
            
            .content h2 {{
                font-size: 26px;
            }}
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
                    <i class="far fa-calendar"></i>
                    {datetime.now().strftime("%B %d, %Y")}
                </span>
                <span class="meta-item">
                    <i class="far fa-clock"></i>
                    {max(1, article['word_count'] // 200)} min read
                </span>
                <span class="meta-item">
                    <i class="fas fa-tag"></i>
                    {topic['keyword']}
                </span>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="content">
'''
    
    # Add sections
    for section in article['sections']:
        if section['title']:
            html += f"<h2>{section['title']}</h2>\n"
        
        paragraphs = section['content'].strip().split('\n')
        for para in paragraphs:
            if para.strip():
                html += f"<p>{para.strip()}</p>\n"
    
    html += f'''
            <div class="cta-section">
                <div class="cta-icon">
                    <i class="fas fa-gift"></i>
                </div>
                <h3>Make Every Gift Unforgettable</h3>
                <p>Transform any gift into a cherished memory with SayPlay's voice message technology. Record your heartfelt message and let it play with a simple tap. No app needed!</p>
                <a href="https://sayplay.co.uk" class="cta-button">
                    <i class="fas fa-arrow-right"></i>
                    Discover SayPlay
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


def main():
    print("\n" + "="*70)
    print("TITAN V2 - PROFESSIONAL CONTENT GENERATOR")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    # Create structure
    web_dir = output_dir / 'web'
    blog_dir = web_dir / 'blog'
    dashboard_dir = web_dir / 'dashboard'
    images_dir = web_dir / 'images'
    
    for d in [web_dir, blog_dir, dashboard_dir, images_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Initialize
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    image_gen = ProfessionalImageGenerator()
    
    # Generate content for each topic
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"TOPIC {i}/10: {topic['title']}")
        print(f"{'='*70}")
        
        # Generate article
        print("  📝 Generating article...")
        article = generate_article_with_gemini(topic, gemini_key) if gemini_key else generate_fallback_article(topic)
        
        # Generate hero image
        print("  🖼 Generating hero image...")
        hero_image = image_gen.generate_hero_image(topic['keyword'])
        
        # Convert image to base64
        import base64
        hero_base64 = base64.b64encode(hero_image).decode('utf-8')
        
        # Save image
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        image_file = images_dir / f'{slug}-hero.jpg'
        with open(image_file, 'wb') as f:
            f.write(hero_image)
        
        # Create HTML
        print("  📄 Creating HTML...")
        html = create_professional_html(article, topic, hero_base64)
        
        # Save HTML
        html_file = blog_dir / f'{slug}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ Article complete: {article['word_count']} words")
    
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
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #e0e0e0;
        }}
        
        .logo {{
            font-size: 48px;
            font-weight: 800;
            color: #667eea;
        }}
        
        .logo span {{ color: #FFD700; }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        
        .stat {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .stat:hover {{
            transform: translateY(-5px);
        }}
        
        .stat i {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        
        .stat-number {{
            font-size: 56px;
            font-weight: 800;
            margin: 10px 0;
        }}
        
        .articles {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 40px;
        }}
        
        .article-card {{
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s;
            background: white;
        }}
        
        .article-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }}
        
        .article-card h3 {{
            color: #667eea;
            margin: 15px 0;
            font-size: 20px;
        }}
        
        .article-card a {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: #667eea;
            color: white;
            padding: 12px 25px;
            border-radius: 25px;
            text-decoration: none;
            margin-top: 15px;
            transition: all 0.3s;
        }}
        
        .article-card a:hover {{
            background: #5568d3;
            transform: translateX(5px);
        }}
        
        @media (max-width: 768px) {{
            .articles {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Say<span>Play</span> Dashboard</div>
            <p style="color: #666;">{datetime.now().strftime("%B %d, %Y %H:%M")}</p>
        </div>
        
        <div class="stats">
            <div class="stat">
                <i class="fas fa-file-alt"></i>
                <div class="stat-number">{len(topics)}</div>
                <div>Articles Published</div>
            </div>
            <div class="stat">
                <i class="fas fa-check-circle"></i>
                <div class="stat-number">✓</div>
                <div>System Active</div>
            </div>
        </div>
        
        <h2 style="margin-top: 50px; color: #333; font-size: 32px;">
            <i class="fas fa-newspaper"></i> Latest Articles
        </h2>
        <div class="articles">'''
    
    for i, topic in enumerate(topics, 1):
        slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
        dashboard_html += f'''
            <div class="article-card">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 8px 16px; border-radius: 15px; font-size: 14px; font-weight: 700; display: inline-block;">
                    Episode {i}
                </div>
                <h3>{topic['title']}</h3>
                <p style="color: #666; margin: 15px 0;">
                    <i class="fas fa-tag"></i> {topic['category']} • 
                    <i class="fas fa-key"></i> {topic['keyword']}
                </p>
                <a href="/blog/{slug}.html">
                    Read Article <i class="fas fa-arrow-right"></i>
                </a>
            </div>'''
    
    dashboard_html += '''
        </div>
    </div>
</body>
</html>'''
    
    with open(dashboard_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"\n✅ Complete! Generated {len(topics)} professional articles")
    print(f"✅ Output: {output_dir}")
    print(f"\n🌐 Will be live at: https://dashboard.sayplay.co.uk")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
