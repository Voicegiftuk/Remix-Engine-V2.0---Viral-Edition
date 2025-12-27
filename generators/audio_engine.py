#!/usr/bin/env python3
"""
Audio Engine - V2.0 VIRAL EDITION
Generates viral TikTok-style voiceovers using Microsoft Edge TTS (FREE unlimited)
No ElevenLabs subscription needed - uses the same voices as viral TikTok videos
"""
import sys
from pathlib import Path
from typing import Optional, List
import asyncio
import random

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import edge_tts
from loguru import logger

# Configure logging
logger.add(
    "logs/audio_engine.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class AudioEngine:
    """Free unlimited viral voiceover generation"""
    
    # Available viral voices (most popular on TikTok)
    VOICES = {
        # English (US) - Most Viral
        'tiktok_girl': 'en-US-AvaMultilingualNeural',  # The famous TikTok voice
        'tiktok_guy': 'en-US-AndrewMultilingualNeural',  # Male version
        'storyteller': 'en-US-AnaNeural',  # Childlike, emotional
        'professional': 'en-US-GuyNeural',  # Deep, authoritative
        
        # English (UK) - British Accent
        'british_girl': 'en-GB-SoniaNeural',  # Elegant British female
        'british_guy': 'en-GB-RyanNeural',  # Professional British male
        
        # Special Effects
        'excited': 'en-US-AriaNeural',  # Enthusiastic, upbeat
        'calm': 'en-US-JennyNeural',  # Soothing, calming
        'dramatic': 'en-US-DavisNeural'  # Intense, dramatic
    }
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / 'assets/temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("AudioEngine initialized with Edge-TTS")
    
    async def _generate_async(
        self,
        text: str,
        voice: str,
        output_path: Path,
        rate: str = "+0%",
        pitch: str = "+0Hz"
    ) -> Path:
        """
        Async voice generation (internal use)
        
        Args:
            text: Text to speak
            voice: Voice ID from VOICES dict
            output_path: Where to save MP3
            rate: Speech rate adjustment (-50% to +100%)
            pitch: Pitch adjustment (-50Hz to +50Hz)
        
        Returns:
            Path to generated audio file
        """
        try:
            # Create TTS communicator
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                pitch=pitch
            )
            
            # Generate and save
            await communicate.save(str(output_path))
            
            logger.info(f"Generated voiceover: {output_path.name} ({voice})")
            return output_path
            
        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            raise
    
    def generate_voiceover(
        self,
        text: str,
        voice_type: str = 'tiktok_girl',
        output_name: Optional[str] = None,
        rate_variation: bool = True,
        pitch_variation: bool = False
    ) -> Path:
        """
        Generate viral-style voiceover (synchronous wrapper)
        
        Args:
            text: Text to speak (max 500 characters recommended)
            voice_type: Voice style from VOICES dict
            output_name: Custom output filename (auto-generated if None)
            rate_variation: Add micro speed variation (sounds more natural)
            pitch_variation: Add micro pitch variation (optional)
        
        Returns:
            Path to generated MP3 file
        """
        if output_name is None:
            output_name = f"voice_{random.randint(1000, 9999)}.mp3"
        
        output_path = self.temp_dir / output_name
        
        # Get voice ID
        voice_id = self.VOICES.get(voice_type, self.VOICES['tiktok_girl'])
        
        # Add micro-variations for more natural sound
        rate = "+0%"
        pitch = "+0Hz"
        
        if rate_variation:
            # Random rate between -5% and +5% (imperceptible but more natural)
            rate_val = random.randint(-5, 5)
            rate = f"{rate_val:+d}%"
        
        if pitch_variation:
            # Random pitch between -3Hz and +3Hz
            pitch_val = random.randint(-3, 3)
            pitch = f"{pitch_val:+d}Hz"
        
        # Run async function in sync context
        asyncio.run(
            self._generate_async(text, voice_id, output_path, rate, pitch)
        )
        
        return output_path
    
    def generate_hook_voice(
        self,
        hook_text: str,
        voice_type: str = 'excited',
        output_name: Optional[str] = None
    ) -> Path:
        """
        Generate voice for video hook (upbeat, attention-grabbing)
        
        Args:
            hook_text: Hook text (keep under 15 words)
            voice_type: Voice style (excited, tiktok_girl, dramatic)
            output_name: Custom output filename
        
        Returns:
            Path to generated MP3
        """
        # Use faster rate for hooks (more energy)
        output_path = self.generate_voiceover(
            text=hook_text,
            voice_type=voice_type,
            output_name=output_name,
            rate_variation=False  # Consistent energy for hooks
        )
        
        logger.info(f"Generated hook voice: {hook_text[:30]}...")
        return output_path
    
    def generate_caption_voice(
        self,
        caption_text: str,
        voice_type: str = 'storyteller',
        output_name: Optional[str] = None
    ) -> Path:
        """
        Generate voice for longer captions (calm, clear)
        
        Args:
            caption_text: Full caption text
            voice_type: Voice style (storyteller, calm, professional)
            output_name: Custom output filename
        
        Returns:
            Path to generated MP3
        """
        output_path = self.generate_voiceover(
            text=caption_text,
            voice_type=voice_type,
            output_name=output_name,
            rate_variation=True,  # Natural variation for longer content
            pitch_variation=True
        )
        
        logger.info(f"Generated caption voice: {len(caption_text)} chars")
        return output_path
    
    def list_available_voices(self) -> List[str]:
        """Get list of available voice types"""
        return list(self.VOICES.keys())
    
    async def list_all_edge_voices(self):
        """List ALL available Edge TTS voices (diagnostic)"""
        voices = await edge_tts.list_voices()
        return voices


# Singleton instance
audio_engine = AudioEngine()


def main():
    """Test audio generation"""
    print("🗣️  Testing Audio Engine...")
    print(f"\nAvailable voices: {audio_engine.list_available_voices()}\n")
    
    # Test hook voice
    print("Generating hook voice...")
    hook_audio = audio_engine.generate_hook_voice(
        "TAP THIS CARD TO HEAR THEIR VOICE!",
        voice_type='excited'
    )
    print(f"✓ Hook audio: {hook_audio}")
    
    # Test caption voice
    print("\nGenerating caption voice...")
    caption_audio = audio_engine.generate_caption_voice(
        "Make any gift personal with a voice message. Just tap the NFC sticker and hear their voice instantly. No app needed.",
        voice_type='storyteller'
    )
    print(f"✓ Caption audio: {caption_audio}")
    
    # Test TikTok voice
    print("\nGenerating TikTok voice...")
    tiktok_audio = audio_engine.generate_voiceover(
        "The most personal gift you can give!",
        voice_type='tiktok_girl'
    )
    print(f"✓ TikTok audio: {tiktok_audio}")
    
    print("\n✅ All audio generated successfully!")
    print(f"\n💡 Audio files saved to: {audio_engine.temp_dir}")
    
    # Show file info
    for audio_file in audio_engine.temp_dir.glob("voice_*.mp3"):
        size_kb = audio_file.stat().st_size / 1024
        print(f"   - {audio_file.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
