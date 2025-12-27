#!/usr/bin/env python3
"""
Video Engine - V2.0 VIRAL EDITION
Enhanced video generation with:
- Hash breaking (prevents duplicate content penalties)
- Pro HTML/CSS overlays
- Viral voiceovers
- Advanced effects
"""
import sys
from pathlib import Path
from typing import Optional, List, Tuple
import random

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    ImageClip, concatenate_videoclips
)
from moviepy.video.fx.all import colorx, speedx, crop
from loguru import logger

# Import our pro engines
from generators.overlay_engine import overlay_engine
from generators.audio_engine import audio_engine

# Configure logging
logger.add(
    "logs/video_engine_v2.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class VideoEngineV2:
    """
    Advanced video generation with hash breaking and pro features
    
    Key Features:
    - Prevents duplicate content penalties via micro-variations
    - Pro HTML/CSS text overlays
    - Viral TikTok voiceovers
    - Random effects for uniqueness
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.assets_dir = self.base_dir / 'assets'
        self.output_dir = self.base_dir / 'output/videos'
        self.temp_dir = self.assets_dir / 'temp'
        
        # Create directories
        for directory in [self.output_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Video settings
        self.resolution = (1080, 1920)  # 9:16 vertical
        self.fps = 30
        
        logger.info("VideoEngineV2 initialized with hash breaking")
    
    def apply_hash_breaker(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Apply invisible micro-variations to break file hash
        
        This prevents Instagram/TikTok from flagging video as duplicate content.
        Changes are imperceptible to humans but change the file signature.
        
        Techniques used:
        1. Micro speed variation (0.99x - 1.01x)
        2. Micro color saturation shift (±2%)
        3. Micro crop position shift (±10 pixels)
        4. Random horizontal flip (50% chance)
        
        Args:
            clip: Original video clip
        
        Returns:
            Modified clip with broken hash
        """
        logger.debug("Applying hash breaker...")
        
        # 1. Micro speed variation (imperceptible)
        speed_factor = random.uniform(0.99, 1.01)
        clip = clip.fx(speedx, speed_factor)
        logger.debug(f"Speed: {speed_factor:.4f}x")
        
        # 2. Micro color saturation shift
        color_factor = random.uniform(0.98, 1.02)
        clip = clip.fx(colorx, color_factor)
        logger.debug(f"Color: {color_factor:.4f}x")
        
        # 3. Micro crop shift (breaks visual fingerprint)
        x_offset = random.randint(-10, 10)
        y_offset = random.randint(-10, 10)
        
        w, h = clip.size
        clip = clip.crop(
            x1=max(0, x_offset),
            y1=max(0, y_offset),
            x2=min(w, w + x_offset),
            y2=min(h, h + y_offset)
        )
        logger.debug(f"Crop offset: ({x_offset}, {y_offset})")
        
        # 4. Random horizontal flip (50% chance)
        if random.random() < 0.5:
            clip = clip.fx(lambda c: c.fl_image(lambda img: img[:, ::-1]))
            logger.debug("Applied horizontal flip")
        
        logger.info("✓ Hash breaker applied - video is now algorithmically unique")
        return clip
    
    def generate_video(
        self,
        hook_text: str,
        cta_text: str,
        occasion: str = "general",
        use_voiceover: bool = True,
        use_pro_overlays: bool = True,
        output_name: Optional[str] = None
    ) -> Path:
        """
        Generate complete viral video with all v2.0 features
        
        Args:
            hook_text: Hook text for top overlay (max 8 words)
            cta_text: Call-to-action text for bottom
            occasion: Content occasion (birthday, wedding, etc.)
            use_voiceover: Add viral TikTok voice
            use_pro_overlays: Use HTML/CSS overlays (vs basic text)
            output_name: Custom output filename
        
        Returns:
            Path to generated video file
        """
        if output_name is None:
            output_name = f"video_{random.randint(10000, 99999)}.mp4"
        
        output_path = self.output_dir / output_name
        
        logger.info(f"Generating video: {output_name}")
        logger.info(f"Hook: {hook_text}")
        logger.info(f"CTA: {cta_text}")
        
        try:
            # 1. Select and load source clips
            clips = self._select_source_clips()
            logger.info(f"Selected {len(clips)} source clips")
            
            # 2. Apply hash breaking to each clip
            clips = [self.apply_hash_breaker(clip) for clip in clips]
            
            # 3. Concatenate clips
            base_video = concatenate_videoclips(clips, method="compose")
            logger.info(f"Base video duration: {base_video.duration:.2f}s")
            
            # 4. Create overlays
            overlays = []
            
            if use_pro_overlays:
                # Pro HTML/CSS overlays
                hook_overlay = overlay_engine.create_hook_overlay(
                    text=hook_text,
                    style="tiktok",
                    position="top"
                )
                
                cta_overlay = overlay_engine.create_cta_overlay(
                    text=cta_text,
                    style="modern"
                )
                
                # Add hook overlay (first 5 seconds)
                hook_clip = (ImageClip(str(hook_overlay))
                            .set_duration(min(5, base_video.duration))
                            .set_position("center"))
                overlays.append(hook_clip)
                
                # Add CTA overlay (last 3 seconds)
                cta_clip = (ImageClip(str(cta_overlay))
                           .set_duration(min(3, base_video.duration))
                           .set_start(max(0, base_video.duration - 3))
                           .set_position("center"))
                overlays.append(cta_clip)
                
                logger.info("✓ Pro overlays created")
            
            # 5. Add voiceover (optional)
            if use_voiceover:
                voice_path = audio_engine.generate_hook_voice(
                    hook_text=hook_text,
                    voice_type='excited'
                )
                
                voice_audio = AudioFileClip(str(voice_path))
                
                # Mix with base audio if exists
                if base_video.audio:
                    # Lower base audio volume, add voice
                    base_audio = base_video.audio.volumex(0.3)
                    voice_audio = voice_audio.volumex(0.9)
                    final_audio = CompositeAudioClip([base_audio, voice_audio])
                else:
                    final_audio = voice_audio
                
                base_video = base_video.set_audio(final_audio)
                logger.info("✓ Voiceover added")
            
            # 6. Composite final video
            if overlays:
                final_video = CompositeVideoClip([base_video] + overlays)
            else:
                final_video = base_video
            
            # 7. Export
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None  # Suppress MoviePy progress bar
            )
            
            # Cleanup
            final_video.close()
            for clip in clips:
                clip.close()
            
            logger.success(f"✓ Video generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise
    
    def _select_source_clips(self) -> List[VideoFileClip]:
        """
        Select and load random source clips from each category
        
        Returns:
            List of VideoFileClip objects
        """
        categories = {
            'sticking': self.assets_dir / 'raw_video/sticking',
            'scanning': self.assets_dir / 'raw_video/scanning',
            'reaction': self.assets_dir / 'raw_video/reaction'
        }
        
        selected_clips = []
        
        for category_name, category_path in categories.items():
            if not category_path.exists():
                logger.warning(f"Category folder missing: {category_path}")
                continue
            
            # Get all video files
            video_files = list(category_path.glob('*.mp4')) + \
                         list(category_path.glob('*.mov'))
            
            if not video_files:
                logger.warning(f"No clips in {category_name}")
                continue
            
            # Select random clip
            selected_file = random.choice(video_files)
            clip = VideoFileClip(str(selected_file))
            
            # Resize to target resolution
            clip = clip.resize(self.resolution)
            
            selected_clips.append(clip)
            logger.debug(f"Selected {category_name}: {selected_file.name}")
        
        if not selected_clips:
            raise ValueError("No video clips found in any category")
        
        return selected_clips
    
    def generate_batch(
        self,
        count: int,
        hooks: List[str],
        ctas: List[str],
        use_voiceover: bool = True,
        use_pro_overlays: bool = True
    ) -> List[Path]:
        """
        Generate batch of videos
        
        Args:
            count: Number of videos to generate
            hooks: List of hook texts to cycle through
            ctas: List of CTA texts to cycle through
            use_voiceover: Add voiceovers
            use_pro_overlays: Use pro HTML/CSS overlays
        
        Returns:
            List of paths to generated videos
        """
        generated_videos = []
        
        logger.info(f"Starting batch generation: {count} videos")
        
        for i in range(count):
            hook = hooks[i % len(hooks)]
            cta = ctas[i % len(ctas)]
            
            try:
                video_path = self.generate_video(
                    hook_text=hook,
                    cta_text=cta,
                    use_voiceover=use_voiceover,
                    use_pro_overlays=use_pro_overlays,
                    output_name=f"video_{i+1:03d}.mp4"
                )
                generated_videos.append(video_path)
                logger.info(f"Batch progress: {i+1}/{count}")
                
            except Exception as e:
                logger.error(f"Failed to generate video {i+1}: {e}")
                continue
        
        logger.success(f"✓ Batch complete: {len(generated_videos)}/{count} videos")
        return generated_videos


# Singleton instance
video_engine_v2 = VideoEngineV2()


def main():
    """Test video generation"""
    print("🎬 Testing Video Engine V2.0...")
    
    # Check for source clips
    print("\nChecking for source clips...")
    base_dir = Path(__file__).parent.parent
    
    for category in ['sticking', 'scanning', 'reaction']:
        path = base_dir / f'assets/raw_video/{category}'
        if path.exists():
            clips = list(path.glob('*.mp4')) + list(path.glob('*.mov'))
            print(f"  {category}: {len(clips)} clips")
        else:
            print(f"  {category}: folder not found")
    
    # Generate test video
    print("\nGenerating test video...")
    print("(This requires source clips to be present)")
    
    try:
        video_path = video_engine_v2.generate_video(
            hook_text="TAP TO HEAR\nTHEIR VOICE! 🎁",
            cta_text="Visit SayPlay.co.uk",
            use_voiceover=True,
            use_pro_overlays=True,
            output_name="test_viral_video.mp4"
        )
        
        print(f"\n✅ Video generated: {video_path}")
        print(f"   Size: {video_path.stat().st_size / 1_000_000:.2f} MB")
        
    except Exception as e:
        print(f"\n⚠️  Generation skipped: {e}")
        print("   Add source clips to assets/raw_video/ to test")


if __name__ == "__main__":
    main()
