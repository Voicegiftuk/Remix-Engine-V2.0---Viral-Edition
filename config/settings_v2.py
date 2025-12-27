#!/usr/bin/env python3
"""
Configuration System - V2.0 VIRAL EDITION
Centralized settings with safe defaults
"""
from pathlib import Path
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class SettingsV2(BaseSettings):
    """
    V2.0 Configuration with safe defaults
    
    Key changes from V1.0:
    - Safe mode enabled by default
    - Telegram-first distribution
    - Voice and overlay settings
    - Hash breaking always enabled
    """
    
    # ============================================
    # API KEYS (Required)
    # ============================================
    
    GEMINI_API_KEY: str = Field(
        default="",
        description="Google Gemini API key (required)"
    )
    
    TELEGRAM_BOT_TOKEN: str = Field(
        default="",
        description="Telegram bot token (required for safe mode)"
    )
    
    TELEGRAM_CHAT_ID: str = Field(
        default="",
        description="Your Telegram chat ID (required for safe mode)"
    )
    
    # ============================================
    # OPTIONAL API KEYS (Not recommended for main accounts)
    # ============================================
    
    INSTAGRAM_USERNAME: Optional[str] = Field(
        default=None,
        description="Instagram username (burner account only!)"
    )
    
    INSTAGRAM_PASSWORD: Optional[str] = Field(
        default=None,
        description="Instagram password (burner account only!)"
    )
    
    TIKTOK_USERNAME: Optional[str] = Field(
        default=None,
        description="TikTok username (burner account only!)"
    )
    
    TIKTOK_PASSWORD: Optional[str] = Field(
        default=None,
        description="TikTok password (burner account only!)"
    )
    
    # ============================================
    # DISTRIBUTION SETTINGS (V2.0)
    # ============================================
    
    SAFE_MODE: bool = Field(
        default=True,
        description="Use safe Telegram-first distribution (recommended)"
    )
    
    ALLOW_AUTO_POSTING: bool = Field(
        default=False,
        description="Allow automated posting (DANGER: only for burner accounts)"
    )
    
    DEFAULT_PLATFORM: str = Field(
        default="instagram",
        description="Default target platform (instagram/tiktok)"
    )
    
    # ============================================
    # VIDEO SETTINGS
    # ============================================
    
    VIDEO_WIDTH: int = Field(default=1080, description="Video width (9:16)")
    VIDEO_HEIGHT: int = Field(default=1920, description="Video height (9:16)")
    VIDEO_FPS: int = Field(default=30, description="Frames per second")
    
    # ============================================
    # VOICE SETTINGS (V2.0)
    # ============================================
    
    ENABLE_VOICEOVER: bool = Field(
        default=True,
        description="Add voiceovers to videos"
    )
    
    DEFAULT_VOICE: str = Field(
        default="tiktok_girl",
        description="Default voice type (tiktok_girl, excited, storyteller, etc.)"
    )
    
    VOICE_RATE_VARIATION: bool = Field(
        default=True,
        description="Add micro speed variations (more natural)"
    )
    
    VOICE_PITCH_VARIATION: bool = Field(
        default=False,
        description="Add micro pitch variations (optional)"
    )
    
    # ============================================
    # OVERLAY SETTINGS (V2.0)
    # ============================================
    
    USE_PRO_OVERLAYS: bool = Field(
        default=True,
        description="Use HTML/CSS overlays (vs basic text)"
    )
    
    DEFAULT_OVERLAY_STYLE: str = Field(
        default="tiktok",
        description="Overlay visual style (tiktok, instagram, youtube, minimal)"
    )
    
    OVERLAY_POSITION: str = Field(
        default="top",
        description="Hook overlay position (top, center, bottom)"
    )
    
    # ============================================
    # HASH BREAKING (V2.0)
    # ============================================
    
    ENABLE_HASH_BREAKING: bool = Field(
        default=True,
        description="Apply hash breaking (CRITICAL - always True)"
    )
    
    HASH_BREAK_SPEED_RANGE: tuple = Field(
        default=(0.99, 1.01),
        description="Speed variation range"
    )
    
    HASH_BREAK_COLOR_RANGE: tuple = Field(
        default=(0.98, 1.02),
        description="Color saturation range"
    )
    
    HASH_BREAK_CROP_PIXELS: int = Field(
        default=10,
        description="Maximum crop offset in pixels"
    )
    
    HASH_BREAK_FLIP_CHANCE: float = Field(
        default=0.5,
        description="Probability of horizontal flip (0.0-1.0)"
    )
    
    # ============================================
    # AI CONTENT SETTINGS
    # ============================================
    
    MAX_HOOK_WORDS: int = Field(
        default=8,
        description="Maximum words in hook (for voice clarity)"
    )
    
    VOICEOVER_DURATION: int = Field(
        default=15,
        description="Target voiceover duration in seconds"
    )
    
    CAPTION_MAX_LENGTH: int = Field(
        default=150,
        description="Maximum caption length in characters"
    )
    
    HASHTAG_COUNT: int = Field(
        default=10,
        description="Number of hashtags to generate"
    )
    
    # ============================================
    # CONTENT OCCASIONS
    # ============================================
    
    DEFAULT_OCCASIONS: List[str] = Field(
        default=["general", "birthday", "wedding", "anniversary", "christmas"],
        description="Occasions to cycle through"
    )
    
    # ============================================
    # BATCH PROCESSING
    # ============================================
    
    DAILY_VIDEO_COUNT: int = Field(
        default=3,
        description="Videos to generate per daily run"
    )
    
    DAILY_IMAGE_COUNT: int = Field(
        default=5,
        description="Images to generate per daily run"
    )
    
    # ============================================
    # FILE PATHS
    # ============================================
    
    BASE_DIR: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent,
        description="Base directory"
    )
    
    @property
    def assets_dir(self) -> Path:
        """Assets directory path"""
        return self.BASE_DIR / 'assets'
    
    @property
    def output_dir(self) -> Path:
        """Output directory path"""
        return self.BASE_DIR / 'output'
    
    @property
    def logs_dir(self) -> Path:
        """Logs directory path"""
        return self.BASE_DIR / 'logs'
    
    @property
    def temp_dir(self) -> Path:
        """Temporary files directory"""
        return self.assets_dir / 'temp'
    
    # ============================================
    # VALIDATION
    # ============================================
    
    def validate_required(self) -> List[str]:
        """
        Validate required settings
        
        Returns:
            List of missing required settings
        """
        missing = []
        
        # Always required
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        
        # Required for safe mode
        if self.SAFE_MODE:
            if not self.TELEGRAM_BOT_TOKEN:
                missing.append("TELEGRAM_BOT_TOKEN")
            if not self.TELEGRAM_CHAT_ID:
                missing.append("TELEGRAM_CHAT_ID")
        
        # Required for auto-posting (not recommended)
        if self.ALLOW_AUTO_POSTING:
            if self.DEFAULT_PLATFORM == "instagram":
                if not self.INSTAGRAM_USERNAME or not self.INSTAGRAM_PASSWORD:
                    missing.append("INSTAGRAM credentials")
            elif self.DEFAULT_PLATFORM == "tiktok":
                if not self.TIKTOK_USERNAME or not self.TIKTOK_PASSWORD:
                    missing.append("TIKTOK credentials")
        
        return missing
    
    def get_voice_config(self) -> dict:
        """Get voice-related configuration"""
        return {
            "enabled": self.ENABLE_VOICEOVER,
            "default_voice": self.DEFAULT_VOICE,
            "rate_variation": self.VOICE_RATE_VARIATION,
            "pitch_variation": self.VOICE_PITCH_VARIATION,
            "duration": self.VOICEOVER_DURATION
        }
    
    def get_overlay_config(self) -> dict:
        """Get overlay-related configuration"""
        return {
            "enabled": self.USE_PRO_OVERLAYS,
            "style": self.DEFAULT_OVERLAY_STYLE,
            "position": self.OVERLAY_POSITION
        }
    
    def get_hash_break_config(self) -> dict:
        """Get hash breaking configuration"""
        return {
            "enabled": self.ENABLE_HASH_BREAKING,
            "speed_range": self.HASH_BREAK_SPEED_RANGE,
            "color_range": self.HASH_BREAK_COLOR_RANGE,
            "crop_pixels": self.HASH_BREAK_CROP_PIXELS,
            "flip_chance": self.HASH_BREAK_FLIP_CHANCE
        }
    
    def is_safe_mode_ready(self) -> bool:
        """Check if safe mode is properly configured"""
        return bool(
            self.GEMINI_API_KEY and
            self.TELEGRAM_BOT_TOKEN and
            self.TELEGRAM_CHAT_ID
        )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton instance
settings = SettingsV2()


def main():
    """Test configuration system"""
    print("⚙️  Testing Configuration System V2.0...\n")
    
    print("📋 Current Settings:")
    print(f"   Safe Mode: {settings.SAFE_MODE}")
    print(f"   Voiceover: {settings.ENABLE_VOICEOVER}")
    print(f"   Default Voice: {settings.DEFAULT_VOICE}")
    print(f"   Pro Overlays: {settings.USE_PRO_OVERLAYS}")
    print(f"   Overlay Style: {settings.DEFAULT_OVERLAY_STYLE}")
    print(f"   Hash Breaking: {settings.ENABLE_HASH_BREAKING}")
    print(f"   Default Platform: {settings.DEFAULT_PLATFORM}")
    
    print("\n🔍 Validation:")
    missing = settings.validate_required()
    if missing:
        print(f"   ⚠️  Missing: {', '.join(missing)}")
        print("   Set these in .env file")
    else:
        print("   ✅ All required settings configured")
    
    print("\n🛡️  Safety Check:")
    if settings.is_safe_mode_ready():
        print("   ✅ Safe mode ready (Telegram configured)")
    else:
        print("   ⚠️  Configure Telegram for safe mode")
    
    if settings.ALLOW_AUTO_POSTING:
        print("   ⚠️  AUTO-POSTING ENABLED")
        print("   🚨 Only use with burner accounts!")
    else:
        print("   ✅ Auto-posting disabled (safe)")
    
    print("\n📁 Directories:")
    print(f"   Base: {settings.BASE_DIR}")
    print(f"   Assets: {settings.assets_dir}")
    print(f"   Output: {settings.output_dir}")
    print(f"   Logs: {settings.logs_dir}")
    print(f"   Temp: {settings.temp_dir}")
    
    print("\n🎤 Voice Config:")
    voice_config = settings.get_voice_config()
    for key, value in voice_config.items():
        print(f"   {key}: {value}")
    
    print("\n🎨 Overlay Config:")
    overlay_config = settings.get_overlay_config()
    for key, value in overlay_config.items():
        print(f"   {key}: {value}")
    
    print("\n👻 Hash Breaking Config:")
    hash_config = settings.get_hash_break_config()
    for key, value in hash_config.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    main()
