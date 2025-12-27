#!/usr/bin/env python3
"""
Main Orchestrator - V2.0 VIRAL EDITION
Complete control center for the Remix Engine

Safe by default - Telegram-first distribution
All v2.0 features integrated and ready
"""
import sys
from pathlib import Path
import argparse
from typing import List, Optional
import random

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from config.settings_v2 import settings
from generators.ai_content_v2 import AIContentGeneratorV2
from generators.overlay_engine import overlay_engine
from generators.audio_engine import audio_engine
from generators.video_engine_v2 import video_engine_v2
from publishers.safe_publisher import SafePublisher
import asyncio

# Configure logging
logger.add(
    settings.logs_dir / "main_v2_{time}.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
)


class RemixEngineV2:
    """
    Main orchestrator for Remix Engine V2.0
    
    Features:
    - Safe Telegram-first distribution
    - Pro HTML/CSS overlays
    - Free unlimited voiceovers
    - Hash breaking (anti-duplicate)
    - AI content generation
    """
    
    def __init__(self):
        """Initialize Remix Engine V2.0"""
        logger.info("=" * 60)
        logger.info("REMIX ENGINE V2.0 - VIRAL EDITION")
        logger.info("=" * 60)
        
        # Validate configuration
        self._validate_setup()
        
        # Initialize AI
        self.ai = AIContentGeneratorV2(settings.GEMINI_API_KEY)
        
        # Initialize safe publisher (if configured)
        self.publisher = None
        if settings.is_safe_mode_ready():
            self.publisher = SafePublisher(
                settings.TELEGRAM_BOT_TOKEN,
                settings.TELEGRAM_CHAT_ID
            )
            logger.info("✓ Safe publisher initialized (Telegram)")
        
        logger.success("✓ Remix Engine V2.0 initialized")
    
    def _validate_setup(self):
        """Validate required configuration"""
        missing = settings.validate_required()
        
        if missing:
            logger.error(f"Missing required settings: {', '.join(missing)}")
            logger.error("Set these in .env file")
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        
        if settings.SAFE_MODE and not settings.is_safe_mode_ready():
            logger.warning("Safe mode enabled but Telegram not configured")
            logger.warning("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        
        if settings.ALLOW_AUTO_POSTING:
            logger.warning("⚠️  AUTO-POSTING ENABLED")
            logger.warning("🚨 Only use with burner accounts!")
        
        logger.success("✓ Configuration validated")
    
    def generate_single_video(
        self,
        occasion: Optional[str] = None,
        platform: str = "instagram",
        output_name: Optional[str] = None
    ) -> tuple:
        """
        Generate single video with all v2.0 features
        
        Args:
            occasion: Content occasion (random if None)
            platform: Target platform
            output_name: Custom output filename
        
        Returns:
            Tuple of (video_path, content_package)
        """
        # Select occasion
        if occasion is None:
            occasion = random.choice(settings.DEFAULT_OCCASIONS)
        
        logger.info(f"Generating video: {occasion} / {platform}")
        
        # 1. Generate AI content
        logger.info("Step 1/3: Generating AI content...")
        content = self.ai.generate_complete_package(
            occasion=occasion,
            platform=platform,
            include_voiceover=settings.ENABLE_VOICEOVER
        )
        
        logger.info(f"  Hook: {content['hook']}")
        logger.info(f"  CTA: {content['cta']}")
        
        # 2. Generate video
        logger.info("Step 2/3: Generating video...")
        video_path = video_engine_v2.generate_video(
            hook_text=content['hook'],
            cta_text=content['cta'],
            occasion=occasion,
            use_voiceover=settings.ENABLE_VOICEOVER,
            use_pro_overlays=settings.USE_PRO_OVERLAYS,
            output_name=output_name
        )
        
        logger.success(f"✓ Video generated: {video_path}")
        
        # 3. Prepare full package
        content['video_path'] = video_path
        
        logger.success("✓ Complete package ready")
        return video_path, content
    
    def generate_batch(
        self,
        count: int,
        platform: str = "instagram",
        occasions: Optional[List[str]] = None
    ) -> List[tuple]:
        """
        Generate batch of videos
        
        Args:
            count: Number of videos to generate
            platform: Target platform
            occasions: List of occasions to cycle through
        
        Returns:
            List of (video_path, content_package) tuples
        """
        if occasions is None:
            occasions = settings.DEFAULT_OCCASIONS
        
        logger.info(f"Starting batch generation: {count} videos")
        logger.info(f"Platform: {platform}")
        logger.info(f"Occasions: {', '.join(occasions)}")
        
        results = []
        
        for i in range(count):
            occasion = occasions[i % len(occasions)]
            
            try:
                video_path, content = self.generate_single_video(
                    occasion=occasion,
                    platform=platform,
                    output_name=f"video_{i+1:03d}.mp4"
                )
                
                results.append((video_path, content))
                logger.info(f"Batch progress: {i+1}/{count}")
                
            except Exception as e:
                logger.error(f"Failed to generate video {i+1}: {e}")
                continue
        
        logger.success(f"✓ Batch complete: {len(results)}/{count} videos")
        return results
    
    async def send_to_telegram(
        self,
        video_path: Path,
        content: dict,
        platform: str = "instagram"
    ) -> bool:
        """
        Send video package to Telegram
        
        Args:
            video_path: Path to generated video
            content: Content package (hook, caption, hashtags, etc.)
            platform: Target platform
        
        Returns:
            True if sent successfully
        """
        if not self.publisher:
            logger.error("Telegram publisher not initialized")
            return False
        
        logger.info(f"Sending to Telegram: {video_path.name}")
        
        success = await self.publisher.send_video_package(
            video_path=video_path,
            caption=content['caption'],
            hashtags=content['hashtags'],
            platform=platform
        )
        
        if success:
            logger.success("✓ Sent to Telegram")
        else:
            logger.error("✗ Telegram send failed")
        
        return success
    
    async def send_batch_to_telegram(
        self,
        results: List[tuple],
        platform: str = "instagram"
    ) -> int:
        """
        Send batch of videos to Telegram
        
        Args:
            results: List of (video_path, content) tuples
            platform: Target platform
        
        Returns:
            Number of videos sent successfully
        """
        if not self.publisher:
            logger.error("Telegram publisher not initialized")
            return 0
        
        logger.info(f"Sending batch to Telegram: {len(results)} videos")
        
        videos = [r[0] for r in results]
        captions = [r[1]['caption'] for r in results]
        hashtags_list = [r[1]['hashtags'] for r in results]
        
        sent_count = await self.publisher.send_daily_batch(
            videos=videos,
            captions=captions,
            hashtags_list=hashtags_list,
            platform=platform
        )
        
        logger.success(f"✓ Sent {sent_count}/{len(results)} videos to Telegram")
        return sent_count
    
    def run_daily_workflow(
        self,
        video_count: Optional[int] = None,
        platform: str = "instagram"
    ):
        """
        Run complete daily workflow
        
        This is the main function called by GitHub Actions
        
        Args:
            video_count: Number of videos to generate (uses setting if None)
            platform: Target platform
        """
        logger.info("=" * 60)
        logger.info("STARTING DAILY WORKFLOW")
        logger.info("=" * 60)
        
        if video_count is None:
            video_count = settings.DAILY_VIDEO_COUNT
        
        logger.info(f"Videos to generate: {video_count}")
        logger.info(f"Target platform: {platform}")
        logger.info(f"Safe mode: {settings.SAFE_MODE}")
        
        # 1. Generate videos
        results = self.generate_batch(
            count=video_count,
            platform=platform
        )
        
        if not results:
            logger.error("No videos generated - aborting workflow")
            return
        
        # 2. Send to Telegram (safe mode)
        if settings.SAFE_MODE:
            logger.info("Safe mode: Sending to Telegram...")
            
            sent_count = asyncio.run(
                self.send_batch_to_telegram(results, platform)
            )
            
            logger.success(f"✓ Workflow complete: {sent_count} videos sent to Telegram")
            logger.info("Check your phone to post manually (30 seconds per video)")
        
        else:
            logger.warning("Safe mode disabled - videos generated but not distributed")
            logger.warning("Enable safe mode or manually distribute videos")
        
        logger.info("=" * 60)
        logger.info("WORKFLOW COMPLETE")
        logger.info("=" * 60)


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Remix Engine V2.0 - Viral Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 3 videos and send to Telegram (safe mode)
  python main_v2.py --mode daily
  
  # Generate single test video
  python main_v2.py --mode single --occasion birthday
  
  # Generate custom batch
  python main_v2.py --mode batch --count 5 --platform tiktok
  
  # Test Telegram connection
  python main_v2.py --mode test-telegram
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['daily', 'single', 'batch', 'test-telegram', 'test-features'],
        default='daily',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=None,
        help='Number of videos to generate (batch mode)'
    )
    
    parser.add_argument(
        '--platform',
        choices=['instagram', 'tiktok'],
        default='instagram',
        help='Target platform'
    )
    
    parser.add_argument(
        '--occasion',
        type=str,
        default=None,
        help='Content occasion (single mode)'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    try:
        engine = RemixEngineV2()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)
    
    # Execute mode
    try:
        if args.mode == 'daily':
            # Run daily workflow
            engine.run_daily_workflow(
                video_count=args.count,
                platform=args.platform
            )
        
        elif args.mode == 'single':
            # Generate single video
            video_path, content = engine.generate_single_video(
                occasion=args.occasion,
                platform=args.platform
            )
            
            print(f"\n✅ Video generated: {video_path}")
            print(f"   Hook: {content['hook']}")
            print(f"   Caption: {content['caption']}")
            print(f"   Hashtags: {' '.join(content['hashtags'])}")
            
            # Send to Telegram if configured
            if settings.SAFE_MODE and engine.publisher:
                print("\nSending to Telegram...")
                success = asyncio.run(
                    engine.send_to_telegram(video_path, content, args.platform)
                )
                if success:
                    print("✓ Sent to Telegram - check your phone!")
        
        elif args.mode == 'batch':
            # Generate batch
            count = args.count or settings.DAILY_VIDEO_COUNT
            results = engine.generate_batch(
                count=count,
                platform=args.platform
            )
            
            print(f"\n✅ Generated {len(results)} videos")
            
            # Send to Telegram if configured
            if settings.SAFE_MODE and engine.publisher:
                print("\nSending batch to Telegram...")
                sent_count = asyncio.run(
                    engine.send_batch_to_telegram(results, args.platform)
                )
                print(f"✓ Sent {sent_count} videos to Telegram")
        
        elif args.mode == 'test-telegram':
            # Test Telegram connection
            if not engine.publisher:
                print("❌ Telegram not configured")
                print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
                sys.exit(1)
            
            print("Testing Telegram connection...")
            success = asyncio.run(engine.publisher.send_test_message())
            
            if success:
                print("✅ Telegram connection successful!")
                print("Check your phone for the test message")
            else:
                print("❌ Telegram connection failed")
                print("Check bot token and chat ID")
        
        elif args.mode == 'test-features':
            # Test individual features
            print("🧪 Testing V2.0 Features...\n")
            
            print("1. Testing overlay engine...")
            hook_overlay = overlay_engine.create_hook_overlay(
                "TEST OVERLAY! 🎁",
                style="tiktok"
            )
            print(f"   ✓ Overlay created: {hook_overlay}")
            
            print("\n2. Testing audio engine...")
            voice = audio_engine.generate_voiceover(
                "This is a test voiceover!",
                voice_type='tiktok_girl'
            )
            print(f"   ✓ Voice created: {voice}")
            
            print("\n3. Testing AI content...")
            content = engine.ai.generate_complete_package(
                occasion="birthday",
                platform="instagram"
            )
            print(f"   ✓ Hook: {content['hook']}")
            print(f"   ✓ Caption: {content['caption'][:50]}...")
            
            print("\n✅ All features working!")
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
