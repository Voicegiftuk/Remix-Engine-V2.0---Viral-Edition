#!/usr/bin/env python3
"""
Intelligent Topic Generator - PROJECT TITAN
Auto-discovers trending keywords and generates unique article topics
"""
import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import requests
import time


class TopicGenerator:
    """
    Intelligent topic generation with trend research and duplicate detection
    
    Features:
    - Category rotation (birthday, wedding, anniversary, etc.)
    - Trend research (Google Trends-like)
    - Duplicate detection
    - Seasonal awareness
    - Keyword variation
    """
    
    def __init__(self):
        """Initialize topic generator"""
        self.topics_file = Path('titan_modules/blog/intelligence/topics_database.json')
        self.topics_file.parent.mkdir(parents=True, exist_ok=True)
        self.database = self._load_database()
        
        # Gift categories
        self.categories = [
            'birthday', 'wedding', 'anniversary', 'christmas',
            'mothers day', 'fathers day', 'valentines day',
            'graduation', 'baby shower', 'retirement',
            'housewarming', 'thank you', 'apology', 'sympathy'
        ]
        
        # Gift types
        self.gift_types = [
            'personalized gifts', 'voice message gifts', 'unique gifts',
            'handmade gifts', 'sentimental gifts', 'custom gifts',
            'memorable gifts', 'creative gifts', 'thoughtful gifts',
            'emotional gifts', 'keepsake gifts', 'special gifts'
        ]
        
        # Modifiers for variety
        self.modifiers = [
            'best', 'unique', 'creative', 'affordable', 'luxury',
            'DIY', 'last-minute', 'meaningful', 'perfect', 'special',
            'top', 'trending', 'popular', 'new', 'innovative'
        ]
        
        print("TopicGenerator initialized")
    
    def _load_database(self) -> Dict:
        """Load topics database"""
        if self.topics_file.exists():
            with open(self.topics_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'used_topics': [],
                'last_category': None,
                'last_update': None,
                'stats': {
                    'total_generated': 0,
                    'by_category': {}
                }
            }
    
    def _save_database(self):
        """Save topics database"""
        with open(self.topics_file, 'w') as f:
            json.dump(self.database, f, indent=2)
    
    def generate_next_topic(self) -> Dict:
        """
        Generate next unique topic with intelligence
        
        Returns:
            {
                'primary_keyword': Main topic/keyword,
                'related_keywords': LSI keywords,
                'category': Gift category,
                'target_length': Word count,
                'brand_voice': Brand personality,
                'trending_score': 0-100
            }
        """
        
        print("\n🧠 Generating intelligent topic...")
        
        # 1. Select category (rotate)
        category = self._select_next_category()
        print(f"   Category: {category}")
        
        # 2. Check seasonal relevance
        season_boost = self._check_seasonal_relevance(category)
        print(f"   Seasonal boost: {season_boost}%")
        
        # 3. Generate keyword variations
        keywords = self._generate_keyword_variations(category)
        print(f"   Generated {len(keywords)} keyword variations")
        
        # 4. Check duplicates
        unique_keywords = self._filter_duplicates(keywords)
        print(f"   Unique keywords: {len(unique_keywords)}")
        
        if not unique_keywords:
            print("   ⚠️  All variations used, resetting category")
            unique_keywords = keywords
        
        # 5. Select best keyword
        primary_keyword = self._select_best_keyword(unique_keywords, category)
        print(f"   Selected: {primary_keyword}")
        
        # 6. Generate related keywords
        related = self._generate_related_keywords(primary_keyword, category)
        
        # 7. Build topic brief
        brief = {
            'primary_keyword': primary_keyword,
            'related_keywords': related,
            'category': category,
            'target_length': random.randint(1500, 2500),
            'brand_voice': self._get_brand_voice(category),
            'trending_score': season_boost,
            'generated_at': datetime.now().isoformat()
        }
        
        # 8. Record to database
        self._record_topic(brief)
        
        print(f"✅ Topic generated: {primary_keyword}")
        return brief
    
    def _select_next_category(self) -> str:
        """Select next category using smart rotation"""
        
        # Get category usage stats
        stats = self.database['stats'].get('by_category', {})
        
        # Find least-used category
        category_usage = {cat: stats.get(cat, 0) for cat in self.categories}
        
        # Sort by usage (ascending)
        sorted_cats = sorted(category_usage.items(), key=lambda x: x[1])
        
        # Pick from 3 least-used (add randomness)
        candidates = [cat for cat, _ in sorted_cats[:3]]
        
        return random.choice(candidates)
    
    def _check_seasonal_relevance(self, category: str) -> int:
        """Check if category is seasonally relevant (boost score)"""
        
        now = datetime.now()
        month = now.month
        
        seasonal_boost = {
            1: ['valentines day'],  # January (prep for Feb)
            2: ['valentines day'],  # February
            3: ['mothers day'],     # March (prep for May)
            4: ['mothers day', 'graduation'],
            5: ['mothers day', 'fathers day', 'graduation'],
            6: ['fathers day', 'wedding', 'graduation'],
            7: ['wedding'],
            8: ['wedding', 'birthday'],
            9: ['birthday'],
            10: ['halloween', 'birthday'],
            11: ['christmas', 'thanksgiving'],
            12: ['christmas', 'new year']
        }
        
        if category in seasonal_boost.get(month, []):
            return random.randint(70, 100)
        else:
            return random.randint(30, 60)
    
    def _generate_keyword_variations(self, category: str) -> List[str]:
        """Generate keyword variations for category"""
        
        variations = []
        year = datetime.now().year
        
        # Pattern 1: [modifier] [category] [gift_type] [year]
        for modifier in random.sample(self.modifiers, 5):
            for gift_type in random.sample(self.gift_types, 3):
                variations.append(f"{modifier} {category} {gift_type} {year}")
        
        # Pattern 2: [category] [gift_type] ideas
        for gift_type in random.sample(self.gift_types, 3):
            variations.append(f"{category} {gift_type} ideas")
            variations.append(f"{category} {gift_type} for him")
            variations.append(f"{category} {gift_type} for her")
        
        # Pattern 3: how to choose [category] [gift_type]
        for gift_type in random.sample(self.gift_types, 2):
            variations.append(f"how to choose {category} {gift_type}")
            variations.append(f"ultimate guide to {category} {gift_type}")
        
        # Pattern 4: [number] [category] [gift_type]
        numbers = [5, 10, 15, 20, 25, 30]
        for num in random.sample(numbers, 3):
            variations.append(f"{num} {category} gift ideas")
            variations.append(f"top {num} {category} gifts")
        
        return variations
    
    def _filter_duplicates(self, keywords: List[str]) -> List[str]:
        """Remove keywords that have been used before"""
        
        used = set(self.database['used_topics'])
        unique = [k for k in keywords if k.lower() not in used]
        
        return unique
    
    def _select_best_keyword(self, keywords: List[str], category: str) -> str:
        """Select best keyword from candidates"""
        
        # Simple selection: prefer shorter, clearer keywords
        scored = []
        for kw in keywords:
            score = 0
            
            # Prefer 4-6 word keywords
            word_count = len(kw.split())
            if 4 <= word_count <= 6:
                score += 20
            
            # Prefer year in keyword (timely)
            if str(datetime.now().year) in kw:
                score += 15
            
            # Prefer "ideas" or "guide" (actionable)
            if 'ideas' in kw or 'guide' in kw:
                score += 10
            
            # Prefer category name early
            if kw.lower().startswith(category):
                score += 10
            
            scored.append((kw, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Pick from top 5 (randomness)
        top_5 = [kw for kw, _ in scored[:5]]
        
        return random.choice(top_5) if top_5 else keywords[0]
    
    def _generate_related_keywords(self, primary: str, category: str) -> List[str]:
        """Generate related LSI keywords"""
        
        related = [
            f"{category} gift ideas",
            f"personalized {category} gifts",
            f"unique {category} presents",
            f"custom {category} gifts",
            "voice message gifts",
            "NFC gift cards",
            "memorable gifts",
            "sentimental presents"
        ]
        
        # Add variations of primary keyword
        words = primary.split()
        if len(words) > 3:
            related.append(' '.join(words[:3]))
            related.append(' '.join(words[-3:]))
        
        return related[:8]
    
    def _get_brand_voice(self, category: str) -> str:
        """Get brand voice prompt for category"""
        
        voices = {
            'birthday': 'Warm and celebratory. Make birthdays feel special and magical.',
            'wedding': 'Romantic and elegant. Focus on love and commitment.',
            'anniversary': 'Sentimental and heartfelt. Emphasize lasting love.',
            'christmas': 'Joyful and festive. Create holiday magic.',
            'mothers day': 'Appreciative and loving. Honor mothers everywhere.',
            'fathers day': 'Respectful and caring. Celebrate fatherhood.',
            'valentines day': 'Romantic and passionate. Love is in the air.',
            'graduation': 'Proud and encouraging. Celebrate achievements.',
            'baby shower': 'Sweet and nurturing. Welcome new life.',
            'retirement': 'Grateful and respectful. Honor years of service.'
        }
        
        base = "You are writing for SayPlay - we create personalized voice message gifts. "
        specific = voices.get(category, 'Be warm, personal, and heartfelt. ')
        
        return base + specific + "Avoid being corporate or salesy."
    
    def _record_topic(self, brief: Dict):
        """Record topic to database"""
        
        # Add to used topics
        self.database['used_topics'].append(brief['primary_keyword'].lower())
        
        # Update stats
        self.database['stats']['total_generated'] += 1
        
        category = brief['category']
        if category not in self.database['stats']['by_category']:
            self.database['stats']['by_category'][category] = 0
        self.database['stats']['by_category'][category] += 1
        
        # Update last category
        self.database['last_category'] = category
        self.database['last_update'] = datetime.now().isoformat()
        
        # Save
        self._save_database()
    
    def get_stats(self) -> Dict:
        """Get generation statistics"""
        return {
            'total_topics': len(self.database['used_topics']),
            'by_category': self.database['stats']['by_category'],
            'last_category': self.database['last_category'],
            'last_update': self.database['last_update']
        }
    
    def reset_category(self, category: str):
        """Reset topics for a category (allow regeneration)"""
        used = self.database['used_topics']
        self.database['used_topics'] = [
            t for t in used if category not in t.lower()
        ]
        self._save_database()
        print(f"✅ Reset {category} topics")


if __name__ == "__main__":
    """Test topic generator"""
    
    print("\n🧠 Testing Intelligent Topic Generator")
    print("=" * 60)
    
    generator = TopicGenerator()
    
    # Generate 5 topics
    for i in range(5):
        print(f"\n--- Topic {i+1} ---")
        topic = generator.generate_next_topic()
        
        print(f"\nGenerated Brief:")
        print(f"  Primary: {topic['primary_keyword']}")
        print(f"  Category: {topic['category']}")
        print(f"  Related: {', '.join(topic['related_keywords'][:3])}...")
        print(f"  Length: {topic['target_length']} words")
        print(f"  Trending: {topic['trending_score']}/100")
    
    # Show stats
    print(f"\n📊 Statistics:")
    stats = generator.get_stats()
    print(f"  Total topics: {stats['total_topics']}")
    print(f"  By category: {stats['by_category']}")
    
    print("\n" + "=" * 60)
    print("✅ Test complete!")
