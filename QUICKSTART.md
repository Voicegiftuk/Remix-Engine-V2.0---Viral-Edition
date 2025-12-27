# ⚡ QUICK START - REMIX ENGINE V2.0

**Get running in 10 minutes!**

---

## 🚀 FASTEST PATH TO FIRST VIDEO

### Step 1: Download & Extract (1 min)

```bash
# Extract archive
unzip remix-engine-v2.zip
# or: tar -xzf remix-engine-v2.tar.gz

cd remix-engine-v2
```

### Step 2: Install (3 min)

```bash
# Install Python packages
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y ffmpeg imagemagick chromium-browser

# Or macOS
brew install ffmpeg imagemagick chromium
```

### Step 3: Configure (2 min)

```bash
# Copy environment template
cp .env.example .env

# Edit and add your keys
nano .env
```

**Minimum required:**
- `GEMINI_API_KEY` - Get from: https://makersuite.google.com/app/apikey
- `TELEGRAM_BOT_TOKEN` - Message @BotFather on Telegram, send /newbot
- `TELEGRAM_CHAT_ID` - Message your bot, visit: https://api.telegram.org/bot<TOKEN>/getUpdates

### Step 4: Validate (1 min)

```bash
python setup_v2.py
```

Should see: ✅ All checks passed

### Step 5: Test (1 min)

```bash
python test_v2.py
```

Should see: ✅ Most tests passed (some warnings OK if no video clips yet)

### Step 6: Generate! (2 min)

```bash
# Generate single test video
python main_v2.py --mode single --occasion birthday
```

**What happens:**
1. AI generates hook, caption, hashtags
2. Creates pro overlay with HTML/CSS
3. Generates viral voiceover (TikTok voice)
4. Creates video with hash breaking
5. Sends to your Telegram

**Check your phone!** 📱

---

## 📱 POSTING (30 seconds)

When video arrives on Telegram:

1. Save video to gallery
2. Open Instagram (or TikTok)
3. Create new Reel/video
4. Upload saved video
5. **TAP MUSIC → Add trending audio** (CRITICAL!)
6. Go back to Telegram, copy caption
7. Paste caption in Instagram
8. Post!

**Time: 30 seconds**  
**Ban risk: 0%**  
**Reach: Maximum (trending audio boost)**

---

## 🎯 DAILY WORKFLOW

### Automated (GitHub Actions - Recommended)

1. Push code to GitHub
2. Add secrets (Settings → Secrets → Actions)
3. Enable Actions
4. Done! Runs 3x daily automatically

**Time:** 0 minutes (fully automated)  
**Your work:** Post manually when phone buzzes (30s × 3)

### Manual (Run Yourself)

```bash
# Run daily generation
python main_v2.py --mode daily
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Add line (runs at 9 AM, 3 PM, 9 PM)
0 9,15,21 * * * cd /path/to/remix-engine-v2 && python main_v2.py --mode daily
```

---

## 🎬 ADDING VIDEO CLIPS

For full functionality, add your filmed clips:

```bash
# Copy clips to respective folders
cp sticking_clips/*.mp4 assets/raw_video/sticking/
cp scanning_clips/*.mp4 assets/raw_video/scanning/
cp reaction_clips/*.mp4 assets/raw_video/reaction/

# Add product photos
cp product_photos/*.jpg assets/backgrounds/
```

**What to film:**
- **Sticking** (10 clips): Hand placing NFC sticker on various products
- **Scanning** (10 clips): Phone tapping the sticker
- **Reaction** (10 clips): Screen recordings of voice messages playing

**Result:** 10 × 10 × 10 = 1,000 unique video combinations!

---

## ⚙️ COMMON COMMANDS

```bash
# Validate setup
python setup_v2.py

# Run tests
python test_v2.py

# Generate single video
python main_v2.py --mode single

# Generate daily batch (3 videos)
python main_v2.py --mode daily

# Generate custom batch
python main_v2.py --mode batch --count 5 --platform tiktok

# Test Telegram connection
python main_v2.py --mode test-telegram

# Test individual features
python main_v2.py --mode test-features
```

---

## 🆘 QUICK FIXES

**"GEMINI_API_KEY not set"**
```bash
# Get free key: https://makersuite.google.com/app/apikey
# Add to .env file
```

**"Telegram not configured"**
```bash
# 1. Message @BotFather on Telegram
# 2. Send: /newbot
# 3. Follow instructions, copy token
# 4. Add to .env file
```

**"No video clips found"**
```bash
# Expected on first run
# Add clips to assets/raw_video/
# Or just test with pro overlays & voice
```

**"FFmpeg not found"**
```bash
# Ubuntu: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
```

---

## 📖 FULL DOCUMENTATION

- **README.md** - Complete guide (must read!)
- **V2.0_UPGRADE_GUIDE.md** - All features explained
- **GITHUB_SETUP_MANUAL.md** - GitHub deployment
- **GITHUB_ERRORS_SOLUTIONS.md** - Troubleshooting

---

## ✅ SUCCESS CHECKLIST

After quick start, you should have:

- ☑ Remix Engine V2.0 installed
- ☑ Dependencies installed
- ☑ Configuration validated
- ☑ Tests passing
- ☑ First video generated
- ☑ Telegram delivery working
- ☑ Posted first video manually

**Next:**
- Film your 30 source clips
- Deploy to GitHub Actions
- Let automation handle the rest!

---

## 🎉 YOU'RE LIVE!

**V2.0 is running!**

**Daily workflow:**
1. System generates 3 videos (automatic)
2. Sends to Telegram (automatic)
3. You post manually (90 seconds total)
4. Repeat forever (£0/month)

**Your content factory is operational! 🚀**

---

**Questions?** Check README.md or run:
```bash
python setup_v2.py  # Diagnostics
python test_v2.py   # Feature tests
```

**Ready for more?** Read V2.0_UPGRADE_GUIDE.md for advanced features!
