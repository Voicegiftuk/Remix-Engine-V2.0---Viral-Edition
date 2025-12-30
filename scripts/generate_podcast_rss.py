"""
PODCAST RSS FEED GENERATOR
Creates Apple Podcasts / Spotify compatible RSS feed
"""
from pathlib import Path
from datetime import datetime
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class PodcastRSSGenerator:
    """
    Generate podcast RSS feed for Apple/Spotify/Google
    """
    
    def __init__(self):
        self.show_info = {
            'title': 'SayPlay Gift Guide',
            'description': 'Your daily guide to finding the perfect personalized gifts. Discover unique ideas, expert tips, and the magic of voice message gifts with SayPlay.',
            'author': 'SayPlay - VoiceGift UK',
            'email': 'podcast@sayplay.co.uk',
            'website': 'https://sayplay.co.uk',
            'image': 'https://sayplay.co.uk/podcast-cover.jpg',
            'category': 'Leisure',
            'subcategory': 'Hobbies',
            'language': 'en-GB',
            'copyright': '2025 VoiceGift UK Ltd',
            'explicit': 'no'
        }
    
    def generate_rss(self, podcast_dir: Path, output_file: Path):
        """Generate complete RSS feed"""
        
        print("\n🎙 Generating podcast RSS feed...")
        
        # Create RSS structure
        rss = Element('rss', {
            'version': '2.0',
            'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:atom': 'http://www.w3.org/2005/Atom'
        })
        
        channel = SubElement(rss, 'channel')
        
        # Add channel info
        self._add_element(channel, 'title', self.show_info['title'])
        self._add_element(channel, 'description', self.show_info['description'])
        self._add_element(channel, 'link', self.show_info['website'])
        self._add_element(channel, 'language', self.show_info['language'])
        self._add_element(channel, 'copyright', self.show_info['copyright'])
        
        # iTunes specific tags
        self._add_element(channel, 'itunes:author', self.show_info['author'])
        self._add_element(channel, 'itunes:summary', self.show_info['description'])
        self._add_element(channel, 'itunes:explicit', self.show_info['explicit'])
        
        # iTunes image
        itunes_image = SubElement(channel, 'itunes:image', {'href': self.show_info['image']})
        
        # iTunes category
        category = SubElement(channel, 'itunes:category', {'text': self.show_info['category']})
        SubElement(category, 'itunes:category', {'text': self.show_info['subcategory']})
        
        # Owner
        owner = SubElement(channel, 'itunes:owner')
        self._add_element(owner, 'itunes:name', self.show_info['author'])
        self._add_element(owner, 'itunes:email', self.show_info['email'])
        
        # Self-reference
        SubElement(channel, 'atom:link', {
            'href': 'https://sayplay.co.uk/podcast.xml',
            'rel': 'self',
            'type': 'application/rss+xml'
        })
        
        # Add episodes
        episodes = self._get_episodes(podcast_dir)
        
        for episode in episodes:
            item = SubElement(channel, 'item')
            
            self._add_element(item, 'title', episode['title'])
            self._add_element(item, 'description', episode['description'])
            self._add_element(item, 'itunes:summary', episode['description'])
            self._add_element(item, 'itunes:author', self.show_info['author'])
            self._add_element(item, 'itunes:episode', str(episode['episode_number']))
            self._add_element(item, 'itunes:episodeType', 'full')
            self._add_element(item, 'itunes:explicit', 'no')
            
            # Enclosure (audio file)
            SubElement(item, 'enclosure', {
                'url': episode['audio_url'],
                'length': str(episode['file_size']),
                'type': 'audio/mpeg'
            })
            
            self._add_element(item, 'guid', episode['audio_url'])
            self._add_element(item, 'pubDate', episode['pub_date'])
            self._add_element(item, 'itunes:duration', str(episode['duration']))
        
        # Pretty print XML
        xml_string = minidom.parseString(tostring(rss, 'utf-8')).toprettyxml(indent='  ')
        
        # Save RSS feed
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        print(f"✅ RSS feed generated: {output_file}")
        print(f"   Episodes: {len(episodes)}")
        print(f"   Feed URL: https://sayplay.co.uk/podcast.xml")
        
        return output_file
    
    def _get_episodes(self, podcast_dir: Path) -> list:
        """Get all podcast episodes"""
        episodes = []
        
        # Find all MP3 files
        mp3_files = sorted(podcast_dir.glob('*_PODCAST.mp3'))
        
        for i, mp3_file in enumerate(mp3_files, 1):
            # Load metadata
            meta_file = mp3_file.with_name(mp3_file.name.replace('_PODCAST.mp3', '_PODCAST_META.json'))
            
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    'title': mp3_file.stem.replace('-', ' ').title(),
                    'duration_seconds': 300,
                    'episode_number': i
                }
            
            # Get file size
            file_size = mp3_file.stat().st_size
            
            # Create episode data
            episode = {
                'title': metadata['title'],
                'description': f"In this episode, we explore {metadata['title'].lower()}. Discover thoughtful gift ideas, expert tips, and the perfect ways to make your gifts truly memorable.",
                'audio_url': f"https://sayplay.co.uk/podcasts/{mp3_file.name}",
                'file_size': file_size,
                'duration': metadata.get('duration_seconds', 300),
                'episode_number': metadata.get('episode_number', i),
                'pub_date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
            }
            
            episodes.append(episode)
        
        return episodes
    
    def _add_element(self, parent, tag, text):
        """Helper to add element with text"""
        elem = SubElement(parent, tag)
        elem.text = text
        return elem


def main():
    """Generate RSS feed"""
    
    # Find podcast directory
    output_dirs = sorted(Path('.').glob('TITAN_OUTPUT_*'), reverse=True)
    
    if not output_dirs:
        print("❌ No output directory found")
        return
    
    output_dir = output_dirs[0]
    podcast_dir = output_dir / '02_PODCAST'
    
    if not podcast_dir.exists():
        print("❌ Podcast directory not found")
        return
    
    # Output RSS to web directory
    web_dir = output_dir / 'web'
    web_dir.mkdir(parents=True, exist_ok=True)
    
    rss_file = web_dir / 'podcast.xml'
    
    generator = PodcastRSSGenerator()
    generator.generate_rss(podcast_dir, rss_file)
    
    print("\n📋 NEXT STEPS:")
    print("1. Deploy to Vercel (RSS will be at sayplay.co.uk/podcast.xml)")
    print("2. Submit RSS to Apple Podcasts Connect")
    print("3. Spotify/Google will auto-discover!")


if __name__ == '__main__':
    main()
