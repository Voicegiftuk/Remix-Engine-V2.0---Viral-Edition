#!/usr/bin/env python3
"""
TITAN MODULE #8: SOCIAL POSTER
Auto-distributes content to Pinterest, LinkedIn, Medium
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List
import requests
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"📱 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class SocialPoster:
    """Multi-platform content distribution"""
    
    def __init__(self):
        """Initialize with API credentials"""
        self.pinterest_token = os.getenv('PINTEREST_ACCESS_TOKEN')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.medium_token = os.getenv('MEDIUM_INTEGRATION_TOKEN')
        
        logger.info("SocialPoster initialized")
    
    def post_to_pinterest(self, article: Dict, image_url: str) -> Dict:
        """Post article to Pinterest"""
        
        if not self.pinterest_token:
            logger.warning("Pinterest token not configured")
            return {'success': False, 'platform': 'pinterest', 'reason': 'no_token'}
        
        try:
            # Pinterest API v5
            url = "https://api.pinterest.com/v5/pins"
            
            headers = {
                'Authorization': f'Bearer {self.pinterest_token}',
                'Content-Type': 'application/json'
            }
            
            # Create compelling pin
            payload = {
                'board_id': os.getenv('PINTEREST_BOARD_ID'),
                'media_source': {
                    'source_type': 'image_url',
                    'url': image_url
                },
                'title': article['title'][:100],
                'description': self._create_pinterest_description(article),
                'link': article.get('url', 'https://sayplay.co.uk'),
                'alt_text': article['title']
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                pin_data = response.json()
                logger.success(f"Posted to Pinterest: {pin_data.get('id')}")
                return {
                    'success': True,
                    'platform': 'pinterest',
                    'pin_id': pin_data.get('id'),
                    'url': f"https://pinterest.com/pin/{pin_data.get('id')}"
                }
            else:
                logger.error(f"Pinterest error: {response.status_code} - {response.text}")
                return {'success': False, 'platform': 'pinterest', 'error': response.text}
                
        except Exception as e:
            logger.error(f"Pinterest exception: {e}")
            return {'success': False, 'platform': 'pinterest', 'error': str(e)}
    
    def post_to_linkedin(self, article: Dict) -> Dict:
        """Post article to LinkedIn"""
        
        if not self.linkedin_token:
            logger.warning("LinkedIn token not configured")
            return {'success': False, 'platform': 'linkedin', 'reason': 'no_token'}
        
        try:
            # Get user profile first
            profile_url = "https://api.linkedin.com/v2/me"
            headers = {
                'Authorization': f'Bearer {self.linkedin_token}',
                'Content-Type': 'application/json'
            }
            
            profile = requests.get(profile_url, headers=headers).json()
            author = f"urn:li:person:{profile['id']}"
            
            # Create professional post
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            payload = {
                'author': author,
                'lifecycleState': 'PUBLISHED',
                'specificContent': {
                    'com.linkedin.ugc.ShareContent': {
                        'shareCommentary': {
                            'text': self._create_linkedin_post(article)
                        },
                        'shareMediaCategory': 'ARTICLE',
                        'media': [{
                            'status': 'READY',
                            'originalUrl': article.get('url', 'https://sayplay.co.uk')
                        }]
                    }
                },
                'visibility': {
                    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                post_data = response.json()
                logger.success(f"Posted to LinkedIn: {post_data.get('id')}")
                return {
                    'success': True,
                    'platform': 'linkedin',
                    'post_id': post_data.get('id')
                }
            else:
                logger.error(f"LinkedIn error: {response.status_code} - {response.text}")
                return {'success': False, 'platform': 'linkedin', 'error': response.text}
                
        except Exception as e:
            logger.error(f"LinkedIn exception: {e}")
            return {'success': False, 'platform': 'linkedin', 'error': str(e)}
    
    def post_to_medium(self, article: Dict) -> Dict:
        """Republish full article to Medium"""
        
        if not self.medium_token:
            logger.warning("Medium token not configured")
            return {'success': False, 'platform': 'medium', 'reason': 'no_token'}
        
        try:
            # Get user ID
            user_url = "https://api.medium.com/v1/me"
            headers = {
                'Authorization': f'Bearer {self.medium_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            user_response = requests.get(user_url, headers=headers)
            user_id = user_response.json()['data']['id']
            
            # Create post
            post_url = f"https://api.medium.com/v1/users/{user_id}/posts"
            
            payload = {
                'title': article['title'],
                'contentFormat': 'html',
                'content': article['html'],
                'tags': self._extract_tags(article),
                'publishStatus': 'public',
                'canonicalUrl': article.get('url', 'https://sayplay.co.uk')
            }
            
            response = requests.post(post_url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                post_data = response.json()['data']
                logger.success(f"Posted to Medium: {post_data.get('url')}")
                return {
                    'success': True,
                    'platform': 'medium',
                    'post_id': post_data.get('id'),
                    'url': post_data.get('url')
                }
            else:
                logger.error(f"Medium error: {response.status_code} - {response.text}")
                return {'success': False, 'platform': 'medium', 'error': response.text}
                
        except Exception as e:
            logger.error(f"Medium exception: {e}")
            return {'success': False, 'platform': 'medium', 'error': str(e)}
    
    def scan_reddit_opportunities(self, keyword: str) -> List[Dict]:
        """Scan Reddit for relevant posts to comment on"""
        
        try:
            # Reddit API (no auth needed for read-only)
            subreddits = ['gifts', 'GiftIdeas', 'wedding', 'weddingplanning', 'birthday']
            opportunities = []
            
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/search.json"
                params = {
                    'q': keyword,
                    'sort': 'new',
                    'limit': 5,
                    't': 'day'
                }
                
                headers = {'User-Agent': 'SayPlay Bot 1.0'}
                response = requests.get(url, params=params, headers=headers)
                
                if response.status_code == 200:
                    posts = response.json()['data']['children']
                    
                    for post in posts:
                        data = post['data']
                        opportunities.append({
                            'platform': 'reddit',
                            'subreddit': subreddit,
                            'title': data['title'],
                            'url': f"https://reddit.com{data['permalink']}",
                            'score': data['score'],
                            'num_comments': data['num_comments']
                        })
            
            logger.success(f"Found {len(opportunities)} Reddit opportunities")
            return opportunities
            
        except Exception as e:
            logger.error(f"Reddit scan failed: {e}")
            return []
    
    def scan_quora_opportunities(self, keyword: str) -> List[Dict]:
        """Scan Quora for relevant questions"""
        
        try:
            # Quora doesn't have public API, use web scraping
            # For now, return placeholder
            logger.warning("Quora scanning requires setup")
            return []
            
        except Exception as e:
            logger.error(f"Quora scan failed: {e}")
            return []
    
    def distribute_article(self, article: Dict, image_url: str = None) -> Dict:
        """Distribute article to all platforms"""
        
        logger.info(f"Distributing: {article.get('title', 'Untitled')}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'article_title': article.get('title'),
            'platforms': []
        }
        
        # Pinterest (visual platform)
        if image_url:
            pinterest_result = self.post_to_pinterest(article, image_url)
            results['platforms'].append(pinterest_result)
            time.sleep(2)
        
        # LinkedIn (professional)
        linkedin_result = self.post_to_linkedin(article)
        results['platforms'].append(linkedin_result)
        time.sleep(2)
        
        # Medium (republishing)
        medium_result = self.post_to_medium(article)
        results['platforms'].append(medium_result)
        time.sleep(2)
        
        # Find opportunities
        keyword = article.get('keyword', 'personalized gifts')
        reddit_opps = self.scan_reddit_opportunities(keyword)
        quora_opps = self.scan_quora_opportunities(keyword)
        
        results['opportunities'] = {
            'reddit': reddit_opps[:5],  # Top 5
            'quora': quora_opps[:5]
        }
        
        # Count successes
        successes = sum(1 for p in results['platforms'] if p.get('success'))
        logger.success(f"Distribution complete: {successes}/{len(results['platforms'])} platforms")
        
        return results
    
    def _create_pinterest_description(self, article: Dict) -> str:
        """Create engaging Pinterest description"""
        description = article.get('meta_description', article.get('title', ''))
        
        # Add hashtags
        hashtags = [
            '#PersonalizedGifts',
            '#VoiceMessage',
            '#SayPlay',
            '#UniqueGifts',
            '#GiftIdeas'
        ]
        
        return f"{description}\n\n{' '.join(hashtags)}"
    
    def _create_linkedin_post(self, article: Dict) -> str:
        """Create professional LinkedIn post"""
        title = article.get('title', '')
        url = article.get('url', 'https://sayplay.co.uk')
        
        post = f"""🎁 {title}

In the age of digital connections, the most meaningful gifts capture authentic emotions.

Voice message gifts are revolutionizing how we celebrate life's special moments - combining cutting-edge NFC technology with timeless emotional connection.

Read more: {url}

#Innovation #GiftTech #PersonalizedGifts #CustomerExperience #SayPlay"""
        
        return post
    
    def _extract_tags(self, article: Dict) -> List[str]:
        """Extract relevant tags for Medium"""
        keyword = article.get('keyword', '')
        category = article.get('category', '')
        
        tags = [
            'gifts',
            'voice-message',
            'personalization',
            'technology',
            'celebration'
        ]
        
        if category:
            tags.append(category)
        
        return tags[:5]  # Medium allows max 5 tags


def send_telegram_notification(results: Dict):
    """Send distribution report to Telegram"""
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        return
    
    # Count stats
    total = len(results['platforms'])
    success = sum(1 for p in results['platforms'] if p.get('success'))
    
    reddit_count = len(results.get('opportunities', {}).get('reddit', []))
    
    message = f"""📱 <b>Social Distribution Complete!</b>

📰 {results['article_title']}

✅ Posted: {success}/{total} platforms
"""
    
    # Add platform links
    for platform in results['platforms']:
        if platform.get('success'):
            emoji = {'pinterest': '📌', 'linkedin': '💼', 'medium': '📝'}.get(platform['platform'], '✅')
            url = platform.get('url', '')
            if url:
                message += f"{emoji} {platform['platform'].title()}: {url}\n"
        else:
            message += f"❌ {platform['platform'].title()}: {platform.get('reason', 'failed')}\n"
    
    if reddit_count > 0:
        message += f"\n🔍 Found {reddit_count} Reddit opportunities"
    
    message += "\n\n🤖 Automated by Titan Social Poster"
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
        )
    except Exception as e:
        print(f"Telegram notification failed: {e}")


if __name__ == "__main__":
    """Test the social poster"""
    
    print("\n🧪 Testing Social Poster...\n")
    
    # Test article
    test_article = {
        'title': 'Perfect Birthday Gifts 2025 | SayPlay Voice Message Gifts',
        'keyword': 'birthday gifts 2025',
        'category': 'birthday',
        'meta_description': 'Discover unique personalized birthday gifts with voice messages...',
        'html': '<h1>Test Article</h1><p>This is a test...</p>',
        'url': 'https://sayplay.co.uk/blog/perfect-birthday-gifts-2025'
    }
    
    test_image = 'https://sayplay.co.uk/images/gift-card.jpg'
    
    poster = SocialPoster()
    results = poster.distribute_article(test_article, test_image)
    
    print("\n📊 Results:")
    print(json.dumps(results, indent=2))
    
    # Send notification
    send_telegram_notification(results)
    
    print("\n✅ Test complete!")
