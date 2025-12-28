#!/usr/bin/env python3
"""
Pinterest Publisher - Visual Search Engine
PROJECT TITAN - The Syndicate Module

Why Pinterest is CRITICAL for SayPlay:
- 450M monthly users searching for gift ideas
- 97% of searches are UNBRANDED ("birthday gift ideas" not "Nike shoes")
- Average user spends 14 minutes browsing (high intent)
- 85% use Pinterest to plan purchases
- UK/US primary markets (our target)

Pinterest = The Google of Visual Gift Ideas

Strategy:
- Auto-publish product images with SayPlay branding
- Target gift-related keywords (birthday, wedding, etc.)
- Link directly to product pages (direct sales)
- Board organization by occasion (birthday, wedding, etc.)
- Seasonal campaigns (Christmas, Valentine's, Mother's Day)

ROI: Pinterest drives 33% more referral traffic than Facebook for e-commerce
"""
import os
import asyncio
import time
from typing import Dict, List, Optional
from pathlib import Path
import requests


class PinterestPublisher:
    """
    Automated Pinterest publisher for visual product marketing
    
    Uses Pinterest API v5 with direct requests (no SDK needed)
    
    Features:
    - Board management (organize by occasion)
    - Pin creation with rich metadata
    - Keyword optimization for search
    - Link to product pages (conversion tracking)
    - Batch upload (10+ pins/day)
    
    Pinterest Best Practices:
    - Vertical images (2:3 ratio, 1000x1500px optimal)
    - Text overlay with value prop
    - Clear call-to-action
    - Product showcase in lifestyle context
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Pinterest publisher
        
        Args:
            access_token: Pinterest API access token
                         Get from: https://developers.pinterest.com/apps/
        """
        self.access_token = access_token
        self.base_url = 'https://api.pinterest.com/v5'
        self.user_id = None
        self.boards = {}
        
        if access_token:
            self._authenticate()
        
        print("PinterestPublisher initialized")
    
    def _authenticate(self):
        """Get authenticated user info and boards"""
        try:
            # Get user info
            response = requests.get(
                f'{self.base_url}/user_account',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.user_id = data.get('id', 'unknown')
                username = data.get('username', 'Unknown')
                print(f"✓ Authenticated as @{username}")
                
                # Load boards
                self._load_boards()
                return True
            else:
                print(f"✗ Authentication failed: {response.status_code}")
                if response.status_code == 401:
                    print("  Token invalid or expired. Get new token from:")
                    print("  https://developers.pinterest.com/apps/")
                return False
        
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    def _load_boards(self):
        """Load user's Pinterest boards"""
        try:
            response = requests.get(
                f'{self.base_url}/boards',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                boards = data.get('items', [])
                for board in boards:
                    self.boards[board['name']] = board['id']
                
                print(f"✓ Loaded {len(self.boards)} boards")
            else:
                print(f"⚠ Could not load boards: {response.status_code}")
        
        except Exception as e:
            print(f"⚠ Failed to load boards: {e}")
    
    async def publish(
        self,
        image_path: str,
        title: str,
        description: str,
        link: str,
        board: str = 'Gift Ideas',
        keywords: List[str] = None
    ) -> Dict:
        """
        Publish pin to Pinterest
        
        Args:
            image_path: Path to image (vertical, 1000x1500px recommended)
            title: Pin title (100 chars max, include keywords)
            description: Pin description (500 chars max, SEO-optimized)
            link: URL to product page
            board: Board name to pin to
            keywords: Additional keywords for search
        
        Returns:
            Publication result with Pinterest URL
        """
        
        if not self.access_token:
            print("✗ Not authenticated with Pinterest")
            return {'status': 'error', 'error': 'not_authenticated'}
        
        print(f"📌 Publishing to Pinterest: {title}")
        
        # Ensure board exists
        board_id = await self._get_or_create_board(board)
        if not board_id:
            return {'status': 'error', 'error': 'board_creation_failed'}
        
        # Optimize metadata
        optimized_title = self._optimize_title(title, keywords)
        optimized_desc = self._optimize_description(description, keywords)
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            return {'status': 'error', 'error': 'image_not_found'}
        
        # Upload and create pin
        try:
            # Step 1: Upload image to Pinterest
            with open(image_path, 'rb') as img:
                files = {'file': img}
                headers = {'Authorization': f'Bearer {self.access_token}'}
                
                upload_response = requests.post(
                    f'{self.base_url}/media',
                    headers=headers,
                    files=files
                )
            
            if upload_response.status_code != 201:
                error_data = upload_response.json() if upload_response.text else {}
                error_msg = error_data.get('message', f'Status {upload_response.status_code}')
                print(f"✗ Image upload failed: {error_msg}")
                return {'status': 'error', 'error': f'image_upload_failed: {error_msg}'}
            
            media_id = upload_response.json()['id']
            print(f"✓ Image uploaded: {media_id}")
            
            # Step 2: Create pin
            pin_data = {
                'board_id': board_id,
                'media_source': {
                    'source_type': 'image_upload',
                    'media_id': media_id
                },
                'title': optimized_title,
                'description': optimized_desc,
                'link': link,
                'alt_text': f"SayPlay {title}"  # Accessibility + SEO
            }
            
            pin_response = requests.post(
                f'{self.base_url}/pins',
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                },
                json=pin_data
            )
            
            if pin_response.status_code == 201:
                pin = pin_response.json()
                pin_id = pin.get('id', 'unknown')
                pin_url = f"https://pinterest.com/pin/{pin_id}"
                
                print(f"✓ Published to Pinterest: {pin_url}")
                
                return {
                    'status': 'success',
                    'pinterest_url': pin_url,
                    'pin_id': pin_id,
                    'board': board
                }
            
            else:
                error_data = pin_response.json() if pin_response.text else {}
                error_msg = error_data.get('message', f'Status {pin_response.status_code}')
                print(f"✗ Pin creation failed: {error_msg}")
                return {'status': 'error', 'error': error_msg}
        
        except Exception as e:
            print(f"✗ Pinterest publish exception: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def batch_publish(
        self,
        images: List[Dict],
        board: str = 'Gift Ideas'
    ) -> List[Dict]:
        """
        Batch publish multiple pins
        
        Args:
            images: List of image dicts with path, title, description, link
            board: Board to publish to
        
        Returns:
            List of publication results
        """
        
        results = []
        
        print(f"\n📌 Batch publishing {len(images)} pins to Pinterest...")
        
        for idx, img in enumerate(images, 1):
            print(f"\n[{idx}/{len(images)}] Publishing: {img['title']}")
            
            result = await self.publish(
                image_path=img['path'],
                title=img['title'],
                description=img['description'],
                link=img['link'],
                board=board,
                keywords=img.get('keywords')
            )
            
            results.append(result)
            
            # Rate limiting (Pinterest allows ~200 pins/day)
            # Add small delay between pins
            if idx < len(images):  # Don't delay after last pin
                print("  Waiting 2 seconds (rate limiting)...")
                await asyncio.sleep(2)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"\n✅ Batch complete: {success_count}/{len(images)} successful")
        
        return results
    
    async def _get_or_create_board(self, board_name: str) -> Optional[str]:
        """Get board ID or create if doesn't exist"""
        
        # Check if board exists
        if board_name in self.boards:
            return self.boards[board_name]
        
        # Create new board
        try:
            board_data = {
                'name': board_name,
                'description': f"Beautiful {board_name.lower()} ideas from SayPlay",
                'privacy': 'PUBLIC'
            }
            
            response = requests.post(
                f'{self.base_url}/boards',
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json'
                },
                json=board_data
            )
            
            if response.status_code == 201:
                board = response.json()
                board_id = board['id']
                self.boards[board_name] = board_id
                
                print(f"✓ Created board: {board_name}")
                return board_id
            
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('message', f'Status {response.status_code}')
                print(f"✗ Board creation failed: {error_msg}")
                return None
        
        except Exception as e:
            print(f"✗ Board creation error: {e}")
            return None
    
    def _optimize_title(self, title: str, keywords: List[str] = None) -> str:
        """
        Optimize pin title for Pinterest search
        
        Pinterest title best practices:
        - 100 chars max
        - Include primary keyword
        - Clear value proposition
        - Emotional trigger
        """
        
        # Add SayPlay branding if not present
        if 'sayplay' not in title.lower():
            title = f"{title} | SayPlay"
        
        # Truncate if too long
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title
    
    def _optimize_description(self, description: str, keywords: List[str] = None) -> str:
        """
        Optimize pin description for Pinterest search
        
        Pinterest description best practices:
        - 500 chars max
        - Include 3-5 keywords naturally
        - Call-to-action
        - Hashtags (3-5 relevant)
        """
        
        # Add keywords naturally if provided
        if keywords:
            keyword_phrase = " | ".join(keywords[:3])
            if keyword_phrase.lower() not in description.lower():
                description = f"{description}\n\n{keyword_phrase}"
        
        # Add CTA
        if 'shop' not in description.lower() and 'discover' not in description.lower():
            description += "\n\n👉 Discover more at SayPlay.co.uk"
        
        # Add hashtags
        hashtags = self._generate_hashtags(description, keywords)
        description += f"\n\n{hashtags}"
        
        # Truncate if too long
        if len(description) > 500:
            description = description[:497] + "..."
        
        return description
    
    def _generate_hashtags(self, text: str, keywords: List[str] = None) -> str:
        """Generate relevant hashtags for Pinterest"""
        
        hashtags = set()
        
        # From keywords
        if keywords:
            for kw in keywords[:3]:
                tag = kw.replace(' ', '').replace('-', '').title()
                hashtags.add(f"#{tag}")
        
        # Default SayPlay hashtags
        default = ['#PersonalizedGifts', '#VoiceMessage', '#UniqueGifts', '#GiftIdeas']
        hashtags.update(default[:3])
        
        return ' '.join(list(hashtags)[:5])  # Max 5 hashtags
    
    def get_stats(self) -> Dict:
        """Get account stats"""
        stats = {
            'authenticated': self.access_token is not None,
            'user_id': self.user_id,
            'boards_loaded': len(self.boards),
            'boards': list(self.boards.keys())
        }
        return stats


async def test_pinterest():
    """Test Pinterest publisher"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("\n📌 Testing Pinterest Publisher...")
    print("=" * 50)
    
    token = os.getenv('PINTEREST_TOKEN')
    if not token:
        print("\n⚠️  PINTEREST_TOKEN not found in .env")
        print("\n📝 To get your Pinterest token:")
        print("   1. Go to: https://developers.pinterest.com/apps/")
        print("   2. Create app (or use existing)")
        print("   3. Get access token")
        print("   4. Add to .env: PINTEREST_TOKEN=your_token_here")
        return
    
    # Initialize
    publisher = PinterestPublisher(token)
    
    if not publisher.user_id:
        print("\n❌ Authentication failed")
        print("   Check your PINTEREST_TOKEN is valid")
        return
    
    # Show stats
    stats = publisher.get_stats()
    print(f"\n✅ Pinterest Publisher ready!")
    print(f"   User ID: {stats['user_id']}")
    print(f"   Boards: {stats['boards_loaded']}")
    if stats['boards']:
        print(f"   Board names: {', '.join(stats['boards'][:5])}")
    
    print("\n💡 Pinterest is THE platform for gift discovery")
    print("   • 450M users searching for gift ideas monthly")
    print("   • 97% unbranded searches (high conversion potential)")
    print("   • Perfect for SayPlay's visual products")
    
    print("\n📋 Next steps:")
    print("   1. Create product photos (1000x1500px vertical)")
    print("   2. Add SayPlay logo/branding")
    print("   3. Use publish() or batch_publish() methods")
    print("   4. Target gift keywords (birthday, wedding, etc.)")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    """Run test"""
    asyncio.run(test_pinterest())
```

**Commit message:**
```
Fix Pinterest publisher - use requests only, proper async, better error handling
