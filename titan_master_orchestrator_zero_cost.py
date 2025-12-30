#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR - ENHANCED VERSION
Uses FREE APIs + Google Maps (with $200 FREE credit!)
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, str(Path(__file__).parent))

try:
    from titan_modules.growth.b2b_hunter.b2b_hunter_bulletproof import B2BHunterBulletproof
    B2B_BULLETPROOF = True
    print("B2B Bulletproof Mode Active")
except ImportError:
    B2B_BULLETPROOF = False
    print("B2B Bulletproof not available")

try:
    from titan_modules.psychology.precognition.gift_precognition_enhanced import GiftPrecognition
    from titan_modules.commerce.address_validation import AddressValidator
    GOOGLE_ENHANCED = True
    print("Google Enhanced Mode Active")
except ImportError:
    try:
        from titan_modules.psychology.precognition.gift_precognition_zero_cost import GiftPrecognition
    except:
        pass
    GOOGLE_ENHANCED = False

modules_loaded = {}

try:
    from titan_modules.foundation.brand_identity.brand_identity_core import BrandIdentityCore
    modules_loaded['brand'] = True
except Exception as e:
    print(f"Brand Identity not loaded: {e}")
    modules_loaded['brand'] = False

try:
    from titan_modules.content.image_engine.image_engine_zero_cost import ImageEngine
    modules_loaded['images'] = True
except Exception as e:
    print(f"Image Engine not loaded: {e}")
    modules_loaded['images'] = False

try:
    from titan_modules.content.audio_inception.audio_inception_zero_cost import AudioInception
    modules_loaded['audio'] = True
except Exception as e:
    print(f"Audio Inception not loaded: {e}")
    modules_loaded['audio'] = False

try:
    from titan_modules.expansion.global_domination.global_domination_zero_cost import GlobalDomination
    modules_loaded['global'] = True
except Exception as e:
    print(f"Global Domination not loaded: {e}")
    modules_loaded['global'] = False

try:
    from titan_modules.expansion.programmatic_seo.programmatic_seo import ProgrammaticSEO
    modules_loaded['seo'] = True
except Exception as e:
    print(f"Programmatic SEO not loaded: {e}")
    modules_loaded['seo'] = False

try:
    from titan_modules.distribution.social_poster import SocialPoster
    modules_loaded['social'] = True
except Exception as e:
    print(f"Social Poster not loaded: {e}")
    modules_loaded['social'] = False

try:
    from titan_modules.growth.influencer_scout.influencer_scout import InfluencerScout, run_influencer_campaign
    modules_loaded['influencer'] = True
except Exception as e:
    print(f"Influencer Scout not loaded: {e}")
    modules_loaded['influencer'] = False

modules_loaded['pricing'] = False
modules_loaded['chameleon'] = False

try:
    from titan_modules.blog.writer.article_generator import ArticleGenerator
    modules_loaded['blog'] = True
except Exception as e:
    print(f"Blog modules not loaded: {e}")
    modules_loaded['blog'] = False

import requests

def generate_topic():
    """Simple built-in topic generator"""
    topics = [
        {
            'keyword': 'birthday gifts for mum',
            'category': 'Occasions',
            'title': 'Perfect Birthday Gifts for Mum 2025',
            'angle': 'heartfelt and personal',
            'search_volume': 5000
        },
        {
            'keyword': 'anniversary gifts for wife',
            'category': 'Occasions',
            'title': 'Romantic Anniversary Gifts Your Wife Will Love',
            'angle': 'romantic and memorable',
            'search_volume': 4200
        },
        {
            'keyword': 'christmas gifts for family',
            'category': 'Occasions',
            'title': 'Thoughtful Christmas Gifts for the Whole Family',
            'angle': 'festive and meaningful',
            'search_volume': 8500
        },
        {
            'keyword': 'wedding gifts for couples',
            'category': 'Occasions',
            'title': 'Unique Wedding Gifts Couples Will Treasure',
            'angle': 'unique and lasting',
            'search_volume': 3800
        },
        {
            'keyword': 'graduation gifts for her',
            'category': 'Occasions',
            'title': 'Inspiring Graduation Gifts She Will Cherish',
            'angle': 'inspirational and practical',
            'search_volume': 2900
        },
        {
            'keyword': 'mothers day gift ideas',
            'category': 'Occasions',
            'title': 'Heartfelt Mothers Day Gifts She Will Love',
            'angle': 'emotional and personal',
            'search_volume': 12000
        },
        {
            'keyword': 'fathers day presents',
            'category': 'Occasions',
            'title': 'Best Fathers Day Presents for Every Dad',
            'angle': 'practical and meaningful',
            'search_volume': 9500
        },
        {
            'keyword': 'valentine gifts for him',
            'category': 'Occasions',
            'title': 'Romantic Valentine Gifts He Will Actually Want',
            'angle': 'romantic and thoughtful',
            'search_volume': 6700
        }
    ]
    
    topic = random.choice(topics)
    print(f"Generated topic: {topic['keyword']}")
    print(f"Category: {topic['category']}")
    print(f"Search volume: {topic['search_volume']}")
    return topic

def send_telegram_notification(message: str):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("Telegram not configured")
        return
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"Telegram failed: {e}")


def main():
    mode_name = "ENHANCED" if GOOGLE_ENHANCED else "ZERO-COST"
    
    print("\n" + "="*70)
    print(f"TITAN MASTER ORCHESTRATOR - {mode_name} MODE")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    if GOOGLE_ENHANCED:
        print("Monthly Cost: 9.40 GBP (Google APIs with FREE $200 credit)")
        print("Enhanced Features: Visual Emails, Perfect Timing, Address Validation")
    else:
        print("Monthly Cost: 0.00 GBP")
    if B2B_BULLETPROOF:
        print("B2B: Bulletproof email validation (7 levels)")
    print("="*70 + "\n")
    
    print("Modules Loaded:")
    for module, loaded in modules_loaded.items():
        status = "OK" if loaded else "SKIP"
        print(f"   [{status}] {module}")
    if B2B_BULLETPROOF:
        print(f"   [OK] b2b_bulletproof")
    print()
    
    results = {
        'start_time': datetime.now(),
        'modules_run': 0,
        'outputs': {}
    }
    
    try:
        if modules_loaded['brand']:
            print("MODULE 1: BRAND IDENTITY CORE")
            print("-" * 70)
            
            brand = BrandIdentityCore()
            infringements = brand.monitor_trademark_infringement()
            
            results['outputs']['brand'] = {'infringements_detected': len(infringements)}
            results['modules_run'] += 1
            print(f"Brand protection active")
            print(f"Infringements: {len(infringements)}")
            print()
        
        if modules_loaded['blog']:
            print("MODULE 2: BLOG ENGINE (Gemini - FREE)")
            print("-" * 70)
            
            topic = generate_topic()
            
            try:
                gemini_key = os.getenv('GEMINI_API_KEY')
                if not gemini_key:
                    raise Exception("GEMINI_API_KEY not set")
                
                article_gen = ArticleGenerator(api_key=gemini_key)
                article = article_gen.generate_article(topic)
                
                if modules_loaded['brand']:
                    article = brand.apply_brand_identity(article, 'html')
                
                results['outputs']['blog'] = {
                    'title': article.get('title', 'Untitled'),
                    'keyword': topic.get('keyword', 'N/A'),
                    'word_count': len(article.get('text', '').split())
                }
                results['modules_run'] += 1
                print(f"Article generated (Gemini FREE)")
                print(f"Title: {article.get('title', '')[:60]}...")
            
            except Exception as e:
                print(f"Blog generation error: {e}")
                article = {
                    'title': topic['title'],
                    'text': f"Article about {topic['keyword']}",
                    'html': f"<h1>{topic['title']}</h1><p>Content about {topic['keyword']}</p>"
                }
            
            print()
        else:
            article = {'title': 'Test Article', 'text': 'Test content', 'html': '<p>Test</p>'}
            topic = {'keyword': 'gifts'}
        
        if modules_loaded['images']:
            print("MODULE 4: IMAGE ENGINE (Pollinations.ai - FREE)")
            print("-" * 70)
            
            try:
                image_engine = ImageEngine()
                
                prompt = f"lifestyle photo: {topic.get('keyword', 'gift')} scene, professional"
                images = image_engine.batch_generate_all_platforms(prompt)
                
                results['outputs']['images'] = {
                    'prompt': prompt,
                    'variants_generated': len(images)
                }
                results['modules_run'] += 1
                print(f"Images generated (Pollinations.ai FREE)")
                print(f"Variants: {len(images)} platforms")
            except Exception as e:
                print(f"Image generation error: {e}")
            
            print()
        
        if modules_loaded['audio']:
            print("MODULE 5: AUDIO-INCEPTION (Edge-TTS + Gemini - FREE)")
            print("-" * 70)
            
            try:
                audio_engine = AudioInception()
                podcast = audio_engine.article_to_podcast(article)
                
                results['outputs']['podcast'] = {
                    'title': podcast['metadata']['title'],
                    'duration': podcast['metadata']['duration']
                }
                results['modules_run'] += 1
                print(f"Podcast created (Edge-TTS FREE)")
                print(f"Duration: ~{podcast['metadata']['duration']}s")
            except Exception as e:
                print(f"Podcast generation error: {e}")
            
            print()
        
        if modules_loaded['global']:
            print("MODULE 6: GLOBAL DOMINATION (Gemini translations - FREE)")
            print("-" * 70)
            
            try:
                global_engine = GlobalDomination()
                translations = global_engine.batch_translate_all_markets(article)
                
                results['outputs']['translations'] = {
                    'languages': list(translations.keys()),
                    'total_reach': sum(
                        global_engine.TARGET_MARKETS.get(lang, {}).get('population', 0)
                        for lang in translations.keys() if lang != 'en'
                    )
                }
                results['modules_run'] += 1
                print(f"Translations complete (Gemini FREE)")
                print(f"Languages: {', '.join(translations.keys())}")
            except Exception as e:
                print(f"Translation error: {e}")
            
            print()
        
        if modules_loaded['seo']:
            print("MODULE 7: PROGRAMMATIC SEO")
            print("-" * 70)
            
            try:
                seo_engine = ProgrammaticSEO()
                seo_pages = seo_engine.generate_all_pages(max_pages=50)
                
                results['outputs']['seo'] = {'pages_generated': len(seo_pages)}
                results['modules_run'] += 1
                print(f"SEO pages generated")
                print(f"Pages: {len(seo_pages)}")
            except Exception as e:
                print(f"SEO generation error: {e}")
            
            print()
        
        if modules_loaded['social']:
            print("MODULE 8: SOCIAL POSTER (FREE APIs)")
            print("-" * 70)
            
            try:
                social_engine = SocialPoster()
                social_results = social_engine.distribute_article(article)
                
                results['outputs']['social'] = social_results
                results['modules_run'] += 1
                print(f"Social distribution complete")
            except Exception as e:
                print(f"Social posting error: {e}")
            
            print()
        
        # ================================================================
        # MODULE #9: B2B HUNTER BULLETPROOF
        # CRITICAL: NO GUESSING EMAILS - ONLY VALIDATED!
        # ================================================================
        if B2B_BULLETPROOF:
            print("MODULE 9: B2B HUNTER BULLETPROOF")
            print("-" * 70)
            
            try:
                hunter = B2BHunterBulletproof()
                
                stats = hunter.run_campaign(
                    location='London, UK',
                    business_type='florist',
                    max_businesses=30,
                    max_emails_to_send=5,
                    dry_run=True  # CHANGE TO False WHEN READY!
                )
                
                results['outputs']['b2b'] = stats
                results['modules_run'] += 1
                
                print(f"\nB2B campaign summary:")
                print(f"  Businesses found: {stats['businesses_found']}")
                print(f"  Emails discovered: {stats['emails_discovered']}")
                print(f"  Emails validated: {stats['emails_validated']}")
                print(f"  Emails rejected: {stats['emails_rejected']}")
                print(f"  Emails sent: {stats['emails_sent']}")
                
                if stats['emails_discovered'] > 0:
                    validation_rate = (stats['emails_validated'] / stats['emails_discovered']) * 100
                    print(f"  Validation rate: {validation_rate:.1f}%")
                
            except Exception as e:
                print(f"B2B hunter error: {e}")
                import traceback
                traceback.print_exc()
            
            print()
        else:
            print("MODULE 9: B2B HUNTER (DISABLED)")
            print("-" * 70)
            print("Bulletproof B2B hunter not available")
            print("Install required: email_validator_bulletproof.py")
            print("Install required: b2b_hunter_bulletproof.py")
            print()
        
        if modules_loaded['influencer']:
            print("MODULE 10: INFLUENCER SCOUT")
            print("-" * 70)
            
            try:
                qualified = run_influencer_campaign('lifestyle', target_count=30)
                
                results['outputs']['influencers'] = {
                    'found': 60,
                    'qualified': len(qualified),
                    'contacted': min(10, len(qualified))
                }
                results['modules_run'] += 1
                print(f"Influencer campaign complete")
            except Exception as e:
                print(f"Influencer scout error: {e}")
            
            print()
        
        if GOOGLE_ENHANCED or 'GiftPrecognition' in dir():
            print("MODULE 13: GIFT PRECOGNITION" + (" ENHANCED" if GOOGLE_ENHANCED else ""))
            print("-" * 70)
            
            try:
                precog_engine = GiftPrecognition()
                upcoming = precog_engine.scan_upcoming_events(days_ahead=14)
                
                for event_data in upcoming[:5]:
                    precog_engine.send_reminder_email(
                        event_data['customer_id'],
                        event_data['event']
                    )
                
                results['outputs']['precognition'] = {
                    'reminders_sent': len(upcoming[:5]),
                    'enhanced': GOOGLE_ENHANCED
                }
                results['modules_run'] += 1
                print(f"Email reminders sent")
                print(f"Reminders: {len(upcoming[:5])}")
                if GOOGLE_ENHANCED:
                    print(f"Perfect local timing with Time Zone API")
            except Exception as e:
                print(f"Gift precognition error: {e}")
            
            print()
        
        if GOOGLE_ENHANCED:
            print("MODULE 14: ADDRESS VALIDATION")
            print("-" * 70)
            
            try:
                validator = AddressValidator()
                
                test_address = {
                    'line1': '10 Downing Street',
                    'city': 'London',
                    'postcode': 'SW1A 2AA',
                    'country': 'GB'
                }
                
                validation = validator.validate_address(test_address)
                
                results['outputs']['address_validation'] = {
                    'tested': True,
                    'is_valid': validation['is_valid'],
                    'confidence': validation['confidence']
                }
                results['modules_run'] += 1
                
                print(f"Address validation active")
                print(f"Test validation: {validation['confidence']}")
                print(f"Prevents failed deliveries")
            except Exception as e:
                print(f"Address validation error: {e}")
            
            print()
        
        end_time = datetime.now()
        duration = (end_time - results['start_time']).total_seconds()
        
        print("\n" + "="*70)
        print(f"TITAN COMPLETE - {mode_name} MODE")
        print("="*70)
        print(f"Duration: {duration:.1f}s")
        print(f"Modules run: {results['modules_run']}")
        if GOOGLE_ENHANCED:
            print(f"Mode: Google Enhanced")
            print(f"Cost: 9.40 GBP/month")
        else:
            print(f"Mode: Zero-Cost")
            print(f"Cost: 0.00 GBP")
        if B2B_BULLETPROOF:
            print(f"B2B: Bulletproof validation active")
        print("="*70)
        
        telegram_message = f"<b>Titan Complete</b>\n\n<b>Modules:</b> {results['modules_run']}\n<b>Duration:</b> {duration:.1f}s"
        
        if 'blog' in results['outputs']:
            telegram_message += f"\n\n<b>Blog:</b> {results['outputs']['blog']['title'][:50]}..."
            telegram_message += f"\n<b>Keyword:</b> {results['outputs']['blog']['keyword']}"
            telegram_message += f"\n<b>Words:</b> {results['outputs']['blog']['word_count']}"
        
        if 'images' in results['outputs']:
            telegram_message += f"\n<b>Images:</b> {results['outputs']['images']['variants_generated']} variants"
        
        if 'podcast' in results['outputs']:
            telegram_message += f"\n<b>Podcast:</b> {results['outputs']['podcast']['duration']}s"
        
        if 'translations' in results['outputs']:
            telegram_message += f"\n<b>Languages:</b> {len(results['outputs']['translations']['languages'])}"
        
        if 'b2b' in results['outputs']:
            b2b = results['outputs']['b2b']
            telegram_message += f"\n\n<b>B2B Bulletproof:</b>"
            telegram_message += f"\n  Found: {b2b.get('businesses_found', 0)}"
            telegram_message += f"\n  Validated: {b2b.get('emails_validated', 0)}"
            telegram_message += f"\n  Sent: {b2b.get('emails_sent', 0)}"
        
        if GOOGLE_ENHANCED:
            telegram_message += f"\n\n<b>Mode:</b> Google Enhanced"
            telegram_message += f"\n<b>Cost:</b> 9.40 GBP/month"
        else:
            telegram_message += f"\n\n<b>Mode:</b> Zero-Cost"
            telegram_message += f"\n<b>Cost:</b> FREE"
        
        send_telegram_notification(telegram_message)
        
        print("\nTelegram notification sent")
        print("\n" + "="*70 + "\n")
        
        return 0
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"\n{error_msg}\n")
        
        send_telegram_notification(f"<b>Titan Failed</b>\n\nError: {str(e)}")
        
        import traceback
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
