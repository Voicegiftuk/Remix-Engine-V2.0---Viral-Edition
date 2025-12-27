# OVERLAY GRAPHICS

Place your overlay graphics here (sticker, play button, etc.)

## Required Files

### 1. sticker.png
- **Purpose**: NFC sticker graphic to overlay on product mockups
- **Size**: 200x200px recommended
- **Format**: PNG with transparency
- **Design**: Your actual NFC sticker design

### 2. play_button.png (Optional)
- **Purpose**: Play button for mockups
- **Size**: 200x200px recommended
- **Format**: PNG with transparency
- **Note**: If not provided, system will generate one automatically

## Creating Your Sticker Graphic

### Option 1: Use Actual Photo
1. Photograph your NFC sticker on white background
2. Remove background (use remove.bg or Photoshop)
3. Resize to 200x200px
4. Save as PNG with transparency
5. Name as: `sticker.png`

### Option 2: Design in Canva
1. Go to canva.com
2. Create 200x200px design
3. Add your SayPlay branding
4. Add NFC chip icon (from Canva elements)
5. Download as PNG (transparent background)
6. Save as: `sticker.png`

### Option 3: Figma/Photoshop
1. Create 200x200px artboard
2. Design circular sticker
3. Include: SayPlay logo, NFC icon, "Tap to Play"
4. Export PNG with transparency
5. Save as: `sticker.png`

## Design Guidelines

### Sticker Design Best Practices
- **Shape**: Circular or rounded square
- **Colors**: Match SayPlay brand (use your colors)
- **Icons**: NFC symbol, audio/voice icon
- **Text**: "Tap to Play", "Just Tap, No App"
- **Size**: Clear and readable at small sizes

### Example Sticker Elements
```
┌─────────────┐
│   SayPlay   │  ← Brand name
│             │
│    [NFC]    │  ← NFC icon
│   🎙️ TAP    │  ← Voice icon + action
│             │
│   to PLAY   │  ← Call to action
└─────────────┘
```

## Play Button (Optional)

If you want custom play button:

### Design Specs
- 200x200px PNG
- Circular shape
- White background with opacity
- Black/dark play triangle
- Subtle shadow for depth

### Or Use Auto-Generated
The system automatically generates a play button if `play_button.png` is not found. It creates:
- White circular background
- Black play triangle
- Professional appearance

## Free Design Resources

### Icons
- **Flaticon**: flaticon.com (NFC icons)
- **Noun Project**: thenounproject.com (audio icons)
- **Material Icons**: fonts.google.com/icons

### Colors
Use your brand colors, or SayPlay suggestions:
- Primary: #4A90E2 (blue)
- Secondary: #50C878 (green)
- Accent: #FF6B6B (red/pink)

## File Checklist

```bash
# Check which files exist
ls -la *.png
```

Required:
- [ ] sticker.png (your NFC sticker design)

Optional:
- [ ] play_button.png (custom play button)
- [ ] logo.png (additional branding)

## Quick Start

**Don't have graphics yet?**

1. Start without `sticker.png` - mockups will work without it
2. Add it later when ready - just drop in this folder
3. System will automatically use it in next generation

**Need help designing?**

Contact a designer on:
- Fiverr (£5-£20 for simple sticker design)
- Upwork
- 99designs

Or use Canva free tier and design it yourself in 15 minutes!

## Current Status

```bash
# Check overlay files
ls -1 *.png 2>/dev/null | wc -l
```

**Recommended**: 1-2 files
**Current**: 0 files
