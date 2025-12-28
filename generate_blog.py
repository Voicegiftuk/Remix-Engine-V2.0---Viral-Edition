#!/usr/bin/env python3
"""Generate blog article - called by GitHub Actions"""
import os
import sys
import json

sys.path.insert(0, '.')

# Get API key from environment
api_key = os.environ.get('GEMINI_API_KEY')

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    sys.exit(1)

print(f"✓ API Key loaded: {len(api_key)} chars")

from titan_modules.blog.intelligence.topic_generator import TopicGenerator
from titan_modules.blog.writer.article_generator import ArticleGenerator

# Generate topic
print('\n🎯 Generating topic...')
topic_gen = TopicGenerator()
brief = topic_gen.generate_next_topic()

print(f'Topic: {brief["primary_keyword"]}')
print(f'Category: {brief["category"]}')

# Generate article
print('\n✍️  Writing article...')
article_gen = ArticleGenerator(api_key)
article = article_gen.write_article(brief)

print(f'\n✅ Complete: {article["word_count"]} words')

# Create HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: system-ui, sans-serif;
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
        <h3>Create Your Own Voice Message Gift</h3>
        <p>Turn your words into unforgettable memories</p>
        <a href="https://sayplay.co.uk" class="cta-button">Shop Now</a>
    </div>
    <div class="footer">
        <p><strong>SayPlay | Just Tap - No App Needed</strong></p>
        <p>🌐 <a href="https://sayplay.co.uk" style="color:#FF6B35">SayPlay.co.uk</a></p>
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
    'words': article['word_count']
}

with open('article_meta.json', 'w') as f:
    json.dump(meta, f)

# Output for GitHub Actions
github_output = os.environ.get('GITHUB_OUTPUT')
if github_output:
    with open(github_output, 'a') as f:
        f.write(f"title={article['title']}\n")
        f.write(f"keyword={brief['primary_keyword']}\n")
        f.write(f"category={brief['category']}\n")
        f.write(f"words={article['word_count']}\n")

print('\n✓ Files saved!')
print(f'  - test_article.html')
print(f'  - article_meta.json')
