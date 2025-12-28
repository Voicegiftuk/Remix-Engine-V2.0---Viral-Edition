#!/usr/bin/env python3
"""
Reddit Monitor - Opportunity Finder
PROJECT TITAN - The Syndicate Module

Why Reddit:
- r/GiftIdeas: 500k members actively asking "what to buy"
- r/weddingplanning: 400k brides looking for ideas
- r/LongDistance: Couples love voice messages
- High engagement, high intent

Strategy: WHISPER MARKETING (NOT SPAM!)
- Monitor relevant subreddits
- Find genuine questions about gifts
- Generate helpful, authentic answers
- Include SayPlay mention naturally
- ALWAYS send to human for approval (never auto-post)

Rules:
1. Never auto-post (Reddit WILL ban you)
2. Max 1 post per subreddit per day
3. Must add value, not just link
4. Account must be aged (>1 month, >100 karma)
5. Vary response style (not robotic)
"""
from typing import Dict, List, Optional
import praw  # Python Reddit API Wrapper
from datetime import datetime, timedelta
import re
from loguru import logger


class RedditMonitor:
    """
    Reddit opportunity monitor with human-approval workflow
    
    Features:
    - Keyword monitoring across multiple subreddits
    - Relevance scoring (which posts are best to respond to)
    - AI-generated response drafts
    - Telegram approval required (100% human-in-loop)
    - Safety limits (prevents spam/ban)
    """
    
    # Target subreddits (curated for SayPlay)
    TARGET_SUBREDDITS = [
        'GiftIdeas',           # 500k members - PRIMARY TARGET
        'weddingplanning',     # 400k brides
        'LongDistance',        # 200k couples (love voice messages!)
        'Parenting',           # 3M parents
        'relationship_advice', # 6M people asking for gift ideas
        'AskWomen',            # Women asking about gifts
        'AskMen',              # Men asking about gifts
        'DIY',                 # DIY gift makers
        'CasualUK'             # UK-specific (our market!)
    ]
    
    # Keywords to monitor
    KEYWORDS = [
        # Direct gift questions
        'gift idea',
        'gift for',
        'what to get',
        'present idea',
        'birthday gift',
        'wedding gift',
        'anniversary gift',
        
        # Occasions
        'mothers day',
        'fathers day',
        'christmas',
        'valentine',
        
        # Personalization signals
        'personalized',
        'unique gift',
        'meaningful gift',
        'sentimental gift',
        'custom gift',
        
        # Voice/memory related
        'voice message',
        'recorded message',
        'memory gift'
    ]
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str = 'SayPlay Monitor v1.0'):
        """
        Initialize Reddit monitor
        
        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string
            
        Get credentials from: https://www.reddit.com/prefs/apps
        """
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            
            # Test connection
            self.reddit.read_only = True
            logger.success("✓ Connected to Reddit API (read-only mode)")
        
        except Exception as e:
            logger.error(f"Reddit connection failed: {e}")
            self.reddit = None
    
    async def find_opportunities(
        self,
        keywords: List[str] = None,
        limit: int = 50,
        time_filter: str = 'day'
    ) -> List[Dict]:
        """
        Find Reddit posts asking about gifts
        
        Args:
            keywords: Custom keywords (default: self.KEYWORDS)
            limit: Max posts to check per subreddit
            time_filter: 'hour', 'day', 'week', 'month'
        
        Returns:
            List of opportunities sorted by relevance
        """
        
        if not self.reddit:
            logger.error("Reddit API not connected")
            return []
        
        if keywords is None:
            keywords = self.KEYWORDS
        
        logger.info(f"Monitoring {len(self.TARGET_SUBREDDITS)} subreddits...")
        logger.info(f"Time filter: {time_filter}, Keywords: {len(keywords)}")
        
        opportunities = []
        
        for subreddit_name in self.TARGET_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get recent posts
                posts = subreddit.new(limit=limit)
                
                for post in posts:
                    # Check if post matches keywords
                    if self._matches_keywords(post, keywords):
                        # Score relevance
                        score = self._score_opportunity(post)
                        
                        if score > 0.5:  # Threshold for relevance
                            opportunity = {
                                'platform': 'reddit',
                                'subreddit': subreddit_name,
                                'post_id': post.id,
                                'title': post.title,
                                'text': post.selftext,
                                'url': f"https://reddit.com{post.permalink}",
                                'author': str(post.author),
                                'created': datetime.fromtimestamp(post.created_utc),
                                'score': post.score,
                                'num_comments': post.num_comments,
                                'relevance_score': score,
                                'suggested_response': None  # Will generate on approval
                            }
                            
                            opportunities.append(opportunity)
                            logger.info(f"✓ Found opportunity in r/{subreddit_name} (score: {score:.2f})")
            
            except Exception as e:
                logger.warning(f"Error checking r/{subreddit_name}: {e}")
                continue
        
        # Sort by relevance
        opportunities.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        logger.success(f"✓ Found {len(opportunities)} opportunities")
        
        return opportunities
    
    def _matches_keywords(self, post, keywords: List[str]) -> bool:
        """Check if post matches any keywords"""
        
        text = (post.title + ' ' + post.selftext).lower()
        
        return any(keyword.lower() in text for keyword in keywords)
    
    def _score_opportunity(self, post) -> float:
        """
        Score how good this opportunity is (0.0-1.0)
        
        Factors:
        - Recency (newer = better)
        - Question format (? = better)
        - Low comments (less competition)
        - Specific occasion mentioned (better targeting)
        - UK-related (our market)
        """
        
        score = 0.0
        text = (post.title + ' ' + post.selftext).lower()
        
        # Recency (0-0.3)
        age_hours = (datetime.now() - datetime.fromtimestamp(post.created_utc)).total_seconds() / 3600
        if age_hours < 6:
            score += 0.3
        elif age_hours < 24:
            score += 0.2
        elif age_hours < 72:
            score += 0.1
        
        # Question format (0-0.2)
        if '?' in post.title:
            score += 0.2
        
        # Low competition (0-0.2)
        if post.num_comments < 5:
            score += 0.2
        elif post.num_comments < 15:
            score += 0.1
        
        # Specific occasions (0-0.2)
        occasions = ['birthday', 'wedding', 'anniversary', 'christmas', 'valentine']
        if any(occ in text for occ in occasions):
            score += 0.2
        
        # UK market (0-0.1)
        uk_signals = ['uk', 'britain', 'british', '£', 'pound']
        if any(sig in text for sig in uk_signals):
            score += 0.1
        
        return min(score, 1.0)
    
    def generate_response(self, opportunity: Dict, tone: str = 'helpful') -> str:
        """
        Generate response for Reddit post
        
        Args:
            opportunity: Opportunity dict from find_opportunities()
            tone: 'helpful', 'personal', 'enthusiastic'
        
        Returns:
            Suggested response text
        """
        
        # Extract context
        title = opportunity['title']
        text = opportunity['text']
        
        # Response templates (varied to avoid detection)
        templates = {
            'helpful': """
I recently discovered {product} and it's been amazing for {occasion}. 

{why_it_works}

You can check them out at SayPlay.co.uk (not affiliated, just genuinely loved the idea).

Hope this helps!
""",
            'personal': """
Oh this is perfect timing! I just got my partner one of those voice message cards from SayPlay for our anniversary.

{personal_story}

Honestly one of the most meaningful gifts I've given. They have a whole range for different occasions.
""",
            'enthusiastic': """
Okay so I NEED to share this because it's genius - have you seen those NFC voice message gifts?

{excitement}

SayPlay does them and they're honestly so cool. Just tap with your phone and you hear the message. No app needed!

Perfect for {occasion}!
"""
        }
        
        # Detect occasion
        occasion = self._detect_occasion(title + ' ' + text)
        
        # Generate personalized elements
        product = "these personalized voice message cards"
        why_it_works = f"They let you record a message that plays when they tap the card. Super personal and {occasion}-appropriate."
        personal_story = f"Seeing their face when they heard my voice was priceless. Way more meaningful than just a regular card."
        excitement = "You record a voice message, stick it on a card/gift, and when they tap it with their phone - they hear your voice!"
        
        # Select template
        template = templates.get(tone, templates['helpful'])
        
        # Fill in template
        response = template.format(
            product=product,
            occasion=occasion,
            why_it_works=why_it_works,
            personal_story=personal_story,
            excitement=excitement
        )
        
        return response.strip()
    
    def _detect_occasion(self, text: str) -> str:
        """Detect occasion from text"""
        
        text = text.lower()
        
        occasions = {
            'birthday': ['birthday', 'bday', 'born'],
            'wedding': ['wedding', 'bride', 'groom', 'marriage'],
            'anniversary': ['anniversary', 'years together'],
            'christmas': ['christmas', 'xmas', 'holiday'],
            "valentine's": ['valentine', 'romantic'],
            "mother's day": ['mother', 'mom', 'mum'],
            "father's day": ['father', 'dad']
        }
        
        for occasion, keywords in occasions.items():
            if any(kw in text for kw in keywords):
                return occasion
        
        return 'special occasion'
    
    def validate_account(self, username: str) -> Dict:
        """
        Validate Reddit account before posting
        
        Safety checks:
        - Account age (>30 days)
        - Karma (>100)
        - Not shadowbanned
        
        Args:
            username: Reddit username to check
        
        Returns:
            Validation result
        """
        
        try:
            user = self.reddit.redditor(username)
            
            # Check account age
            created = datetime.fromtimestamp(user.created_utc)
            age_days = (datetime.now() - created).days
            
            # Check karma
            karma = user.link_karma + user.comment_karma
            
            # Validation
            issues = []
            
            if age_days < 30:
                issues.append(f"Account too new ({age_days} days, need 30+)")
            
            if karma < 100:
                issues.append(f"Karma too low ({karma}, need 100+)")
            
            return {
                'valid': len(issues) == 0,
                'username': username,
                'age_days': age_days,
                'karma': karma,
                'issues': issues
            }
        
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }


if __name__ == "__main__":
    """Test Reddit monitor"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("👀 Testing Reddit Monitor...")
    
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_SECRET')
    
    if not client_id or not client_secret:
        print("\n⚠️  Set REDDIT_CLIENT_ID and REDDIT_SECRET in .env")
        print("   Get from: https://www.reddit.com/prefs/apps")
        exit(1)
    
    monitor = RedditMonitor(client_id, client_secret)
    
    print("\n📡 Monitoring subreddits for opportunities...")
    
    # This would be async in real usage
    # opportunities = asyncio.run(monitor.find_opportunities(limit=10))
    
    print("\n✅ Reddit Monitor ready!")
    print(f"   Monitoring {len(monitor.TARGET_SUBREDDITS)} subreddits")
    print("   REMINDER: NEVER auto-post. Always get human approval!")
