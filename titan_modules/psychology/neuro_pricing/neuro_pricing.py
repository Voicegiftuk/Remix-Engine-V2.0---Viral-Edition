#!/usr/bin/env python3
"""
TITAN MODULE #11: NEURO-PRICING
Dynamic pricing based on device, location, browsing behavior, and psychological triggers
"""
import os
import sys
from typing import Dict, Optional
from datetime import datetime
import hashlib

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pathlib import Path

class Logger:
    @staticmethod
    def info(msg): print(f"💰 {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class NeuroPricing:
    """Dynamic pricing optimization engine"""
    
    # Base prices (£)
    BASE_PRICES = {
        'single_card': 19.99,
        'premium_card': 29.99,
        'bundle_3': 49.99,
        'bundle_5': 74.99,
        'business_100': 1499.99
    }
    
    # Device multipliers
    DEVICE_MULTIPLIERS = {
        'iphone_15_pro': 1.20,      # Latest iPhone: +20%
        'iphone_14': 1.15,           # Recent iPhone: +15%
        'iphone_13': 1.10,           # Older iPhone: +10%
        'iphone': 1.05,              # Generic iPhone: +5%
        'android_samsung_s24': 1.10, # Flagship Android: +10%
        'android_flagship': 1.05,    # Other flagship: +5%
        'android': 1.00,             # Generic Android: 0%
        'desktop_mac': 1.15,         # MacBook: +15%
        'desktop_windows': 1.05,     # Windows: +5%
        'tablet': 1.00               # Tablet: 0%
    }
    
    # Location multipliers
    LOCATION_MULTIPLIERS = {
        'london_central': 1.25,      # Central London: +25%
        'london_outer': 1.15,        # Outer London: +15%
        'manchester': 1.10,          # Major cities: +10%
        'birmingham': 1.10,
        'edinburgh': 1.10,
        'uk_affluent': 1.15,         # Affluent areas: +15%
        'uk_standard': 1.00,         # Standard UK: 0%
        'international': 1.20        # International: +20%
    }
    
    # Time-based multipliers
    TIME_MULTIPLIERS = {
        'christmas_season': 1.30,    # Dec 1-24: +30%
        'valentines': 1.25,          # Feb 1-14: +25%
        'mothers_day': 1.25,         # March: +25%
        'black_friday': 0.80,        # Nov 24-30: -20%
        'peak_hours': 1.05,          # 12-8 PM: +5%
        'off_hours': 0.95,           # 12-6 AM: -5%
        'weekend': 1.10,             # Sat-Sun: +10%
        'standard': 1.00
    }
    
    # Behavioral multipliers
    BEHAVIOR_MULTIPLIERS = {
        'first_visit': 0.90,         # First-time: -10% (acquire)
        'returning_no_purchase': 0.85, # Returner: -15% (convert)
        'cart_abandoner': 0.75,      # Abandoned cart: -25% (recover)
        'previous_buyer': 1.10,      # Repeat customer: +10% (LTV)
        'high_value_buyer': 1.20,    # High LTV: +20%
        'frequent_visitor': 1.00,    # Frequent: 0% (neutral)
        'quick_buyer': 1.15          # Fast decision: +15%
    }
    
    def __init__(self):
        """Initialize pricing engine"""
        logger.info("NeuroPricing initialized")
    
    def calculate_dynamic_price(
        self, 
        product: str, 
        visitor_data: Dict,
        behavior_profile: Optional[Dict] = None
    ) -> Dict:
        """Calculate optimized price for visitor"""
        
        base_price = self.BASE_PRICES.get(product, 19.99)
        
        # Detect context
        device_type = self._detect_device_tier(visitor_data)
        location_tier = self._detect_location_tier(visitor_data)
        time_context = self._get_time_context()
        behavior_segment = self._analyze_behavior(visitor_data, behavior_profile)
        
        # Apply multipliers
        device_mult = self.DEVICE_MULTIPLIERS.get(device_type, 1.00)
        location_mult = self.LOCATION_MULTIPLIERS.get(location_tier, 1.00)
        time_mult = self.TIME_MULTIPLIERS.get(time_context, 1.00)
        behavior_mult = self.BEHAVIOR_MULTIPLIERS.get(behavior_segment, 1.00)
        
        # Calculate final price
        final_price = base_price * device_mult * location_mult * time_mult * behavior_mult
        
        # Apply psychological pricing
        final_price = self._apply_psychological_pricing(final_price)
        
        # Calculate discount perception
        original_price = base_price * 1.40  # Show "original" as 40% higher
        discount_pct = int(((original_price - final_price) / original_price) * 100)
        
        result = {
            'product': product,
            'base_price': round(base_price, 2),
            'final_price': round(final_price, 2),
            'original_price': round(original_price, 2),
            'discount_percent': discount_pct,
            'you_save': round(original_price - final_price, 2),
            'multipliers': {
                'device': f"{device_mult:.2f}x ({device_type})",
                'location': f"{location_mult:.2f}x ({location_tier})",
                'time': f"{time_mult:.2f}x ({time_context})",
                'behavior': f"{behavior_mult:.2f}x ({behavior_segment})"
            },
            'pricing_strategy': self._get_pricing_strategy(behavior_segment),
            'urgency_message': self._generate_urgency_message(time_context, behavior_segment)
        }
        
        logger.success(f"Price: £{result['final_price']} (was £{result['original_price']})")
        return result
    
    def _detect_device_tier(self, visitor_data: Dict) -> str:
        """Detect device sophistication level"""
        
        user_agent = visitor_data.get('user_agent', '').lower()
        
        # iPhone detection (most specific first)
        if 'iphone' in user_agent:
            if '15' in user_agent and 'pro' in user_agent:
                return 'iphone_15_pro'
            elif '15' in user_agent:
                return 'iphone_14'  # Treat as premium
            elif '14' in user_agent:
                return 'iphone_14'
            elif '13' in user_agent:
                return 'iphone_13'
            else:
                return 'iphone'
        
        # Android detection
        elif 'android' in user_agent:
            if 's24' in user_agent or 's23' in user_agent:
                return 'android_samsung_s24'
            elif 'pixel' in user_agent or 'galaxy' in user_agent:
                return 'android_flagship'
            else:
                return 'android'
        
        # Desktop detection
        elif 'macintosh' in user_agent or 'mac os' in user_agent:
            return 'desktop_mac'
        elif 'windows' in user_agent:
            return 'desktop_windows'
        elif 'ipad' in user_agent or 'tablet' in user_agent:
            return 'tablet'
        
        return 'android'  # Default fallback
    
    def _detect_location_tier(self, visitor_data: Dict) -> str:
        """Detect location affluence level"""
        
        city = visitor_data.get('city', '').lower()
        postcode = visitor_data.get('postcode', '').upper()
        country = visitor_data.get('country', '').upper()
        
        # UK affluent postcodes (partial list)
        affluent_prefixes = ['SW1', 'SW3', 'SW7', 'W1', 'W8', 'W11', 'NW3', 'NW8']
        
        if postcode:
            if any(postcode.startswith(prefix) for prefix in affluent_prefixes):
                return 'uk_affluent'
        
        # Cities
        if 'london' in city:
            if any(area in city for area in ['central', 'westminster', 'kensington']):
                return 'london_central'
            else:
                return 'london_outer'
        elif city in ['manchester', 'birmingham', 'edinburgh', 'bristol']:
            return city
        elif country == 'GB' or country == 'UK':
            return 'uk_standard'
        else:
            return 'international'
    
    def _get_time_context(self) -> str:
        """Get time-based pricing context"""
        
        now = datetime.now()
        month = now.month
        day = now.day
        weekday = now.weekday()
        hour = now.hour
        
        # Seasonal events
        if month == 12 and day <= 24:
            return 'christmas_season'
        elif month == 2 and day <= 14:
            return 'valentines'
        elif month == 3 and 15 <= day <= 31:
            return 'mothers_day'
        elif month == 11 and 24 <= day <= 30:
            return 'black_friday'
        
        # Weekend
        if weekday >= 5:  # Saturday, Sunday
            return 'weekend'
        
        # Time of day
        if 12 <= hour < 20:
            return 'peak_hours'
        elif 0 <= hour < 6:
            return 'off_hours'
        
        return 'standard'
    
    def _analyze_behavior(self, visitor_data: Dict, behavior_profile: Optional[Dict]) -> str:
        """Analyze visitor behavior pattern"""
        
        if not behavior_profile:
            return 'first_visit'
        
        visit_count = behavior_profile.get('visit_count', 0)
        purchase_count = behavior_profile.get('purchase_count', 0)
        cart_abandonment_count = behavior_profile.get('cart_abandonment_count', 0)
        total_spent = behavior_profile.get('total_spent', 0)
        time_on_site = behavior_profile.get('time_on_site', 0)
        
        # High-value buyer
        if total_spent > 200:
            return 'high_value_buyer'
        
        # Previous buyer
        if purchase_count > 0:
            return 'previous_buyer'
        
        # Cart abandoner
        if cart_abandonment_count > 0:
            return 'cart_abandoner'
        
        # Quick buyer (< 5 min on site before purchase)
        if time_on_site < 300 and purchase_count > 0:
            return 'quick_buyer'
        
        # Returning no purchase
        if visit_count > 1 and purchase_count == 0:
            return 'returning_no_purchase'
        
        # Frequent visitor
        if visit_count > 5:
            return 'frequent_visitor'
        
        # First visit (default)
        return 'first_visit'
    
    def _apply_psychological_pricing(self, price: float) -> float:
        """Apply .99 / .95 pricing psychology"""
        
        # Round to nearest .99 or .95
        if price < 20:
            # Use .99 for lower prices
            return int(price) + 0.99
        elif price < 50:
            # Use .95 for mid-range
            return int(price) + 0.95
        else:
            # Round to .99 for higher prices
            return int(price) + 0.99
    
    def _get_pricing_strategy(self, behavior_segment: str) -> str:
        """Get pricing strategy explanation"""
        
        strategies = {
            'first_visit': 'Acquisition discount to convert new customer',
            'returning_no_purchase': 'Conversion incentive for returning visitor',
            'cart_abandoner': 'Recovery discount to complete abandoned purchase',
            'previous_buyer': 'Loyalty premium (customer willing to pay more)',
            'high_value_buyer': 'Premium pricing for high LTV customer',
            'frequent_visitor': 'Standard pricing for engaged prospect',
            'quick_buyer': 'Premium pricing (decisive buyer, low friction)'
        }
        
        return strategies.get(behavior_segment, 'Standard pricing')
    
    def _generate_urgency_message(self, time_context: str, behavior_segment: str) -> str:
        """Generate urgency message"""
        
        if time_context == 'christmas_season':
            return '🎄 Order before Dec 20 for Christmas delivery!'
        elif time_context == 'valentines':
            return '💝 Valentine\'s Day is approaching - order today!'
        elif time_context == 'black_friday':
            return '🔥 Black Friday Special - Ends Soon!'
        elif behavior_segment == 'cart_abandoner':
            return '⏰ Your cart is waiting - complete your order now!'
        elif behavior_segment == 'first_visit':
            return '🎁 Welcome offer - Limited time only!'
        else:
            return '📦 Order today for fast delivery'


if __name__ == "__main__":
    """Test neuro-pricing"""
    
    print("\n🧪 Testing Neuro-Pricing...\n")
    
    engine = NeuroPricing()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'iPhone 15 Pro, Central London, First Visit',
            'visitor': {
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 iPhone 15 Pro',
                'city': 'London Central',
                'postcode': 'SW1A 1AA',
                'country': 'GB'
            },
            'behavior': {
                'visit_count': 1,
                'purchase_count': 0
            }
        },
        {
            'name': 'Android, Manchester, Cart Abandoner',
            'visitor': {
                'user_agent': 'Mozilla/5.0 (Linux; Android 13)',
                'city': 'Manchester',
                'country': 'GB'
            },
            'behavior': {
                'visit_count': 3,
                'cart_abandonment_count': 1,
                'purchase_count': 0
            }
        },
        {
            'name': 'MacBook, London, High-Value Buyer',
            'visitor': {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'city': 'London',
                'postcode': 'W1',
                'country': 'GB'
            },
            'behavior': {
                'visit_count': 5,
                'purchase_count': 3,
                'total_spent': 250
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print("-" * 60)
        
        result = engine.calculate_dynamic_price(
            'single_card',
            scenario['visitor'],
            scenario['behavior']
        )
        
        print(f"  Base Price:     £{result['base_price']}")
        print(f"  Final Price:    £{result['final_price']}")
        print(f"  Original Price: £{result['original_price']}")
        print(f"  Discount:       {result['discount_percent']}% off")
        print(f"  You Save:       £{result['you_save']}")
        print(f"\n  Multipliers:")
        for key, value in result['multipliers'].items():
            print(f"    {key.capitalize()}: {value}")
        print(f"\n  Strategy: {result['pricing_strategy']}")
        print(f"  Urgency: {result['urgency_message']}")
    
    print("\n✅ Neuro-Pricing test complete!")
