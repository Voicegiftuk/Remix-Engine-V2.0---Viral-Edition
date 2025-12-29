#!/usr/bin/env python3
"""
TITAN MODULE #5: AUDIO-INCEPTION (ZERO-COST VERSION)
Uses Edge-TTS - FREE Microsoft voices (no limits!)
Uses Gemini - FREE for podcast script generation
"""
import os
import sys
import asyncio
from typing import Dict, List
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"🎙️ {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class AudioInception:
    """Blog to Podcast conversion using FREE tools"""
    
    # FREE Edge-TTS voices (British English)
    VOICES = {
        'emma': 'en-GB-SoniaNeural',      # Female, warm, friendly
        'james': 'en-GB-RyanNeural'       # Male, professional, clear
    }
    
    def __init__(self):
        """Initialize zero-cost audio engine"""
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        logger.info("Audio-Inception initialized (Zero-Cost Mode)")
        logger.info("Using Edge-TTS (FREE) + Gemini (FREE)")
        
        # Check if edge-tts is installed
        try:
            import edge_tts
            self.edge_tts = edge_tts
            logger.success("Edge-TTS available")
        except ImportError:
            logger.warning("Edge-TTS not installed. Run: pip install edge-tts")
            self.edge_tts = None
    
    def article_to_podcast(self, article: Dict) -> Dict:
        """Convert blog article to podcast episode"""
        
        title = article.get('title', 'Untitled')
        text = article.get('text', '')
        keyword = article.get('keyword', 'gifts')
        
        logger.info(f"Converting to podcast: {title[:50]}...")
        
        # Generate podcast script using Gemini (FREE)
        script = self._generate_podcast_script(title, text, keyword)
        
        # Generate audio using Edge-TTS (FREE)
        audio_bytes = self._generate_audio_from_script(script)
        
        # Create RSS entry
        duration = len(script) * 3  # Rough estimate
        
        metadata = {
            'title': f"The Gift of Memory: {title}",
            'description': f"In this episode, Emma and James discuss {keyword} and personalized gifting.",
            'duration': duration,
            'episode_number': 1,  # Would increment in production
            'publish_date': '2025-01-15',
            'keywords': [keyword, 'personalized gifts', 'voice messages']
        }
        
        result = {
            'metadata': metadata,
            'script': script,
            'audio': audio_bytes,
            'rss_entry': self._generate_rss_entry(metadata)
        }
        
        logger.success(f"Podcast created: {duration}s")
        return result
    
    def _generate_podcast_script(
        self, 
        title: str, 
        content: str, 
        keyword: str
    ) -> List[Dict]:
        """Generate natural podcast dialogue using Gemini (FREE)"""
        
        logger.info("Generating podcast script with Gemini...")
        
        if not self.gemini_key:
            logger.warning("Gemini API not configured - using mock script")
            return self._mock_podcast_script(title, keyword)
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')  # FREE tier
            
            prompt = f"""Create a natural podcast dialogue between two hosts about this article.

Article Title: {title}
Main Topic: {keyword}
Content: {content[:500]}...

Create a 5-minute conversation with:
- Emma (Host 1): Enthusiastic, asks engaging questions
- James (Host 2): Knowledgeable, provides insights

Format as JSON array:
[
  {{"speaker": "Emma", "text": "Hello and welcome..."}},
  {{"speaker": "James", "text": "Thanks Emma..."}}
]

Make it natural, conversational, and engaging. Include:
1. Warm introduction
2. Discussion of main points
3. Personal anecdotes
4. Call to action
5. Friendly outro

Return ONLY the JSON array, nothing else."""
            
            response = model.generate_content(prompt)
            
            # Parse JSON response
            import re
            json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
            if json_match:
                script = json.loads(json_match.group())
                logger.success(f"Generated {len(script)} dialogue segments")
                return script
            else:
                logger.warning("Could not parse Gemini response - using mock")
                return self._mock_podcast_script(title, keyword)
                
        except Exception as e:
            logger.error(f"Gemini script generation failed: {e}")
            return self._mock_podcast_script(title, keyword)
    
    def _mock_podcast_script(self, title: str, keyword: str) -> List[Dict]:
        """Fallback mock script"""
        
        return [
            {
                "speaker": "Emma",
                "text": f"Hello and welcome to The Gift of Memory! I'm Emma, and today we're talking about {keyword}."
            },
            {
                "speaker": "James",
                "text": f"Thanks Emma! I'm excited to discuss {title}. This is such an important topic."
            },
            {
                "speaker": "Emma",
                "text": "Absolutely! Personalized gifts create lasting memories. What makes them special?"
            },
            {
                "speaker": "James",
                "text": "It's the emotional connection. When you hear someone's actual voice, it brings back that moment instantly."
            },
            {
                "speaker": "Emma",
                "text": "That's beautiful! And with SayPlay, you can capture those voices forever."
            },
            {
                "speaker": "James",
                "text": "Exactly. Just tap the card with your phone - no app needed - and you hear their message."
            },
            {
                "speaker": "Emma",
                "text": "It's like keeping a piece of that person with you always. Perfect for birthdays, anniversaries, or just because."
            },
            {
                "speaker": "James",
                "text": "And the beauty is it lasts forever. You can replay it anytime you miss them."
            },
            {
                "speaker": "Emma",
                "text": "If you want to try SayPlay for yourself, visit sayplay.co.uk. James, final thoughts?"
            },
            {
                "speaker": "James",
                "text": "Give the gift of your voice. Give the gift of memory. Thanks for listening everyone!"
            },
            {
                "speaker": "Emma",
                "text": "See you next time on The Gift of Memory!"
            }
        ]
    
    def _generate_audio_from_script(self, script: List[Dict]) -> bytes:
        """Generate audio using Edge-TTS (FREE)"""
        
        if not self.edge_tts:
            logger.warning("Edge-TTS not available - returning empty audio")
            return b''
        
        logger.info("Generating audio with Edge-TTS...")
        
        try:
            # Run async audio generation
            audio_bytes = asyncio.run(self._async_generate_audio(script))
            logger.success(f"Generated {len(audio_bytes):,} bytes audio")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Audio generation failed: {e}")
            return b''
    
    async def _async_generate_audio(self, script: List[Dict]) -> bytes:
        """Async audio generation with Edge-TTS"""
        
        audio_segments = []
        
        for segment in script:
            speaker = segment['speaker']
            text = segment['text']
            
            # Select voice
            voice = self.VOICES.get(speaker.lower(), self.VOICES['emma'])
            
            # Generate audio for this segment
            communicate = self.edge_tts.Communicate(text, voice)
            
            # Collect audio bytes
            segment_audio = b''
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    segment_audio += chunk["data"]
            
            audio_segments.append(segment_audio)
            
            logger.info(f"  Generated: {speaker} ({len(segment_audio):,} bytes)")
        
        # Combine all segments
        # Note: This is a simple concatenation
        # In production, you'd use pydub to properly merge with silence between
        full_audio = b''.join(audio_segments)
        
        return full_audio
    
    def _generate_rss_entry(self, metadata: Dict) -> str:
        """Generate RSS feed entry for podcast"""
        
        rss = f"""
    <item>
        <title>{metadata['title']}</title>
        <description>{metadata['description']}</description>
        <pubDate>{metadata['publish_date']}</pubDate>
        <enclosure url="https://sayplay.co.uk/podcasts/episode_{metadata['episode_number']}.mp3" 
                   type="audio/mpeg" 
                   length="0"/>
        <itunes:duration>{metadata['duration']}</itunes:duration>
        <itunes:keywords>{', '.join(metadata['keywords'])}</itunes:keywords>
    </item>"""
        
        return rss
    
    def save_audio(self, audio_bytes: bytes, filename: str):
        """Save audio to file"""
        
        try:
            with open(filename, 'wb') as f:
                f.write(audio_bytes)
            logger.success(f"Saved: {filename}")
        except Exception as e:
            logger.error(f"Save failed: {e}")


if __name__ == "__main__":
    """Test zero-cost audio engine"""
    
    print("\n🧪 Testing ZERO-COST Audio-Inception...\n")
    
    engine = AudioInception()
    
    # Test article
    article = {
        'title': 'Perfect Birthday Gifts 2025',
        'text': 'Voice message gifts are the perfect way to celebrate birthdays...',
        'keyword': 'birthday gifts'
    }
    
    # Generate podcast
    print("Generating podcast...")
    podcast = engine.article_to_podcast(article)
    
    print(f"\n✓ Podcast created!")
    print(f"  Title: {podcast['metadata']['title']}")
    print(f"  Duration: ~{podcast['metadata']['duration']}s")
    print(f"  Script segments: {len(podcast['script'])}")
    print(f"  Audio size: {len(podcast['audio']):,} bytes")
    
    # Save audio if generated
    if podcast['audio']:
        engine.save_audio(podcast['audio'], 'test_podcast.mp3')
    
    # Show script preview
    print("\nScript Preview:")
    for i, segment in enumerate(podcast['script'][:3], 1):
        print(f"  {i}. {segment['speaker']}: {segment['text'][:60]}...")
    
    print("\n✅ Zero-cost audio engine test complete!")
    print("💰 Cost: £0.00")
    print("🎉 Unlimited podcast generation!")
