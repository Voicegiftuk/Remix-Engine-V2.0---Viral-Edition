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
            {'keyword': 'first anniversary gifts', 'category': 'Anniversary', 'title': 'Special First Anniversary Gifts to Remember', 'angle': 'sentimental and sweet', 'search_volume': 3100},
            
            # Christmas gifts
            {'keyword': 'christmas gifts for family', 'category': 'Christmas', 'title': 'Thoughtful Christmas Gifts for the Whole Family', 'angle': 'festive and meaningful', 'search_volume': 8500},
            {'keyword': 'christmas gifts for mum', 'category': 'Christmas', 'title': 'Perfect Christmas Gifts for Mum', 'angle': 'warm and personal', 'search_volume': 6200},
            {'keyword': 'christmas gifts for dad', 'category': 'Christmas', 'title': 'Great Christmas Gifts Dad Will Actually Use', 'angle': 'practical and thoughtful', 'search_volume': 5800},
            {'keyword': 'secret santa gifts', 'category': 'Christmas', 'title': 'Creative Secret Santa Gift Ideas Under £20', 'angle': 'fun and affordable', 'search_volume': 7100},
            
            # Wedding gifts
            {'keyword': 'wedding gifts for couples', 'category': 'Wedding', 'title': 'Unique Wedding Gifts Couples Will Treasure', 'angle': 'unique and lasting', 'search_volume': 3800},
            {'keyword': 'wedding gifts for bride', 'category': 'Wedding', 'title': 'Beautiful Wedding Gifts for the Bride', 'angle': 'elegant and personal', 'search_volume': 2900},
            {'keyword': 'wedding gifts for groom', 'category': 'Wedding', 'title': 'Thoughtful Wedding Gifts for the Groom', 'angle': 'masculine and meaningful', 'search_volume': 2600},
            
            # Mother's Day
            {'keyword': 'mothers day gift ideas', 'category': 'Mothers Day', 'title': 'Heartfelt Mothers Day Gifts She Will Love', 'angle': 'emotional and personal', 'search_volume': 12000},
            {'keyword': 'mothers day gifts from daughter', 'category': 'Mothers Day', 'title': 'Special Mothers Day Gifts from Daughter', 'angle': 'tender and meaningful', 'search_volume': 4100},
            {'keyword': 'first mothers day gifts', 'category': 'Mothers Day', 'title': 'Perfect First Mothers Day Gift Ideas', 'angle': 'sentimental and sweet', 'search_volume': 3200},
            
            # Father's Day
            {'keyword': 'fathers day presents', 'category': 'Fathers Day', 'title': 'Best Fathers Day Presents for Every Dad', 'angle': 'practical and meaningful', 'search_volume': 9500},
            {'keyword': 'fathers day gifts from daughter', 'category': 'Fathers Day', 'title': 'Touching Fathers Day Gifts from Daughter', 'angle': 'heartfelt and special', 'search_volume': 3800},
            {'keyword': 'first fathers day gifts', 'category': 'Fathers Day', 'title': 'Memorable First Fathers Day Gift Ideas', 'angle': 'sentimental and unique', 'search_volume': 3100},
            
            # Valentine's Day
            {'keyword': 'valentine gifts for him', 'category': 'Valentines', 'title': 'Romantic Valentine Gifts He Will Actually Want', 'angle': 'romantic and thoughtful', 'search_volume': 6700},
            {'keyword': 'valentine gifts for her', 'category': 'Valentines', 'title': 'Beautiful Valentine Gifts She Will Adore', 'angle': 'romantic and elegant', 'search_volume': 7200},
            {'keyword': 'valentine gifts for wife', 'category': 'Valentines', 'title': 'Special Valentine Gifts for Your Wife', 'angle': 'romantic and personal', 'search_volume': 5100},
            
            # Graduation
            {'keyword': 'graduation gifts for her', 'category': 'Graduation', 'title': 'Inspiring Graduation Gifts She Will Cherish', 'angle': 'inspirational and practical', 'search_volume': 2900},
            {'keyword': 'graduation gifts for him', 'category': 'Graduation', 'title': 'Thoughtful Graduation Gifts for Him', 'angle': 'motivational and useful', 'search_volume': 2600},
            {'keyword': 'university graduation gifts', 'category': 'Graduation', 'title': 'Perfect University Graduation Gift Ideas', 'angle': 'celebratory and practical', 'search_volume': 3400},
            
            # New Baby
            {'keyword': 'new baby gifts', 'category': 'Baby', 'title': 'Beautiful New Baby Gift Ideas', 'angle': 'sweet and practical', 'search_volume': 5800},
            {'keyword': 'baby shower gifts', 'category': 'Baby', 'title': 'Unique Baby Shower Gift Ideas', 'angle': 'thoughtful and useful', 'search_volume': 6200},
            
            # Thank You gifts
            {'keyword': 'thank you gifts', 'category': 'Thank You', 'title': 'Thoughtful Thank You Gift Ideas', 'angle': 'grateful and meaningful', 'search_volume': 4100},
            {'keyword': 'teacher appreciation gifts', 'category': 'Thank You', 'title': 'Perfect Teacher Appreciation Gifts', 'angle': 'grateful and thoughtful', 'search_volume': 3700},
            
            # Housewarming
            {'keyword': 'housewarming gifts', 'category': 'Housewarming', 'title': 'Best Housewarming Gift Ideas', 'angle': 'practical and welcoming', 'search_volume': 4500},
            {'keyword': 'new home gifts', 'category': 'Housewarming', 'title': 'Thoughtful New Home Gift Ideas', 'angle': 'warm and practical', 'search_volume': 3900},
            
            # Retirement
            {'keyword': 'retirement gifts', 'category': 'Retirement', 'title': 'Meaningful Retirement Gift Ideas', 'angle': 'celebratory and memorable', 'search_volume': 3600},
            {'keyword': 'retirement gifts for men', 'category': 'Retirement', 'title': 'Great Retirement Gifts for Men', 'angle': 'practical and thoughtful', 'search_volume': 2800},
            
            # Get Well
            {'keyword': 'get well gifts', 'category': 'Get Well', 'title': 'Thoughtful Get Well Gift Ideas', 'angle': 'caring and comforting', 'search_volume': 2900},
            {'keyword': 'sympathy gifts', 'category': 'Sympathy', 'title': 'Comforting Sympathy Gift Ideas', 'angle': 'compassionate and meaningful', 'search_volume': 3100},
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
    
    def get_season_appropriate_topics(self, count: int = 10) -> List[Dict]:
        """
        Get topics appropriate for current season/month
        """
        month = datetime.now().month
        
        # Filter by season
        if month in [11, 12]:  # November, December
            seasonal = [t for t in self.topics_database if 'Christmas' in t['category']]
        elif month == 2:  # February
            seasonal = [t for t in self.topics_database if 'Valentine' in t['category']]
        elif month == 3:  # March
            seasonal = [t for t in self.topics_database if 'Mother' in t['category']]
        elif month == 6:  # June
            seasonal = [t for t in self.topics_database if 'Father' in t['category'] or 'Wedding' in t['category']]
        elif month == 5:  # May
            seasonal = [t for t in self.topics_database if 'Graduation' in t['category']]
        else:
            # Mix of general topics
            return self.generate_daily_topics(count)
        
        # Mix seasonal with general
        general = [t for t in self.topics_database if t['category'] not in ['Christmas', 'Valentines', 'Mothers Day', 'Fathers Day']]
        
        mixed = seasonal[:count//2] + random.sample(general, count - count//2)
        random.shuffle(mixed)
        
        return mixed[:count]
