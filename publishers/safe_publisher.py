#!/usr/bin/env python3
"""
Safe Publisher - V2.0 VIRAL EDITION
Telegram-first distribution strategy

ZERO BAN RISK approach:
- System generates content
- Sends to your Telegram
- You post manually in 30 seconds
- Adds trending audio natively
- 100% safe for brand accounts

This eliminates the IP/detection risks of automated posting
while maintaining 99% automation efficiency.
"""
import sys
from pathlib import Path
from typing import List, Optional
import asyncio

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from telegram import Bot
from telegram.error import TelegramError
from loguru import logger

# Configure logging
logger.add(
    "logs/safe_publisher.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class SafePublisher:
    """
    Telegram-first safe distribution
    
    The "Human Proxy" Method:
    1. System does 99.9% of the work (generation)
    2. Sends complete package to Telegram
    3. You do final 0.1% (30 seconds manual posting)
    
    Benefits:
    - Zero ban risk
    - Add trending audio in-app
    - Quality control before posting
    - Preserves £100k+ social media assets
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize safe publisher
        
        Args:
            bot_token: Telegram bot token
            chat_id: Your Telegram chat ID
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        
        logger.info("SafePublisher initialized (Telegram-first mode)")
    
    async def send_video_package(
        self,
        video_path: Path,
        caption: str,
        hashtags: List[str],
        platform: str = "instagram"
    ) -> bool:
        """
        Send complete posting package to Telegram
        
        Args:
            video_path: Path to generated video
            caption: AI-generated caption
            hashtags: List of hashtags
            platform: Target platform (instagram/tiktok)
        
        Returns:
            True if sent successfully
        """
        try:
            # Prepare caption with hashtags
            full_caption = f"{caption}\n\n{' '.join(hashtags)}"
            
            # Prepare platform-specific instructions
            instructions = self._get_posting_instructions(platform)
            
            # Send video
            with open(video_path, 'rb') as video:
                await self.bot.send_video(
                    chat_id=self.chat_id,
                    video=video,
                    caption=f"📹 NEW {platform.upper()} VIDEO\n\n{full_caption[:200]}...",
                    supports_streaming=True
                )
            
            logger.info(f"✓ Sent video to Telegram: {video_path.name}")
            
            # Send copyable caption block
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"📋 COPY THIS CAPTION:\n\n{full_caption}"
            )
            
            logger.info("✓ Sent caption block")
            
            # Send posting instructions
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=instructions
            )
            
            logger.info("✓ Sent posting instructions")
            
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram send failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Send package failed: {e}")
            return False
    
    async def send_daily_batch(
        self,
        videos: List[Path],
        captions: List[str],
        hashtags_list: List[List[str]],
        platform: str = "instagram"
    ) -> int:
        """
        Send daily batch of videos to Telegram
        
        Args:
            videos: List of video paths
            captions: List of captions (same length as videos)
            hashtags_list: List of hashtag lists
            platform: Target platform
        
        Returns:
            Number of videos sent successfully
        """
        sent_count = 0
        
        logger.info(f"Sending daily batch: {len(videos)} videos")
        
        # Send header message
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=f"🚀 DAILY CONTENT READY!\n\n"
                 f"Platform: {platform.upper()}\n"
                 f"Videos: {len(videos)}\n"
                 f"Time to post: ~{len(videos) * 30} seconds\n\n"
                 f"Save each video → Open {platform} → Add trending audio → Paste caption → Post!"
        )
        
        # Send each video package
        for i, (video, caption, hashtags) in enumerate(zip(videos, captions, hashtags_list), 1):
            success = await self.send_video_package(
                video_path=video,
                caption=caption,
                hashtags=hashtags,
                platform=platform
            )
            
            if success:
                sent_count += 1
            
            # Small delay between sends
            await asyncio.sleep(2)
        
        # Send summary
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=f"✅ BATCH COMPLETE!\n\n"
                 f"Sent: {sent_count}/{len(videos)} videos\n"
                 f"Ready to post to {platform}!"
        )
        
        logger.success(f"✓ Batch sent: {sent_count}/{len(videos)} videos")
        return sent_count
    
    def _get_posting_instructions(self, platform: str) -> str:
        """Get platform-specific posting instructions"""
        
        instructions = {
            'instagram': """
📸 INSTAGRAM POSTING STEPS:

1. Save video to gallery (tap and hold)
2. Open Instagram
3. Tap + (create)
4. Select Reel
5. Choose saved video
6. ⭐ TAP MUSIC ICON - Add trending audio!
7. Copy caption from message above
8. Paste caption
9. Add location (optional)
10. Share!

⏱️ Time: ~30 seconds
🎵 Adding trending audio = 3x more reach!
            """,
            
            'tiktok': """
🎵 TIKTOK POSTING STEPS:

1. Save video to gallery
2. Open TikTok
3. Tap + (create)
4. Upload saved video
5. ⭐ TAP SOUNDS - Add trending sound!
6. Copy caption from message above
7. Paste caption
8. Select "Who can view" → Everyone
9. Post!

⏱️ Time: ~25 seconds
🎵 Trending sounds = CRITICAL for TikTok!
            """
        }
        
        return instructions.get(platform, instructions['instagram'])
    
    async def send_analytics_reminder(self):
        """Send reminder to check analytics"""
        await self.bot.send_message(
            chat_id=self.chat_id,
            text="📊 WEEKLY REMINDER:\n\n"
                 "Check your social media analytics:\n"
                 "- Which videos got most reach?\n"
                 "- Which hooks worked best?\n"
                 "- What time had best engagement?\n\n"
                 "Use insights to optimize next week's content!"
        )
        
        logger.info("✓ Sent analytics reminder")
    
    async def send_test_message(self) -> bool:
        """Test Telegram connection"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text="✅ Remix Engine V2.0 Connected!\n\n"
                     "Your safe content delivery system is ready.\n"
                     "Zero ban risk. Maximum reach. 30 seconds daily."
            )
            logger.success("✓ Test message sent successfully")
            return True
            
        except TelegramError as e:
            logger.error(f"Test message failed: {e}")
            return False


# Synchronous wrapper functions
def send_video_package_sync(
    video_path: Path,
    caption: str,
    hashtags: List[str],
    bot_token: str,
    chat_id: str,
    platform: str = "instagram"
) -> bool:
    """Sync wrapper for sending video package"""
    publisher = SafePublisher(bot_token, chat_id)
    return asyncio.run(
        publisher.send_video_package(video_path, caption, hashtags, platform)
    )


def send_daily_batch_sync(
    videos: List[Path],
    captions: List[str],
    hashtags_list: List[List[str]],
    bot_token: str,
    chat_id: str,
    platform: str = "instagram"
) -> int:
    """Sync wrapper for sending daily batch"""
    publisher = SafePublisher(bot_token, chat_id)
    return asyncio.run(
        publisher.send_daily_batch(videos, captions, hashtags_list, platform)
    )


def test_connection_sync(bot_token: str, chat_id: str) -> bool:
    """Sync wrapper for testing connection"""
    publisher = SafePublisher(bot_token, chat_id)
    return asyncio.run(publisher.send_test_message())


def main():
    """Test safe publisher"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("📱 Testing Safe Publisher (Telegram)...")
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("\n⚠️  Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
        print("   Get token from @BotFather on Telegram")
        return
    
    print(f"\nBot Token: {bot_token[:20]}...")
    print(f"Chat ID: {chat_id}")
    
    # Test connection
    print("\nSending test message...")
    success = test_connection_sync(bot_token, chat_id)
    
    if success:
        print("✅ Connection successful!")
        print("   Check your Telegram for the message")
    else:
        print("❌ Connection failed")
        print("   Check bot token and chat ID")


if __name__ == "__main__":
    main()
