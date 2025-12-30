"""
MULTI-TOPIC GENERATOR
Generates 10 diverse topics for daily content
Ensures variety and prevents duplication
"""
import random
from datetime import datetime
from typing import List, Dict
import hashlib


class MultiTopicGenerator:
    """
    Generate multiple diverse topics for daily content production
    """
    
    def __init__(self):
        # Comprehensive topic database
        self.topics_database = [
            # Birthday gifts
            {'keyword': 'birthday gifts for mum', 'category': 'Birthday', 'title': 'Perfect Birthday Gifts for Mum 2025', 'angle': 'heartfelt and personal', 'search_volume': 5000},
            {'keyword': 'birthday gifts for dad', 'category': 'Birthday', 'title': 'Thoughtful Birthday Gifts Your Dad Will Love', 'angle': 'practical and meaningful', 'search_volume': 4200},
            {'keyword': 'birthday gifts for wife', 'category': 'Birthday', 'title': 'Romantic Birthday Gifts for Your Wife', 'angle': 'romantic and special', 'search_volume': 3800},
            {'keyword': 'birthday gifts for husband', 'category': 'Birthday', 'title': 'Best Birthday Gifts for Your Husband', 'angle': 'thoughtful and unique', 'search_volume': 3500},
            {'keyword': 'birthday gifts for best friend', 'category': 'Birthday', 'title': 'Creative Birthday Gifts for Your Best Friend', 'angle': 'fun and memorable', 'search_volume': 4100},
            
            # Anniversary gifts
            {'keyword': 'anniversary gifts for wife', 'category': 'Anniversary', 'title': 'Romantic Anniversary Gifts Your Wife Will Treasure', 'angle': 'romantic and memorable', 'search_volume': 4200},
            {'keyword': 'anniversary gifts for husband', 'category': 'Anniversary', 'title': 'Meaningful Anniversary Gifts for Your Husband', 'angle': 'heartfelt and lasting', 'search_volume': 3900},
            {'keyword': 'wedding anniversary gifts', 'category': 'Anniversary', 'title': 'Beautiful Wedding Anniversary Gift Ideas', 'angle': 'elegant and romantic', 'search_volume': 5200},
            
            # Christmas gifts
            {'keyword': 'christmas gifts for mum', 'category': 'Christmas', 'title': 'Perfect Christmas Gifts for Mum', 'angle': 'warm and personal', 'search_volume': 6200},
            {'keyword': 'christmas gifts for dad', 'category': 'Christmas', 'title': 'Great Christmas Gifts Dad Will Actually Use', 'angle': 'practical and thoughtful', 'search_volume': 5800},
            
            # Wedding gifts
            {'keyword': 'wedding gifts for couples', 'category': 'Wedding', 'title': 'Unique Wedding Gifts Couples Will Treasure', 'angle': 'unique and lasting', 'search_volume': 3800},
            
            # Mother's Day
            {'keyword': 'mothers day gift ideas', 'category': 'Mothers Day', 'title': 'Heartfelt Mothers Day Gifts She Will Love', 'angle': 'emotional and personal', 'search_volume': 12000},
            
            # Father's Day
            {'keyword': 'fathers day presents', 'category': 'Fathers Day', 'title': 'Best Fathers Day Presents for Every Dad', 'angle': 'practical and meaningful', 'search_volume': 9500},
            
            # Valentine's Day
            {'keyword': 'valentine gifts for him', 'category': 'Valentines', 'title': 'Romantic Valentine Gifts He Will Actually Want', 'angle': 'romantic and thoughtful', 'search_volume': 6700},
            {'keyword': 'valentine gifts for her', 'category': 'Valentines', 'title': 'Beautiful Valentine Gifts She Will Adore', 'angle': 'romantic and elegant', 'search_volume': 7200},
        ]
        
        self.used_topics_today = set()
    
    def generate_daily_topics(self, count: int = 10) -> List[Dict]:
        """
        Generate diverse topics for today's content
        Ensures no duplicates and good variety
        """
        print(f"\n📋 Generating {count} diverse topics for today...")
        
        # Get date-based seed for consistency within same day
        today = datetime.now().strftime('%Y-%m-%d')
        seed = int(hashlib.md5(today.encode()).hexdigest(), 16) % (10 ** 8)
        random.seed(seed)
        
        # Shuffle topics
        shuffled_topics = self.topics_database.copy()
        random.shuffle(shuffled_topics)
        
        # Select topics ensuring category diversity
        selected_topics = []
        categories_used = set()
        
        for topic in shuffled_topics:
            if len(selected_topics) >= count:
                break
            
            # Prefer diverse categories
            if topic['category'] not in categories_used or len(categories_used) >= 5:
                selected_topics.append(topic)
                categories_used.add(topic['category'])
        
        # Add episode numbers
        for i, topic in enumerate(selected_topics):
            topic['episode_number'] = i + 1
        
        # Print summary
        print(f"\n✅ Selected {len(selected_topics)} topics:")
        for i, topic in enumerate(selected_topics, 1):
            print(f"   {i}. [{topic['category']}] {topic['title']}")
        
        print()
        
        return selected_topics
