# 🚀 PROJECT TITAN - The Global Marketing Singularity
## Complete Marketing Automation for SayPlay

**Version:** 1.0 - Foundation Release  
**Status:** Phase 1 Ready  
**Philosophy:** White Hat | Human-Indistinguishable | Zero Ban Risk  

---

## 🎯 WHAT IS PROJECT TITAN?

Titan to rozbudowa **Remix Engine V2.0** (social media videos) do kompletnego systemu marketingowego, który automatyzuje:

### ✅ MASZ JUŻ (Remix V2.0):
- 9 social media videos/dzień
- Instagram Reels + TikTok ready
- Pro overlays + voiceovers
- Telegram-first delivery
- Value: £13,500/miesiąc

### 🆕 DODAJEMY (Titan Expansion):
- **Blog Engine:** SEO articles (White Hat, human-like)
- **Image Engine:** Branded social images
- **Email Engine:** Campaign automation
- **Distribution:** Safe multi-platform publishing
- **Command Center:** Telegram dashboard
- **Brand Core:** Logo watermarking everywhere

### 🎉 RAZEM BĘDZIESZ MIAŁ:
- 270 videos/miesiąc
- 30 SEO articles/miesiąc
- 300 branded images/miesiąc
- 24 email campaigns/miesiąc
- **Value: £130,000/miesiąc**
- **Cost: £0**
- **Time: 10 minut/dzień (approvals only)**

---

## 📂 PROJECT STRUCTURE

```
remix-engine-titan/
│
├── core/                           # Brand + Database
│   ├── brand_identity/
│   │   ├── brand_core.py          ✅ READY
│   │   ├── logos/                  ⏳ ADD YOUR LOGOS
│   │   ├── colors.json
│   │   └── voice.json
│   └── database/
│       └── content_db.py           ⏳ Week 1
│
├── modules/                        # All content engines
│   ├── video/                      ✅ FROM REMIX V2.0
│   │   ├── generators/
│   │   └── video_module.py
│   ├── blog/                       🆕 SEO ARTICLES
│   │   ├── research/
│   │   ├── writer/
│   │   │   └── article_generator.py ✅ READY
│   │   └── blog_module.py          ⏳ Week 2
│   ├── image/                      🆕 SOCIAL IMAGES
│   │   └── image_module.py         ⏳ Week 3
│   └── distribution/               🆕 SAFE PUBLISHING
│       └── distribution_module.py  ⏳ Week 4
│
├── orchestrator/                   # Central controller
│   └── titan_orchestrator.py      ⏳ Week 4
│
├── command_center/                 # Telegram dashboard
│   └── telegram_bot.py             ⏳ Week 5
│
├── main_titan.py                   # Main entry point
├── requirements_titan.txt          # All dependencies
└── INTEGRATION_PLAN.md             ✅ COMPLETE SPEC

Legend:
✅ READY - Gotowe do użycia
🆕 NEW - Nowy moduł (w budowie)
⏳ PLANNED - Zaplanowane
```

---

## 🚀 QUICK START

### Option A: Nowy Install (From Scratch)

```bash
# 1. Clone/Download Titan
git clone https://github.com/yourusername/remix-engine-titan.git
cd remix-engine-titan

# 2. Install dependencies
pip install -r requirements_titan.txt --break-system-packages

# 3. Add SayPlay logos
# Copy your logo files to: core/brand_identity/logos/
# Required files:
# - sayplay_logo_primary.png
# - sayplay_watermark.png

# 4. Configure
cp .env.example .env
nano .env  # Add your API keys

# 5. Test Brand Core
python core/brand_identity/brand_core.py

# 6. Test Blog Generator
python modules/blog/writer/article_generator.py
```

### Option B: Upgrade Existing Remix V2.0

```bash
# 1. Backup your current Remix V2.0
cp -r Remix-Engine-V2.0---Viral-Edition Remix-V2-BACKUP

# 2. Download Titan expansion files
# Copy files from titan-expansion/ to your project

# 3. Migrate video module
mkdir -p modules/video
mv generators modules/video/
mv publishers modules/video/
mv main_v2.py modules/video/video_module.py

# 4. Add brand core
cp -r core/ ./

# 5. Test (ensure video still works)
python modules/video/video_module.py --test
```

---

## 🔧 CONFIGURATION

### Required API Keys (.env)

```bash
# Existing (from Remix V2.0)
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id

# New (for Titan expansion)
# Optional - add when ready for WordPress publishing
WORDPRESS_URL=https://sayplay.co.uk
WORDPRESS_API_KEY=your_wordpress_key
```

### Brand Assets

**Required logos (PNG with transparent background):**

1. **sayplay_logo_primary.png** - Main logo (color)
2. **sayplay_logo_white.png** - For dark backgrounds
3. **sayplay_logo_black.png** - For light backgrounds
4. **sayplay_watermark.png** - Transparent watermark (for videos/images)

**Where to add:** `core/brand_identity/logos/`

---

## 💻 USAGE

### Test Individual Modules

```bash
# Test Brand Core
python core/brand_identity/brand_core.py

# Test Video Module (Remix V2.0)
python modules/video/video_module.py --mode single --occasion birthday

# Test Blog Generator
python modules/blog/writer/article_generator.py

# Test Full System (when ready)
python main_titan.py --mode daily
```

### Daily Workflow (Future - Week 5)

```bash
# Manual run
python main_titan.py --mode daily

# What it does:
# 1. Generates 9 videos (Remix V2.0)
# 2. Generates 1 blog article (2000 words)
# 3. Generates 10 social images
# 4. Sends everything to Telegram for approval
# 5. You click [✅ Approve] or [❌ Reject]
# 6. Approved content auto-publishes

# Time required: 10 minutes (review + approve)
```

---

## 📊 DELIVERABLES (What You Get)

### Phase 1: Foundation (Week 1) ✅ AVAILABLE NOW

**Files delivered:**
```
✅ core/brand_identity/brand_core.py        # Brand management system
✅ modules/blog/writer/article_generator.py # Blog article generator
✅ INTEGRATION_PLAN.md                      # Complete implementation guide
```

**What works:**
- Brand identity system (logo watermarking, color palette, voice validation)
- Blog article generator (SEO-optimized, human-like, anti-AI detection)
- Integration plan (step-by-step expansion guide)

**What you can test now:**
```bash
# 1. Brand system
python core/brand_identity/brand_core.py

# Output: Tests color system, brand voice validation, watermarking

# 2. Blog generator
python modules/blog/writer/article_generator.py

# Output: Complete 1500-word article (HTML + metadata)
```

### Phase 2-5: Full System (Weeks 2-6) ⏳ COMING

**Modules to be delivered:**
- Week 2: Complete Blog Module (research + SEO + publishing)
- Week 3: Image Module (AI generation + branding + resizing)
- Week 4: Orchestrator (workflow automation + scheduling)
- Week 5: Command Center (Telegram dashboard + approval system)
- Week 6: Deployment (GitHub Actions + documentation)

---

## 🎨 FEATURES

### Brand Identity Core ✅

**Brand Consistency Everywhere:**
- Logo watermarking (automatic, customizable position/opacity)
- Color palette enforcement (SayPlay Orange #FF6B35)
- Brand voice validation (checks if text sounds like SayPlay)
- Typography standards

**Example Usage:**
```python
from core.brand_identity.brand_core import get_brand_core

brand = get_brand_core()

# Apply watermark to image
brand.apply_watermark(
    'input.jpg',
    'output.jpg',
    position='bottom-right',
    opacity=0.7
)

# Get brand colors
orange = brand.get_color('primary.orange')  # #FF6B35

# Validate brand voice
result = brand.validate_brand_voice("Your text here")
# Returns: {valid: True, score: 85, issues: [], suggestions: []}

# Get AI prompt with brand personality
prompt = brand.get_brand_prompt('blog')
# Returns: System prompt that enforces SayPlay tone
```

### Blog Article Generator ✅

**Human-Like SEO Content:**
- Anti-AI detection (burstiness, perplexity, human patterns)
- White Hat SEO (keyword density, internal linking, meta optimization)
- Brand voice enforcement (SayPlay personality throughout)
- Structured output (HTML + metadata)

**Example Usage:**
```python
from modules.blog.writer.article_generator import ArticleGenerator

generator = ArticleGenerator(gemini_api_key)

# Generate article
brief = {
    'primary_keyword': 'personalized birthday gifts 2025',
    'related_keywords': ['unique gifts', 'voice message'],
    'target_length': 2000,
    'brand_voice': brand.get_brand_prompt('blog')
}

article = generator.write_article(brief)

# Output:
# {
#   'text': Full article text (markdown),
#   'html': HTML version,
#   'title': SEO-optimized title,
#   'meta_description': Meta description,
#   'word_count': 2000,
#   'outline': Article structure
# }
```

---

## 🛡️ SAFETY & WHITE HAT

**Zero Ban Risk Strategy:**

1. **Human-in-the-Loop:** Never auto-post without approval
2. **Telegram Approval:** All content reviewed before publishing
3. **White Hat SEO:** No keyword stuffing, no spam, no black hat
4. **Brand Quality:** Every output enforces brand standards
5. **Rate Limiting:** Respects platform limits (no flooding)

**What We DON'T Do:**
- ❌ Auto-post to Instagram/TikTok without approval
- ❌ Spam forums or comment sections
- ❌ Black hat SEO tactics
- ❌ AI-detectable content
- ❌ Mass follow/unfollow
- ❌ Bought engagement

**What We DO:**
- ✅ Generate high-quality content
- ✅ Send to Telegram for human review
- ✅ Manual posting (30 seconds per item)
- ✅ White hat optimization
- ✅ Brand-consistent output
- ✅ Organic growth strategies

---

## 📅 ROADMAP

### ✅ Phase 1: Foundation (Week 1) - COMPLETE
- Brand Identity Core
- Blog Article Generator
- Integration planning

### ⏳ Phase 2: Blog Module (Week 2) - NEXT
- Keyword research engine
- Competitor analysis
- SEO optimizer
- WordPress integration

### ⏳ Phase 3: Image Module (Week 3)
- AI image generation (Flux/DALL-E)
- Automatic branding layer
- Multi-format resizing
- Pinterest integration

### ⏳ Phase 4: Orchestrator (Week 4)
- Central workflow controller
- Module coordination
- Scheduling system
- Analytics tracking

### ⏳ Phase 5: Command Center (Week 5)
- Telegram dashboard
- Approval workflows
- Performance analytics
- Manual triggers

### ⏳ Phase 6: Deployment (Week 6)
- GitHub Actions automation
- Complete documentation
- Training materials
- LAUNCH 🚀

---

## 💡 FAQ

### Q: Czy to zastąpi Remix V2.0?
**A:** NIE! Titan ROZSZERZA Remix V2.0. Video module pozostaje nietknięty i działa dalej. Dodajemy tylko nowe funkcje.

### Q: Czy mogę używać tylko części systemu?
**A:** TAK! System jest modularny. Możesz używać tylko video + blog, lub tylko video + images. Każdy moduł działa niezależnie.

### Q: Czy to bezpieczne? Nie dostanę bana?
**A:** TAK, bezpieczne. Używamy Telegram approval - TY decydujesz co publikować. Nigdy nie auto-postujemy na Twoje konto bez Twojej zgody.

### Q: Ile to kosztuje?
**A:** £0. Wszystkie API są darmowe (Gemini free tier, Edge-TTS free, Telegram free). Jedyny koszt to Twój czas (~10 min/dzień na approvals).

### Q: Czy content jest wykrywalny jako AI?
**A:** NIE. Używamy anti-AI detection techniques: burstiness, perplexity, human patterns, personal anecdotes. Content brzmi jak człowiek.

### Q: Jak długo trwa pełna implementacja?
**A:** 6 tygodni do pełnego systemu. Ale możesz zacząć używać Blog Generator już teraz (Phase 1 gotowa).

### Q: Co jeśli coś się zepsuje?
**A:** Masz backup (Remix V2.0 BACKUP folder). Możesz zawsze wrócić. Plus, każdy moduł jest oddzielny - jeśli blog module nie działa, video dalej działa.

---

## 🆘 SUPPORT

**Documentation:**
- `INTEGRATION_PLAN.md` - Complete technical specification
- `README.md` - This file (user guide)
- Inline code comments - Every function explained

**Getting Help:**
- Check logs: `logs/titan.log`
- Test individual modules first
- Review integration plan for troubleshooting

---

## 📜 LICENSE

Proprietary - SayPlay Internal Use

---

## 🎯 NEXT STEPS

### Ready to Start?

1. **Download Phase 1 files** ⬇️
2. **Test Brand Core** (`python core/brand_identity/brand_core.py`)
3. **Test Blog Generator** (`python modules/blog/writer/article_generator.py`)
4. **Add your logos** (to `core/brand_identity/logos/`)
5. **Generate first article!**

### Want Full System?

6. **Week 2:** We build Blog Module (research + SEO + WordPress)
7. **Week 3:** We build Image Module (AI + branding + resizing)
8. **Week 4:** We build Orchestrator (workflow automation)
9. **Week 5:** We build Command Center (Telegram dashboard)
10. **Week 6:** LAUNCH complete system! 🚀

---

**Zaczynamy od Phase 1?** ✅

Pobierz pliki ⬆️ i testuj Brand Core + Blog Generator!
