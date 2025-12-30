"""
PODCAST RSS FEED GENERATOR
"""
from pathlib import Path
from datetime import datetime
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class PodcastRSSGenerator:
    """Generate podcast RSS feed"""
    
    def __init__(self):
        self.show_info = {
            'title': 'SayPlay Gift Guide',
            'description': 'Your daily guide to perfect personalized gifts.',
            'author': 'SayPlay - VoiceGift UK',
            'email': 'podcast@sayplay.co.uk',
            'website': 'https://dashboard.sayplay.co.uk',
            'image': 'https://dashboard.sayplay.co.uk/podcast-cover.jpg',
            'category': 'Leisure',
            'language': 'en-GB'
        }
    
    def generate_rss(self, podcast_dir: Path, output_file: Path):
        """Generate RSS feed"""
        print("\n🎙 Generating podcast RSS...")
        
        rss = Element('rss', {'version': '2.0'})
        channel = SubElement(rss, 'channel')
        
        self._add_element(channel, 'title', self.show_info['title'])
        self._add_element(channel, 'description', self.show_info['description'])
        self._add_element(channel, 'link', self.show_info['website'])
        
        episodes = self._get_episodes(podcast_dir)
        
        for episode in episodes:
            item = SubElement(channel, 'item')
            self._add_element(item, 'title', episode['title'])
            self._add_element(item, 'description', episode['description'])
            SubElement(item, 'enclosure', {
                'url': episode['audio_url'],
                'length': str(episode['file_size']),
                'type': 'audio/mpeg'
            })
            self._add_element(item, 'pubDate', episode['pub_date'])
        
        xml_string = minidom.parseString(tostring(rss, 'utf-8')).toprettyxml(indent='  ')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        print(f"✅ RSS generated: {output_file}")
        return output_file
    
    def _get_episodes(self, podcast_dir: Path) -> list:
        episodes = []
        mp3_files = sorted(podcast_dir.glob('*_PODCAST.mp3'))
        
        for i, mp3_file in enumerate(mp3_files, 1):
            episodes.append({
                'title': f"Episode {i}: Gift Ideas",
                'description': f"Discover thoughtful gift ideas.",
                'audio_url': f"https://dashboard.sayplay.co.uk/podcasts/{mp3_file.name}",
                'file_size': mp3_file.stat().st_size,
                'pub_date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
            })
        
        return episodes
    
    def _add_element(self, parent, tag, text):
        elem = SubElement(parent, tag)
        elem.text = text
        return elem


def main():
    output_dirs = sorted(Path('.').glob('TITAN_OUTPUT_*'), reverse=True)
    if not output_dirs:
        return
    
    podcast_dir = output_dirs[0] / '02_PODCAST'
    if not podcast_dir.exists():
        return
    
    web_dir = output_dirs[0] / 'web'
    web_dir.mkdir(parents=True, exist_ok=True)
    
    generator = PodcastRSSGenerator()
    generator.generate_rss(podcast_dir, web_dir / 'podcast.xml')


if __name__ == '__main__':
    main()
