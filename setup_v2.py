#!/usr/bin/env python3
"""
Setup Validator - V2.0 VIRAL EDITION
Validates complete system setup and dependencies
"""
import sys
import subprocess
from pathlib import Path
import shutil


class SetupValidatorV2:
    """Validates Remix Engine V2.0 setup"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("=" * 60)
        print("REMIX ENGINE V2.0 - SETUP VALIDATOR")
        print("=" * 60)
        print()
        
        self.check_python_version()
        self.check_system_dependencies()
        self.check_python_packages()
        self.check_directory_structure()
        self.check_configuration()
        self.check_assets()
        self.check_permissions()
        
        self.print_summary()
    
    def check_python_version(self):
        """Check Python version"""
        print("🐍 Checking Python Version...")
        
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major == 3 and version.minor >= 11:
            self._pass(f"Python {version_str}")
        elif version.major == 3 and version.minor >= 9:
            self._warn(f"Python {version_str} (3.11+ recommended)")
        else:
            self._fail(f"Python {version_str} (3.11+ required)")
        
        print()
    
    def check_system_dependencies(self):
        """Check system-level dependencies"""
        print("🔧 Checking System Dependencies...")
        
        dependencies = {
            'ffmpeg': 'FFmpeg (video processing)',
            'convert': 'ImageMagick (image processing)',
            'chromium-browser': 'Chromium (HTML rendering)',
            'google-chrome': 'Chrome (HTML rendering alternative)'
        }
        
        for cmd, description in dependencies.items():
            if shutil.which(cmd):
                self._pass(f"{description}")
            else:
                if cmd in ['chromium-browser', 'google-chrome']:
                    # Only one browser needed
                    continue
                self._fail(f"{description} not found")
        
        # Check if at least one browser exists
        if shutil.which('chromium-browser') or shutil.which('google-chrome'):
            self._pass("Browser for HTML rendering")
        else:
            self._warn("No browser found (install chromium or chrome)")
        
        print()
    
    def check_python_packages(self):
        """Check Python package installations"""
        print("📦 Checking Python Packages...")
        
        required_packages = [
            ('moviepy', 'Video processing'),
            ('PIL', 'Image processing (Pillow)'),
            ('google.generativeai', 'AI content (Gemini)'),
            ('telegram', 'Telegram bot'),
            ('loguru', 'Logging'),
            ('pydantic', 'Configuration'),
            ('html2image', 'Pro overlays (V2.0)'),
            ('edge_tts', 'Voiceovers (V2.0)')
        ]
        
        for package, description in required_packages:
            try:
                __import__(package)
                self._pass(f"{description}")
            except ImportError:
                self._fail(f"{description} not installed")
        
        print()
    
    def check_directory_structure(self):
        """Check required directories exist"""
        print("📁 Checking Directory Structure...")
        
        required_dirs = [
            'assets',
            'assets/raw_video',
            'assets/raw_video/sticking',
            'assets/raw_video/scanning',
            'assets/raw_video/reaction',
            'assets/backgrounds',
            'assets/music',
            'assets/overlays',
            'assets/temp',
            'output',
            'output/videos',
            'output/images',
            'logs',
            'config',
            'generators',
            'publishers'
        ]
        
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if full_path.exists():
                self._pass(f"{dir_path}/")
            else:
                # Create missing directories
                full_path.mkdir(parents=True, exist_ok=True)
                self._pass(f"{dir_path}/ (created)")
        
        print()
    
    def check_configuration(self):
        """Check configuration files and environment"""
        print("⚙️  Checking Configuration...")
        
        # Check .env file
        env_file = self.base_dir / '.env'
        if env_file.exists():
            self._pass(".env file exists")
            
            # Load and check keys
            env_content = env_file.read_text()
            
            if 'GEMINI_API_KEY=' in env_content and \
               'GEMINI_API_KEY=your_key_here' not in env_content and \
               'GEMINI_API_KEY=""' not in env_content:
                self._pass("Gemini API key configured")
            else:
                self._fail("Gemini API key not set")
            
            if 'TELEGRAM_BOT_TOKEN=' in env_content and \
               'TELEGRAM_BOT_TOKEN=""' not in env_content:
                self._pass("Telegram bot token configured")
            else:
                self._warn("Telegram not configured (required for safe mode)")
            
        else:
            env_example = self.base_dir / '.env.example'
            if env_example.exists():
                self._warn(".env file missing (copy from .env.example)")
            else:
                self._fail(".env file missing")
        
        # Check config files
        config_files = [
            'config/settings_v2.py',
            'config/prompts_v2.json'
        ]
        
        for config_file in config_files:
            if (self.base_dir / config_file).exists():
                self._pass(f"{config_file}")
            else:
                if 'prompts' in config_file:
                    self._warn(f"{config_file} (will use defaults)")
                else:
                    self._fail(f"{config_file} missing")
        
        print()
    
    def check_assets(self):
        """Check asset availability"""
        print("🎬 Checking Assets...")
        
        # Check video clips
        categories = ['sticking', 'scanning', 'reaction']
        total_clips = 0
        
        for category in categories:
            category_path = self.base_dir / f'assets/raw_video/{category}'
            clips = list(category_path.glob('*.mp4')) + \
                   list(category_path.glob('*.mov'))
            
            clip_count = len(clips)
            total_clips += clip_count
            
            if clip_count >= 10:
                self._pass(f"{category}: {clip_count} clips")
            elif clip_count > 0:
                self._warn(f"{category}: {clip_count} clips (10 recommended)")
            else:
                self._warn(f"{category}: No clips (add .mp4 or .mov files)")
        
        if total_clips >= 30:
            self._pass(f"Total clips: {total_clips} (optimal)")
        elif total_clips >= 3:
            self._pass(f"Total clips: {total_clips} (minimum met)")
        else:
            self._warn("Add video clips to generate content")
        
        # Check backgrounds
        backgrounds_path = self.base_dir / 'assets/backgrounds'
        images = list(backgrounds_path.glob('*.jpg')) + \
                list(backgrounds_path.glob('*.png'))
        
        if len(images) >= 5:
            self._pass(f"Background images: {len(images)}")
        elif len(images) > 0:
            self._warn(f"Background images: {len(images)} (5+ recommended)")
        else:
            self._warn("No background images (optional)")
        
        print()
    
    def check_permissions(self):
        """Check file permissions"""
        print("🔐 Checking Permissions...")
        
        # Check if main scripts are executable
        scripts = ['main_v2.py', 'test_v2.py', 'setup_v2.py']
        
        for script in scripts:
            script_path = self.base_dir / script
            if script_path.exists():
                if script_path.stat().st_mode & 0o111:  # Check execute permission
                    self._pass(f"{script} is executable")
                else:
                    self._warn(f"{script} not executable (run: chmod +x {script})")
            else:
                self._warn(f"{script} not found")
        
        # Check write permissions for output directories
        output_dirs = [
            self.base_dir / 'output',
            self.base_dir / 'logs',
            self.base_dir / 'assets/temp'
        ]
        
        for dir_path in output_dirs:
            if dir_path.exists():
                test_file = dir_path / '.write_test'
                try:
                    test_file.touch()
                    test_file.unlink()
                    self._pass(f"{dir_path.name}/ writable")
                except Exception:
                    self._fail(f"{dir_path.name}/ not writable")
        
        print()
    
    def _pass(self, check_name):
        """Record passed check"""
        print(f"   ✅ {check_name}")
        self.checks_passed += 1
    
    def _fail(self, check_name):
        """Record failed check"""
        print(f"   ❌ {check_name}")
        self.checks_failed += 1
    
    def _warn(self, message):
        """Record warning"""
        print(f"   ⚠️  {message}")
        self.warnings.append(message)
    
    def print_summary(self):
        """Print validation summary"""
        print("=" * 60)
        print("SETUP SUMMARY")
        print("=" * 60)
        
        total_checks = self.checks_passed + self.checks_failed
        pass_rate = (self.checks_passed / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\nChecks Passed: {self.checks_passed}")
        print(f"Checks Failed: {self.checks_failed}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        print("\n" + "=" * 60)
        
        if self.checks_failed == 0:
            print("✅ SETUP COMPLETE!")
            print("Remix Engine V2.0 is ready to use")
            print()
            print("Next steps:")
            print("1. Run: python test_v2.py")
            print("2. Generate test video: python main_v2.py --mode single")
            print("3. Start daily workflow: python main_v2.py --mode daily")
        else:
            print(f"⚠️  {self.checks_failed} ISSUE(S) FOUND")
            print("Fix issues before using the system")
            print()
            
            if self.checks_failed > 0:
                print("Common fixes:")
                print("- Install dependencies: pip install -r requirements.txt")
                print("- Install system tools: sudo apt-get install ffmpeg imagemagick")
                print("- Configure .env: cp .env.example .env (then edit)")
                print("- Add video clips: copy .mp4 files to assets/raw_video/")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        print("=" * 60)


def main():
    """Run setup validation"""
    validator = SetupValidatorV2()
    validator.run_all_checks()


if __name__ == "__main__":
    main()
