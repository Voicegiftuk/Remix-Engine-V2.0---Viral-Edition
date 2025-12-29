#!/usr/bin/env python3
"""
TITAN MODULE #6: GLOBAL DOMINATION (ZERO-COST VERSION)
Uses Gemini for translations - COMPLETELY FREE!
"""
import os
import sys
import json
from typing import Dict, List, Optional
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"🌍 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class GlobalDomination:
    """International expansion using FREE Gemini translations"""
    
    # Target markets (same as before)
    TARGET_MARKETS = {
        'es': {
            'name': 'Spanish',
            'native_name': 'Español',
            'countries': ['ES', 'MX', 'AR', 'CO'],
            'population': 500_000_000,
            'currency': '€',
            'price_multiplier': 0.95
        },
        'de': {
            'name': 'German',
            'native_name': 'Deutsch',
            'countries': ['DE', 'AT', 'CH'],
            'population': 100_000_000,
            'currency': '€',
            'price_multiplier': 1.15
        },
        'fr': {
            'name': 'French',
            'native_name': 'Français',
            'countries': ['FR', 'BE', 'CH', 'CA'],
            'population': 300_000_000,
            'currency': '€',
            'price_multiplier': 1.10
        },
        'it': {
            'name': 'Italian',
            'native_name': 'Italiano',
            'countries': ['IT'],
            'population': 60_000_000,
            'currency': '€',
            'price_multiplier': 1.05
        },
        'pl': {
            'name': 'Polish',
            'native_name': 'Polski',
            'countries': ['PL'],
            'population': 40_000_000,
            'currency': 'zł',
            'price_multiplier': 0.75
        }
    }
    
    # Cultural patterns (same as before)
    CULTURAL_PATTERNS = {
        'es': {'formality': 'informal', 'emoji_usage': 'high'},
        'de': {'formality': 'formal', 'emoji_usage': 'low'},
        'fr': {'formality': 'formal', 'emoji_usage': 'medium'},
        'it': {'formality': 'informal', 'emoji_usage': 'high'},
        'pl': {'formality': 'informal', 'emoji_usage': 'medium'}
    }
    
    def __init__(self):
        """Initialize zero-cost translation engine"""
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        logger.info("Global Domination initialized (Zero-Cost Mode)")
        logger.info(f"Using Gemini for FREE translations to {len(self.TARGET_MARKETS)} languages")
        
        if not self.gemini_key:
            logger.warning("GEMINI_API_KEY not set - translations will use mock data")
    
    def translate_content(
        self,
        content: Dict,
        target_language: str,
        content_type: str = 'article'
    ) -> Dict:
        """Translate and localize content using Gemini (FREE)"""
        
        if target_language not in self.TARGET_MARKETS:
            logger.error(f"Unsupported language: {target_language}")
            return content
        
        market = self.TARGET_MARKETS[target_language]
        logger.info(f"Translating to {market['name']}...")
        
        translated_content = content.copy()
        
        # Translate title
        if 'title' in content:
            translated_content['title'] = self._translate_with_gemini(
                content['title'],
                target_language,
                'title'
            )
        
        # Translate body
        if 'text' in content:
            translated_content['text'] = self._translate_with_gemini(
                content['text'],
                target_language,
                'body'
            )
        
        if 'html' in content:
            translated_content['html'] = self._translate_with_gemini(
                content['html'],
                target_language,
                'html'
            )
        
        # Apply cultural adaptation
        translated_content = self._apply_cultural_adaptation(
            translated_content,
            target_language
        )
        
        # Localize pricing
        translated_content = self._localize_pricing(
            translated_content,
            target_language
        )
        
        # Add metadata
        translated_content['language'] = target_language
        translated_content['market'] = market
        
        logger.success(f"Translation complete: {target_language}")
        return translated_content
    
    def _translate_with_gemini(
        self,
        text: str,
        target_language: str,
        content_type: str = 'body'
    ) -> str:
        """Translate using Gemini (FREE)"""
        
        if not self.gemini_key:
            logger.warning("Gemini not configured - using mock translation")
            return f"[{self.TARGET_MARKETS[target_language]['native_name']}] {text}"
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')  # FREE tier
            
            market = self.TARGET_MARKETS[target_language]
            culture = self.CULTURAL_PATTERNS[target_language]
            
            # Create context-aware prompt
            formality = culture['formality']
            
            prompt = f"""Translate this {content_type} to {market['name']} ({market['native_name']}).

Instructions:
- Use {formality} tone
- Maintain emotional warmth and authenticity
- Adapt cultural references naturally
- Keep brand name "SayPlay" unchanged
- Preserve any HTML tags if present
- Make it sound native, not like a translation

Text to translate:
{text}

Return ONLY the translated text, nothing else."""
            
            response = model.generate_content(prompt)
            translated = response.text.strip()
            
            logger.info(f"  Translated {len(text)} → {len(translated)} chars")
            return translated
            
        except Exception as e:
            logger.error(f"Gemini translation failed: {e}")
            return f"[{market['native_name']}] {text}"
    
    def batch_translate_all_markets(self, content: Dict) -> Dict[str, Dict]:
        """Translate to ALL markets using FREE Gemini"""
        
        logger.info(f"Batch translating to {len(self.TARGET_MARKETS)} markets...")
        
        translations = {
            'en': content  # Original English
        }
        
        for lang_code in self.TARGET_MARKETS.keys():
            try:
                translations[lang_code] = self.translate_content(content, lang_code)
            except Exception as e:
                logger.error(f"Translation failed for {lang_code}: {e}")
                translations[lang_code] = None
        
        logger.success(f"Batch translation complete: {sum(1 for t in translations.values() if t)} successful")
        return translations
    
    def _apply_cultural_adaptation(self, content: Dict, target_language: str) -> Dict:
        """Apply cultural adaptations"""
        
        culture = self.CULTURAL_PATTERNS.get(target_language, {})
        content['cultural_context'] = culture
        
        return content
    
    def _localize_pricing(self, content: Dict, target_language: str) -> Dict:
        """Localize pricing for market"""
        
        market = self.TARGET_MARKETS[target_language]
        multiplier = market['price_multiplier']
        currency = market['currency']
        
        if 'price' in content:
            original_price = content['price']
            localized_price = original_price * multiplier
            
            content['localized_price'] = {
                'amount': round(localized_price, 2),
                'currency': currency,
                'formatted': f"{currency}{localized_price:.2f}"
            }
        
        return content
    
    def create_regional_landing_page(self, content: Dict, target_language: str) -> str:
        """Create fully localized landing page"""
        
        market = self.TARGET_MARKETS[target_language]
        culture = self.CULTURAL_PATTERNS[target_language]
        
        # Translate content
        translated = self.translate_content(content, target_language)
        
        # Build HTML
        html = f"""<!DOCTYPE html>
<html lang="{target_language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{translated.get('title', 'SayPlay')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 60px;
            max-width: 900px;
            margin: 0 auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{ font-size: 2.5em; color: #1a1a1a; margin-bottom: 20px; }}
        .content {{ font-size: 1.1em; line-height: 1.8; color: #333; }}
        .cta {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 60px;
            font-size: 1.3em;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            margin: 30px 0;
            display: inline-block;
            text-decoration: none;
        }}
        .price {{ font-size: 2em; color: #667eea; font-weight: bold; margin: 20px 0; }}
        .footer {{ margin-top: 40px; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{translated.get('title', 'SayPlay')}</h1>
        <div class="content">
            {translated.get('html', translated.get('text', ''))}
        </div>
        
        {'<div class="price">' + translated.get('localized_price', {}).get('formatted', '') + '</div>' if 'localized_price' in translated else ''}
        
        <a href="https://sayplay.co.uk/shop" class="cta">
            {self._get_cta_text(target_language)}
        </a>
        
        <div class="footer">
            <p>SayPlay™ - {market['name']}</p>
            <p>© 2025 SayPlay. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
        
        logger.success(f"Regional landing page created: {target_language}")
        return html
    
    def _get_cta_text(self, target_language: str) -> str:
        """Get localized CTA text"""
        
        cta_texts = {
            'es': 'Comprar Ahora →',
            'de': 'Jetzt Kaufen →',
            'fr': 'Acheter Maintenant →',
            'it': 'Acquista Ora →',
            'pl': 'Kup Teraz →'
        }
        
        return cta_texts.get(target_language, 'Shop Now →')
    
    def estimate_market_size(self) -> Dict:
        """Estimate total addressable market"""
        
        total_population = sum(m['population'] for m in self.TARGET_MARKETS.values())
        penetration_rate = 0.001
        avg_order_value = 25
        orders_per_year = 2
        
        annual_revenue_potential = (
            total_population *
            penetration_rate *
            avg_order_value *
            orders_per_year
        )
        
        result = {
            'total_population': total_population,
            'penetration_rate': penetration_rate,
            'estimated_customers': int(total_population * penetration_rate),
            'avg_order_value': avg_order_value,
            'annual_revenue_potential': annual_revenue_potential,
            'monthly_revenue_potential': annual_revenue_potential / 12,
            'markets': len(self.TARGET_MARKETS)
        }
        
        logger.info(f"Market size: {total_population:,} people → £{annual_revenue_potential:,.0f}/year potential")
        return result


if __name__ == "__main__":
    """Test zero-cost translations"""
    
    print("\n🧪 Testing ZERO-COST Global Domination...\n")
    
    engine = GlobalDomination()
    
    # Test content
    test_content = {
        'title': 'Perfect Birthday Gifts 2025 | SayPlay',
        'text': 'Voice message gifts are the perfect way to celebrate. With SayPlay, you can create lasting memories.',
        'html': '<h1>Perfect Birthday Gifts</h1><p>Voice message gifts are amazing!</p>',
        'price': 19.99
    }
    
    # Test 1: Single translation
    print("Test 1: Spanish translation")
    spanish = engine.translate_content(test_content, 'es')
    print(f"✓ Title: {spanish['title']}")
    print(f"✓ Price: {spanish.get('localized_price', {}).get('formatted', 'N/A')}")
    
    # Test 2: Batch translation
    print("\nTest 2: Batch translation to all markets")
    all_translations = engine.batch_translate_all_markets(test_content)
    print(f"✓ Translated to {len(all_translations)} languages")
    for lang, trans in all_translations.items():
        if trans and lang != 'en':
            print(f"  • {lang}: {trans['title'][:50]}...")
    
    # Test 3: Market size
    print("\nTest 3: Market size estimation")
    market_size = engine.estimate_market_size()
    print(f"✓ Total population: {market_size['total_population']:,}")
    print(f"✓ Annual revenue potential: £{market_size['annual_revenue_potential']:,.0f}")
    
    print("\n✅ Zero-cost global domination test complete!")
    print("💰 Cost: £0.00 (Gemini FREE tier)")
    print("🌍 Reach: 1 billion people!")
