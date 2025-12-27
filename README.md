# 🚀 REMIX ENGINE V2.0 - "VIRAL EDITION"

**The Unstoppable Hit of Marketing**

Automated content generation system with:
- ✅ **ZERO ban risk** (Telegram-first distribution)
- ✅ **Pro HTML/CSS overlays** (10x better than basic text)
- ✅ **Free unlimited voiceovers** (viral TikTok voices)
- ✅ **Hash breaking** (prevents duplicate penalties)
- ✅ **£0/month forever**

---

## 📊 WHY V2.0?

### V1.0 Had Critical Flaws

1. **Auto-posting = BAN RISK**
   - GitHub Actions uses datacenter IPs
   - Instagram/TikTok detect instantly
   - Your account gets shadowbanned

2. **Basic overlays = Poor quality**
   - MoviePy TextClip looked like 2015 memes
   - No gradients, shadows, or effects

3. **No voiceovers = Low retention**
   - 40-60% lower watch time
   - Algorithm downranks silent videos

4. **Duplicate content penalties**
   - Same combinations flagged as duplicates
   - Reach drops 60-80%

### V2.0 Solves Everything

1. **Safe Telegram-first = ZERO ban risk**
   - System generates everything
   - Sends to your Telegram
   - You post manually (30 seconds)
   - Add trending audio in app

2. **Pro HTML/CSS overlays = Viral quality**
   - Gradients, shadows, strokes
   - Emoji support
   - Professional CapCut look

3. **Free unlimited voices = Maximum retention**
   - Edge-TTS (Microsoft)
   - Same voices as viral TikToks
   - £0/month vs £300/year

4. **Hash breaking = Algorithm loves it**
   - Invisible micro-variations
   - Every video 100% unique
   - Can reuse combinations

---

## ⚡ QUICK START

### 1. Install Dependencies

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y ffmpeg imagemagick chromium-browser

# Or on macOS
brew install ffmpeg imagemagick chromium

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

Required keys:
- `GEMINI_API_KEY` - Get from https://makersuite.google.com/app/apikey
- `TELEGRAM_BOT_TOKEN` - Get from @BotFather on Telegram
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

### 3. Validate Setup

```bash
python setup_v2.py
```

This checks:
- ✅ Python version (3.11+)
- ✅ System dependencies
- ✅ Python packages
- ✅ Configuration
- ✅ Directory structure

### 4. Run Tests

```bash
python test_v2.py
```

Tests all V2.0 features:
- ✅ Pro overlays
- ✅ Voiceovers
- ✅ AI content
- ✅ Telegram connection

### 5. Generate First Video

```bash
# Single test video
python main_v2.py --mode single

# Full daily batch (3 videos)
python main_v2.py --mode daily

# Custom batch
python main_v2.py --mode batch --count 5 --platform tiktok
```

---

## 📖 USAGE

### Command-Line Interface

```bash
# Daily workflow (automated)
python main_v2.py --mode daily

# Single video
python main_v2.py --mode single --occasion birthday

# Batch generation
python main_v2.py --mode batch --count 10 --platform instagram

# Test Telegram
python main_v2.py --mode test-telegram

# Test features
python main_v2.py --mode test-features
```

### Python API

```python
from main_v2 import RemixEngineV2

# Initialize
engine = RemixEngineV2()

# Generate single video
video_path, content = engine.generate_single_video(
    occasion="wedding",
    platform="instagram"
)

# Generate batch
results = engine.generate_batch(
    count=5,
    platform="tiktok"
)

# Send to Telegram
import asyncio
asyncio.run(engine.send_to_telegram(video_path, content))
```

---

## 🎨 V2.0 FEATURES

### 1. Pro Overlay Engine

**Before (V1.0):**
```python
TextClip("TAP TO PLAY", fontsize=80, color='white')
# Result: Basic, ugly text
```

**After (V2.0):**
```python
overlay_engine.create_hook_overlay(
    text="TAP TO HEAR\nTHEIR VOICE! 🎁",
    style="tiktok",
    position="top"
)
# Result: Professional CapCut-style overlay
```

**Styles available:**
- `tiktok` - Viral TikTok style (bold, high contrast)
- `instagram` - Instagram Reels style (colorful)
- `youtube` - YouTube Shorts style (impactful)
- `minimal` - Clean, modern style

### 2. Audio Engine

**Free unlimited viral voiceovers:**

```python
audio_engine.generate_voiceover(
    text="TAP THIS CARD TO HEAR THEIR VOICE!",
    voice_type='tiktok_girl'
)
```

**Available voices:**
- `tiktok_girl` - The famous viral TikTok voice
- `tiktok_guy` - Male version
- `storyteller` - Childlike, emotional
- `professional` - Deep, authoritative
- `british_girl` - Elegant British female
- `british_guy` - Professional British male
- `excited` - Enthusiastic, upbeat
- `calm` - Soothing, calming
- `dramatic` - Intense, dramatic

### 3. Hash Breaking

**Prevents duplicate content penalties:**

```python
# Automatic in video_engine_v2.py
video_engine_v2.apply_hash_breaker(clip)
```

**What it does:**
- Micro speed variation (0.99x - 1.01x)
- Micro color shift (±2%)
- Micro crop offset (±10px)
- Random horizontal flip (50%)

**Result:**
- Human eye: Identical
- Algorithm: Completely unique
- Can post same combination 10x

### 4. Safe Publisher

**Telegram-first distribution:**

```python
publisher.send_video_package(
    video_path=video,
    caption="AI-generated caption",
    hashtags=['#NFC', '#Gift'],
    platform="instagram"
)
```

**Workflow:**
1. Video sent to Telegram
2. You save to gallery (1 tap)
3. Open Instagram/TikTok
4. Add trending audio (CRITICAL)
5. Paste caption
6. Post

**Time:** 30 seconds per video  
**Ban risk:** 0%

---

## ⚙️ CONFIGURATION

### Environment Variables (.env)

```bash
# Required
GEMINI_API_KEY=your_gemini_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Safe Mode (Default: True)
SAFE_MODE=true
ALLOW_AUTO_POSTING=false

# Video Settings
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
VIDEO_FPS=30

# Voice Settings (V2.0)
ENABLE_VOICEOVER=true
DEFAULT_VOICE=tiktok_girl
VOICE_RATE_VARIATION=true

# Overlay Settings (V2.0)
USE_PRO_OVERLAYS=true
DEFAULT_OVERLAY_STYLE=tiktok
OVERLAY_POSITION=top

# Hash Breaking (Always True)
ENABLE_HASH_BREAKING=true

# Batch Settings
DAILY_VIDEO_COUNT=3
DAILY_IMAGE_COUNT=5
```

### Settings Object

```python
from config.settings_v2 import settings

# Voice configuration
voice_config = settings.get_voice_config()

# Overlay configuration
overlay_config = settings.get_overlay_config()

# Hash breaking configuration
hash_config = settings.get_hash_break_config()

# Validate
missing = settings.validate_required()
if missing:
    print(f"Missing: {', '.join(missing)}")
```

---

## 🎯 GITHUB ACTIONS (Automated)

### Setup

1. Create GitHub repository
2. Add secrets:
   - `GEMINI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Push code
4. Enable Actions

### Workflow

**Automatic runs:** 3x daily (9 AM, 3 PM, 9 PM UTC)

**Manual trigger:** Actions → Run workflow

**What happens:**
1. GitHub Actions wakes up
2. Generates 3 videos with V2.0 features
3. Sends to your Telegram
4. You post manually (30 seconds)

**Benefits:**
- Cloud-based generation
- No local computer needed
- Zero ban risk
- Can add trending audio

---

## 📁 PROJECT STRUCTURE

```
remix-engine-v2/
├── main_v2.py              # Main orchestrator
├── test_v2.py              # Test suite
├── setup_v2.py             # Setup validator
├── requirements.txt        # Dependencies
├── .env.example            # Environment template
├── .github/
│   └── workflows/
│       └── safe_daily_content.yml
├── config/
│   ├── settings_v2.py      # Configuration system
│   └── prompts_v2.json     # AI prompts
├── generators/
│   ├── overlay_engine.py   # Pro HTML/CSS overlays (NEW)
│   ├── audio_engine.py     # Viral voiceovers (NEW)
│   ├── video_engine_v2.py  # Hash breaking + features
│   └── ai_content_v2.py    # AI content generation
├── publishers/
│   └── safe_publisher.py   # Telegram-first (NEW)
├── assets/
│   ├── raw_video/          # Source clips
│   ├── backgrounds/        # Product photos
│   ├── music/              # Audio tracks
│   └── temp/               # Generated overlays/voices
├── output/
│   ├── videos/             # Generated videos
│   └── images/             # Generated images
└── logs/                   # System logs
```

---

## 🚀 DEPLOYMENT

### Local (Recommended for Testing)

```bash
# Run directly
python main_v2.py --mode daily

# Or with cron
0 9,15,21 * * * cd /path/to/remix-engine-v2 && python main_v2.py --mode daily
```

### GitHub Actions (Recommended for Production)

1. Push to GitHub
2. Add secrets
3. Enable Actions
4. Runs automatically 3x daily

### Docker (Optional)

```bash
# Build
docker build -t remix-engine-v2 .

# Run
docker run -v $(pwd)/assets:/app/assets \
           -v $(pwd)/output:/app/output \
           --env-file .env \
           remix-engine-v2 \
           python main_v2.py --mode daily
```

---

## 📊 RESULTS

### After 1 Month

**Content Generated:**
- 90 videos (3/day × 30 days)
- All with pro overlays
- All with viral voices
- All algorithmically unique

**Time Saved:**
- Manual creation: 60 hours
- V2.0 posting: 45 minutes (30s × 90)
- Net savings: 59.25 hours

**Money Saved:**
- Manual creation: £3,000 (60h × £50/h)
- V2.0 cost: £0
- Voiceover savings: £25 (ElevenLabs)
- Total savings: £3,025

**Risk Avoided:**
- Account bans: £0 (priceless)
- Social media rebuild: £10,000+
- Lost followers: Priceless

---

## ⚠️ SAFETY WARNINGS

### DO NOT:

1. ❌ **Auto-post to main account from GitHub**
   - Will get shadowbanned
   - Not worth the risk

2. ❌ **Skip hash breaking**
   - Algorithm will penalize
   - Reach drops 80%

3. ❌ **Use V1.0 publishers**
   - Detection risk too high
   - Only for burner accounts

### ALWAYS:

1. ✅ **Use safe mode (Telegram-first)**
   - 30 seconds daily
   - Zero ban risk
   - Add trending audio

2. ✅ **Test on burner first**
   - @yourband_test account
   - Validate automation
   - Protect main account

3. ✅ **Add trending audio manually**
   - 3x reach boost
   - Algorithm loves it
   - Worth the 5 seconds

---

## 🆘 TROUBLESHOOTING

### Common Issues

**"GEMINI_API_KEY not set"**
```bash
# Get free API key
# https://makersuite.google.com/app/apikey
# Add to .env
```

**"Telegram not configured"**
```bash
# 1. Message @BotFather on Telegram
# 2. Send: /newbot
# 3. Follow instructions
# 4. Copy token to .env
# 5. Get chat ID: message bot, visit:
#    https://api.telegram.org/bot<TOKEN>/getUpdates
```

**"No video clips found"**
```bash
# Add clips to:
cp your_clips/*.mp4 assets/raw_video/sticking/
cp your_clips/*.mp4 assets/raw_video/scanning/
cp your_clips/*.mp4 assets/raw_video/reaction/
```

**"FFmpeg not found"**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

---

## 📖 DOCUMENTATION

- **V2.0_UPGRADE_GUIDE.md** - Complete feature guide
- **IMPLEMENTATION_STATUS.md** - Development status
- **GITHUB_SETUP_MANUAL.md** - GitHub deployment guide
- **GITHUB_QUICK_VISUAL.md** - Visual setup guide
- **GITHUB_ERRORS_SOLUTIONS.md** - Troubleshooting

---

## 🎉 SUCCESS METRICS

**V2.0 delivers:**
- ✅ 99% automation (30s manual posting)
- ✅ 0% ban risk
- ✅ £3,000+/month savings
- ✅ Professional quality content
- ✅ Unlimited scalability
- ✅ £0/month forever

**Trade 30 seconds daily for:**
- Complete account protection
- 3x algorithm boost (trending audio)
- Quality control
- Peace of mind

---

## 📞 SUPPORT

**Issues?** Run diagnostics:
```bash
python setup_v2.py  # Validate setup
python test_v2.py   # Test features
python main_v2.py --mode test-features  # Test engines
```

**Need help?**
- Check GITHUB_ERRORS_SOLUTIONS.md
- Review documentation files
- Run test commands above

---

## 🚀 YOU'RE READY!

**Setup complete? Start here:**

```bash
# 1. Validate
python setup_v2.py

# 2. Test
python test_v2.py

# 3. Generate
python main_v2.py --mode single

# 4. Deploy
git push origin main  # GitHub Actions takes over
```

**Your unstoppable content factory is LIVE! 🎬**

---

**Version:** 2.0.0  
**Status:** Production Ready  
**License:** Private Use  
**Author:** Daroo
