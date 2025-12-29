#!/usr/bin/env python3
"""
TITAN MODULE #9: B2B HUNTER
Automated B2B prospecting: find businesses, analyze style, send personalized outreach
"""
import os
import sys
import json
import requests
from typing import Dict, List
from pathlib import Path
import time
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"🎯 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class B2BHunter:
    """Automated B2B prospect finder and outreach"""
    
    # Target business categories
    TARGET_CATEGORIES = [
        'florist',
        'flower_shop',
        'wedding_venue',
        'event_planner',
        'gift_shop',
        'party_supplies',
        'bridal_shop',
        'wedding_photographer'
    ]
    
    def __init__(self):
        """Initialize with API keys"""
        self.google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        
        self.prospects_db = self._load_prospects()
        logger.info("B2BHunter initialized")
    
    def find_businesses(self, location: str, category: str, radius: int = 50000) -> List[Dict]:
        """Find businesses on Google Maps"""
        
        if not self.google_maps_key:
            logger.warning("Google Maps API not configured")
            return self._generate_mock_businesses(location, category)
        
        try:
            # Google Places API
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            
            params = {
                'location': location,  # lat,lng
                'radius': radius,  # meters
                'type': category,
                'key': self.google_maps_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                businesses = []
                
                for place in data.get('results', []):
                    business = {
                        'id': place['place_id'],
                        'name': place['name'],
                        'address': place.get('vicinity'),
                        'rating': place.get('rating'),
                        'category': category,
                        'location': place['geometry']['location']
                    }
                    
                    # Get details
                    details = self._get_business_details(place['place_id'])
                    business.update(details)
                    
                    businesses.append(business)
                    time.sleep(0.5)  # Rate limiting
                
                logger.success(f"Found {len(businesses)} businesses")
                return businesses
            else:
                logger.error(f"Google Maps API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Business search failed: {e}")
            return []
    
    def scrape_instagram_profile(self, instagram_handle: str) -> Dict:
        """Analyze Instagram profile for style and aesthetic"""
        
        # In production, use Instagram API or scraper
        # For now, return mock analysis
        
        logger.info(f"Analyzing Instagram: @{instagram_handle}")
        
        analysis = {
            'handle': instagram_handle,
            'followers': 0,
            'aesthetic': 'modern',  # modern, vintage, rustic, elegant
            'color_palette': ['#FF6B6B', '#4ECDC4', '#45B7D1'],
            'posting_frequency': 'high',  # high, medium, low
            'engagement_rate': 0,
            'target_audience': 'millennials',  # millennials, gen-z, boomers
            'content_style': 'lifestyle'  # lifestyle, product, educational
        }
        
        return analysis
    
    def analyze_business_style(self, business: Dict) -> Dict:
        """Analyze business aesthetic and values"""
        
        # Analyze from name, description, photos
        name = business.get('name', '').lower()
        description = business.get('description', '').lower()
        
        style_indicators = {
            'luxury': ['luxury', 'premium', 'exclusive', 'high-end', 'boutique'],
            'rustic': ['rustic', 'vintage', 'barn', 'country', 'farmhouse'],
            'modern': ['modern', 'contemporary', 'minimalist', 'sleek'],
            'traditional': ['traditional', 'classic', 'timeless', 'elegant'],
            'eco': ['eco', 'sustainable', 'green', 'natural', 'organic']
        }
        
        detected_styles = []
        for style, keywords in style_indicators.items():
            if any(kw in name or kw in description for kw in keywords):
                detected_styles.append(style)
        
        if not detected_styles:
            detected_styles = ['modern']  # default
        
        analysis = {
            'primary_style': detected_styles[0],
            'secondary_styles': detected_styles[1:],
            'price_point': self._estimate_price_point(business),
            'target_market': self._estimate_target_market(business)
        }
        
        logger.info(f"Style: {analysis['primary_style']} | Price: {analysis['price_point']}")
        return analysis
    
    def generate_cold_email(self, business: Dict, style_analysis: Dict) -> str:
        """Generate personalized cold email"""
        
        name = business['name']
        primary_style = style_analysis['primary_style']
        price_point = style_analysis['price_point']
        category = business['category']
        
        # Select email template based on style
        templates = {
            'luxury': self._luxury_email_template,
            'rustic': self._rustic_email_template,
            'modern': self._modern_email_template,
            'traditional': self._traditional_email_template,
            'eco': self._eco_email_template
        }
        
        template_func = templates.get(primary_style, templates['modern'])
        email = template_func(name, category, price_point)
        
        logger.success(f"Generated {primary_style} email for {name}")
        return email
    
    def send_cold_email(self, email_address: str, subject: str, body: str) -> bool:
        """Send cold email via SendGrid"""
        
        if not self.sendgrid_key:
            logger.warning("SendGrid not configured")
            logger.info(f"Would send to: {email_address}")
            logger.info(f"Subject: {subject}")
            return False
        
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            
            headers = {
                'Authorization': f'Bearer {self.sendgrid_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'personalizations': [{
                    'to': [{'email': email_address}],
                    'subject': subject
                }],
                'from': {
                    'email': 'partnerships@sayplay.co.uk',
                    'name': 'SayPlay B2B Team'
                },
                'content': [{
                    'type': 'text/html',
                    'value': body
                }]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 202]:
                logger.success(f"Email sent to {email_address}")
                return True
            else:
                logger.error(f"SendGrid error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
    
    def track_prospect(self, business: Dict, status: str = 'contacted'):
        """Track prospect in database"""
        
        prospect_id = business['id']
        
        if prospect_id not in self.prospects_db:
            self.prospects_db[prospect_id] = {
                'business': business,
                'status': status,  # contacted, replied, negotiating, closed, rejected
                'contacted_at': time.time(),
                'follow_ups': []
            }
        else:
            self.prospects_db[prospect_id]['status'] = status
        
        self._save_prospects()
        logger.info(f"Prospect tracked: {business['name']} - {status}")
    
    def schedule_follow_up(self, prospect_id: str, days: int = 7):
        """Schedule follow-up email"""
        
        if prospect_id in self.prospects_db:
            follow_up_time = time.time() + (days * 86400)
            self.prospects_db[prospect_id]['follow_ups'].append({
                'scheduled': follow_up_time,
                'type': 'email',
                'sent': False
            })
            self._save_prospects()
            logger.info(f"Follow-up scheduled for {days} days")
    
    def _get_business_details(self, place_id: str) -> Dict:
        """Get detailed business info from Google Places"""
        
        if not self.google_maps_key:
            return {}
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_phone_number,website,formatted_address,rating,user_ratings_total',
                'key': self.google_maps_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                result = response.json().get('result', {})
                return {
                    'phone': result.get('formatted_phone_number'),
                    'website': result.get('website'),
                    'address': result.get('formatted_address'),
                    'review_count': result.get('user_ratings_total', 0)
                }
            else:
                return {}
                
        except Exception as e:
            logger.warning(f"Details fetch failed: {e}")
            return {}
    
    def _estimate_price_point(self, business: Dict) -> str:
        """Estimate business price point"""
        
        rating = business.get('rating', 3.5)
        name = business.get('name', '').lower()
        
        luxury_keywords = ['luxury', 'premium', 'exclusive', 'boutique']
        if any(kw in name for kw in luxury_keywords) or rating >= 4.5:
            return 'premium'
        elif rating >= 4.0:
            return 'mid-range'
        else:
            return 'budget'
    
    def _estimate_target_market(self, business: Dict) -> str:
        """Estimate target customer demographic"""
        
        category = business.get('category', '')
        
        if category in ['wedding_venue', 'bridal_shop']:
            return 'millennials'
        elif category in ['florist', 'gift_shop']:
            return 'broad'
        else:
            return 'general'
    
    def _luxury_email_template(self, name: str, category: str, price_point: str) -> str:
        """Luxury brand email template"""
        
        return f"""<html>
<body style="font-family: Georgia, serif; color: #2c2c2c;">
    <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <h2 style="color: #1a1a1a; font-weight: 300;">Dear {name} Team,</h2>
        
        <p style="line-height: 1.8; font-size: 16px;">
            We've been following your exceptional work in creating unforgettable experiences 
            for your discerning clientele.
        </p>
        
        <p style="line-height: 1.8; font-size: 16px;">
            At SayPlay, we craft premium voice message gifts that resonate with luxury brands 
            like yours. Our NFC-enabled cards allow your clients to capture and preserve 
            authentic emotional moments—perfect as thoughtful additions to your premium packages.
        </p>
        
        <p style="line-height: 1.8; font-size: 16px;">
            <strong>Exclusive B2B Partnership Benefits:</strong><br>
            • 40% wholesale discount on bulk orders (500+ units)<br>
            • Custom co-branding options<br>
            • White-label solutions<br>
            • Dedicated account manager
        </p>
        
        <p style="line-height: 1.8; font-size: 16px;">
            Would you be open to a brief conversation about how SayPlay can complement 
            your premium offerings?
        </p>
        
        <p style="line-height: 1.8; font-size: 16px;">
            Warmest regards,<br>
            <strong>The SayPlay Partnership Team</strong><br>
            partnerships@sayplay.co.uk<br>
            +44 (0) 20 XXXX XXXX
        </p>
    </div>
</body>
</html>"""
    
    def _modern_email_template(self, name: str, category: str, price_point: str) -> str:
        """Modern/contemporary email template"""
        
        return f"""<html>
<body style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 30px 20px;">
        <h2 style="color: #4A90E2;">Hi {name}! 👋</h2>
        
        <p style="line-height: 1.6;">
            Love what you're doing! We noticed your innovative approach to {category}s 
            and thought there might be a great synergy opportunity.
        </p>
        
        <p style="line-height: 1.6;">
            SayPlay makes voice message gifts with NFC technology (tap-to-play, no app needed). 
            Perfect for adding a personal touch to your client experience.
        </p>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #4A90E2;">Partnership Perks:</h3>
            <ul style="line-height: 1.8;">
                <li>35% wholesale discount</li>
                <li>Custom branding available</li>
                <li>Drop-shipping options</li>
                <li>Marketing materials included</li>
            </ul>
        </div>
        
        <p style="line-height: 1.6;">
            Fancy a quick chat? We'd love to explore how we can work together.
        </p>
        
        <p style="line-height: 1.6;">
            Cheers,<br>
            <strong>SayPlay Team</strong><br>
            📧 partnerships@sayplay.co.uk
        </p>
    </div>
</body>
</html>"""
    
    def _rustic_email_template(self, name: str, category: str, price_point: str) -> str:
        """Rustic/vintage email template"""
        return self._modern_email_template(name, category, price_point)  # Simplified
    
    def _traditional_email_template(self, name: str, category: str, price_point: str) -> str:
        """Traditional email template"""
        return self._luxury_email_template(name, category, price_point)  # Simplified
    
    def _eco_email_template(self, name: str, category: str, price_point: str) -> str:
        """Eco/sustainable email template"""
        return self._modern_email_template(name, category, price_point)  # Simplified
    
    def _generate_mock_businesses(self, location: str, category: str) -> List[Dict]:
        """Generate mock businesses for testing"""
        
        mock_names = {
            'florist': ['Blooming Marvellous', 'The Flower Studio', 'Petal Pushers'],
            'wedding_venue': ['The Manor House', 'Riverside Gardens', 'Castle Hall'],
            'gift_shop': ['Thoughtful Gifts', 'The Present Company', 'Gift Emporium']
        }
        
        names = mock_names.get(category, ['Business A', 'Business B', 'Business C'])
        
        businesses = []
        for idx, name in enumerate(names):
            businesses.append({
                'id': f'mock_{category}_{idx}',
                'name': name,
                'address': f'{location}',
                'category': category,
                'rating': 4.0 + (idx * 0.3),
                'phone': f'+44 20 1234 {5600 + idx}',
                'website': f'https://{name.lower().replace(" ", "")}.co.uk',
                'description': f'Leading {category} in {location}'
            })
        
        logger.info(f"Generated {len(businesses)} mock businesses")
        return businesses
    
    def _load_prospects(self) -> Dict:
        """Load prospects database"""
        db_path = Path('b2b_prospects.json')
        if db_path.exists():
            with open(db_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_prospects(self):
        """Save prospects database"""
        with open('b2b_prospects.json', 'w') as f:
            json.dump(self.prospects_db, f, indent=2)


if __name__ == "__main__":
    """Test B2B Hunter"""
    
    print("\n🧪 Testing B2B Hunter...\n")
    
    hunter = B2BHunter()
    
    # Test 1: Find businesses
    print("Test 1: Finding businesses")
    businesses = hunter.find_businesses('London, UK', 'florist')
    print(f"✓ Found {len(businesses)} businesses")
    
    if businesses:
        # Test 2: Analyze style
        print("\nTest 2: Analyzing business style")
        business = businesses[0]
        style = hunter.analyze_business_style(business)
        print(f"✓ Style: {style['primary_style']} | Price: {style['price_point']}")
        
        # Test 3: Generate email
        print("\nTest 3: Generating cold email")
        email = hunter.generate_cold_email(business, style)
        print("✓ Email generated")
        
        # Save example
        with open('test_b2b_email.html', 'w') as f:
            f.write(email)
        print("✓ Saved: test_b2b_email.html")
        
        # Test 4: Track prospect
        print("\nTest 4: Tracking prospect")
        hunter.track_prospect(business, 'contacted')
        print("✓ Prospect tracked")
    
    print("\n✅ B2B Hunter test complete!")
