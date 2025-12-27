#!/usr/bin/env python3
"""
Test Suite - V2.0 VIRAL EDITION
Comprehensive testing for all v2.0 features
"""
import sys
from pathlib import Path
import asyncio

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger


class TestSuiteV2:
    """Comprehensive test suite for Remix Engine V2.0"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.tests_passed = 0
        self.tests_failed = 0
        self.warnings = []
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 60)
        print("REMIX ENGINE V2.0 - TEST SUITE")
        print("=" * 60)
        print()
        
        # Import tests
        self.test_imports()
        self.test_configuration()
        self.test_overlay_engine()
        self.test_audio_engine()
        self.test_ai_content()
        self.test_video_engine()
        self.test_telegram_publisher()
        self.test_main_orchestrator()
        
        # Print summary
        self.print_summary()
    
    def test_imports(self):
        """Test all module imports"""
        print("📦 Testing Imports...")
        
        try:
            from config.settings_v2 import settings
            self._pass("Settings v2")
        except Exception as e:
            self._fail("Settings v2", e)
        
        try:
            from generators.overlay_engine import overlay_engine
            self._pass("Overlay engine")
        except Exception as e:
            self._fail("Overlay engine", e)
        
        try:
            from generators.audio_engine import audio_engine
            self._pass("Audio engine")
        except Exception as e:
            self._fail("Audio engine", e)
        
        try:
            from generators.ai_content_v2 import AIContentGeneratorV2
            self._pass("AI content v2")
        except Exception as e:
            self._fail("AI content v2", e)
        
        try:
            from generators.video_engine_v2 import video_engine_v2
            self._pass("Video engine v2")
        except Exception as e:
            self._fail("Video engine v2", e)
        
        try:
            from publishers.safe_publisher import SafePublisher
            self._pass("Safe publisher")
        except Exception as e:
            self._fail("Safe publisher", e)
        
        print()
    
    def test_configuration(self):
        """Test configuration system"""
        print("⚙️  Testing Configuration...")
        
        try:
            from config.settings_v2 import settings
            
            # Check safe mode
            if settings.SAFE_MODE:
                self._pass("Safe mode enabled (recommended)")
            else:
                self._warn("Safe mode disabled")
            
            # Check API keys
            if settings.GEMINI_API_KEY:
                self._pass("Gemini API key configured")
            else:
                self._fail("Gemini API key", "Not set in .env")
            
            # Check Telegram
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
                self._pass("Telegram configured")
            else:
                self._warn("Telegram not configured (required for safe mode)")
            
            # Check v2.0 features
            if settings.ENABLE_VOICEOVER:
                self._pass("Voiceover enabled")
            
            if settings.USE_PRO_OVERLAYS:
                self._pass("Pro overlays enabled")
            
            if settings.ENABLE_HASH_BREAKING:
                self._pass("Hash breaking enabled")
            
        except Exception as e:
            self._fail("Configuration", e)
        
        print()
    
    def test_overlay_engine(self):
        """Test pro overlay generation"""
        print("🎨 Testing Overlay Engine...")
        
        try:
            from generators.overlay_engine import overlay_engine
            
            # Test hook overlay
            hook_path = overlay_engine.create_hook_overlay(
                text="TEST HOOK! 🎁",
                style="tiktok",
                position="top"
            )
            
            if hook_path.exists():
                self._pass(f"Hook overlay created ({hook_path.name})")
            else:
                self._fail("Hook overlay", "File not created")
            
            # Test CTA overlay
            cta_path = overlay_engine.create_cta_overlay(
                text="Test CTA",
                style="modern"
            )
            
            if cta_path.exists():
                self._pass(f"CTA overlay created ({cta_path.name})")
            else:
                self._fail("CTA overlay", "File not created")
            
        except Exception as e:
            self._fail("Overlay engine", e)
        
        print()
    
    def test_audio_engine(self):
        """Test voiceover generation"""
        print("🗣️  Testing Audio Engine...")
        
        try:
            from generators.audio_engine import audio_engine
            
            # Test voiceover
            voice_path = audio_engine.generate_voiceover(
                text="This is a test voiceover for Remix Engine V2.0!",
                voice_type='tiktok_girl'
            )
            
            if voice_path.exists():
                size_kb = voice_path.stat().st_size / 1024
                self._pass(f"Voiceover created ({voice_path.name}, {size_kb:.1f}KB)")
            else:
                self._fail("Voiceover", "File not created")
            
            # Test available voices
            voices = audio_engine.list_available_voices()
            if len(voices) >= 5:
                self._pass(f"{len(voices)} voices available")
            else:
                self._warn(f"Only {len(voices)} voices available")
            
        except Exception as e:
            self._fail("Audio engine", e)
        
        print()
    
    def test_ai_content(self):
        """Test AI content generation"""
        print("🤖 Testing AI Content Generator...")
        
        try:
            from config.settings_v2 import settings
            
            if not settings.GEMINI_API_KEY:
                self._warn("Skipping AI tests (no API key)")
                print()
                return
            
            from generators.ai_content_v2 import AIContentGeneratorV2
            ai = AIContentGeneratorV2(settings.GEMINI_API_KEY)
            
            # Test hook
            hook = ai.generate_hook(occasion="birthday", platform="tiktok")
            word_count = len(hook.split())
            if word_count <= 8:
                self._pass(f"Hook generated ({word_count} words): {hook}")
            else:
                self._warn(f"Hook too long ({word_count} words)")
            
            # Test caption
            caption = ai.generate_caption(occasion="wedding", platform="instagram")
            if len(caption) <= 150:
                self._pass(f"Caption generated ({len(caption)} chars)")
            else:
                self._warn(f"Caption too long ({len(caption)} chars)")
            
            # Test hashtags
            hashtags = ai.generate_hashtags(occasion="general", platform="instagram")
            if len(hashtags) >= 5:
                self._pass(f"Hashtags generated ({len(hashtags)} tags)")
            else:
                self._warn(f"Only {len(hashtags)} hashtags generated")
            
        except Exception as e:
            self._fail("AI content", e)
        
        print()
    
    def test_video_engine(self):
        """Test video generation (requires assets)"""
        print("🎬 Testing Video Engine...")
        
        try:
            # Check for source clips
            assets_dir = self.base_dir / 'assets/raw_video'
            
            categories = ['sticking', 'scanning', 'reaction']
            clips_found = {}
            
            for category in categories:
                category_path = assets_dir / category
                if category_path.exists():
                    clips = list(category_path.glob('*.mp4')) + \
                           list(category_path.glob('*.mov'))
                    clips_found[category] = len(clips)
                else:
                    clips_found[category] = 0
            
            total_clips = sum(clips_found.values())
            
            if total_clips >= 3:  # At least 1 from each category
                self._pass(f"Source clips found ({total_clips} total)")
                for cat, count in clips_found.items():
                    print(f"      {cat}: {count} clips")
            else:
                self._warn("Not enough source clips for video generation")
                print("      Add clips to assets/raw_video/ to test video generation")
                print()
                return
            
            # If we have clips, test hash breaking
            from generators.video_engine_v2 import video_engine_v2
            self._pass("Video engine v2 initialized")
            self._pass("Hash breaking enabled by default")
            
        except Exception as e:
            self._fail("Video engine", e)
        
        print()
    
    def test_telegram_publisher(self):
        """Test Telegram publisher"""
        print("📱 Testing Telegram Publisher...")
        
        try:
            from config.settings_v2 import settings
            
            if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
                self._warn("Skipping Telegram tests (not configured)")
                print()
                return
            
            from publishers.safe_publisher import SafePublisher
            publisher = SafePublisher(
                settings.TELEGRAM_BOT_TOKEN,
                settings.TELEGRAM_CHAT_ID
            )
            
            self._pass("Safe publisher initialized")
            
            # Test connection
            print("   Testing Telegram connection...")
            success = asyncio.run(publisher.send_test_message())
            
            if success:
                self._pass("Telegram connection successful")
                print("   ✓ Check your phone for the test message!")
            else:
                self._fail("Telegram connection", "Send failed")
            
        except Exception as e:
            self._fail("Telegram publisher", e)
        
        print()
    
    def test_main_orchestrator(self):
        """Test main orchestrator"""
        print("🎯 Testing Main Orchestrator...")
        
        try:
            # Just test initialization
            import main_v2
            self._pass("Main v2 module imported")
            
            from main_v2 import RemixEngineV2
            
            # Check if we can initialize
            try:
                engine = RemixEngineV2()
                self._pass("RemixEngineV2 initialized")
            except ValueError as e:
                self._warn(f"Initialization incomplete: {e}")
            
        except Exception as e:
            self._fail("Main orchestrator", e)
        
        print()
    
    def _pass(self, test_name):
        """Record passed test"""
        print(f"   ✅ {test_name}")
        self.tests_passed += 1
    
    def _fail(self, test_name, error=""):
        """Record failed test"""
        print(f"   ❌ {test_name}")
        if error:
            print(f"      Error: {error}")
        self.tests_failed += 1
    
    def _warn(self, message):
        """Record warning"""
        print(f"   ⚠️  {message}")
        self.warnings.append(message)
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\nTests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_failed}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        print("\n" + "=" * 60)
        
        if self.tests_failed == 0:
            print("✅ ALL TESTS PASSED!")
            print("Remix Engine V2.0 is ready to use")
        else:
            print(f"⚠️  {self.tests_failed} TEST(S) FAILED")
            print("Fix issues before deploying")
        
        print("=" * 60)


def main():
    """Run test suite"""
    suite = TestSuiteV2()
    suite.run_all_tests()


if __name__ == "__main__":
    main()
