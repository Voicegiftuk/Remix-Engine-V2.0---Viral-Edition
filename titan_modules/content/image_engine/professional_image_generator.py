"""
PROFESSIONAL IMAGE GENERATOR
- Multiple APIs (Unsplash, Pexels, Pixabay)
- Auto-overlay SayPlay logo
- Multiple sizes for different platforms
- Professional design
"""
import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
from typing import Dict, List, Optional
from pathlib import Path
import time


class ProfessionalImageGenerator:
    """
    Generate professional images with SayPlay branding
    """
    
    def __init__(self):
        self.unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        self.pexels_key = os.getenv('PEXELS_API_KEY', '')
        self.pixabay_key = os.getenv('PIXABAY_API_KEY', '')
        
        # Image specifications for different purposes
        self.image_specs = {
            'hero': {'width': 1200, 'height': 630, 'purpose': 'Blog header'},
            'instagram': {'width': 1080, 'height': 1080, 'purpose': 'Instagram post'},
            'pinterest': {'width': 1000, 'height': 1500, 'purpose': 'Pinterest pin'},
            'youtube': {'width': 1920, 'height': 1080, 'purpose': 'YouTube thumbnail'},
            'podcast': {'width': 3000, 'height': 3000, 'purpose': 'Podcast cover'}
        }
        
        print(f"Image Generator initialized")
        if self.unsplash_key:
            print("  ✅ Unsplash API configured")
        if self.pexels_key:
            print("  ✅ Pexels API configured")
        if self.pixabay_key:
            print("  ✅ Pixabay API configured")
    
    def generate_image_set(self, keyword: str, article_title: str) -> Dict[str, bytes]:
        """
        Generate complete set of images for one article
        Returns dict with all image types
        """
        images = {}
        
        # Generate different search queries for variety
        queries = self._generate_queries(keyword)
        
        for img_type, spec in self.image_specs.items():
            print(f"  Generating {img_type} image ({spec['width']}x{spec['height']})...")
            
            # Try to fetch base image
            base_image = self._fetch_image(queries[0], spec['width'], spec['height'])
            
            if base_image:
                # Add SayPlay branding
                branded_image = self._add_branding(
                    base_image, 
                    img_type,
                    article_title if img_type == 'hero' else None
                )
                
                images[img_type] = branded_image
                print(f"    ✅ {img_type} created")
            else:
                print(f"    ⚠️ {img_type} failed")
            
            time.sleep(1)
        
        return images
    
    def _generate_queries(self, keyword: str) -> List[str]:
        """Generate diverse search queries"""
        base = keyword.lower().replace('gifts', '').strip()
        
        return [
            f"{keyword} elegant lifestyle",
            f"{base} modern minimalist",
            f"{keyword} professional photography",
            f"{base} beautiful composition",
            f"{keyword} premium quality"
        ]
    
    def _fetch_image(self, query: str, width: int, height: int) -> Optional[Image.Image]:
        """Fetch image from available APIs"""
        
        # Try Unsplash first (best quality)
        if self.unsplash_key:
            img = self._fetch_unsplash(query, width, height)
            if img:
                return img
        
        # Try Pexels
        if self.pexels_key:
            img = self._fetch_pexels(query, width, height)
            if img:
                return img
        
        # Try Pixabay
        if self.pixabay_key:
            img = self._fetch_pixabay(query, width, height)
            if img:
                return img
        
        return None
    
    def _fetch_unsplash(self, query: str, width: int, height: int) -> Optional[Image.Image]:
        """Fetch from Unsplash"""
        try:
            url = "https://api.unsplash.com/photos/random"
            params = {
                'query': query,
                'orientation': 'landscape' if width > height else 'portrait',
                'client_id': self.unsplash_key
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['raw'] + f"&w={width}&h={height}&fit=crop"
                
                img_response = requests.get(image_url, timeout=20)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content))
        except Exception as e:
            print(f"      Unsplash error: {str(e)[:50]}")
        
        return None
    
    def _fetch_pexels(self, query: str, width: int, height: int) -> Optional[Image.Image]:
        """Fetch from Pexels"""
        try:
            url = "https://api.pexels.com/v1/search"
            headers = {'Authorization': self.pexels_key}
            params = {
                'query': query,
                'per_page': 1,
                'orientation': 'landscape' if width > height else 'portrait'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    image_url = data['photos'][0]['src']['large2x']
                    
                    img_response = requests.get(image_url, timeout=20)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        return img.resize((width, height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"      Pexels error: {str(e)[:50]}")
        
        return None
    
    def _fetch_pixabay(self, query: str, width: int, height: int) -> Optional[Image.Image]:
        """Fetch from Pixabay"""
        try:
            url = "https://pixabay.com/api/"
            params = {
                'key': self.pixabay_key,
                'q': query,
                'image_type': 'photo',
                'per_page': 3
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data['hits']:
                    image_url = data['hits'][0]['largeImageURL']
                    
                    img_response = requests.get(image_url, timeout=20)
                    if img_response.status_code == 200:
                        img = Image.open(BytesIO(img_response.content))
                        return img.resize((width, height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"      Pixabay error: {str(e)[:50]}")
        
        return None
    
    def _add_branding(self, img: Image.Image, img_type: str, title: Optional[str] = None) -> bytes:
        """
        Add SayPlay branding to image
        Different styles for different image types
        """
        # Create a copy to work with
        img = img.copy()
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        if img_type == 'hero':
            # Hero: Logo bottom right + optional title overlay
            img = self._add_hero_branding(img, title)
        
        elif img_type == 'instagram':
            # Instagram: Centered logo watermark
            img = self._add_instagram_branding(img)
        
        elif img_type == 'pinterest':
            # Pinterest: Top text + bottom CTA
            img = self._add_pinterest_branding(img, title)
        
        elif img_type == 'youtube':
            # YouTube: Bold text overlay
            img = self._add_youtube_branding(img, title)
        
        elif img_type == 'podcast':
            # Podcast: Full branded cover
            img = self._add_podcast_branding(img, title)
        
        # Convert to bytes
        output = BytesIO()
        img.save(output, format='JPEG', quality=95, optimize=True)
        return output.getvalue()
    
    def _add_hero_branding(self, img: Image.Image, title: Optional[str]) -> Image.Image:
        """Add branding for hero image"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Add semi-transparent overlay at bottom
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Dark gradient at bottom
        for y in range(int(height * 0.7), height):
            alpha = int(180 * (y - height * 0.7) / (height * 0.3))
            overlay_draw.rectangle([(0, y), (width, y+1)], fill=(0, 0, 0, alpha))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Add "SayPlay" logo text bottom right
        try:
            # Try to load a nice font
            logo_size = int(height * 0.08)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            font = ImageFont.load_default()
        
        logo_text = "SayPlay"
        bbox = draw.textbbox((0, 0), logo_text, font=font)
        logo_width = bbox[2] - bbox[0]
        
        # Position bottom right with padding
        logo_x = width - logo_width - int(width * 0.05)
        logo_y = height - int(height * 0.12)
        
        # Draw with gradient effect (Say in purple, Play in gold)
        draw.text((logo_x, logo_y), "Say", fill=(102, 126, 234), font=font)
        say_width = draw.textbbox((0, 0), "Say", font=font)[2]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        return img
    
    def _add_instagram_branding(self, img: Image.Image) -> Image.Image:
        """Add watermark for Instagram"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Centered semi-transparent logo
        try:
            logo_size = int(height * 0.06)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            font = ImageFont.load_default()
        
        logo_text = "SayPlay"
        bbox = draw.textbbox((0, 0), logo_text, font=font)
        logo_width = bbox[2] - bbox[0]
        
        logo_x = (width - logo_width) // 2
        logo_y = int(height * 0.05)
        
        # Add semi-transparent background
        padding = 20
        bg_coords = [
            (logo_x - padding, logo_y - padding),
            (logo_x + logo_width + padding, logo_y + logo_size + padding)
        ]
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(bg_coords, fill=(255, 255, 255, 200))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Draw logo
        draw.text((logo_x, logo_y), "Say", fill=(102, 126, 234), font=font)
        say_width = draw.textbbox((0, 0), "Say", font=font)[2]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        return img
    
    def _add_pinterest_branding(self, img: Image.Image, title: Optional[str]) -> Image.Image:
        """Add branding for Pinterest pin"""
        # Similar to hero but optimized for Pinterest's tall format
        return self._add_hero_branding(img, title)
    
    def _add_youtube_branding(self, img: Image.Image, title: Optional[str]) -> Image.Image:
        """Add branding for YouTube thumbnail"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Bold text overlay with title
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Dark background for text
        overlay_draw.rectangle([(0, int(height * 0.3)), (width, int(height * 0.7))], 
                              fill=(0, 0, 0, 180))
        
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Add SayPlay logo
        try:
            logo_size = int(height * 0.12)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
        except:
            font = ImageFont.load_default()
        
        logo_y = int(height * 0.45)
        draw.text((int(width * 0.1), logo_y), "Say", fill=(102, 126, 234), font=font)
        say_width = draw.textbbox((0, 0), "Say", font=font)[2]
        draw.text((int(width * 0.1) + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        return img
    
    def _add_podcast_branding(self, img: Image.Image, title: Optional[str]) -> Image.Image:
        """Create podcast cover art"""
        # For podcast, create a heavily branded cover
        overlay = Image.new('RGBA', img.size, (102, 126, 234, 200))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Large centered SayPlay logo
        try:
            logo_size = int(height * 0.2)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", logo_size)
            
            subtitle_size = int(height * 0.08)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", subtitle_size)
        except:
            font = ImageFont.load_default()
            subtitle_font = font
        
        # Center logo
        logo_text = "SayPlay"
        bbox = draw.textbbox((0, 0), logo_text, font=font)
        logo_width = bbox[2] - bbox[0]
        
        logo_x = (width - logo_width) // 2
        logo_y = int(height * 0.35)
        
        draw.text((logo_x, logo_y), "Say", fill=(255, 255, 255), font=font)
        say_width = draw.textbbox((0, 0), "Say", font=font)[2]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=font)
        
        # Add "PODCAST" subtitle
        subtitle = "GIFT GUIDE PODCAST"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        subtitle_y = logo_y + logo_size + 40
        
        draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 255, 255), font=subtitle_font)
        
        return img
    
    def create_podcast_cover_master(self) -> bytes:
        """
        Create master podcast cover for the show
        Used once for Spotify for Podcasters setup
        """
        # Create gradient background
        img = Image.new('RGB', (3000, 3000), (102, 126, 234))
        
        # Add gradient
        for y in range(3000):
            r = int(102 + (118 - 102) * y / 3000)
            g = int(126 + (75 - 126) * y / 3000)
            b = int(234 + (162 - 234) * y / 3000)
            
            for x in range(3000):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Add main branding
        try:
            logo_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 400)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 150)
            tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 100)
        except:
            logo_font = ImageFont.load_default()
            subtitle_font = logo_font
            tagline_font = logo_font
        
        # Center "SayPlay"
        logo_text = "SayPlay"
        bbox = draw.textbbox((0, 0), logo_text, font=logo_font)
        logo_width = bbox[2] - bbox[0]
        
        logo_x = (3000 - logo_width) // 2
        logo_y = 900
        
        draw.text((logo_x, logo_y), "Say", fill=(255, 255, 255), font=logo_font)
        say_width = draw.textbbox((0, 0), "Say", font=logo_font)[2]
        draw.text((logo_x + say_width, logo_y), "Play", fill=(255, 215, 0), font=logo_font)
        
        # Subtitle
        subtitle = "GIFT GUIDE"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (3000 - subtitle_width) // 2
        draw.text((subtitle_x, 1500), subtitle, fill=(255, 255, 255), font=subtitle_font)
        
        # Tagline
        tagline = "Your Daily Inspiration for Perfect Gifts"
        bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
        tagline_width = bbox[2] - bbox[0]
        tagline_x = (3000 - tagline_width) // 2
        draw.text((tagline_x, 1750), tagline, fill=(255, 255, 255), font=tagline_font)
        
        # Save
        output = BytesIO()
        img.save(output, format='JPEG', quality=95)
        return output.getvalue()
