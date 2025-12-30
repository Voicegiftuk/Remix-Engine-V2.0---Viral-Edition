#!/usr/bin/env python3
"""
B2B HUNTER - BULLETPROOF VERSION
100% validated emails only
Zero tolerance for errors
"""
import os
import time
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime

# Import bulletproof validator
try:
    from .email_validator_bulletproof import BulletproofEmailValidator, EmailFinder
except ImportError:
    from email_validator_bulletproof import BulletproofEmailValidator, EmailFinder


class B2BHunterBulletproof:
    """
    B2B Hunter with bulletproof email validation
    Will NOT send to any unvalidated email
    """
    
    def __init__(self):
        self.google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        
        if not self.google_maps_key:
            raise Exception("GOOGLE_MAPS_API_KEY required")
        if not self.sendgrid_key:
            raise Exception("SENDGRID_API_KEY required")
        
        self.validator = BulletproofEmailValidator()
        self.finder = EmailFinder()
        
        self.stats = {
            'businesses_found': 0,
            'emails_discovered': 0,
            'emails_validated': 0,
            'emails_rejected': 0,
            'emails_sent': 0,
            'validation_log': []
        }
    
    def find_businesses(self, location: str, business_type: str, max_results: int = 30) -> List[Dict]:
        """Find businesses using Google Places API"""
        print(f"\nSEARCHING: {business_type} in {location}")
        print(f"{'='*70}\n")
        
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f'{business_type} in {location}',
            'key': self.google_maps_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Places API error: {data.get('status')}")
                return []
            
            businesses = []
            for place in data.get('results', [])[:max_results]:
                business = {
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'address': place.get('formatted_address'),
                    'rating': place.get('rating'),
                    'lat': place.get('geometry', {}).get('location', {}).get('lat'),
                    'lng': place.get('geometry', {}).get('location', {}).get('lng')
                }
                
                # Get detailed info
                details = self.get_place_details(place['place_id'])
                business.update(details)
                
                businesses.append(business)
            
            self.stats['businesses_found'] = len(businesses)
            print(f"Found {len(businesses)} businesses\n")
            
            return businesses
            
        except Exception as e:
            print(f"Error finding businesses: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Dict:
        """Get detailed place information"""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'website,formatted_phone_number,email,business_status,opening_hours',
            'key': self.google_maps_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == 'OK':
                result = data.get('result', {})
                return {
                    'website': result.get('website'),
                    'phone': result.get('formatted_phone_number'),
                    'email': result.get('email'),
                    'status': result.get('business_status'),
                    'open_now': result.get('opening_hours', {}).get('open_now')
                }
        except:
            pass
        
        return {}
    
    def process_business(self, business: Dict, index: int, total: int) -> Optional[str]:
        """
        Process single business - find and validate email
        Returns validated email or None
        """
        print(f"\n[{index}/{total}] {business['name']}")
        print(f"{'─'*70}")
        print(f"Address: {business.get('address', 'N/A')}")
        print(f"Website: {business.get('website', 'N/A')}")
        print(f"Phone: {business.get('phone', 'N/A')}")
        if business.get('rating'):
            print(f"Rating: {business.get('rating')} stars")
        
        # STEP 1: Find email
        email = self.finder.find_email_multi_source(
            business_name=business['name'],
            website=business.get('website'),
            places_email=business.get('email')
        )
        
        if not email:
            print(f"  SKIP: No email found from any source")
            return None
        
        self.stats['emails_discovered'] += 1
        
        # STEP 2: Validate email (BULLETPROOF)
        domain = email.split('@')[1] if '@' in email else ''
        is_valid, reason, detailed_results = self.validator.validate_email_bulletproof(
            email=email,
            domain=domain
        )
        
        # Log validation
        self.stats['validation_log'].append({
            'business': business['name'],
            'email': email,
            'valid': is_valid,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        
        if is_valid:
            self.stats['emails_validated'] += 1
            return email
        else:
            self.stats['emails_rejected'] += 1
            print(f"  REJECTED: {reason}")
            return None
    
    def generate_email_content(self, business: Dict) -> str:
        """Generate personalized email content"""
        name = business.get('name', 'there')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">Partnership Opportunity</h1>
    </div>
    
    <div style="padding: 30px; background: #f9f9f9;">
        <p>Hi {name} team,</p>
        
        <p>I'm reaching out because we've created something that could add real value to your customer experience.</p>
        
        <p><strong>SayPlay</strong> lets people add personal voice messages to any gift - simply tap an NFC sticker with their phone to hear the message. No app needed.</p>
        
        <div style="background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #667eea;">Perfect for Your Customers</h3>
            <ul style="line-height: 1.8;">
                <li>Add a personal touch to every gift</li>
                <li>Unique product offering</li>
                <li>No inventory risk - we handle fulfillment</li>
                <li>Wholesale pricing with attractive margins</li>
            </ul>
        </div>
        
        <p>Would you be open to a brief 15-minute call to explore this?</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="https://calendly.com/sayplay/partnership" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Schedule a Call</a>
        </div>
        
        <p>Best regards,<br>
        <strong>SayPlay Partnership Team</strong><br>
        <a href="https://sayplay.gift" style="color: #667eea;">sayplay.gift</a></p>
    </div>
    
    <div style="background: #333; color: #999; padding: 20px; text-align: center; font-size: 12px;">
        <p>You're receiving this because we believe SayPlay could benefit your business.</p>
    </div>
</body>
</html>
"""
        return html
    
    def send_email_sendgrid(self, to_email: str, business: Dict) -> bool:
        """
        Send email via SendGrid
        FINAL safety check before sending
        """
        # FINAL VALIDATION before sending
        if '@' not in to_email or len(to_email) < 5:
            print(f"  BLOCKED at final check: Invalid format")
            return False
        
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                'Authorization': f'Bearer {self.sendgrid_key}',
                'Content-Type': 'application/json'
            }
            
            subject = f"Partnership Opportunity - {business['name']}"
            content = self.generate_email_content(business)
            
            data = {
                'personalizations': [{
                    'to': [{'email': to_email}],
                    'subject': subject
                }],
                'from': {
                    'email': 'partnerships@sayplay.gift',
                    'name': 'SayPlay Partnerships'
                },
                'content': [{
                    'type': 'text/html',
                    'value': content
                }],
                'tracking_settings': {
                    'click_tracking': {'enable': True},
                    'open_tracking': {'enable': True}
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 202:
                print(f"  EMAIL SENT to {to_email}")
                self.stats['emails_sent'] += 1
                return True
            else:
                print(f"  SendGrid error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"  Send error: {e}")
            return False
    
    def run_campaign(self,
                    location: str,
                    business_type: str,
                    max_businesses: int = 30,
                    max_emails_to_send: int = 5,
                    dry_run: bool = True) -> Dict:
        """
        Run complete B2B campaign
        
        Args:
            location: City or area
            business_type: Type of business (e.g., 'florist')
            max_businesses: Max businesses to find
            max_emails_to_send: Max emails to send (rate limiting)
            dry_run: If True, validate but don't send
        """
        print("\n" + "="*70)
        print("B2B HUNTER - BULLETPROOF CAMPAIGN")
        print("="*70)
        print(f"Location: {location}")
        print(f"Type: {business_type}")
        print(f"Max businesses: {max_businesses}")
        print(f"Max emails to send: {max_emails_to_send}")
        print(f"Mode: {'DRY RUN (no emails sent)' if dry_run else 'LIVE (will send emails)'}")
        print("="*70)
        
        # Find businesses
        businesses = self.find_businesses(location, business_type, max_businesses)
        
        if not businesses:
            print("\nNo businesses found")
            return self.stats
        
        # Process each business
        emails_sent_count = 0
        
        for i, business in enumerate(businesses, 1):
            if emails_sent_count >= max_emails_to_send:
                print(f"\nReached max emails limit ({max_emails_to_send})")
                break
            
            # Find and validate email
            validated_email = self.process_business(business, i, len(businesses))
            
            if not validated_email:
                continue
            
            # Send email (or dry run)
            if dry_run:
                print(f"  [DRY RUN] Would send to: {validated_email}")
                emails_sent_count += 1
            else:
                sent = self.send_email_sendgrid(validated_email, business)
                if sent:
                    emails_sent_count += 1
                    # Rate limiting - 3 seconds between emails
                    if emails_sent_count < max_emails_to_send:
                        time.sleep(3)
        
        # Final report
        self.print_final_report()
        
        # Save validation log
        try:
            self.validator.save_validation_log('b2b_validation_log.json')
        except:
            pass
        
        return self.stats
    
    def print_final_report(self):
        """Print detailed final report"""
        print("\n" + "="*70)
        print("CAMPAIGN COMPLETE - FINAL REPORT")
        print("="*70)
        print(f"Businesses found: {self.stats['businesses_found']}")
        print(f"Emails discovered: {self.stats['emails_discovered']}")
        print(f"Emails validated: {self.stats['emails_validated']}")
        print(f"Emails rejected: {self.stats['emails_rejected']}")
        print(f"Emails sent: {self.stats['emails_sent']}")
        print("─"*70)
        
        if self.stats['emails_discovered'] > 0:
            validation_rate = (self.stats['emails_validated'] / self.stats['emails_discovered']) * 100
            print(f"Validation success rate: {validation_rate:.1f}%")
        
        if self.stats['emails_validated'] > 0:
            send_rate = (self.stats['emails_sent'] / self.stats['emails_validated']) * 100
            print(f"Send success rate: {send_rate:.1f}%")
        
        print("="*70 + "\n")
