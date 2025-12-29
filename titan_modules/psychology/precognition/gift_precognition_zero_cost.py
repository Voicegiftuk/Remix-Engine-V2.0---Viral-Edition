#!/usr/bin/env python3
"""
TITAN MODULE #13: GIFT PRECOGNITION (ZERO-COST VERSION)
Uses EMAIL instead of SMS - FREE with SendGrid (100/day)
"""
import os
import sys
import json
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class Logger:
    @staticmethod
    def info(msg): print(f"🔮 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class GiftPrecognition:
    """Gift reminder system using FREE email (SendGrid)"""
    
    # Gift suggestions by occasion
    GIFT_SUGGESTIONS = {
        'birthday': {
            'mother': {'product': 'Premium Card - Mother\'s Love', 'price': '£24.99'},
            'father': {'product': 'Premium Card - Dad\'s Wisdom', 'price': '£24.99'},
            'partner': {'product': 'Romance Collection', 'price': '£29.99'},
            'friend': {'product': 'Fun Collection', 'price': '£19.99'},
            'default': {'product': 'Premium Card', 'price': '£24.99'}
        },
        'anniversary': {
            'partner': {'product': 'Anniversary Special', 'price': '£34.99'},
            'default': {'product': 'Romance Collection', 'price': '£29.99'}
        },
        'christmas': {
            'default': {'product': 'Christmas Collection', 'price': '£29.99'}
        },
        'mothers_day': {
            'default': {'product': 'Mother\'s Day Special', 'price': '£27.99'}
        },
        'fathers_day': {
            'default': {'product': 'Father\'s Day Special', 'price': '£27.99'}
        }
    }
    
    def __init__(self):
        """Initialize zero-cost reminder system"""
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        self.database_path = Path('gift_precognition_db.json')
        self.database = self._load_database()
        
        logger.info("Gift Precognition initialized (Zero-Cost Mode)")
        logger.info("Using EMAIL reminders (FREE with SendGrid - 100/day)")
    
    def add_important_date(
        self,
        customer_id: str,
        event_data: Dict
    ):
        """Add important date to track"""
        
        if customer_id not in self.database['customers']:
            self.database['customers'][customer_id] = {
                'email': event_data.get('email', ''),
                'name': event_data.get('name', ''),
                'events': []
            }
        
        event = {
            'event_id': f"evt_{len(self.database['customers'][customer_id]['events']) + 1}",
            'type': event_data.get('type', 'birthday'),
            'date': event_data.get('date'),  # MM-DD format
            'recipient_name': event_data.get('recipient_name', ''),
            'relationship': event_data.get('relationship', ''),
            'reminder_sent': False,
            'last_gift': None
        }
        
        self.database['customers'][customer_id]['events'].append(event)
        self._save_database()
        
        logger.success(f"Added event: {event['type']} for {event['recipient_name']}")
    
    def scan_upcoming_events(self, days_ahead: int = 14) -> List[Dict]:
        """Scan for events happening in next N days"""
        
        logger.info(f"Scanning for events in next {days_ahead} days...")
        
        today = datetime.now()
        upcoming = []
        
        for customer_id, customer in self.database['customers'].items():
            for event in customer['events']:
                if event['reminder_sent']:
                    continue
                
                # Parse event date (MM-DD format)
                try:
                    month, day = map(int, event['date'].split('-'))
                    
                    # Create date for this year
                    event_date = datetime(today.year, month, day)
                    
                    # If event already passed this year, use next year
                    if event_date < today:
                        event_date = datetime(today.year + 1, month, day)
                    
                    # Calculate days until event
                    days_until = (event_date - today).days
                    
                    # Check if within reminder window
                    if 0 <= days_until <= days_ahead:
                        upcoming.append({
                            'customer_id': customer_id,
                            'customer_name': customer['name'],
                            'customer_email': customer['email'],
                            'event': event,
                            'days_until': days_until
                        })
                        
                except Exception as e:
                    logger.error(f"Date parse error: {e}")
                    continue
        
        logger.success(f"Found {len(upcoming)} upcoming events")
        return upcoming
    
    def send_reminder_email(self, customer_id: str, event: Dict) -> bool:
        """Send reminder EMAIL using SendGrid (FREE)"""
        
        customer = self.database['customers'].get(customer_id)
        if not customer:
            logger.error(f"Customer not found: {customer_id}")
            return False
        
        email = customer['email']
        name = customer['name']
        
        logger.info(f"Sending reminder to {email}...")
        
        # Get gift suggestion
        suggestion = self.suggest_gift(event, customer)
        
        # Calculate days until
        today = datetime.now()
        month, day = map(int, event['date'].split('-'))
        event_date = datetime(today.year, month, day)
        if event_date < today:
            event_date = datetime(today.year + 1, month, day)
        days_until = (event_date - today).days
        
        # Create email content
        subject = f"🎁 Don't Forget: {event['recipient_name']}'s {event['type'].title()} in {days_until} Days!"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
        .gift-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 10px; 
                    border-left: 4px solid #667eea; }}
        .cta-button {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px;
                      font-weight: bold; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎁 Gift Reminder</h1>
        </div>
        
        <div class="content">
            <p>Hi {name}! 👋</p>
            
            <p><strong>{event['recipient_name']}'s {event['type'].title()}</strong> is in just <strong>{days_until} days</strong>!</p>
            
            <p>Don't let this special moment pass without showing them you care. We have the perfect gift ready for you:</p>
            
            <div class="gift-box">
                <h3>🎁 {suggestion['product']}</h3>
                <p style="font-size: 1.3em; color: #667eea; font-weight: bold;">{suggestion['price']}</p>
                <p>{suggestion['message_idea']}</p>
            </div>
            
            <p>With SayPlay, you can record a personal voice message that {event['recipient_name']} can keep forever. 
            Just tap the card with their phone - no app needed.</p>
            
            <p style="text-align: center;">
                <a href="https://sayplay.co.uk/shop?ref=reminder" class="cta-button">
                    Create Your Gift Now →
                </a>
            </p>
            
            <p style="margin-top: 30px; font-size: 0.9em; color: #666;">
                <em>This is the gift they'll treasure forever. Your voice. Your emotions. Captured in a moment.</em>
            </p>
        </div>
        
        <div class="footer">
            <p>SayPlay™ - Voice Message Gifts That Last Forever</p>
            <p>© 2025 SayPlay. All rights reserved.</p>
            <p style="font-size: 0.8em; margin-top: 10px;">
                <a href="https://sayplay.co.uk/unsubscribe" style="color: #666;">Unsubscribe from reminders</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        text_content = f"""Hi {name}!

{event['recipient_name']}'s {event['type'].title()} is in just {days_until} days!

Don't let this special moment pass. We recommend:

{suggestion['product']} - {suggestion['price']}
{suggestion['message_idea']}

Order now: https://sayplay.co.uk/shop?ref=reminder

With SayPlay, you can record a personal voice message that {event['recipient_name']} 
can keep forever. Just tap the card with their phone - no app needed.

- The SayPlay Team
"""
        
        # Send email
        sent = self._send_email_via_sendgrid(email, subject, html_content, text_content)
        
        if sent:
            # Mark reminder as sent
            event['reminder_sent'] = True
            event['reminder_sent_at'] = datetime.now().isoformat()
            self._save_database()
            
            logger.success(f"Reminder sent to {email}")
        
        return sent
    
    def _send_email_via_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str
    ) -> bool:
        """Send email using SendGrid (FREE 100/day)"""
        
        if not self.sendgrid_key:
            logger.warning("SendGrid not configured - email not sent")
            return False
        
        try:
            import requests
            
            url = "https://api.sendgrid.com/v3/mail/send"
            
            headers = {
                'Authorization': f'Bearer {self.sendgrid_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'personalizations': [{
                    'to': [{'email': to_email}]
                }],
                'from': {
                    'email': 'reminders@sayplay.co.uk',
                    'name': 'SayPlay Gift Reminders'
                },
                'subject': subject,
                'content': [
                    {
                        'type': 'text/plain',
                        'value': text_content
                    },
                    {
                        'type': 'text/html',
                        'value': html_content
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 202:
                logger.success(f"Email sent: {response.status_code}")
                return True
            else:
                logger.error(f"SendGrid error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
    
    def suggest_gift(self, event: Dict, customer: Dict) -> Dict:
        """Suggest appropriate gift for occasion"""
        
        event_type = event['type']
        relationship = event['relationship']
        
        # Get suggestions for this event type
        event_suggestions = self.GIFT_SUGGESTIONS.get(event_type, {})
        
        # Try to match relationship
        suggestion = event_suggestions.get(
            relationship,
            event_suggestions.get('default', {'product': 'Premium Card', 'price': '£24.99'})
        )
        
        # Add message idea
        message_ideas = {
            'birthday': f"Record a happy birthday message that {event['recipient_name']} can replay forever",
            'anniversary': f"Share your favorite memory together",
            'christmas': f"Record a warm Christmas greeting",
            'mothers_day': "Tell her how much she means to you",
            'fathers_day': "Share what you've learned from him"
        }
        
        suggestion['message_idea'] = message_ideas.get(
            event_type,
            f"Record a heartfelt message for {event['recipient_name']}"
        )
        
        return suggestion
    
    def track_purchase(self, customer_id: str, event_id: str, product: str):
        """Track when customer purchases gift"""
        
        customer = self.database['customers'].get(customer_id)
        if not customer:
            return
        
        for event in customer['events']:
            if event['event_id'] == event_id:
                event['last_gift'] = {
                    'product': product,
                    'purchased_at': datetime.now().isoformat()
                }
                break
        
        self._save_database()
        logger.info(f"Purchase tracked: {product}")
    
    def reset_annual_reminders(self):
        """Reset reminder flags for new year"""
        
        logger.info("Resetting annual reminders...")
        
        for customer in self.database['customers'].values():
            for event in customer['events']:
                event['reminder_sent'] = False
        
        self._save_database()
        logger.success("Annual reminders reset")
    
    def _load_database(self) -> Dict:
        """Load customer database"""
        
        if self.database_path.exists():
            with open(self.database_path, 'r') as f:
                return json.load(f)
        
        return {'customers': {}}
    
    def _save_database(self):
        """Save customer database"""
        
        with open(self.database_path, 'w') as f:
            json.dump(self.database, f, indent=2)


def daily_reminder_check():
    """Run daily to check and send reminders"""
    
    precog = GiftPrecognition()
    
    # Scan for events in next 14 days
    upcoming = precog.scan_upcoming_events(days_ahead=14)
    
    # Send reminders
    for event_data in upcoming:
        precog.send_reminder_email(
            event_data['customer_id'],
            event_data['event']
        )
    
    logger.info(f"Daily check complete: {len(upcoming)} reminders sent")


if __name__ == "__main__":
    """Test zero-cost gift precognition"""
    
    print("\n🧪 Testing ZERO-COST Gift Precognition...\n")
    
    precog = GiftPrecognition()
    
    # Test 1: Add important date
    print("Test 1: Adding important date")
    precog.add_important_date('cust_001', {
        'type': 'birthday',
        'date': '01-20',  # January 20
        'recipient_name': 'Mum',
        'relationship': 'mother',
        'email': 'test@example.com',
        'name': 'John Smith'
    })
    print("✓ Date added")
    
    # Test 2: Scan upcoming events
    print("\nTest 2: Scanning upcoming events")
    upcoming = precog.scan_upcoming_events(days_ahead=30)
    print(f"✓ Found {len(upcoming)} upcoming events")
    
    # Test 3: Gift suggestion
    print("\nTest 3: Gift suggestion")
    if upcoming:
        event = upcoming[0]
        suggestion = precog.suggest_gift(event['event'], {})
        print(f"✓ Suggestion: {suggestion['product']} - {suggestion['price']}")
        print(f"  Idea: {suggestion['message_idea']}")
    
    print("\n✅ Zero-cost gift precognition test complete!")
    print("💰 Cost: £0.00 (SendGrid free 100/day)")
    print("📧 Email reminders instead of SMS!")
