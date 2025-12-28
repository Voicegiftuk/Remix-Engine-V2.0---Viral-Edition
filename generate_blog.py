#!/usr/bin/env python3
"""Generate blog article - PROFESSIONAL DESIGN"""
import os
import sys
import json
import base64
from pathlib import Path

sys.path.insert(0, '.')

# Verify API key
api_key = os.environ.get('GEMINI_API_KEY')

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found!")
    print("Available env vars:", [k for k in os.environ.keys() if 'GEMINI' in k or 'GOOGLE' in k])
    sys.exit(1)

print(f"✅ API Key loaded: {len(api_key)} chars")
print(f"   Using NEW Google Genai SDK")

from titan_modules.blog.intelligence.topic_generator import TopicGenerator
from titan_modules.blog.writer.article_generator import ArticleGenerator

# Generate topic
print('\n🎯 Generating intelligent topic...')
topic_gen = TopicGenerator()
brief = topic_gen.generate_next_topic()

print(f'✓ Topic: {brief["primary_keyword"]}')
print(f'✓ Category: {brief["category"]}')
print(f'✓ Trending: {brief["trending_score"]}/100')

# Generate article
print('\n✍️  Writing article with NEW Google Genai SDK...')
article_gen = ArticleGenerator(api_key)
article = article_gen.write_article(brief)

print(f'\n✅ Article complete!')
print(f'   Words: {article["word_count"]}')
print(f'   Sections: {len(article["outline"])}')

# Load logo as base64
logo_base64 = ""
logo_path = Path('assets/brand/sayplay_logo.png')

if logo_path.exists():
    try:
        with open(logo_path, 'rb') as f:
            logo_data = base64.b64encode(f.read()).decode('utf-8')
            logo_base64 = f'data:image/png;base64,{logo_data}'
        print('✓ Logo loaded from file')
    except Exception as e:
        print(f'⚠️  Logo load failed: {e}')

# Fallback: Use external URL if base64 failed
if not logo_base64:
    logo_base64 = 'https://sayplay.co.uk/logo.png'  # Update with real URL if needed
    print('⚠️  Using fallback logo URL')

# Create professional branded HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="{article['meta_description']}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 0;
            background: #FFFFFF;
            color: #1a1a1a;
            line-height: 1.8;
        }}
        
        /* Professional Header */
        .header {{
            background: #FFFFFF;
            border-bottom: 1px solid #e5e5e5;
            padding: 30px 40px;
            text-align: center;
        }}
        
        .logo-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 12px;
        }}
        
        .logo-img {{
            height: 50px;
            width: auto;
        }}
        
        .brand-name {{
            font-size: 2em;
            font-weight: 700;
            color: #1a1a1a;
            letter-spacing: -0.5px;
        }}
        
        .tagline {{
            font-size: 1em;
            color: #666;
            font-weight: 400;
        }}
        
        /* Article Content */
        .article {{
            background: white;
            padding: 50px 40px;
        }}
        
        h1 {{
            color: #1a1a1a;
            font-size: 2.5em;
            margin-bottom: 0.5em;
            font-weight: 700;
            line-height: 1.2;
        }}
        
        h2 {{
            color: #1a1a1a;
            margin-top: 2em;
            font-size: 1.8em;
            font-weight: 600;
            padding-bottom: 12px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        h3 {{
            color: #333;
            margin-top: 1.5em;
            font-size: 1.4em;
            font-weight: 600;
        }}
        
        p {{
            margin: 1.2em 0;
            font-size: 1.05em;
            color: #333;
        }}
        
        strong {{
            color: #1a1a1a;
            font-weight: 600;
        }}
        
        /* Call to Action - Only colored element */
        .cta {{
            background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
            color: white;
            padding: 50px 40px;
            margin-top: 60px;
            text-align: center;
        }}
        
        .cta h3 {{
            color: white;
            font-size: 2em;
            margin-bottom: 20px;
            border: none;
            padding: 0;
        }}
        
        .cta p {{
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1em;
        }}
        
        .cta-button {{
            display: inline-block;
            background: white;
            color: #4A90E2;
            padding: 16px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 25px;
            font-size: 1.1em;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px;
            color: #666;
            border-top: 1px solid #e5e5e5;
            background: #fafafa;
        }}
        
        .footer a {{
            color: #4A90E2;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{ padding: 0; }}
            .header {{ padding: 25px 20px; }}
            .article {{ padding: 30px 20px; }}
            .cta {{ padding: 40px 20px; }}
            .logo-img {{ height: 40px; }}
            .brand-name {{ font-size: 1.5em; }}
            h1 {{ font-size: 1.8em; }}
            h2 {{ font-size: 1.4em; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo-container">
            <img src="{logo_base64}" alt="SayPlay Logo" class="logo-img">
            <div class="brand-name">SayPlay</div>
        </div>
        <div class="tagline">Voice Message Gifts That Last Forever</div>
    </div>
    
    <div class="article">
        <h1>{article['title']}</h1>
        {article['html']}
    </div>
    
    <div class="cta">
        <h3>Create Your Own Voice Message Gift</h3>
        <p>Turn your words into unforgettable memories with SayPlay</p>
        <a href="https://sayplay.co.uk" class="cta-button">Shop Now →</a>
    </div>
    
    <div class="footer">
        <p><strong>SayPlay</strong> | Just Tap - No App Needed</p>
        <p>🌐 <a href="https://sayplay.co.uk">SayPlay.co.uk</a></p>
        <p style="margin-top:20px; font-size:0.9em; opacity:0.7">Powered by Titan Content Engine</p>
    </div>
</body>
</html>"""

# Save HTML
with open('test_article.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Save metadata
meta = {
    'title': article['title'],
    'keyword': brief['primary_keyword'],
    'category': brief['category'],
    'words': article['word_count'],
    'trending': brief['trending_score']
}

with open('article_meta.json', 'w') as f:
    json.dump(meta, f, indent=2)

# GitHub Actions output
github_output = os.environ.get('GITHUB_OUTPUT')
if github_output:
    with open(github_output, 'a') as f:
        f.write(f"title={article['title']}\n")
        f.write(f"keyword={brief['primary_keyword']}\n")
        f.write(f"category={brief['category']}\n")
        f.write(f"words={article['word_count']}\n")

print('\n💾 Files saved successfully!')
print(f'   • test_article.html ({article["word_count"]} words)')
print(f'   • article_meta.json')
print('\n🎉 Article ready with professional design!')
