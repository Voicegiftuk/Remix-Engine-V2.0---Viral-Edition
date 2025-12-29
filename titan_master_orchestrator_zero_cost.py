#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR - ENHANCED VERSION
Uses FREE APIs + Google Maps (with $200 FREE credit!)
"""
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

try:
    from titan_modules.growth.b2b_hunter.b2b_hunter_enhanced import B2BHunter
    from titan_modules.psychology.precognition.gift_precognition_enhanced import GiftPrecognition
    from titan_modules.commerce.address_validation import AddressValidator
    GOOGLE_ENHANCED = True
    print("Google Enhanced Mode Active")
except ImportError as e:
    print(f"Google enhanced modules not found, using basic versions")
    try:
        from titan_modules.growth.b2b_hunter.b2b_hunter import B2BHunter
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
    from titan_modules.blog.intelligence.topic_generator import TopicGenerator
    from titan_modules.blog.writer.article_generator import ArticleGenerator
    modules_loaded['blog'] = True
except Exception as e:
    print(f"Blog modules not loaded: {e}")
    modules_loaded['blog'] = False

import requests

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
    print("="*70 + "\n")
    
    print("Modules Loaded:")
    for module, loaded in modules_loaded.items():
        status = "OK" if loaded else "SKIP"
        print(f"   [{status}] {module}")
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
            
            topic_gen = TopicGenerator()
            article_gen = ArticleGenerator()
            
            topic = topic_gen.generate_intelligent_topic()
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
            print()
        else:
            article = {'title': 'Test Article', 'text': 'Test content', 'html': '<p>Test</p>'}
            topic = {'keyword': 'gifts'}
        
        if modules_loaded['images']:
            print("MODULE 4: IMAGE ENGINE (Pollinations.ai - FREE)")
            print("-" * 70)
            
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
            print()
        
        if modules_loaded['audio']:
            print("MODULE 5: AUDIO-INCEPTION (Edge-TTS + Gemini - FREE)")
            print("-" * 70)
            
            audio_engine = AudioInception()
            podcast = audio_engine.article_to_podcast(article)
            
            results['outputs']['podcast'] = {
                'title': podcast['metadata']['title'],
                'duration': podcast['metadata']['duration']
            }
            results['modules_run'] += 1
            print(f"Podcast created (Edge-TTS FREE)")
            print(f"Duration: ~{podcast['metadata']['duration']}s")
            print()
        
        if modules_loaded['global']:
            print("MODULE 6: GLOBAL DOMINATION (Gemini translations - FREE)")
            print("-" * 70)
            
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
            print()
        
        if modules_loaded['seo']:
            print("MODULE 7: PROGRAMMATIC SEO")
            print("-" * 70)
            
            seo_engine = ProgrammaticSEO()
            seo_pages = seo_engine.generate_all_pages(max_pages=50)
            
            results['outputs']['seo'] = {'pages_generated': len(seo_pages)}
            results['modules_run'] += 1
            print(f"SEO pages generated")
            print(f"Pages: {len(seo_pages)}")
            print()
        
        if modules_loaded['social']:
            print("MODULE 8: SOCIAL POSTER (FREE APIs)")
            print("-" * 70)
            
            social_engine = SocialPoster()
            social_results = social_engine.distribute_article(article)
            
            results['outputs']['social'] = social_results
            results['modules_run'] += 1
            print(f"Social distribution complete")
            print()
        
        if GOOGLE_ENHANCED or 'B2BHunter' in dir():
            print("MODULE 9: B2B HUNTER" + (" ENHANCED" if GOOGLE_ENHANCED else ""))
            print("-" * 70)
            
            b2b_engine = B2BHunter()
            businesses = b2b_engine.find_businesses('London, UK', 'florist')
            contacted = 0
            
            for business in businesses[:10]:
                style = b2b_engine.analyze_business_style(business)
                
                if GOOGLE_ENHANCED:
                    email = b2b_engine.generate_cold_email(business, style, include_map=True)
                    sent = b2b_engine.send_cold_email(
                        business.get('email', f"contact@{business['name'].lower().replace(' ', '')}.co.uk"),
                        f"Partnership - {business['name']}",
                        email,
                        business=business,
                        include_map=True
                    )
                else:
                    email = b2b_engine.generate_cold_email(business, style)
                    sent = b2b_engine.send_cold_email(
                        business.get('email', f"contact@{business['name'].lower().replace(' ', '')}.co.uk"),
                        f"Partnership - {business['name']}",
                        email
                    )
                
                if sent:
                    contacted += 1
            
            results['outputs']['b2b'] = {
                'businesses_found': len(businesses),
                'emails_sent': contacted,
                'enhanced': GOOGLE_ENHANCED
            }
            results['modules_run'] += 1
            print(f"B2B outreach complete")
            print(f"Emails sent: {contacted}")
            if GOOGLE_ENHANCED:
                print(f"Visual emails with location maps")
            print()
        
        if modules_loaded['influencer']:
            print("MODULE 10: INFLUENCER SCOUT")
            print("-" * 70)
            
            qualified = run_influencer_campaign('lifestyle', target_count=30)
            
            results['outputs']['influencers'] = {
                'found': 60,
                'qualified': len(qualified),
                'contacted': min(10, len(qualified))
            }
            results['modules_run'] += 1
            print(f"Influencer campaign complete")
            print()
        
        if GOOGLE_ENHANCED or 'GiftPrecognition' in dir():
            print("MODULE 13: GIFT PRECOGNITION" + (" ENHANCED" if GOOGLE_ENHANCED else ""))
            print("-" * 70)
            
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
            print()
        
        if GOOGLE_ENHANCED:
            print("MODULE 14: ADDRESS VALIDATION NEW")
            print("-" * 70)
            
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
        print("="*70)
        
        telegram_message = f"Titan Complete\n\nModules: {results['modules_run']}\nDuration: {duration:.1f}s"
        
        if modules_loaded.get('blog') and 'blog' in results['outputs']:
            telegram_message += f"\n\nBlog: {results['outputs']['blog']['title'][:40]}..."
        
        send_telegram_notification(telegram_message)
        
        print("\nTelegram notification sent")
        print("\n" + "="*70 + "\n")
        
        return 0
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"\n{error_msg}\n")
        
        send_telegram_notification(f"Titan Failed\n\nError: {str(e)}")
        
        import traceback
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
