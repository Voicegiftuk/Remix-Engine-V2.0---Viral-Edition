#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - SIMPLIFIED
"""
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator


def main():
    print("\n" + "="*70)
    print("TITAN V2 - CONTENT GENERATOR")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    # Create web structure
    web_dir = output_dir / 'web'
    blog_dir = web_dir / 'blog'
    dashboard_dir = web_dir / 'dashboard'
    
    for d in [web_dir, blog_dir, dashboard_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Generate topics
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    
    # Create test blog posts
    for topic in topics:
        slug = topic['title'].lower().replace(' ', '-').replace("'", '')[:60]
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} | SayPlay</title>
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
        }}
        .content {{
            padding: 60px 50px;
        }}
        .cta {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px;
            border-radius: 20px;
            margin: 40px 0;
            text-align: center;
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
    <div class="container">
        <div class="header">
            <div class="logo">Say<span>Play</span></div>
            <h1>{topic['title']}</h1>
            <p>📅 {datetime.now().strftime("%B %d, %Y")} • 🔑 {topic['keyword']}</p>
        </div>
        
        <div class="content">
            <h2>Discover Perfect Gift Ideas</h2>
            <p>Finding the right gift can be challenging, but we're here to help you discover meaningful options that will be cherished for years to come.</p>
            
            <div class="cta">
                <div style="font-size: 60px; margin-bottom: 20px;">💝</div>
                <h3>Make Every Gift Unforgettable</h3>
                <p>Add a personal voice message to any gift with SayPlay's NFC technology.</p>
                <a href="https://sayplay.co.uk">Discover SayPlay →</a>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        with open(blog_dir / f'{slug}.html', 'w', encoding='utf-8') as f:
            f.write(html)
    
    # Create dashboard
    dashboard_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SayPlay Content Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        .logo {{
            font-size: 42px;
            font-weight: 800;
            color: #667eea;
            margin-bottom: 10px;
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
        }}
        .article-card:hover {{
            border-color: #667eea;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
        }}
        .article-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        .article-card a {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Say<span>Play</span> Content Dashboard</div>
        <p style="color: #666; margin-top: 10px;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(topics)}</div>
                <div>Articles Published</div>
            </div>
            <div class="stat">
                <div class="stat-number">✓</div>
                <div>System Active</div>
            </div>
        </div>
        
        <h2 style="margin-top: 50px; color: #333;">📝 Latest Articles</h2>
        <div class="articles">'''
    
    for i, topic in enumerate(topics, 1):
        slug = topic['title'].lower().replace(' ', '-').replace("'", '')[:60]
        dashboard_html += f'''
            <div class="article-card">
                <span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 6px 14px; border-radius: 12px; font-size: 13px; font-weight: 700;">Episode {i}</span>
                <h3>{topic['title']}</h3>
                <p style="color: #666; margin: 15px 0;">Category: {topic['category']}</p>
                <a href="/blog/{slug}.html" target="_blank">Read Article →</a>
            </div>'''
    
    dashboard_html += '''
        </div>
    </div>
</body>
</html>'''
    
    with open(dashboard_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print(f"\n✅ Generated {len(topics)} articles")
    print(f"✅ Dashboard created")
    print(f"✅ Output: {output_dir}")
    print(f"\n🌐 Will be live at: https://dashboard.sayplay.co.uk")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
