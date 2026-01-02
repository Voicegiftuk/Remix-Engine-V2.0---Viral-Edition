#!/usr/bin/env python3
"""
Dashboard Index Generator - FIXED VERSION
Creates index.html files for all sections with flexible stats handling
"""
from pathlib import Path
from typing import List, Dict


class DashboardIndexGenerator:
    """Generates index pages for dashboard"""
    
    def __init__(self):
        pass
    
    def generate_main_dashboard(self, output_path: Path, stats: Dict):
        """Generate main dashboard index"""
        
        # FIX: Handle both old and new stats format
        seo_count = stats.get('total_seo') or stats.get('seo', 0)
        blog_count = stats.get('total_blog') or stats.get('blog', 0)
        podcast_count = stats.get('total_podcasts') or stats.get('podcasts', 0)
        last_ep = stats.get('last_episode') or stats.get('last_id', 0)
        last_updated = stats.get('last_updated', 'Never')
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Content Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play Dashboard</div>
            <a href="https://sayplay.co.uk" class="bg-orange-600 text-white px-6 py-2 rounded-full">Shop</a>
        </div>
    </nav>
    
    <div class="max-w-7xl mx-auto px-6 py-12">
        <h1 class="text-5xl font-bold mb-8">Content Dashboard</h1>
        
        <div class="grid md:grid-cols-3 gap-6 mb-12">
            <a href="/seo/" class="bg-white p-8 rounded-lg shadow hover:shadow-xl transition">
                <div class="text-4xl mb-4">📄</div>
                <h2 class="text-3xl font-bold mb-2">{seo_count}</h2>
                <p class="text-lg text-orange-600 font-semibold">SEO Pages</p>
            </a>
            
            <a href="/blog/" class="bg-white p-8 rounded-lg shadow hover:shadow-xl transition">
                <div class="text-4xl mb-4">✍️</div>
                <h2 class="text-3xl font-bold mb-2">{blog_count}</h2>
                <p class="text-lg text-orange-600 font-semibold">Blog Posts</p>
            </a>
            
            <a href="/podcasts/" class="bg-white p-8 rounded-lg shadow hover:shadow-xl transition">
                <div class="text-4xl mb-4">🎙️</div>
                <h2 class="text-3xl font-bold mb-2">{podcast_count}</h2>
                <p class="text-lg text-orange-600 font-semibold">Podcasts</p>
                <p class="text-sm text-gray-600 mt-2">Episode #{last_ep}</p>
            </a>
        </div>
        
        <div class="bg-white p-8 rounded-lg shadow">
            <h2 class="text-2xl font-bold mb-4">SPME V1 System</h2>
            <p class="text-gray-600">Autonomous editorial engine with 4 content blocks. Last updated: {last_updated[:19] if last_updated != 'Never' else 'Never'}</p>
        </div>
    </div>
</body>
</html>"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Main dashboard: {output_path}")
    
    def generate_seo_index(self, output_path: Path, pages: List[Dict]):
        """Generate SEO pages index"""
        pages_html = ""
        for page in pages:
            pages_html += f"""
            <a href="/seo/{page['filename']}" class="block bg-white p-6 rounded-lg shadow hover:shadow-xl transition mb-4">
                <div class="flex justify-between items-start mb-2">
                    <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-bold">{page.get('city', 'UK')}</span>
                    <span class="text-gray-400 text-xs">{page.get('created', '')[:10]}</span>
                </div>
                <h3 class="font-bold text-lg mb-2">{page.get('title', page.get('topic', 'Untitled'))}</h3>
                <p class="text-gray-600 text-sm">{page.get('topic', '')}</p>
            </a>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Pages - SayPlay</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-5xl mx-auto px-6 py-12">
        <h1 class="text-5xl font-bold mb-4">SEO Pages</h1>
        <p class="text-xl text-gray-600 mb-12">{len(pages)} pages</p>
        
        <div class="grid md:grid-cols-2 gap-6">
            {pages_html}
        </div>
    </div>
</body>
</html>"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ SEO index: {output_path}")
    
    def generate_blog_index(self, output_path: Path, posts: List[Dict]):
        """Generate blog posts index"""
        posts_html = ""
        for post in posts:
            posts_html += f"""
            <a href="/blog/{post['filename']}" class="block bg-white p-8 rounded-lg shadow hover:shadow-xl transition mb-6">
                <div class="flex justify-between items-start mb-2">
                    <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-bold">Article</span>
                    <span class="text-gray-400 text-sm">{post.get('created', '')[:10]}</span>
                </div>
                <h2 class="text-2xl font-bold mb-3">{post.get('title', post.get('topic', 'Untitled'))}</h2>
                <p class="text-gray-600">{post.get('topic', '')}</p>
            </a>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - SayPlay</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-4xl mx-auto px-6 py-12">
        <h1 class="text-5xl font-bold mb-4">Blog Articles</h1>
        <p class="text-xl text-gray-600 mb-12">{len(posts)} articles</p>
        
        {posts_html}
    </div>
</body>
</html>"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Blog index: {output_path}")
    
    def generate_podcast_index(self, output_path: Path, episodes: List[Dict]):
        """Generate podcast episodes index"""
        episodes_html = ""
        for ep in episodes:
            episodes_html += f"""
            <div class="bg-white p-8 rounded-lg shadow mb-6">
                <div class="flex justify-between items-start mb-4">
                    <span class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-bold">Episode {ep.get('episode', ep.get('id', '?'))}</span>
                    <span class="text-gray-400 text-sm">{ep.get('created', '')[:10]}</span>
                </div>
                <h2 class="text-2xl font-bold mb-4">{ep.get('topic', 'Untitled')}</h2>
                <audio controls class="w-full">
                    <source src="/podcasts/{ep['filename']}" type="audio/mpeg">
                </audio>
                <a href="/podcasts/{ep['filename']}" download class="inline-block mt-4 text-orange-600 font-semibold">⬇️ Download</a>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Podcasts - SayPlay</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-4xl mx-auto px-6 py-12">
        <h1 class="text-5xl font-bold mb-4">🎙️ Podcasts</h1>
        <p class="text-xl text-gray-600 mb-12">{len(episodes)} episodes</p>
        
        {episodes_html}
    </div>
</body>
</html>"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Podcast index: {output_path}")
