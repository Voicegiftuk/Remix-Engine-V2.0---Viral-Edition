"""
MULTI-TOPIC GENERATOR
Generates 10 diverse topics for daily content
"""
import random
from datetime import datetime
from typing import List, Dict
import hashlib


class MultiTopicGenerator:
    """Generate multiple diverse topics for daily content production"""
    
    def __init__(self):
        self.topics_database = [
            # Birthday
            {'keyword': 'birthday gifts for mum', 'category': 'Birthday', 'title': 'Perfect Birthday Gifts for Mum 2025', 'angle': 'heartfelt and personal'},
            {'keyword': 'birthday gifts for dad', 'category': 'Birthday', 'title': 'Thoughtful Birthday Gifts Your Dad Will Love', 'angle': 'practical and meaningful'},
            {'keyword': 'birthday gifts for wife', 'category': 'Birthday', 'title': 'Romantic Birthday Gifts for Your Wife', 'angle': 'romantic and special'},
            {'keyword': 'birthday gifts for husband', 'category': 'Birthday', 'title': 'Best Birthday Gifts for Your Husband', 'angle': 'thoughtful and unique'},
            {'keyword': 'birthday gifts for best friend', 'category': 'Birthday', 'title': 'Creative Birthday Gifts for Your Best Friend', 'angle': 'fun and memorable'},
            
            # Anniversary
            {'keyword': 'anniversary gifts for wife', 'category': 'Anniversary', 'title': 'Romantic Anniversary Gifts Your Wife Will Treasure', 'angle': 'romantic and memorable'},
            {'keyword': 'anniversary gifts for husband', 'category': 'Anniversary', 'title': 'Meaningful Anniversary Gifts for Your Husband', 'angle': 'heartfelt and lasting'},
            {'keyword': 'wedding anniversary gifts', 'category': 'Anniversary', 'title': 'Beautiful Wedding Anniversary Gift Ideas', 'angle': 'elegant and romantic'},
            
            # Christmas
            {'keyword': 'christmas gifts for mum', 'category': 'Christmas', 'title': 'Perfect Christmas Gifts for Mum', 'angle': 'warm and personal'},
            {'keyword': 'christmas gifts for dad', 'category': 'Christmas', 'title': 'Great Christmas Gifts Dad Will Actually Use', 'angle': 'practical and thoughtful'},
            
            # Wedding
            {'keyword': 'wedding gifts for couples', 'category': 'Wedding', 'title': 'Unique Wedding Gifts Couples Will Treasure', 'angle': 'unique and lasting'},
            
            # Mothers Day
            {'keyword': 'mothers day gift ideas', 'category': 'Mothers Day', 'title': 'Heartfelt Mothers Day Gifts She Will Love', 'angle': 'emotional and personal'},
            
            # Fathers Day
            {'keyword': 'fathers day presents', 'category': 'Fathers Day', 'title': 'Best Fathers Day Presents for Every Dad', 'angle': 'practical and meaningful'},
            
            # Valentines
            {'keyword': 'valentine gifts for him', 'category': 'Valentines', 'title': 'Romantic Valentine Gifts He Will Actually Want', 'angle': 'romantic and thoughtful'},
            {'keyword': 'valentine gifts for her', 'category': 'Valentines', 'title': 'Beautiful Valentine Gifts She Will Adore', 'angle': 'romantic and elegant'},
        ]
    
    def generate_daily_topics(self, count: int = 10) -> List[Dict]:
        """Generate diverse topics for today"""
        print(f"\n📋 Generating {count} diverse topics...")
        
        today = datetime.now().strftime('%Y-%m-%d')
        seed = int(hashlib.md5(today.encode()).hexdigest(), 16) % (10 ** 8)
        random.seed(seed)
        
        shuffled = self.topics_database.copy()
        random.shuffle(shuffled)
        
        selected = []
        categories = set()
        
        for topic in shuffled:
            if len(selected) >= count:
                break
            if topic['category'] not in categories or len(categories) >= 5:
                selected.append(topic)
                categories.add(topic['category'])
        
        for i, topic in enumerate(selected):
            topic['episode_number'] = i + 1
        
        print(f"✅ Selected {len(selected)} topics")
        for i, topic in enumerate(selected, 1):
            print(f"   {i}. [{topic['category']}] {topic['title']}")
        
        return selected
