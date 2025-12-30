"""
LONG-FORM PODCAST GENERATOR
Creates 5-10 minute podcasts with multiple segments
Different topics, stories, and variety
"""
import asyncio
import edge_tts
from typing import Dict, List
import os


class LongFormPodcastGenerator:
    """
    Generate professional 5+ minute podcasts
    Multiple segments with variety
    """
    
    def __init__(self):
        # Premium voices
        self.voices = {
            'female_primary': 'en-GB-SoniaNeural',
            'male_primary': 'en-GB-RyanNeural',
            'female_secondary': 'en-GB-LibbyNeural',
            'male_secondary': 'en-GB-ThomasNeural'
        }
    
    async def generate_podcast(self, article: Dict, topic: Dict, episode_number: int) -> Dict:
        """
        Generate complete 5+ minute podcast
        """
        print(f"  Generating 5+ minute podcast...")
        
        # Create podcast script with multiple segments
        script = self._create_podcast_script(article, topic, episode_number)
        
        # Generate all audio segments
        audio_segments = await self._generate_all_segments(script)
        
        # Combine segments
        full_audio = b"".join(audio_segments)
        
        # Calculate duration
        duration = len(full_audio) // 12000
        
        print(f"  ✅ Podcast created: {duration}s ({duration//60}:{duration%60:02d})")
        
        return {
            'audio': full_audio,
            'metadata': {
                'title': f"Ep {episode_number}: {topic['title']}",
                'duration': duration,
                'episode_number': episode_number,
                'voices_used': list(self.voices.values()),
                'segments': len(script),
                'quality': 'Premium British Neural'
            },
            'script': script
        }
    
    def _create_podcast_script(self, article: Dict, topic: Dict, episode_number: int) -> List[Dict]:
        """
        Create detailed podcast script
        5-7 minutes = ~1000-1200 words spoken
        """
        article_text = article.get('text', '')
        
        # Extract sections from article
        sections = article_text.split('\n\n')
        
        script = []
        
        # SEGMENT 1: Intro (30-45s)
        script.append({
            'voice': self.voices['female_primary'],
            'text': f"""Welcome to the SayPlay Gift Guide podcast! I'm your host, and today 
            we're diving into episode {episode_number}: {topic['title']}. Whether you're searching 
            for that perfect present or looking to add a personal touch to your gift-giving, 
            you're in the right place. Let's get started!"""
        })
        
        # SEGMENT 2: Hook/Story (45-60s)
        script.append({
            'voice': self.voices['male_primary'],
            'text': f"""You know that feeling when you find the absolutely perfect gift? 
            The one that makes someone's eyes light up? That's what we're after today. 
            {topic['keyword']} can be tricky to navigate, but I've got some fantastic 
            ideas that will make you the gift-giving hero."""
        })
        
        # SEGMENT 3: Main content part 1 (90-120s)
        if len(sections) > 1:
            content_part_1 = sections[1][:600] if len(sections[1]) > 600 else sections[1]
            script.append({
                'voice': self.voices['female_primary'],
                'text': content_part_1
            })
        
        # SEGMENT 4: Commentary (30s)
        script.append({
            'voice': self.voices['male_primary'],
            'text': """Those are some brilliant ideas! What I particularly love is how 
            each one adds that personal touch. Because let's be honest, it's not about 
            how much you spend - it's about showing you care."""
        })
        
        # SEGMENT 5: Main content part 2 (90-120s)
        if len(sections) > 3:
            content_part_2 = sections[3][:600] if len(sections[3]) > 600 else sections[3]
            script.append({
                'voice': self.voices['female_secondary'],
                'text': content_part_2
            })
        
        # SEGMENT 6: SayPlay feature (45-60s)
        script.append({
            'voice': self.voices['male_secondary'],
            'text': """Now, here's something really special. With SayPlay's voice message 
            technology, you can add your personal voice to any gift. Imagine giving someone 
            flowers with your heartfelt message that plays when they tap their phone. 
            No app needed - just tap and play. It turns any gift into an unforgettable moment. 
            Visit sayplay dot co dot uk to see how it works."""
        })
        
        # SEGMENT 7: Practical tip (30s)
        script.append({
            'voice': self.voices['female_primary'],
            'text': """Quick tip: Don't wait until the last minute! Shopping early gives you 
            time to find the perfect item and add those personal touches that make all 
            the difference."""
        })
        
        # SEGMENT 8: Outro (30s)
        script.append({
            'voice': self.voices['male_primary'],
            'text': f"""And that wraps up episode {episode_number}! If you found these ideas 
            helpful, make sure to subscribe and check out our other episodes. Tomorrow we'll 
            be exploring even more gift ideas. Until then, happy gift hunting! This has been 
            the SayPlay Gift Guide."""
        })
        
        return script
    
    async def _generate_all_segments(self, script: List[Dict]) -> List[bytes]:
        """Generate audio for all script segments"""
        
        async def generate_segment(segment: Dict) -> bytes:
            """Generate single audio segment"""
            communicate = edge_tts.Communicate(segment['text'], segment['voice'])
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        
        # Generate all segments in parallel
        tasks = [generate_segment(seg) for seg in script]
        return await asyncio.gather(*tasks)
