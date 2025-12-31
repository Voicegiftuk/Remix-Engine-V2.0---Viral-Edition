#!/usr/bin/env python3
"""
Dashboard Index Generator
Creates index.html files for all sections
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from jinja2 import Template


class DashboardIndexGenerator:
    """Generates index pages for dashboard"""
    
    def __init__(self):
        self.main_template = self._main_dashboard_template()
        self.seo_template = self._seo_index_template()
        self.blog_template = self._blog_index_template()
        self.podcast_template = self._podcast_index_template()
    
    def generate_main_dashboard(self, output_path: Path, stats: Dict):
        """Generate main dashboard index"""
        html = self.main_template.render(stats=stats)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Main dashboard: {output_path}")
    
    def generate_seo_index(self, output_path: Path, pages: List[Dict]):
        """Generate SEO pages index"""
        html = self.seo_template.render(pages=pages, total=len(pages))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ SEO index: {output_path}")
    
    def generate_blog_index(self, output_path: Path, posts: List[Dict]):
        """Generate blog posts index"""
        html = self.blog_template.render(posts=posts, total=len(posts))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Blog index: {output_path}")
    
    def generate_podcast_index(self, output_path: Path, episodes: List[Dict]):
        """Generate podcast episodes index"""
        html = self.podcast_template.render(episodes=episodes, total=len(episodes))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Podcast index: {output_path}")
    
    def _main_dashboard_template(self) -> Template:
        """Main dashboard template"""
        return Template("""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Content Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        h1, h2 { font-family: 'Poppins', sans-serif; }
    </style>
</head>
<body class="bg-gradient-to-br from-orange-50 to-orange-100 min-h-screen">
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <div class="text-3xl font-extrabold">
                    <span class="text-orange-600">Say</span><span class="text-gray-900">Play</span>
                    <span class="text-sm font-normal text-gray-500 ml-3">Content Dashboard</span>
                </div>
                <a href="https://sayplay.co.uk" target="_blank" class="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-6 rounded-full transition">
                    Visit Shop
                </a>
            </div>
        </div>
    </nav>
    
    <div class="max-w-7xl mx-auto px-6 py-12">
        <header class="text-center mb-16">
            <h1 class="text-6xl font-extrabold text-gray-900 mb-4">Content Dashboard</h1>
            <p class="text-xl text-gray-600">Automated content generation system for SayPlay</p>
            <div class="mt-6 text-sm text-gray-500">
                Last updated: {{ stats.last_updated or 'Never' }}
            </div>
        </header>
        
        <div class="grid md:grid-cols-3 gap-8 mb-12">
            <!-- SEO Pages Card -->
            <a href="/seo/" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition transform hover:-translate-y-1">
                <div class="text-5xl mb-4">📄</div>
                <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ stats.total_seo }}</h2>
                <p class="text-lg font-semibold text-orange-600 mb-2">SEO Landing Pages</p>
                <p class="text-gray-600 text-sm">Optimized pages for UK cities</p>
                <div class="mt-4 text-orange-600 font-semibold">View All →</div>
            </a>
            
            <!-- Blog Posts Card -->
            <a href="/blog/" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition transform hover:-translate-y-1">
                <div class="text-5xl mb-4">✍️</div>
                <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ stats.total_blog }}</h2>
                <p class="text-lg font-semibold text-orange-600 mb-2">Blog Articles</p>
                <p class="text-gray-600 text-sm">In-depth gift guides</p>
                <div class="mt-4 text-orange-600 font-semibold">View All →</div>
            </a>
            
            <!-- Podcast Episodes Card -->
            <a href="/podcasts/" class="bg-white rounded-2xl shadow-xl p-8 hover:shadow-2xl transition transform hover:-translate-y-1">
                <div class="text-5xl mb-4">🎙️</div>
                <h2 class="text-3xl font-bold text-gray-900 mb-2">{{ stats.total_podcasts }}</h2>
                <p class="text-lg font-semibold text-orange-600 mb-2">Podcast Episodes</p>
                <p class="text-gray-600 text-sm">Latest episode: #{{ stats.last_episode }}</p>
                <div class="mt-4 text-orange-600 font-semibold">Listen Now →</div>
            </a>
        </div>
        
        <div class="bg-white rounded-2xl shadow-xl p-8">
            <h2 class="text-2xl font-bold mb-4">About This Dashboard</h2>
            <p class="text-gray-700 mb-4">
                This dashboard showcases content automatically generated by the TITAN system for SayPlay - 
                a UK-based NFC voice message gift platform. All content is created using AI with a 6-tier 
                cascade fallback system to ensure 100% reliability.
            </p>
            <div class="grid md:grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                    <strong class="text-gray-900">System:</strong> TITAN V7 Ultimate
                </div>
                <div>
                    <strong class="text-gray-900">Frequency:</strong> Daily generation
                </div>
                <div>
                    <strong class="text-gray-900">AI Models:</strong> 6-tier cascade
                </div>
                <div>
                    <strong class="text-gray-900">Reliability:</strong> 100% (guaranteed)
                </div>
            </div>
        </div>
    </div>
    
    <footer class="bg-gray-900 text-white py-8 mt-16">
        <div class="max-w-7xl mx-auto px-6 text-center">
            <p class="text-gray-400">© 2025 SayPlay UK. Automated content generation powered by TITAN.</p>
        </div>
    </footer>
</body>
</html>""")
    
    def _seo_index_template(self) -> Template:
        """SEO pages index template"""
        return Template("""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Pages - SayPlay Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>body{font-family:'Inter'}h1,h2{font-family:'Poppins'}</style>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-7xl mx-auto px-6 py-12">
        <header class="mb-12">
            <h1 class="text-5xl font-extrabold text-gray-900 mb-4">SEO Landing Pages</h1>
            <p class="text-xl text-gray-600">{{ total }} pages optimized for UK cities</p>
        </header>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for page in pages %}
            <a href="{{ page.filename }}" class="bg-white rounded-lg shadow hover:shadow-xl transition p-6 border-l-4 border-orange-500">
                <div class="flex items-start justify-between mb-3">
                    <span class="bg-orange-100 text-orange-800 text-xs font-bold px-3 py-1 rounded-full">{{ page.city }}</span>
                    <span class="text-gray-400 text-xs">{{ page.created[:10] }}</span>
                </div>
                <h3 class="font-bold text-gray-900 mb-2 line-clamp-2">{{ page.title }}</h3>
                <p class="text-sm text-gray-600 mb-3">{{ page.topic }}</p>
                <div class="text-orange-600 font-semibold text-sm">View Page →</div>
            </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>""")
    
    def _blog_index_template(self) -> Template:
        """Blog posts index template"""
        return Template("""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog - SayPlay Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>body{font-family:'Inter'}h1,h2{font-family:'Poppins'}</style>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-5xl mx-auto px-6 py-12">
        <header class="mb-12">
            <h1 class="text-5xl font-extrabold text-gray-900 mb-4">Blog Articles</h1>
            <p class="text-xl text-gray-600">{{ total }} in-depth guides about gift-giving</p>
        </header>
        
        <div class="space-y-6">
            {% for post in posts %}
            <a href="{{ post.filename }}" class="block bg-white rounded-lg shadow hover:shadow-xl transition p-8 border-l-4 border-orange-500">
                <div class="flex items-start justify-between mb-3">
                    <span class="bg-orange-100 text-orange-800 text-xs font-bold px-3 py-1 rounded-full">Article</span>
                    <span class="text-gray-400 text-sm">{{ post.created[:10] }}</span>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-3">{{ post.title }}</h2>
                <p class="text-gray-600 mb-4">{{ post.topic }}</p>
                <div class="text-orange-600 font-semibold">Read Article →</div>
            </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>""")
    
    def _podcast_index_template(self) -> Template:
        """Podcast episodes index template"""
        return Template("""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Podcasts - SayPlay Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>body{font-family:'Inter'}h1,h2{font-family:'Poppins'}</style>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold"><span class="text-orange-600">Say</span>Play</a>
            <a href="/" class="text-gray-600 hover:text-orange-600">← Dashboard</a>
        </div>
    </nav>
    
    <div class="max-w-5xl mx-auto px-6 py-12">
        <header class="mb-12">
            <h1 class="text-5xl font-extrabold text-gray-900 mb-4">🎙️ Podcast Episodes</h1>
            <p class="text-xl text-gray-600">{{ total }} episodes about meaningful gift-giving</p>
        </header>
        
        <div class="space-y-6">
            {% for ep in episodes %}
            <div class="bg-white rounded-lg shadow p-8 border-l-4 border-orange-500">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <span class="bg-orange-100 text-orange-800 text-xs font-bold px-3 py-1 rounded-full">Episode {{ ep.episode }}</span>
                        <span class="text-gray-400 text-sm ml-3">{{ ep.created[:10] }}</span>
                    </div>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-3">{{ ep.topic }}</h2>
                <audio controls class="w-full mt-4">
                    <source src="{{ ep.filename }}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
                <a href="{{ ep.filename }}" download class="inline-block mt-4 text-orange-600 hover:text-orange-700 font-semibold text-sm">
                    ⬇️ Download Episode
                </a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>""")
