#!/usr/bin/env python3
"""
Content Metadata Manager
Tracks all generated content, prevents duplicates, manages episode numbering
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import hashlib


class ContentMetadataManager:
    """Manages content history and prevents duplicates"""
    
    def __init__(self, history_file: Path = Path('content_history.json')):
        self.history_file = history_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load history from JSON"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📖 Loaded history: {len(data.get('seo_pages', []))} SEO, {len(data.get('blog_posts', []))} blogs, {len(data.get('podcasts', []))} podcasts")
                    return data
            except Exception as e:
                print(f"⚠️ Error loading history: {e}")
        
        print("📄 Creating new history file")
        return {
            'seo_pages': [],
            'blog_posts': [],
            'podcasts': [],
            'last_episode_number': 0,
            'last_updated': None
        }
    
    def save(self):
        """Save history to JSON"""
        self.data['last_updated'] = datetime.now().isoformat()
        
        # Ensure directory exists
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Metadata saved: {self.history_file}")
        print(f"   Total: {len(self.data['seo_pages'])} SEO, {len(self.data['blog_posts'])} blogs, {len(self.data['podcasts'])} podcasts")
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for duplicate detection"""
        return hashlib.md5(text.lower().strip().encode()).hexdigest()
    
    def is_duplicate_seo(self, topic: str, city: str) -> bool:
        """Check if SEO page already exists"""
        key = self._generate_hash(f"{topic}_{city}")
        return any(page.get('hash') == key for page in self.data['seo_pages'])
    
    def is_duplicate_blog(self, topic: str) -> bool:
        """Check if blog post already exists"""
        key = self._generate_hash(topic)
        return any(post.get('hash') == key for post in self.data['blog_posts'])
    
    def is_duplicate_podcast(self, topic: str) -> bool:
        """Check if podcast already exists"""
        key = self._generate_hash(topic)
        return any(ep.get('hash') == key for ep in self.data['podcasts'])
    
    def add_seo_page(self, topic: str, city: str, filename: str, title: str):
        """Record new SEO page"""
        self.data['seo_pages'].append({
            'topic': topic,
            'city': city,
            'title': title,
            'filename': filename,
            'hash': self._generate_hash(f"{topic}_{city}"),
            'created': datetime.now().isoformat()
        })
    
    def add_blog_post(self, topic: str, filename: str, title: str):
        """Record new blog post"""
        self.data['blog_posts'].append({
            'topic': topic,
            'title': title,
            'filename': filename,
            'hash': self._generate_hash(topic),
            'created': datetime.now().isoformat()
        })
    
    def add_podcast(self, topic: str, filename: str, episode_num: int):
        """Record new podcast episode"""
        self.data['podcasts'].append({
            'episode': episode_num,
            'topic': topic,
            'filename': filename,
            'hash': self._generate_hash(topic),
            'created': datetime.now().isoformat()
        })
        
        self.data['last_episode_number'] = episode_num
    
    def get_next_episode_number(self) -> int:
        """Get next podcast episode number"""
        return self.data['last_episode_number'] + 1
    
    def get_all_seo_pages(self) -> List[Dict]:
        """Get all SEO pages sorted by date"""
        return sorted(
            self.data['seo_pages'],
            key=lambda x: x.get('created', ''),
            reverse=True
        )
    
    def get_all_blog_posts(self) -> List[Dict]:
        """Get all blog posts sorted by date"""
        return sorted(
            self.data['blog_posts'],
            key=lambda x: x.get('created', ''),
            reverse=True
        )
    
    def get_all_podcasts(self) -> List[Dict]:
        """Get all podcasts sorted by episode number"""
        return sorted(
            self.data['podcasts'],
            key=lambda x: x.get('episode', 0),
            reverse=True
        )
    
    def get_stats(self) -> Dict:
        """Get content statistics"""
        return {
            'total_seo': len(self.data['seo_pages']),
            'total_blog': len(self.data['blog_posts']),
            'total_podcasts': len(self.data['podcasts']),
            'last_episode': self.data['last_episode_number'],
            'last_updated': self.data.get('last_updated')
        }
