#!/usr/bin/env python3
"""
Medium Publisher - Parasite SEO Platform
PROJECT TITAN - The Syndicate Module

Why Medium:
- Instant Google ranking (high domain authority)
- Built-in audience (millions of readers)
- Canonical links allowed (no duplicate content penalty)
- 100% safe to auto-publish

Strategy:
- Republish blog articles from SayPlay.co.uk
- Add canonical link (credit to original)
- Target keywords get instant Google visibility
- Free backlink from high-authority domain
"""
from typing import Dict, Optional
import requests
from loguru import logger


class MediumPublisher:
    """
    Automated publisher for Medium.com
    
    Features:
    - API-based publishing (official, safe)
    - Canonical link support (SEO-safe)
    - Auto-formatting (markdown to Medium)
    - Tag optimization (visibility boost)
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Medium publisher
        
        Args:
            access_token: Medium API access token
                         Get from: https://medium.com/me/settings/security
        """
        self.access_token = access_token
        self.base_url = 'https://api.medium.com/v1'
        self.user_id = None
        
        if access_token:
            self._authenticate()
        
        logger.info("MediumPublisher initialized")
    
    def _authenticate(self):
        """Get authenticated user info"""
        try:
            response = requests.get(
                f'{self.base_url}/me',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.user_id = data['data']['id']
                username = data['data']['username']
                logger.success(f"✓ Authenticated as @{username}")
            else:
                logger.error(f"Authentication failed: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Authentication error: {e}")
    
    async def publish(
        self,
        article: Dict,
        publish_status: str = 'public',
        notify_followers: bool = False
    ) -> Dict:
        """
        Publish article to Medium
        
        Args:
            article: Article package with title, content, url
            publish_status: 'public', 'draft', or 'unlisted'
            notify_followers: Whether to notify your followers
        
        Returns:
            Publication result with Medium URL
        """
        
        if not self.access_token or not self.user_id:
            logger.error("Not authenticated with Medium")
            return {'status': 'error', 'error': 'not_authenticated'}
        
        logger.info(f"Publishing to Medium: {article['title']}")
        
        # Prepare content
        content = self._format_content(article)
        
        # Extract tags from article
        tags = self._extract_tags(article)
        
        # Prepare payload
        payload = {
            'title': article['title'],
            'contentFormat': 'markdown',
            'content': content,
            'tags': tags,
            'publishStatus': publish_status,
            'notifyFollowers': notify_followers,
            'canonicalUrl': article.get('url')  # CRITICAL: Prevents duplicate content penalty
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/users/{self.user_id}/posts',
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                },
                json=payload
            )
            
            if response.status_code == 201:
                data = response.json()['data']
                medium_url = data['url']
                
                logger.success(f"✓ Published to Medium: {medium_url}")
                
                return {
                    'status': 'success',
                    'medium_url': medium_url,
                    'medium_id': data['id'],
                    'published_at': data.get('publishedAt')
                }
            
            else:
                error_msg = response.json().get('errors', [{}])[0].get('message', 'Unknown error')
                logger.error(f"✗ Medium publish failed: {error_msg}")
                
                return {
                    'status': 'error',
                    'error': error_msg,
                    'status_code': response.status_code
                }
        
        except Exception as e:
            logger.error(f"✗ Medium publish exception: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _format_content(self, article: Dict) -> str:
        """
        Format article for Medium
        
        Medium accepts Markdown, so we:
        1. Convert HTML to Markdown if needed
        2. Add intro note about original publication
        3. Add SayPlay branding at end
        """
        
        content = article.get('text', article.get('html', ''))
        
        # Add canonical note at top
        intro = f"""
> **Note:** This article was originally published at [SayPlay.co.uk]({article.get('url', 'https://sayplay.co.uk')})

---

"""
        
        # Add branding at end
        outro = f"""

---

## About SayPlay

We create personalized voice message gifts that let you hear the voices of the people you love. Just tap the card - no app needed.

👉 **[Discover SayPlay](https://sayplay.co.uk)**
"""
        
        return intro + content + outro
    
    def _extract_tags(self, article: Dict) -> list:
        """
        Extract relevant tags for Medium
        
        Medium allows up to 5 tags. We prioritize:
        1. Primary keyword
        2. Occasion
        3. Category
        4. Trending tags
        """
        
        tags = []
        
        # From article metadata
        if 'tags' in article:
            tags.extend(article['tags'][:3])
        
        # Default SayPlay tags
        default_tags = ['Gifts', 'Personalized Gifts', 'Voice Messages']
        
        # Combine and limit to 5
        all_tags = tags + default_tags
        return list(dict.fromkeys(all_tags))[:5]  # Remove duplicates, limit to 5
    
    def get_stats(self) -> Dict:
        """Get Medium publication stats"""
        
        if not self.access_token or not self.user_id:
            return {'error': 'not_authenticated'}
        
        try:
            response = requests.get(
                f'{self.base_url}/users/{self.user_id}/publications',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                publications = response.json()['data']
                return {
                    'publications': len(publications),
                    'details': publications
                }
            
            return {'error': 'failed_to_fetch'}
        
        except Exception as e:
            return {'error': str(e)}


if __name__ == "__main__":
    """Test Medium publisher"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("📝 Testing Medium Publisher...")
    
    token = os.getenv('MEDIUM_TOKEN')
    if not token:
        print("\n⚠️  Set MEDIUM_TOKEN in .env")
        print("   Get token from: https://medium.com/me/settings/security")
        exit(1)
    
    publisher = MediumPublisher(token)
    
    # Test article
    test_article = {
        'title': 'Test Article from SayPlay Automation',
        'text': """
# This is a Test

This article is published automatically from the SayPlay content automation system.

## Why This Matters

Automated publishing allows us to reach more people with our message about preserving memories through voice.

## The Technology

We use:
- AI for content generation
- Medium API for distribution
- White Hat SEO practices

Stay tuned for more!
""",
        'url': 'https://sayplay.co.uk/blog/test-automation',
        'tags': ['Automation', 'AI', 'Content Marketing']
    }
    
    print("\n📤 Publishing test article...")
    
    # This would be async in real usage
    # result = asyncio.run(publisher.publish(test_article, publish_status='draft'))
    
    print("\n✅ Medium Publisher ready!")
    print("   Change publish_status='public' to auto-publish")
