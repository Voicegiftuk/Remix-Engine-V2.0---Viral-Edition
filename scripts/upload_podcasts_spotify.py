"""
SPOTIFY PODCASTERS AUTO-UPLOAD
Automatically uploads all generated podcasts to Spotify
"""
import os
import requests
from pathlib import Path
import json
from datetime import datetime
import base64


class SpotifyPodcastUploader:
    """
    Upload podcasts to Spotify for Podcasters
    """
    
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.show_id = os.getenv('SPOTIFY_SHOW_ID')
        self.access_token = None
    
    def authenticate(self):
        """Get access token from Spotify"""
        print("🔐 Authenticating with Spotify...")
        
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            print("✅ Authenticated successfully")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
    
    def upload_episode(self, audio_file: Path, metadata: dict):
        """Upload single episode to Spotify"""
        print(f"\n📤 Uploading: {metadata['title']}...")
        
        # Spotify Podcasters API endpoint
        url = f"https://api.spotify.com/v1/shows/{self.show_id}/episodes"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "multipart/form-data"
        }
        
        # Prepare episode data
        episode_data = {
            "name": metadata['title'],
            "description": metadata.get('description', ''),
            "release_date": datetime.now().strftime('%Y-%m-%d'),
            "language": "en-GB",
            "explicit": False
        }
        
        # Upload audio file
        with open(audio_file, 'rb') as f:
            files = {'file': (audio_file.name, f, 'audio/mpeg')}
            
            response = requests.post(
                url, 
                headers=headers, 
                data=episode_data, 
                files=files
            )
        
        if response.status_code in [200, 201]:
            episode_id = response.json().get('id')
            episode_url = f"https://open.spotify.com/episode/{episode_id}"
            print(f"✅ Uploaded successfully")
            print(f"   URL: {episode_url}")
            return episode_url
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    
    def upload_all_podcasts(self, podcast_dir: Path):
        """Upload all podcasts from directory"""
        print("\n🎙 Starting Spotify upload...")
        
        if not self.authenticate():
            print("❌ Cannot upload without authentication")
            return []
        
        uploaded = []
        
        # Find all podcast files
        podcast_files = list(podcast_dir.glob('*.mp3'))
        
        for podcast_file in podcast_files:
            # Load metadata
            meta_file = podcast_file.with_suffix('.json')
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    'title': podcast_file.stem.replace('-', ' ').title()
                }
            
            # Upload
            episode_url = self.upload_episode(podcast_file, metadata)
            
            if episode_url:
                uploaded.append({
                    'file': podcast_file.name,
                    'url': episode_url,
                    'title': metadata['title']
                })
        
        print(f"\n✅ Upload complete: {len(uploaded)}/{len(podcast_files)} successful")
        
        return uploaded


def main():
    """Main upload function"""
    # Find podcast directory
    output_dirs = list(Path('.').glob('TITAN_OUTPUT_*/02_PODCAST'))
    
    if not output_dirs:
        print("❌ No podcast directory found")
        return
    
    podcast_dir = output_dirs[0]
    
    uploader = SpotifyPodcastUploader()
    uploaded = uploader.upload_all_podcasts(podcast_dir)
    
    # Save upload log
    log_file = podcast_dir / 'spotify_upload_log.json'
    with open(log_file, 'w') as f:
        json.dump({
            'upload_date': datetime.now().isoformat(),
            'episodes_uploaded': len(uploaded),
            'episodes': uploaded
        }, f, indent=2)
    
    print(f"\n📝 Upload log saved: {log_file}")


if __name__ == '__main__':
    main()
