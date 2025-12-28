#!/usr/bin/env python3
"""Pinterest Publisher - Visual Search Engine"""
import os
import asyncio
import time
from typing import Dict, List, Optional
from pathlib import Path
import requests


class PinterestPublisher:
    """Automated Pinterest publisher for visual product marketing"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.base_url = 'https://api.pinterest.com/v5'
        self.user_id = None
        self.boards = {}
        
        if access_token:
            self._authenticate()
        
        print("PinterestPublisher initialized")
    
    def _authenticate(self):
        try:
            response = requests.get(
                f'{self.base_url}/user_account',
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.user_id = data.get('id', 'unknown')
                username = data.get('username', 'Unknown')
                print(f"Authenticated as @{username}")
                self._load_boards()
                return True
            else:
                print(f"Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def _load_boards(self):
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
                print(f"Loaded {len(self.boards)} boards")
            else:
                print(f"Could not load boards: {response.status_code}")
        except Exception as e:
            print(f"Failed to load boards: {e}")
    
    async def publish(self, image_path: str, title: str, description: str, 
                     link: str, board: str = 'Gift Ideas', 
                     keywords: List[str] = None) -> Dict:
        
        if not self.access_token:
            print("Not authenticated with Pinterest")
            return {'status': 'error', 'error': 'not_authenticated'}
        
        print(f"Publishing to Pinterest: {title}")
        
        board_id = await self._get_or_create_board(board)
        if not board_id:
            return {'status': 'error', 'error': 'board_creation_failed'}
        
        optimized_title = self._optimize_title(title, keywords)
        optimized_desc = self._optimize_description(description, keywords)
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return {'status': 'error', 'error': 'image_not_found'}
        
        try:
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
                print(f"Image upload failed: {error_msg}")
                return {'status': 'error', 'error': f'image_upload_failed: {error_msg}'}
            
            media_id = upload_response.json()['id']
            print(f"Image uploaded: {media_id}")
            
            pin_data = {
                'board_id': board_id,
                'media_source': {
                    'source_type': 'image_upload',
                    'media_id': media_id
                },
                'title': optimized_title,
                'description': optimized_desc,
                'link': link,
                'alt_text': f"SayPlay {title}"
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
                
                print(f"Published to Pinterest: {pin_url}")
                
                return {
                    'status': 'success',
                    'pinterest_url': pin_url,
                    'pin_id': pin_id,
                    'board': board
                }
            else:
                error_data = pin_response.json() if pin_response.text else {}
                error_msg = error_data.get('message', f'Status {pin_response.status_code}')
                print(f"Pin creation failed: {error_msg}")
                return {'status': 'error', 'error': error_msg}
        except Exception as e:
            print(f"Pinterest publish exception: {e}")
            return {'status': 'error', 'error': str(e)}
    
    async def batch_publish(self, images: List[Dict], board: str = 'Gift Ideas') -> List[Dict]:
        results = []
        print(f"Batch publishing {len(images)} pins to Pinterest")
        
        for idx, img in enumerate(images, 1):
            print(f"[{idx}/{len(images)}] Publishing: {img['title']}")
            
            result = await self.publish(
                image_path=img['path'],
                title=img['title'],
                description=img['description'],
                link=img['link'],
                board=board,
                keywords=img.get('keywords')
            )
            
            results.append(result)
            
            if idx < len(images):
                await asyncio.sleep(2)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"Batch complete: {success_count}/{len(images)} successful")
        
        return results
    
    async def _get_or_create_board(self, board_name: str) -> Optional[str]:
        if board_name in self.boards:
            return self.boards[board_name]
        
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
                print(f"Created board: {board_name}")
                return board_id
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('message', f'Status {response.status_code}')
                print(f"Board creation failed: {error_msg}")
                return None
        except Exception as e:
            print(f"Board creation error: {e}")
            return None
    
    def _optimize_title(self, title: str, keywords: List[str] = None) -> str:
        if 'sayplay' not in title.lower():
            title = f"{title} | SayPlay"
        if len(title) > 100:
            title = title[:97] + "..."
        return title
    
    def _optimize_description(self, description: str, keywords: List[str] = None) -> str:
        if keywords:
            keyword_phrase = " | ".join(keywords[:3])
            if keyword_phrase.lower() not in description.lower():
                description = f"{description}\n\n{keyword_phrase}"
        
        if 'shop' not in description.lower() and 'discover' not in description.lower():
            description += "\n\nDiscover more at SayPlay.co.uk"
        
        hashtags = self._generate_hashtags(description, keywords)
        description += f"\n\n{hashtags}"
        
        if len(description) > 500:
            description = description[:497] + "..."
        
        return description
    
    def _generate_hashtags(self, text: str, keywords: List[str] = None) -> str:
        hashtags = set()
        
        if keywords:
            for kw in keywords[:3]:
                tag = kw.replace(' ', '').replace('-', '').title()
                hashtags.add(f"#{tag}")
        
        default = ['#PersonalizedGifts', '#VoiceMessage', '#UniqueGifts', '#GiftIdeas']
        hashtags.update(default[:3])
        
        return ' '.join(list(hashtags)[:5])
    
    def get_stats(self) -> Dict:
        stats = {
            'authenticated': self.access_token is not None,
            'user_id': self.user_id,
            'boards_loaded': len(self.boards),
            'boards': list(self.boards.keys())
        }
        return stats


async def test_pinterest():
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\nTesting Pinterest Publisher")
    
    token = os.getenv('PINTEREST_TOKEN')
    if not token:
        print("\nPINTEREST_TOKEN not found in .env")
        print("Get token from: https://developers.pinterest.com/apps/")
        return
    
    publisher = PinterestPublisher(token)
    
    if not publisher.user_id:
        print("\nAuthentication failed")
        print("Check your PINTEREST_TOKEN is valid")
        return
    
    stats = publisher.get_stats()
    print(f"\nPinterest Publisher ready")
    print(f"User ID: {stats['user_id']}")
    print(f"Boards: {stats['boards_loaded']}")
    if stats['boards']:
        print(f"Board names: {', '.join(stats['boards'][:5])}")
    
    print("\nPinterest is ready for pin creation")


if __name__ == "__main__":
    asyncio.run(test_pinterest())
