#!/usr/bin/env python3
"""
AI Content Generator - V2.0 VIRAL EDITION
Generates viral-optimized content for voice + visual overlays

Optimizations for V2.0:
- Short hooks (max 8 words) for voiceover clarity
- Voice-friendly caption text
- Platform-specific hashtags
- Occasion-aware generation
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional
import random
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from loguru import logger

# Configure logging
logger.add(
    "logs/ai_content_v2.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class AIContentGeneratorV2:
    """
    AI content generation optimized for V2.0 viral features
    
    Key improvements:
    - Hooks optimized for voiceover (max 8 words)
    - Voice-friendly phrasing
    - Platform-specific optimization
    - Occasion-aware content
    """
    
    def __init__(self, api_key: str):
        """
        Initialize AI content generator
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Load prompts
        self.base_dir = Path(__file__).parent.parent
        self.prompts = self._load_prompts()
        
        logger.info("AIContentGeneratorV2 initialized")
    
    def _load_prompts(self) -> Dict:
        """Load prompt templates"""
        prompts_file = self.base_dir / 'config/prompts_v2.json'
        
        if prompts_file.exists():
            with open(prompts_file) as f:
                return json.load(f)
        
        # Default prompts if file doesn't exist
        return {
            "hook_generation": {
                "system": "You are a viral TikTok/Instagram content creator. Generate attention-grabbing hooks.",
                "templates": [
                    "Generate a 5-8 word hook for a video about {occasion} voice message gifts. Make it urgent and emotional. Use emojis.",
                    "Create a viral TikTok hook (max 8 words) about personalized NFC voice gifts for {occasion}. Be dramatic.",
                    "Write a scroll-stopping hook (under 8 words) for {occasion} gift content. Create FOMO."
                ]
            },
            "voiceover_script": {
                "system": "You are writing voiceover scripts. Keep sentences short, clear, and punchy.",
                "templates": [
                    "Write a 15-second voiceover script about {occasion} voice message gifts. 2-3 short sentences. Conversational tone.",
                    "Create a TikTok voiceover (15 seconds) explaining how NFC voice gifts work for {occasion}. Simple and clear.",
                    "Write narrator text for {occasion} gift video. Keep it under 40 words. Create emotional connection."
                ]
            },
            "caption": {
                "system": "You are a social media copywriter. Write engaging, authentic captions.",
                "templates": [
                    "Write an Instagram caption (150 chars) about personalized voice message gifts for {occasion}. Include CTA.",
                    "Create a TikTok caption for {occasion} NFC voice gift. Relatable, emotional, under 150 characters.",
                    "Write caption for {occasion} voice gift video. Make it personal and shareable. Add question."
                ]
            },
            "hashtags": {
                "system": "You are a hashtag researcher. Provide trending, relevant hashtags.",
                "base": ["#NFC", "#VoiceMessage", "#PersonalizedGift", "#GiftIdeas"],
                "occasions": {
                    "birthday": ["#BirthdayGift", "#BirthdaySurprise", "#BdayGift"],
                    "wedding": ["#WeddingGift", "#BridalGift", "#WeddingIdeas"],
                    "anniversary": ["#AnniversaryGift", "#LoveGift", "#Anniversary"],
                    "mothers_day": ["#MothersDay", "#MomGift", "#GiftForMom"],
                    "christmas": ["#ChristmasGift", "#XmasGift", "#HolidayGift"],
                    "general": ["#UniqueGift", "#ThoughtfulGift", "#GiftInspiration"]
                }
            },
            "cta": {
                "templates": [
                    "Get Yours at SayPlay.co.uk",
                    "Shop Now - SayPlay.co.uk",
                    "Visit SayPlay.co.uk",
                    "Tap Link in Bio!",
                    "Available at SayPlay.co.uk"
                ]
            }
        }
    
    def generate_hook(
        self,
        occasion: str = "general",
        platform: str = "tiktok",
        max_words: int = 8
    ) -> str:
        """
        Generate viral hook optimized for voiceover
        
        Args:
            occasion: Content occasion (birthday, wedding, etc.)
            platform: Target platform (tiktok, instagram)
            max_words: Maximum words (for voice clarity)
        
        Returns:
            Hook text (ready for voiceover)
        """
        templates = self.prompts["hook_generation"]["templates"]
        template = random.choice(templates)
        prompt = template.format(occasion=occasion)
        
        try:
            response = self.model.generate_content(
                f"{self.prompts['hook_generation']['system']}\n\n"
                f"{prompt}\n\n"
                f"CRITICAL: Maximum {max_words} words. Must be clear for voiceover. "
                f"Use simple words. Add 1-2 emojis."
            )
            
            hook = response.text.strip().strip('"\'')
            
            # Validate word count
            word_count = len(hook.split())
            if word_count > max_words:
                # Truncate if too long
                words = hook.split()[:max_words]
                hook = ' '.join(words)
                logger.warning(f"Hook truncated to {max_words} words")
            
            logger.info(f"Generated hook: {hook}")
            return hook
            
        except Exception as e:
            logger.error(f"Hook generation failed: {e}")
            # Fallback hooks
            fallbacks = [
                "TAP TO HEAR THEIR VOICE! 🎁",
                "HEAR YOUR MESSAGE! 💝",
                "THE PERFECT GIFT! ✨",
                "PERSONALIZED VOICE GIFT! 🎂",
                "SURPRISE INSIDE! 🎉"
            ]
            return random.choice(fallbacks)
    
    def generate_voiceover_script(
        self,
        occasion: str = "general",
        duration: int = 15
    ) -> str:
        """
        Generate voiceover script (15-30 seconds)
        
        Args:
            occasion: Content occasion
            duration: Target duration in seconds
        
        Returns:
            Voiceover script text
        """
        templates = self.prompts["voiceover_script"]["templates"]
        template = random.choice(templates)
        prompt = template.format(occasion=occasion)
        
        max_words = int(duration * 2.5)  # ~2.5 words per second
        
        try:
            response = self.model.generate_content(
                f"{self.prompts['voiceover_script']['system']}\n\n"
                f"{prompt}\n\n"
                f"Target duration: {duration} seconds (~{max_words} words).\n"
                f"Use short sentences. Clear pronunciation. Conversational tone."
            )
            
            script = response.text.strip().strip('"\'')
            logger.info(f"Generated voiceover script ({len(script.split())} words)")
            return script
            
        except Exception as e:
            logger.error(f"Voiceover generation failed: {e}")
            # Fallback scripts
            fallbacks = {
                "birthday": "Make their birthday unforgettable. Record a personal voice message on an NFC card. They just tap to hear your voice. No app needed. Get yours at SayPlay dot co dot uk.",
                "wedding": "The perfect wedding gift. Record your heartfelt message. They tap the card to hear your voice instantly. Create memories that last forever.",
                "general": "Make any gift personal with a voice message. Just tap the card and hear their voice. No app needed. The most thoughtful gift you can give."
            }
            return fallbacks.get(occasion, fallbacks["general"])
    
    def generate_caption(
        self,
        occasion: str = "general",
        platform: str = "instagram",
        max_length: int = 150
    ) -> str:
        """
        Generate platform-optimized caption
        
        Args:
            occasion: Content occasion
            platform: Target platform
            max_length: Maximum character length
        
        Returns:
            Caption text
        """
        templates = self.prompts["caption"]["templates"]
        template = random.choice(templates)
        prompt = template.format(occasion=occasion)
        
        try:
            response = self.model.generate_content(
                f"{self.prompts['caption']['system']}\n\n"
                f"{prompt}\n\n"
                f"Platform: {platform}. Max {max_length} characters.\n"
                f"Be authentic. Create emotional connection. Add CTA or question."
            )
            
            caption = response.text.strip().strip('"\'')
            
            # Truncate if too long
            if len(caption) > max_length:
                caption = caption[:max_length-3] + "..."
                logger.warning(f"Caption truncated to {max_length} chars")
            
            logger.info(f"Generated caption ({len(caption)} chars)")
            return caption
            
        except Exception as e:
            logger.error(f"Caption generation failed: {e}")
            # Fallback captions
            fallbacks = {
                "birthday": "Make their birthday unforgettable with a voice message they can keep forever 🎂✨",
                "wedding": "The most personal wedding gift - your voice, their hearts 💝",
                "general": "Turn any gift into a memory with a personal voice message 🎁"
            }
            return fallbacks.get(occasion, fallbacks["general"])
    
    def generate_hashtags(
        self,
        occasion: str = "general",
        platform: str = "instagram",
        count: int = 10
    ) -> List[str]:
        """
        Generate platform-optimized hashtags
        
        Args:
            occasion: Content occasion
            platform: Target platform (affects hashtag count)
            count: Number of hashtags to generate
        
        Returns:
            List of hashtags
        """
        hashtags_config = self.prompts["hashtags"]
        
        # Base hashtags
        hashtags = hashtags_config["base"].copy()
        
        # Add occasion-specific
        occasion_tags = hashtags_config["occasions"].get(
            occasion,
            hashtags_config["occasions"]["general"]
        )
        hashtags.extend(occasion_tags)
        
        # Platform-specific adjustments
        if platform == "tiktok":
            # TikTok: Add trending general tags
            hashtags.extend(["#FYP", "#ForYou", "#Viral", "#TikTokMadeMeBuyIt"])
        elif platform == "instagram":
            # Instagram: Add engagement tags
            hashtags.extend(["#InstaGood", "#GiftOfTheDay", "#ShopSmall"])
        
        # Shuffle and limit
        random.shuffle(hashtags)
        return hashtags[:count]
    
    def generate_cta(self) -> str:
        """Generate call-to-action text"""
        return random.choice(self.prompts["cta"]["templates"])
    
    def generate_complete_package(
        self,
        occasion: str = "general",
        platform: str = "instagram",
        include_voiceover: bool = True
    ) -> Dict:
        """
        Generate complete content package for one video
        
        Args:
            occasion: Content occasion
            platform: Target platform
            include_voiceover: Generate voiceover script
        
        Returns:
            Dictionary with all content
        """
        logger.info(f"Generating complete package: {occasion} / {platform}")
        
        package = {
            "hook": self.generate_hook(occasion, platform),
            "caption": self.generate_caption(occasion, platform),
            "hashtags": self.generate_hashtags(occasion, platform),
            "cta": self.generate_cta(),
            "occasion": occasion,
            "platform": platform
        }
        
        if include_voiceover:
            package["voiceover"] = self.generate_voiceover_script(occasion)
        
        logger.success("✓ Complete package generated")
        return package
    
    def generate_batch(
        self,
        count: int,
        occasions: Optional[List[str]] = None,
        platform: str = "instagram"
    ) -> List[Dict]:
        """
        Generate batch of content packages
        
        Args:
            count: Number of packages to generate
            occasions: List of occasions to cycle through
            platform: Target platform
        
        Returns:
            List of content packages
        """
        if occasions is None:
            occasions = ["general", "birthday", "wedding", "anniversary"]
        
        packages = []
        logger.info(f"Generating batch: {count} packages")
        
        for i in range(count):
            occasion = occasions[i % len(occasions)]
            
            try:
                package = self.generate_complete_package(
                    occasion=occasion,
                    platform=platform,
                    include_voiceover=True
                )
                packages.append(package)
                logger.info(f"Batch progress: {i+1}/{count}")
                
            except Exception as e:
                logger.error(f"Failed to generate package {i+1}: {e}")
                continue
        
        logger.success(f"✓ Batch complete: {len(packages)}/{count} packages")
        return packages


def main():
    """Test AI content generation"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("🤖 Testing AI Content Generator V2.0...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n⚠️  Set GEMINI_API_KEY in .env")
        print("   Get key from: https://makersuite.google.com/app/apikey")
        return
    
    ai = AIContentGeneratorV2(api_key)
    
    # Test hook generation
    print("\n📝 Generating hook...")
    hook = ai.generate_hook(occasion="birthday", platform="tiktok")
    print(f"   Hook: {hook}")
    
    # Test voiceover script
    print("\n🗣️  Generating voiceover...")
    voiceover = ai.generate_voiceover_script(occasion="wedding")
    print(f"   Script: {voiceover}")
    
    # Test caption
    print("\n✍️  Generating caption...")
    caption = ai.generate_caption(occasion="general", platform="instagram")
    print(f"   Caption: {caption}")
    
    # Test hashtags
    print("\n#️⃣  Generating hashtags...")
    hashtags = ai.generate_hashtags(occasion="birthday", platform="instagram")
    print(f"   Hashtags: {' '.join(hashtags)}")
    
    # Test complete package
    print("\n📦 Generating complete package...")
    package = ai.generate_complete_package(occasion="anniversary", platform="tiktok")
    print(f"   Hook: {package['hook']}")
    print(f"   Caption: {package['caption']}")
    print(f"   Voiceover: {package['voiceover']}")
    print(f"   Hashtags: {' '.join(package['hashtags'])}")
    print(f"   CTA: {package['cta']}")
    
    print("\n✅ All tests complete!")


if __name__ == "__main__":
    main()
