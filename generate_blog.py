#!/usr/bin/env python3
"""Generate blog article - NEW GOOGLE GENAI SDK"""
import os
import sys
import json

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

# Generate article with NEW SDK
print('\n✍️  Writing article with NEW Google Genai SDK...')
article_gen = ArticleGenerator(api_key)
article = article_gen.write_article(brief)

print(f'\n✅ Article complete!')
print(f'   Words: {article["word_count"]}')
print(f'   Sections: {len(article["outline"])}')

# Create branded HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #FAFAFA;
            color: #2C3E50;
            line-height: 1.7;
        }}
        .header {{
            background: linear-gradient(135deg, #FF6B35 0%, #FF8C61 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
        }}
        .logo {{ font-size: 3em; font-weight: bold; margin-bottom: 10px; }}
        .tagline {{ font-size: 1.2em; opacity: 0.95; }}
        .article {{
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #FF6B35; font-size: 2.5em; margin-bottom: 0.5em; }}
        h2 {{
            color: #004E89;
            margin-top: 2em;
            font-size: 1.8em;
            border-bottom: 3px solid #FF6B35;
            padding-bottom: 10px;
        }}
        h3 {{ color: #1A659E; margin-top: 1.5em; font-size: 1.4em; }}
        p {{ margin: 1.2em 0; font-size: 1.1em; }}
        strong {{ color: #FF6B35; }}
        .cta {{
            background: linear-gradient(135deg, #004E89 0%, #1A659E 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-top: 50px;
            text-align: center;
        }}
        .cta h3 {{ color: white; font-size: 2em; margin-bottom: 20px; }}
        .cta-button {{
            display: inline-block;
            background: #FF6B35;
            color: white;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
        }}
        .footer {{
            text-align: center;
            padding: 40px;
            color: #666;
            margin-top: 50px;
        }}
        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .header, .article {{ padding: 30px 20px; }}
            h1 {{ font-size: 1.8em; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎁 SayPlay</div>
        <div class="tagline">Voice Message Gifts That Last Forever</div>
    </div>
    <div class="article">
        <h1>{article['title']}</h1>
        {article['html']}
    </div>
    <div class="cta">
        <h3>🎁 Create Your Own Voice Message Gift</h3>
        <p>Turn your words into unforgettable memories with SayPlay</p>
        <a href="https://sayplay.co.uk" class="cta-button">Shop Now →</a>
    </div>
    <div class="footer">
        <p><strong>SayPlay | Just Tap - No App Needed</strong></p>
        <p>🌐 <a href="https://sayplay.co.uk" style="color:#FF6B35">SayPlay.co.uk</a></p>
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
print('\n🎉 NEW Google Genai SDK working perfectly!')
