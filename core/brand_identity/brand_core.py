#!/usr/bin/env python3
"""
Brand Identity Core - PROJECT TITAN
Centralne zarządzanie zasobami marki SayPlay

Purpose:
- Logo management (all variants)
- Color palette enforcement
- Brand voice validation
- Typography standards
"""
from pathlib import Path
from typing import Dict, List, Optional
import json
from PIL import Image, ImageDraw, ImageFont
from loguru import logger


class BrandIdentityCore:
    """
    Centralny system zarządzania tożsamością marki SayPlay
    
    Wszystkie moduły (video, blog, image, email) muszą przejść przez ten system
    aby zapewnić spójność brandingu
    """
    
    def __init__(self, brand_dir: Path = None):
        """
        Initialize brand identity system
        
        Args:
            brand_dir: Path to brand assets directory
        """
        if brand_dir is None:
            brand_dir = Path(__file__).parent
        
        self.brand_dir = brand_dir
        self.logos_dir = brand_dir / 'logos'
        self.colors_file = brand_dir / 'colors.json'
        self.voice_file = brand_dir / 'voice.json'
        
        # Load brand configuration
        self.colors = self._load_colors()
        self.voice = self._load_voice()
        
        logger.info("BrandIdentityCore initialized")
    
    def _load_colors(self) -> Dict:
        """Load brand color palette"""
        if self.colors_file.exists():
            with open(self.colors_file) as f:
                return json.load(f)
        
        # Default SayPlay colors
        return {
            "primary": {
                "orange": "#FF6B35",
                "hex": "#FF6B35",
                "rgb": [255, 107, 53]
            },
            "secondary": {
                "dark": "#2C3E50",
                "light": "#ECF0F1"
            },
            "accent": {
                "gold": "#F39C12",
                "red": "#E74C3C"
            },
            "social": {
                "instagram": "#E4405F",
                "tiktok": "#000000",
                "pinterest": "#E60023"
            }
        }
    
    def _load_voice(self) -> Dict:
        """Load brand voice configuration"""
        if self.voice_file.exists():
            with open(self.voice_file) as f:
                return json.load(f)
        
        # Default SayPlay brand voice
        return {
            "personality": {
                "traits": ["warm", "personal", "emotional", "trustworthy"],
                "avoid": ["corporate", "salesy", "aggressive", "robotic"]
            },
            "tone": {
                "empathetic": True,
                "conversational": True,
                "inspiring": True,
                "professional": False  # We're personal, not corporate
            },
            "voice_patterns": [
                "We believe memories matter",
                "Create moments that last",
                "Your voice, their heart",
                "Make every gift personal",
                "Hear the love in every tap"
            ],
            "writing_style": {
                "sentence_length": "varied",  # Short and long mixed
                "use_contractions": True,     # "We're" not "We are"
                "use_emojis": "sparingly",    # 1-2 per post max
                "storytelling": True,         # Use anecdotes
                "active_voice": True          # "You tap" not "it is tapped"
            },
            "keywords": {
                "primary": ["voice message", "personal", "memory", "gift"],
                "emotional": ["love", "connection", "heart", "meaningful"],
                "product": ["NFC", "tap", "card", "sticker"]
            }
        }
    
    def get_logo(self, variant: str = "primary", size: tuple = None) -> Optional[Path]:
        """
        Get logo file path
        
        Args:
            variant: Logo variant (primary, white, black, icon, watermark)
            size: Optional resize (width, height)
        
        Returns:
            Path to logo file or None if not found
        """
        logo_files = {
            "primary": "sayplay_logo_primary.png",
            "white": "sayplay_logo_white.png",
            "black": "sayplay_logo_black.png",
            "icon": "sayplay_icon.png",
            "watermark": "sayplay_watermark.png"
        }
        
        logo_path = self.logos_dir / logo_files.get(variant, logo_files["primary"])
        
        if not logo_path.exists():
            logger.warning(f"Logo not found: {logo_path}")
            return None
        
        # TODO: If size specified, resize logo
        # For now, return original
        return logo_path
    
    def apply_watermark(
        self,
        image_path: Path,
        output_path: Path,
        position: str = "bottom-right",
        opacity: float = 0.7,
        scale: float = 0.15
    ) -> Path:
        """
        Apply SayPlay watermark to image
        
        Args:
            image_path: Input image
            output_path: Where to save watermarked image
            position: Where to place logo (bottom-right, top-left, etc.)
            opacity: Logo transparency (0.0-1.0)
            scale: Logo size relative to image (0.1-0.3)
        
        Returns:
            Path to watermarked image
        """
        try:
            # Load base image
            base = Image.open(image_path).convert('RGBA')
            base_width, base_height = base.size
            
            # Load watermark
            watermark_path = self.get_logo('watermark')
            if not watermark_path:
                logger.error("Watermark logo not found")
                return image_path
            
            watermark = Image.open(watermark_path).convert('RGBA')
            
            # Resize watermark
            wm_width = int(base_width * scale)
            wm_height = int(watermark.height * (wm_width / watermark.width))
            watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
            
            # Adjust opacity
            watermark_alpha = watermark.split()[3]
            watermark_alpha = watermark_alpha.point(lambda p: int(p * opacity))
            watermark.putalpha(watermark_alpha)
            
            # Calculate position
            positions = {
                "bottom-right": (base_width - wm_width - 20, base_height - wm_height - 20),
                "bottom-left": (20, base_height - wm_height - 20),
                "top-right": (base_width - wm_width - 20, 20),
                "top-left": (20, 20),
                "center": ((base_width - wm_width) // 2, (base_height - wm_height) // 2)
            }
            
            pos = positions.get(position, positions["bottom-right"])
            
            # Paste watermark
            base.paste(watermark, pos, watermark)
            
            # Save
            base.convert('RGB').save(output_path, quality=95)
            
            logger.success(f"✓ Watermark applied: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Watermark failed: {e}")
            return image_path
    
    def get_color(self, color_name: str, format: str = "hex") -> str:
        """
        Get brand color
        
        Args:
            color_name: Color name (primary, secondary, etc.)
            format: Output format (hex, rgb)
        
        Returns:
            Color value in requested format
        """
        # Navigate nested dict
        parts = color_name.split('.')
        color = self.colors
        
        for part in parts:
            color = color.get(part, {})
        
        if format == "hex":
            return color.get("hex", color.get("orange", "#FF6B35"))
        elif format == "rgb":
            return tuple(color.get("rgb", [255, 107, 53]))
        
        return str(color)
    
    def validate_brand_voice(self, text: str) -> Dict:
        """
        Validate if text matches SayPlay brand voice
        
        Args:
            text: Text to validate
        
        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "score": 0.0,
            "issues": [],
            "suggestions": []
        }
        
        text_lower = text.lower()
        
        # Check for avoided words/phrases
        avoid = self.voice["personality"]["avoid"]
        for word in avoid:
            if word in text_lower:
                results["issues"].append(f"Avoid '{word}' - too {word}")
                results["score"] -= 10
        
        # Check for brand keywords
        keywords = self.voice["keywords"]["primary"]
        keyword_count = sum(1 for kw in keywords if kw in text_lower)
        results["score"] += keyword_count * 5
        
        # Check for emotional words
        emotional = self.voice["keywords"]["emotional"]
        emotional_count = sum(1 for ew in emotional if ew in text_lower)
        results["score"] += emotional_count * 3
        
        # Check writing style
        if self.voice["writing_style"]["use_contractions"]:
            # Count contractions vs formal
            contractions = ["we're", "you're", "it's", "that's", "here's"]
            has_contractions = any(c in text_lower for c in contractions)
            if not has_contractions and len(text.split()) > 10:
                results["suggestions"].append("Use contractions for conversational tone")
                results["score"] -= 5
        
        # Final score
        results["score"] = max(0, min(100, results["score"] + 50))  # Normalize to 0-100
        results["valid"] = results["score"] >= 60
        
        return results
    
    def get_brand_prompt(self, content_type: str = "general") -> str:
        """
        Get AI prompt that enforces brand voice
        
        Args:
            content_type: Type of content (blog, social, email)
        
        Returns:
            System prompt for AI
        """
        base_prompt = f"""You are writing for SayPlay - a brand that creates personalized voice message gifts using NFC technology.

BRAND PERSONALITY:
- Warm and personal (not corporate)
- Emotional and heartfelt (we care about memories)
- Trustworthy and authentic (real connections matter)

VOICE PATTERNS:
{chr(10).join('- ' + p for p in self.voice['voice_patterns'])}

WRITING STYLE:
- Use contractions (we're, you're, it's)
- Mix short and long sentences (natural rhythm)
- Tell stories and use examples
- Active voice ("you tap" not "it is tapped")
- Use emojis sparingly (1-2 max)

KEYWORDS TO INCLUDE:
Primary: {', '.join(self.voice['keywords']['primary'])}
Emotional: {', '.join(self.voice['keywords']['emotional'])}

AVOID:
- Corporate jargon
- Aggressive sales language
- Robotic phrasing
- Being too formal
"""
        
        if content_type == "blog":
            base_prompt += "\nFORMAT: Write in a conversational blog style with personal anecdotes."
        elif content_type == "social":
            base_prompt += "\nFORMAT: Short, punchy, scroll-stopping content."
        elif content_type == "email":
            base_prompt += "\nFORMAT: Friendly email as if from a friend, not a company."
        
        return base_prompt


# Singleton instance
_brand_core = None

def get_brand_core() -> BrandIdentityCore:
    """Get global brand core instance"""
    global _brand_core
    if _brand_core is None:
        _brand_core = BrandIdentityCore()
    return _brand_core


if __name__ == "__main__":
    """Test brand core"""
    print("🎨 Testing Brand Identity Core...")
    
    brand = BrandIdentityCore()
    
    # Test colors
    print(f"\n📊 Primary Color: {brand.get_color('primary.orange')}")
    print(f"Instagram Color: {brand.get_color('social.instagram')}")
    
    # Test brand voice validation
    print("\n✍️ Testing Brand Voice...")
    
    good_text = "We believe every gift should be personal. That's why we created SayPlay - tap to hear their voice and feel the love."
    bad_text = "Our corporate solution leverages NFC technology to facilitate voice message transmission for enhanced gift personalization."
    
    good_result = brand.validate_brand_voice(good_text)
    bad_result = brand.validate_brand_voice(bad_text)
    
    print(f"\nGood Text Score: {good_result['score']}/100 - Valid: {good_result['valid']}")
    print(f"Bad Text Score: {bad_result['score']}/100 - Valid: {bad_result['valid']}")
    print(f"Issues: {bad_result['issues']}")
    
    # Test brand prompt
    print("\n🤖 Brand Prompt for AI:")
    print(brand.get_brand_prompt('blog')[:200] + "...")
    
    print("\n✅ Brand Core tests complete!")
