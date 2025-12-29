#!/usr/bin/env python3
"""
TITAN MODULE #4: IMAGE ENGINE (ZERO-COST VERSION)
Uses Pollinations.ai - completely free, no API key needed!
"""
import os
import sys
import requests
from typing import Dict, List, Optional
from pathlib import Path
from io import BytesIO
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"🎨 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class ImageEngine:
    """AI image generation using FREE Pollinations.ai"""
    
    # Platform specifications
    PLATFORM_SIZES = {
        'pinterest': (1000, 1500),
        'instagram_post': (1080, 1080),
        'instagram_story': (1080, 1920),
        'facebook_post': (1200, 630),
        'facebook_story': (1080, 1920),
        'linkedin_post': (1200, 627),
        'twitter_post': (1200, 675),
        'blog_thumbnail': (1200, 630)
    }
    
    def __init__(self):
        """Initialize zero-cost image engine"""
        logger.info("Image Engine initialized (Zero-Cost Mode)")
        logger.info("Using Pollinations.ai - FREE unlimited generations!")
    
    def generate_lifestyle_photo(
        self, 
        prompt: str, 
        style: str = 'photographic',
        width: int = 1024,
        height: int = 1024
    ) -> Optional[bytes]:
        """
        Generate lifestyle photo using Pollinations.ai
        
        COMPLETELY FREE - No API key needed!
        """
        
        logger.info(f"Generating: {prompt[:50]}...")
        
        try:
            # Enhance prompt for better results
            enhanced_prompt = self._enhance_prompt(prompt, style)
            
            # Pollinations.ai endpoint (FREE!)
            # Format: https://image.pollinations.ai/prompt/{your_prompt}?width={w}&height={h}
            
            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            params = {
                'width': width,
                'height': height,
                'nologo': 'true',  # Remove Pollinations watermark
                'enhance': 'true'   # Better quality
            }
            
            # Generate image
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                image_bytes = response.content
                logger.success(f"Generated {len(image_bytes)} bytes")
                return image_bytes
            else:
                logger.error(f"Generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return None
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt for better results"""
        
        style_modifiers = {
            'photographic': 'professional photography, high quality, sharp focus, natural lighting',
            'artistic': 'artistic, creative, beautiful composition',
            'modern': 'modern, clean, minimalist aesthetic',
            'lifestyle': 'lifestyle photography, authentic, warm, inviting'
        }
        
        modifier = style_modifiers.get(style, style_modifiers['photographic'])
        
        enhanced = f"{prompt}, {modifier}, 8k resolution, detailed"
        
        return enhanced
    
    def auto_crop_for_platform(
        self, 
        image_bytes: bytes, 
        platform: str
    ) -> Optional[bytes]:
        """Smart crop image for specific platform"""
        
        if platform not in self.PLATFORM_SIZES:
            logger.error(f"Unknown platform: {platform}")
            return None
        
        target_width, target_height = self.PLATFORM_SIZES[platform]
        
        try:
            # Open image
            img = Image.open(BytesIO(image_bytes))
            
            # Get current dimensions
            current_width, current_height = img.size
            
            # Calculate aspect ratios
            current_aspect = current_width / current_height
            target_aspect = target_width / target_height
            
            # Smart crop to target aspect ratio
            if current_aspect > target_aspect:
                # Image is wider - crop width
                new_width = int(current_height * target_aspect)
                left = (current_width - new_width) // 2
                img = img.crop((left, 0, left + new_width, current_height))
            else:
                # Image is taller - crop height
                new_height = int(current_width / target_aspect)
                top = (current_height - new_height) // 2
                img = img.crop((0, top, current_width, top + new_height))
            
            # Resize to exact target size
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Add watermark
            img = self._add_watermark(img)
            
            # Convert back to bytes
            output = BytesIO()
            img.save(output, format='PNG', quality=95)
            
            logger.info(f"Cropped to {target_width}x{target_height} for {platform}")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Crop error: {e}")
            return None
    
    def _add_watermark(self, img: Image.Image) -> Image.Image:
        """Add SayPlay watermark to image"""
        
        try:
            from PIL import ImageDraw, ImageFont
            
            # Create drawing context
            draw = ImageDraw.Draw(img)
            
            # Watermark text
            watermark_text = "SayPlay™"
            
            # Position (bottom-right with padding)
            padding = 20
            
            # Try to use a nice font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Get text size
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            x = img.width - text_width - padding
            y = img.height - text_height - padding
            
            # Draw text with shadow for visibility
            # Shadow
            draw.text((x+2, y+2), watermark_text, fill=(0, 0, 0, 128), font=font)
            # Main text
            draw.text((x, y), watermark_text, fill=(255, 255, 255, 200), font=font)
            
            return img
            
        except Exception as e:
            logger.warning(f"Watermark failed: {e}")
            return img
    
    def batch_generate_all_platforms(self, prompt: str) -> Dict[str, bytes]:
        """
        Generate images for ALL platforms at once
        
        ZERO COST! 🎉
        """
        
        logger.info(f"Batch generating for {len(self.PLATFORM_SIZES)} platforms")
        
        results = {}
        
        # Generate base image (1024x1024)
        base_image = self.generate_lifestyle_photo(prompt, style='lifestyle')
        
        if not base_image:
            logger.error("Base image generation failed")
            return results
        
        # Crop for each platform
        for platform in self.PLATFORM_SIZES.keys():
            cropped = self.auto_crop_for_platform(base_image, platform)
            if cropped:
                results[platform] = cropped
        
        logger.success(f"Generated {len(results)} platform variants")
        return results
    
    def save_image(self, image_bytes: bytes, filename: str):
        """Save image to file"""
        
        try:
            with open(filename, 'wb') as f:
                f.write(image_bytes)
            logger.success(f"Saved: {filename}")
        except Exception as e:
            logger.error(f"Save failed: {e}")


if __name__ == "__main__":
    """Test zero-cost image engine"""
    
    print("\n🧪 Testing ZERO-COST Image Engine...\n")
    
    engine = ImageEngine()
    
    # Test 1: Generate single image
    print("Test 1: Generate lifestyle photo")
    prompt = "person holding beautiful greeting card, smiling, cozy home interior, warm lighting"
    image = engine.generate_lifestyle_photo(prompt)
    
    if image:
        print(f"✓ Generated {len(image):,} bytes")
        engine.save_image(image, 'test_base.png')
    
    # Test 2: Batch generate all platforms
    print("\nTest 2: Generate all platform variants")
    all_images = engine.batch_generate_all_platforms(prompt)
    
    print(f"✓ Generated {len(all_images)} variants:")
    for platform, img_bytes in all_images.items():
        print(f"  • {platform}: {len(img_bytes):,} bytes")
        engine.save_image(img_bytes, f'test_{platform}.png')
    
    print("\n✅ Zero-cost image engine test complete!")
    print("💰 Cost: £0.00")
    print("🎉 Unlimited generations!")
