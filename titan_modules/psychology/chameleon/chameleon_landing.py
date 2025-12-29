#!/usr/bin/env python3
"""
TITAN MODULE #12: CHAMELEON LANDING
Real-time landing page personalization based on traffic source, device, location
"""
import os
import json
from typing import Dict, Optional
from datetime import datetime
import hashlib

class Logger:
    @staticmethod
    def info(msg): print(f"🦎 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")

logger = Logger()


class ChameleonEngine:
    """Dynamic content personalization"""
    
    # Content variants by traffic source
    CONTENT_VARIANTS = {
        'google_search': {
            'headline': 'The #1 Voice Message Gift in {year}',
            'subheadline': 'Found by 100,000+ People Searching for {keyword}',
            'cta': 'See Why Everyone Chooses SayPlay',
            'social_proof': 'As Seen in Google Search Results',
            'urgency': 'Limited Stock - Order Today',
            'focus': 'seo'
        },
        'facebook': {
            'headline': 'Your Friends Are Talking About This Gift',
            'subheadline': 'The Viral Gift Everyone Is Sharing',
            'cta': 'Join 50,000+ Happy Customers',
            'social_proof': 'Trending on Facebook',
            'urgency': '2,347 People Viewing Now',
            'focus': 'social'
        },
        'pinterest': {
            'headline': 'Pin-Worthy Personalized Gifts',
            'subheadline': 'Beautiful Gifts That Create Lasting Memories',
            'cta': 'Save to Your Board',
            'social_proof': 'Pinned 10K+ Times',
            'urgency': 'New Design Just Released',
            'focus': 'visual'
        },
        'instagram': {
            'headline': 'Instagram-Worthy Gifts',
            'subheadline': 'Tag Us @SayPlay in Your Stories',
            'cta': 'Shop the Look',
            'social_proof': '50K+ Followers Love Us',
            'urgency': 'Featured in Stories Today',
            'focus': 'influencer'
        },
        'tiktok': {
            'headline': 'The Gift That Went Viral',
            'subheadline': '2.5M Views on TikTok',
            'cta': 'Get Yours Before They\'re Gone',
            'social_proof': '#SayPlayGift Trending',
            'urgency': 'Order Within 2 Hours',
            'focus': 'viral'
        },
        'linkedin': {
            'headline': 'Professional Corporate Gifts',
            'subheadline': 'Trusted by 500+ Companies',
            'cta': 'Request Business Quote',
            'social_proof': 'B2B Excellence',
            'urgency': 'Bulk Discounts Available',
            'focus': 'b2b'
        },
        'email': {
            'headline': 'Welcome Back! Your Cart is Waiting',
            'subheadline': 'Complete Your Order to Create Magic',
            'cta': 'Finish Checkout Now',
            'social_proof': 'Previous Customers Get 10% Off',
            'urgency': 'Cart Expires in 24 Hours',
            'focus': 'conversion'
        },
        'direct': {
            'headline': 'Voice Message Gifts That Last Forever',
            'subheadline': 'Capture Real Emotions with NFC Technology',
            'cta': 'Discover SayPlay',
            'social_proof': '100,000+ Gifts Delivered',
            'urgency': 'Free Shipping Today',
            'focus': 'brand'
        }
    }
    
    # Device-specific adjustments
    DEVICE_VARIANTS = {
        'iphone': {
            'price_multiplier': 1.15,  # Premium pricing
            'show_premium': True,
            'payment_method': 'Apple Pay',
            'design': 'premium'
        },
        'android': {
            'price_multiplier': 1.0,
            'show_premium': False,
            'payment_method': 'Google Pay',
            'design': 'standard'
        },
        'desktop': {
            'price_multiplier': 1.1,
            'show_premium': True,
            'payment_method': 'Credit Card',
            'design': 'detailed'
        },
        'tablet': {
            'price_multiplier': 1.05,
            'show_premium': False,
            'payment_method': 'PayPal',
            'design': 'standard'
        }
    }
    
    # Location-based content
    LOCATION_VARIANTS = {
        'london': {
            'shipping': 'Next-Day Delivery in London',
            'currency': '£',
            'local_proof': 'Loved by Londoners'
        },
        'manchester': {
            'shipping': 'Free Shipping to Manchester',
            'currency': '£',
            'local_proof': 'Popular in Manchester'
        },
        'uk_other': {
            'shipping': 'Free UK Delivery',
            'currency': '£',
            'local_proof': 'UK\'s Favorite Gift'
        },
        'international': {
            'shipping': 'International Shipping Available',
            'currency': '$',
            'local_proof': 'Ships Worldwide'
        }
    }
    
    def __init__(self):
        """Initialize chameleon engine"""
        logger.info("ChameleonEngine initialized")
    
    def personalize_landing(self, visitor_data: Dict) -> Dict:
        """Generate personalized landing page content"""
        
        # Extract visitor info
        traffic_source = self._detect_traffic_source(visitor_data)
        device_type = self._detect_device(visitor_data)
        location = self._detect_location(visitor_data)
        time_context = self._get_time_context()
        
        # Get base variant
        content = self.CONTENT_VARIANTS.get(traffic_source, self.CONTENT_VARIANTS['direct']).copy()
        device_config = self.DEVICE_VARIANTS.get(device_type, self.DEVICE_VARIANTS['desktop'])
        location_config = self.LOCATION_VARIANTS.get(location, self.LOCATION_VARIANTS['uk_other'])
        
        # Apply personalizations
        content['headline'] = content['headline'].format(
            year=datetime.now().year,
            keyword=visitor_data.get('keyword', 'personalized gifts')
        )
        content['subheadline'] = content['subheadline'].format(
            keyword=visitor_data.get('keyword', 'unique gifts')
        )
        
        # Add device-specific configs
        content['device_config'] = device_config
        content['location_config'] = location_config
        content['time_context'] = time_context
        
        # Add visitor tracking
        content['visitor_id'] = self._generate_visitor_id(visitor_data)
        content['session_id'] = visitor_data.get('session_id', 'new')
        
        logger.success(f"Personalized for: {traffic_source} / {device_type} / {location}")
        
        return content
    
    def _detect_traffic_source(self, visitor_data: Dict) -> str:
        """Detect traffic source from referrer"""
        
        referrer = visitor_data.get('referrer', '').lower()
        utm_source = visitor_data.get('utm_source', '').lower()
        
        if utm_source:
            if 'email' in utm_source:
                return 'email'
            if 'facebook' in utm_source or 'fb' in utm_source:
                return 'facebook'
            if 'pinterest' in utm_source:
                return 'pinterest'
            if 'instagram' in utm_source or 'ig' in utm_source:
                return 'instagram'
            if 'tiktok' in utm_source:
                return 'tiktok'
            if 'linkedin' in utm_source:
                return 'linkedin'
        
        if referrer:
            if 'google' in referrer:
                return 'google_search'
            if 'facebook' in referrer:
                return 'facebook'
            if 'pinterest' in referrer:
                return 'pinterest'
            if 'instagram' in referrer:
                return 'instagram'
            if 'tiktok' in referrer:
                return 'tiktok'
            if 'linkedin' in referrer:
                return 'linkedin'
        
        return 'direct'
    
    def _detect_device(self, visitor_data: Dict) -> str:
        """Detect device type from user agent"""
        
        user_agent = visitor_data.get('user_agent', '').lower()
        
        if 'iphone' in user_agent or 'ipad' in user_agent:
            return 'iphone'
        elif 'android' in user_agent:
            if 'mobile' in user_agent:
                return 'android'
            else:
                return 'tablet'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'tablet'
        else:
            return 'desktop'
    
    def _detect_location(self, visitor_data: Dict) -> str:
        """Detect location from IP or headers"""
        
        city = visitor_data.get('city', '').lower()
        country = visitor_data.get('country', '').lower()
        
        if 'london' in city:
            return 'london'
        elif 'manchester' in city:
            return 'manchester'
        elif country == 'gb' or country == 'uk':
            return 'uk_other'
        else:
            return 'international'
    
    def _get_time_context(self) -> Dict:
        """Get time-based context"""
        
        now = datetime.now()
        hour = now.hour
        
        if 6 <= hour < 12:
            period = 'morning'
            greeting = 'Good Morning'
        elif 12 <= hour < 17:
            period = 'afternoon'
            greeting = 'Good Afternoon'
        elif 17 <= hour < 22:
            period = 'evening'
            greeting = 'Good Evening'
        else:
            period = 'night'
            greeting = 'Still Shopping?'
        
        # Urgency based on time
        if hour >= 20:
            urgency = 'Order before midnight for same-day processing'
        else:
            urgency = 'Order today for fast delivery'
        
        return {
            'period': period,
            'greeting': greeting,
            'urgency': urgency,
            'hour': hour
        }
    
    def _generate_visitor_id(self, visitor_data: Dict) -> str:
        """Generate unique visitor ID"""
        
        # Create hash from IP + user agent
        ip = visitor_data.get('ip', 'unknown')
        user_agent = visitor_data.get('user_agent', 'unknown')
        
        data = f"{ip}:{user_agent}"
        return hashlib.md5(data.encode()).hexdigest()[:16]
    
    def ab_test_variant(self, visitor_id: str, test_name: str) -> str:
        """Assign A/B test variant"""
        
        # Consistent hashing for same visitor
        hash_val = int(hashlib.md5(f"{visitor_id}:{test_name}".encode()).hexdigest(), 16)
        
        # 50/50 split
        return 'A' if hash_val % 2 == 0 else 'B'
    
    def track_conversion(self, visitor_id: str, variant: str, converted: bool):
        """Track conversion for analytics"""
        
        # In production, save to database
        logger.info(f"Conversion tracked: {visitor_id} / {variant} / {converted}")


def generate_chameleon_page(visitor_data: Dict) -> str:
    """Generate complete personalized HTML page"""
    
    engine = ChameleonEngine()
    content = engine.personalize_landing(visitor_data)
    
    # Extract content
    headline = content['headline']
    subheadline = content['subheadline']
    cta = content['cta']
    social_proof = content['social_proof']
    urgency = content['urgency']
    greeting = content['time_context']['greeting']
    shipping = content['location_config']['shipping']
    currency = content['location_config']['currency']
    
    # Device-specific styling
    design = content['device_config']['design']
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{headline} | SayPlay</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 60px;
            max-width: 800px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }}
        .greeting {{ color: #667eea; font-size: 1.2em; margin-bottom: 20px; }}
        h1 {{ font-size: 3em; color: #1a1a1a; margin-bottom: 20px; line-height: 1.2; }}
        .subheadline {{ font-size: 1.5em; color: #666; margin-bottom: 40px; }}
        .cta-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 60px;
            font-size: 1.3em;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transition: transform 0.2s;
        }}
        .cta-button:hover {{ transform: translateY(-3px); }}
        .social-proof {{
            background: #f0f0f0;
            padding: 15px 30px;
            border-radius: 30px;
            display: inline-block;
            margin: 20px 0;
            font-weight: 600;
        }}
        .urgency {{
            color: #ff6b6b;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 20px;
            animation: pulse 2s infinite;
        }}
        .shipping {{ color: #51cf66; font-weight: 600; margin-top: 15px; }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="greeting">{greeting}! 👋</div>
        <h1>{headline}</h1>
        <div class="subheadline">{subheadline}</div>
        <div class="social-proof">⭐ {social_proof}</div>
        <a href="https://sayplay.co.uk/shop" class="cta-button">{cta}</a>
        <div class="urgency">🔥 {urgency}</div>
        <div class="shipping">📦 {shipping}</div>
    </div>
</body>
</html>"""
    
    return html


if __name__ == "__main__":
    """Test chameleon engine"""
    
    print("\n🧪 Testing Chameleon Landing...\n")
    
    # Test different visitor scenarios
    test_visitors = [
        {
            'referrer': 'https://www.google.com',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)',
            'ip': '82.163.x.x',
            'city': 'London',
            'country': 'GB',
            'keyword': 'birthday gifts'
        },
        {
            'referrer': 'https://www.facebook.com',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'ip': '151.224.x.x',
            'city': 'Manchester',
            'country': 'GB',
            'keyword': 'personalized gifts'
        },
        {
            'utm_source': 'pinterest',
            'user_agent': 'Mozilla/5.0 (Linux; Android 11)',
            'ip': '104.28.x.x',
            'country': 'US',
            'keyword': 'unique gifts'
        }
    ]
    
    for idx, visitor in enumerate(test_visitors, 1):
        print(f"Test {idx}:")
        html = generate_chameleon_page(visitor)
        
        filename = f'test_landing_{idx}.html'
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"✓ Saved: {filename}\n")
    
    print("✅ Chameleon Landing test complete!")
