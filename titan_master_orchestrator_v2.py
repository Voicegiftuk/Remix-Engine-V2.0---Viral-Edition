#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - PROFESSIONAL AUTOMATION
- 10 diverse topics daily
- 5+ minute podcasts
- Professional images with logo
- Auto-deploy to Vercel
- Interactive dashboard
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import asyncio

sys.path.insert(0, str(Path(__file__).parent))

# Import core modules
from titan_modules.core.multi_topic_generator import MultiTopicGenerator
from titan_modules.core.dashboard_generator import DashboardGenerator
from titan_modules.content.image_engine.professional_image_generator import ProfessionalImageGenerator
from titan_modules.content.audio_inception.long_form_podcast_generator import LongFormPodcastGenerator

# Import existing modules
try:
    from titan_modules.expansion.global_domination.global_domination_zero_cost import GlobalDomination
    TRANSLATIONS_AVAILABLE = True
except:
    TRANSLATIONS_AVAILABLE = False

try:
    from titan_modules.expansion.programmatic_seo.programmatic_seo import ProgrammaticSEO
    SEO_AVAILABLE = True
except:
    SEO_AVAILABLE = False

import requests
import json


def generate_article_with_gemini(topic: dict, api_key: str) -> dict:
    """Generate article using Gemini"""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""Write a comprehensive, engaging blog article about: {topic['title']}

Keyword: {topic['keyword']}
Target length: 1500-1800 words
Tone: {topic['angle']}

Structure:
- Compelling introduction that hooks the reader emotionally
- 7-9 main sections with detailed, practical information
- Specific gift suggestions with descriptions and why they work
- Real-world examples and scenarios
- Expert tips for choosing and presenting gifts
- Budget considerations (affordable to luxury)
- Where to buy / how to personalize
- Strong conclusion with clear call-to-action

Make it feel authentic, helpful, and engaging. Write in a warm, conversational tone.
Include specific product categories and creative ideas.
Focus on helping people find meaningful gifts that create lasting memories.

DO NOT use generic placeholder text. Write actual, specific, actionable content.
Each section should be 150-250 words with real value."""

        response = model.generate_content(prompt)
        article_text = response.text
        
        # Parse into sections
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
        reading_time = max(1, word_count // 200)
        quality_score = min(100, 50 + (word_count // 20))
        
        print(f"    ✅ Article generated: {word_count} words, quality {quality_score}%")
        
        return {
            'title': topic['title'],
            'text': article_text,
            'sections': sections,
            'word_count': word_count,
            'reading_time': reading_time,
            'quality_score': quality_score,
            'keyword': topic['keyword']
        }
        
    except Exception as e:
        print(f"    ❌ Gemini failed: {e}")
        return None


def save_article_files(article: dict, topic: dict, output_dir: Path):
    """Save article in multiple formats"""
    
    # Create slug
    slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    
    # Article directory
    article_dir = output_dir / 'web' / 'blog'
    article_dir.mkdir(parents=True, exist_ok=True)
    
    files_dir = output_dir / '01_ARTICLE'
    files_dir.mkdir(parents=True, exist_ok=True)
    
    # Build HTML
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{article['text'][:160]}...">
    <meta name="keywords" content="{topic['keyword']}, gifts, sayplay, voice messages">
    <title>{article['title']} | SayPlay</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            line-height: 1.7;
            color: #2d3748;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        .logo {{
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 10px;
        }}
        .logo span {{ color: #FFD700; }}
        h1 {{
            font-size: 42px;
            margin: 20px 0;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        .meta {{
            font-size: 14px;
            opacity: 0.9;
            margin-top: 15px;
        }}
        .content {{
            padding: 60px 50px;
        }}
        h2 {{
            color: #667eea;
            font-size: 32px;
            margin: 40px 0 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid #FFD700;
        }}
        h3 {{
            color: #764ba2;
            font-size: 24px;
            margin: 30px 0 15px;
        }}
        p {{
            margin-bottom: 20px;
            font-size: 17px;
            line-height: 1.8;
        }}
        .cta-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            border-radius: 20px;
            margin: 60px 0;
            text-align: center;
        }}
        .cta-box h3 {{
            color: white;
            font-size: 32px;
            margin: 0 0 15px;
            border: none;
        }}
        .cta-button {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 18px 50px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 18px;
            margin-top: 20px;
            transition: transform 0.3s;
        }}
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        .footer {{
            background: #2d3748;
            color: white;
            padding: 40px;
            text-align: center;
        }}
        @media (max-width: 768px) {{
            h1 {{ font-size: 28px; }}
            .content {{ padding: 40px 25px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Say<span>Play</span></div>
            <h1>{article['title']}</h1>
            <div class="meta">
                📅 {datetime.now().strftime("%B %d, %Y")} • 
                ⏱ {article['reading_time']} min read • 
                🔑 {topic['keyword']}
            </div>
        </div>
        
        <div class="content">
'''
    
    # Add sections
    for section in article['sections']:
        if section['title']:
            html_content += f"<h2>{section['title']}</h2>\n"
        
        paragraphs = section['content'].strip().split('\n')
        for para in paragraphs:
            if para.strip():
                html_content += f"<p>{para.strip()}</p>\n"
    
    html_content += f'''
            <div class="cta-box">
                <div style="font-size: 60px; margin-bottom: 20px;">💝</div>
                <h3>Make Every Gift Unforgettable</h3>
                <p style="color: white; font-size: 18px;">Transform any gift into a cherished memory with SayPlay's voice message technology. Record your heartfelt message and let it play with a simple tap. No app needed!</p>
                <a href="https://sayplay.co.uk" class="cta-button">Discover SayPlay →</a>
            </div>
        </div>
        
        <div class="footer">
            <div style="font-size: 28px; font-weight: 800; margin-bottom: 10px;">
                Say<span style="color: #FFD700;">Play</span>
            </div>
            <p>Voice Messages That Last Forever</p>
            <p style="margin-top: 20px; opacity: 0.7; font-size: 14px;">
                © 2025 VoiceGift UK. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
'''
    
    # Save web version
    web_file = article_dir / f'{slug}.html'
    with open(web_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Save archive version
    archive_file = files_dir / f'{timestamp}_{slug}.html'
    with open(archive_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Save text version
    txt_file = files_dir / f'{timestamp}_{slug}.txt'
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"{article['title']}\n\n")
        f.write(article['text'])
    
    # Save metadata
    meta_file = files_dir / f'{timestamp}_{slug}_META.json'
    with open(meta_file, 'w') as f:
        json.dump({
            'title': article['title'],
            'keyword': topic['keyword'],
            'word_count': article['word_count'],
            'quality_score': article['quality_score'],
            'reading_time': article['reading_time'],
            'generated_at': datetime.now().isoformat(),
            'web_url': f'https://sayplay.co.uk/blog/{slug}'
        }, f, indent=2)
    
    print(f"    ✅ Article saved: {slug}")
    
    return {
        'web_file': web_file,
        'archive_file': archive_file,
        'txt_file': txt_file,
        'meta_file': meta_file,
        'slug': slug
    }


def save_podcast_files(podcast: dict, topic: dict, output_dir: Path):
    """Save podcast audio and metadata"""
    
    slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    
    podcast_dir = output_dir / '02_PODCAST'
    podcast_dir.mkdir(parents=True, exist_ok=True)
    
    # Save MP3
    mp3_file = podcast_dir / f'{timestamp}_{slug}_PODCAST.mp3'
    with open(mp3_file, 'wb') as f:
        f.write(podcast['audio'])
    
    # Save metadata
    meta_file = podcast_dir / f'{timestamp}_{slug}_PODCAST_META.json'
    with open(meta_file, 'w') as f:
        json.dump({
            'title': podcast['metadata']['title'],
            'episode_number': topic['episode_number'],
            'duration_seconds': podcast['metadata']['duration'],
            'quality': podcast['metadata']['quality'],
            'generated_at': datetime.now().isoformat(),
            'file_size_mb': len(podcast['audio']) / (1024 * 1024)
        }, f, indent=2)
    
    # Save script
    script_file = podcast_dir / f'{timestamp}_{slug}_SCRIPT.txt'
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(f"EPISODE {topic['episode_number']}: {podcast['metadata']['title']}\n")
        f.write("=" * 70 + "\n\n")
        for i, segment in enumerate(podcast['script'], 1):
            f.write(f"[SEGMENT {i} - {segment['voice']}]\n")
            f.write(f"{segment['text']}\n\n")
    
    size_mb = len(podcast['audio']) / (1024 * 1024)
    print(f"    ✅ Podcast saved: {size_mb:.1f}MB, {podcast['metadata']['duration']}s")
    
    return {
        'mp3_file': mp3_file,
        'meta_file': meta_file,
        'script_file': script_file
    }


def save_image_files(images: dict, topic: dict, output_dir: Path):
    """Save all generated images"""
    
    slug = topic['title'].lower().replace(' ', '-').replace("'", '').replace(':', '')[:60]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    
    images_dir = output_dir / '03_IMAGES'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    
    for img_type, img_data in images.items():
        img_file = images_dir / f'{timestamp}_{slug}_{img_type.upper()}.jpg'
        with open(img_file, 'wb') as f:
            f.write(img_data)
        saved_files.append(img_file)
    
    # Save metadata
    meta_file = images_dir / f'{timestamp}_{slug}_IMAGES_META.json'
    with open(meta_file, 'w') as f:
        json.dump({
            'topic': topic['title'],
            'images_generated': list(images.keys()),
            'total_images': len(images),
            'generated_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"    ✅ Images saved: {len(images)} types")
    
    return saved_files


def main():
    print("\n" + "="*70)
    print("TITAN MASTER ORCHESTRATOR V2 - PROFESSIONAL AUTOMATION")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("="*70 + "\n")
    
    start_time = datetime.now()
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    
    # Initialize generators
    topic_gen = MultiTopicGenerator()
    image_gen = ProfessionalImageGenerator()
    podcast_gen = LongFormPodcastGenerator()
    
    # Generate topics
    topics = topic_gen.generate_daily_topics(count=10)
    
    results = {
        'start_time': start_time,
        'articles_count': 0,
        'podcasts_count': 0,
        'images_count': 0,
        'seo_pages': 0,
        'modules_run': 0,
        'total_files': 0
    }
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set!")
        return 1
    
    # Process each topic
    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"PROCESSING TOPIC {i}/10: {topic['title']}")
        print(f"{'='*70}")
        
        # Generate article
        print(f"\n📝 Generating article...")
        article = generate_article_with_gemini(topic, gemini_key)
        
        if article:
            article_files = save_article_files(article, topic, output_dir)
            results['articles_count'] += 1
            results['total_files'] += 4
            
            # Store for dashboard
            topic['word_count'] = article['word_count']
            topic['quality_score'] = article['quality_score']
            topic['reading_time'] = article['reading_time']
        else:
            print("    ❌ Article generation failed, skipping...")
            continue
        
        # Generate images
        print(f"\n🖼 Generating images with logo...")
        try:
            images = image_gen.generate_image_set(topic['keyword'], topic['title'])
            if images:
                image_files = save_image_files(images, topic, output_dir)
                results['images_count'] += len(images)
                results['total_files'] += len(images) + 1
        except Exception as e:
            print(f"    ⚠️ Image generation error: {e}")
        
        # Generate podcast
        print(f"\n🎙 Generating 5+ minute podcast...")
        try:
            podcast = asyncio.run(podcast_gen.generate_podcast(article, topic, i))
            podcast_files = save_podcast_files(podcast, topic, output_dir)
            results['podcasts_count'] += 1
            results['total_files'] += 3
        except Exception as e:
            print(f"    ❌ Podcast generation error: {e}")
        
        # Generate translations
        if TRANSLATIONS_AVAILABLE and i <= 3:  # Only first 3 to save time
            print(f"\n🌍 Generating translations...")
            try:
                global_engine = GlobalDomination()
                translations = global_engine.batch_translate_all_markets(article)
                
                trans_dir = output_dir / '04_TRANSLATIONS'
                trans_dir.mkdir(parents=True, exist_ok=True)
                
                slug = topic['title'].lower().replace(' ', '-').replace("'", '')[:60]
                
                for lang, content in translations.items():
                    if lang != 'en':
                        trans_file = trans_dir / f'{timestamp}_{slug}_{lang.upper()}.html'
                        with open(trans_file, 'w', encoding='utf-8') as f:
                            if isinstance(content, dict):
                                f.write(content.get('html', content.get('text', '')))
                            else:
                                f.write(str(content))
                        results['total_files'] += 1
                
                print(f"    ✅ Translated to {len(translations)-1} languages")
            except Exception as e:
                print(f"    ⚠️ Translation error: {e}")
    
    # Generate SEO pages
    if SEO_AVAILABLE:
        print(f"\n{'='*70}")
        print("GENERATING SEO PAGES")
        print(f"{'='*70}")
        try:
            seo_engine = ProgrammaticSEO()
            seo_pages = seo_engine.generate_all_pages(max_pages=100)
            results['seo_pages'] = len(seo_pages)
            print(f"✅ Generated {len(seo_pages)} SEO landing pages")
        except Exception as e:
            print(f"⚠️ SEO generation error: {e}")
    
    # Generate dashboard
    print(f"\n{'='*70}")
    print("GENERATING DASHBOARD")
    print(f"{'='*70}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    results['duration_minutes'] = int(duration // 60)
    results['modules_run'] = 5
    results['time_saved_hours'] = results['articles_count'] * 4 + results['podcasts_count'] * 2
    results['cost_saved'] = results['time_saved_hours'] * 50
    results['roi'] = results['cost_saved'] - 9.40
    
    dashboard_gen = DashboardGenerator(output_dir)
    dashboard_file = dashboard_gen.generate(results, topics)
    
    # Final summary
    print(f"\n{'='*70}")
    print("TITAN COMPLETE")
    print(f"{'='*70}")
    print(f"Duration: {duration:.1f}s ({int(duration//60)}m {int(duration%60)}s)")
    print(f"Articles: {results['articles_count']}")
    print(f"Podcasts: {results['podcasts_count']}")
    print(f"Images: {results['images_count']}")
    print(f"SEO Pages: {results['seo_pages']}")
    print(f"Total Files: {results['total_files']}")
    print(f"Time Saved: {results['time_saved_hours']}h")
    print(f"Cost Saved: £{results['cost_saved']:,.0f}")
    print(f"{'='*70}")
    print(f"\n📊 Dashboard: {dashboard_file}")
    print(f"🌐 Will be live at: https://dashboard.sayplay.co.uk")
    print(f"\n✅ Ready for Vercel deployment!")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
