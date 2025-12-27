#!/usr/bin/env python3
"""
Pro Overlay Engine - V2.0 VIRAL EDITION
Generates professional-looking text overlays using HTML/CSS rendering
Superior to basic MoviePy TextClip - enables gradients, shadows, strokes, emojis
"""
import sys
from pathlib import Path
from typing import Optional, Tuple
import random

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from html2image import Html2Image
from loguru import logger

# Configure logging
logger.add(
    "logs/overlay_engine.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class ProOverlayEngine:
    """Professional HTML/CSS overlay generator for viral aesthetics"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.temp_dir = self.base_dir / 'assets/temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize HTML2Image
        self.hti = Html2Image(
            output_path=str(self.temp_dir),
            size=(1080, 1920)  # 9:16 vertical format
        )
        
        logger.info("ProOverlayEngine initialized")
    
    def create_hook_overlay(
        self,
        text: str,
        style: str = "tiktok",
        position: str = "top",
        output_name: Optional[str] = None
    ) -> Path:
        """
        Create professional text overlay for video hook
        
        Args:
            text: Hook text (max 8 words recommended)
            style: Visual style (tiktok, instagram, youtube, minimal)
            position: Text position (top, center, bottom)
            output_name: Custom output filename (auto-generated if None)
        
        Returns:
            Path to generated PNG overlay
        """
        if output_name is None:
            output_name = f"overlay_hook_{random.randint(1000, 9999)}.png"
        
        # Get style configuration
        style_config = self._get_style_config(style)
        position_css = self._get_position_css(position)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    width: 1080px;
                    height: 1920px;
                    display: flex;
                    align-items: {position_css['align']};
                    justify-content: center;
                }}
                
                .text-container {{
                    width: 90%;
                    text-align: center;
                    margin-top: {position_css['margin_top']};
                    margin-bottom: {position_css['margin_bottom']};
                }}
                
                .hook-text {{
                    font-family: {style_config['font_family']};
                    font-weight: {style_config['font_weight']};
                    font-size: {style_config['font_size']};
                    color: {style_config['color']};
                    text-transform: {style_config['text_transform']};
                    line-height: {style_config['line_height']};
                    
                    /* Stroke effect */
                    -webkit-text-stroke: {style_config['stroke_width']} {style_config['stroke_color']};
                    paint-order: stroke fill;
                    
                    /* Shadow for depth */
                    text-shadow: {style_config['text_shadow']};
                    
                    /* Animation-ready */
                    animation: fadeIn 0.3s ease-in;
                }}
                
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: scale(0.9); }}
                    to {{ opacity: 1; transform: scale(1); }}
                }}
            </style>
        </head>
        <body>
            <div class="text-container">
                <div class="hook-text">{text}</div>
            </div>
        </body>
        </html>
        """
        
        # Render with transparent background
        css_str = "body { background: transparent !important; }"
        
        try:
            self.hti.screenshot(
                html_str=html,
                css_str=css_str,
                save_as=output_name
            )
            
            output_path = self.temp_dir / output_name
            logger.info(f"Created hook overlay: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create overlay: {e}")
            raise
    
    def create_cta_overlay(
        self,
        text: str,
        style: str = "modern",
        output_name: Optional[str] = None
    ) -> Path:
        """
        Create Call-To-Action overlay (bottom of video)
        
        Args:
            text: CTA text (e.g., "Visit SayPlay.co.uk")
            style: Visual style
            output_name: Custom output filename
        
        Returns:
            Path to generated PNG overlay
        """
        if output_name is None:
            output_name = f"overlay_cta_{random.randint(1000, 9999)}.png"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    width: 1080px;
                    height: 1920px;
                    display: flex;
                    align-items: flex-end;
                    justify-content: center;
                }}
                
                .cta-container {{
                    width: 100%;
                    padding: 80px 40px 120px 40px;
                    text-align: center;
                }}
                
                .cta-box {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 25px 50px;
                    border-radius: 50px;
                    display: inline-block;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                }}
                
                .cta-text {{
                    font-family: 'Arial', 'Helvetica', sans-serif;
                    font-weight: 900;
                    font-size: 60px;
                    color: white;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                
                .cta-arrow {{
                    font-size: 70px;
                    margin-left: 20px;
                    animation: bounce 1s infinite;
                }}
                
                @keyframes bounce {{
                    0%, 100% {{ transform: translateX(0); }}
                    50% {{ transform: translateX(10px); }}
                }}
            </style>
        </head>
        <body>
            <div class="cta-container">
                <div class="cta-box">
                    <span class="cta-text">{text}</span>
                    <span class="cta-arrow">→</span>
                </div>
            </div>
        </body>
        </html>
        """
        
        css_str = "body { background: transparent !important; }"
        
        try:
            self.hti.screenshot(
                html_str=html,
                css_str=css_str,
                save_as=output_name
            )
            
            output_path = self.temp_dir / output_name
            logger.info(f"Created CTA overlay: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create CTA overlay: {e}")
            raise
    
    def _get_style_config(self, style: str) -> dict:
        """Get CSS configuration for different visual styles"""
        
        styles = {
            'tiktok': {
                'font_family': "'Impact', 'Arial Black', sans-serif",
                'font_weight': '900',
                'font_size': '110px',
                'color': '#FFFFFF',
                'stroke_width': '6px',
                'stroke_color': '#000000',
                'text_shadow': '8px 8px 0px #000000',
                'text_transform': 'uppercase',
                'line_height': '1.2'
            },
            'instagram': {
                'font_family': "'Helvetica Neue', 'Arial', sans-serif",
                'font_weight': '800',
                'font_size': '100px',
                'color': '#FFFFFF',
                'stroke_width': '4px',
                'stroke_color': '#FF3366',
                'text_shadow': '5px 5px 15px rgba(255, 51, 102, 0.5)',
                'text_transform': 'uppercase',
                'line_height': '1.3'
            },
            'youtube': {
                'font_family': "'Roboto', 'Arial', sans-serif",
                'font_weight': '900',
                'font_size': '120px',
                'color': '#FFD700',
                'stroke_width': '5px',
                'stroke_color': '#000000',
                'text_shadow': '4px 4px 0px #FF0000, 8px 8px 0px #000000',
                'text_transform': 'uppercase',
                'line_height': '1.2'
            },
            'minimal': {
                'font_family': "'SF Pro Display', 'Helvetica', sans-serif",
                'font_weight': '700',
                'font_size': '90px',
                'color': '#FFFFFF',
                'stroke_width': '2px',
                'stroke_color': 'rgba(0,0,0,0.3)',
                'text_shadow': '2px 2px 10px rgba(0,0,0,0.3)',
                'text_transform': 'none',
                'line_height': '1.4'
            }
        }
        
        return styles.get(style, styles['tiktok'])
    
    def _get_position_css(self, position: str) -> dict:
        """Get CSS positioning configuration"""
        
        positions = {
            'top': {
                'align': 'flex-start',
                'margin_top': '200px',
                'margin_bottom': '0px'
            },
            'center': {
                'align': 'center',
                'margin_top': '0px',
                'margin_bottom': '0px'
            },
            'bottom': {
                'align': 'flex-end',
                'margin_top': '0px',
                'margin_bottom': '200px'
            }
        }
        
        return positions.get(position, positions['top'])
    
    def create_emoji_sticker(
        self,
        emoji: str,
        position: Tuple[int, int] = (900, 300),
        size: int = 150,
        output_name: Optional[str] = None
    ) -> Path:
        """
        Create emoji sticker overlay
        
        Args:
            emoji: Emoji character (e.g., '🎁', '❤️', '🎉')
            position: (x, y) coordinates
            size: Emoji size in pixels
            output_name: Custom output filename
        
        Returns:
            Path to generated PNG overlay
        """
        if output_name is None:
            output_name = f"overlay_emoji_{random.randint(1000, 9999)}.png"
        
        x, y = position
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    width: 1080px;
                    height: 1920px;
                }}
                
                .emoji {{
                    position: absolute;
                    left: {x}px;
                    top: {y}px;
                    font-size: {size}px;
                    animation: pulse 2s infinite;
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
            </style>
        </head>
        <body>
            <div class="emoji">{emoji}</div>
        </body>
        </html>
        """
        
        css_str = "body { background: transparent !important; }"
        
        try:
            self.hti.screenshot(
                html_str=html,
                css_str=css_str,
                save_as=output_name
            )
            
            output_path = self.temp_dir / output_name
            logger.info(f"Created emoji overlay: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to create emoji overlay: {e}")
            raise


# Singleton instance
overlay_engine = ProOverlayEngine()


def main():
    """Test overlay generation"""
    print("🎨 Testing Pro Overlay Engine...")
    
    # Test hook overlay
    hook = overlay_engine.create_hook_overlay(
        "TAP TO HEAR\nTHEIR VOICE! 🎁",
        style="tiktok",
        position="top"
    )
    print(f"✓ Hook overlay: {hook}")
    
    # Test CTA overlay
    cta = overlay_engine.create_cta_overlay(
        "Get Yours at SayPlay.co.uk",
        style="modern"
    )
    print(f"✓ CTA overlay: {cta}")
    
    # Test emoji
    emoji = overlay_engine.create_emoji_sticker(
        "🎁",
        position=(900, 300),
        size=150
    )
    print(f"✓ Emoji overlay: {emoji}")
    
    print("\n✅ All overlays generated successfully!")


if __name__ == "__main__":
    main()
