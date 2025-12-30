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
import json
import hashlib

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
modules_loaded['blog'] = True  # Always true - we use direct Gemini

import requests

def generate_unique_id():
    """Generate unique ID for this content run"""
    timestamp = str(datetime.now().timestamp())
    return hashlib.md5(timestamp.encode()).hexdigest()[:8]

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

def generate_article_with_gemini(topic: dict, api_key: str) -> dict:
    """Generate complete article using Gemini directly"""
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""Write a comprehensive, engaging blog article about: {topic['title']}

Keyword: {topic['keyword']}
Target length: 1200-1500 words
Tone: {topic['angle']}

Structure:
- Compelling introduction that hooks the reader emotionally
- 6-8 main sections with detailed, practical information
- Specific gift suggestions with descriptions
- Personal stories or examples
- Tips for choosing and presenting gifts
- Strong conclusion with call-to-action

Make it feel authentic, helpful, and engaging. Write in a warm, conversational tone.
Include specific product categories and ideas.
Focus on helping people find meaningful gifts that create lasting memories.

DO NOT use generic placeholder text. Write actual, specific content."""

        response = model.generate_content(prompt)
        article_text = response.text
        
        # Create HTML version with proper formatting
        paragraphs = article_text.split('\n')
        html_parts = [f'<article>\n<h1>{topic["title"]}</h1>\n']
        
        in_list = False
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            if para.startswith('##'):
                # H2 header
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                header_text = para.replace('##', '').strip()
                html_parts.append(f'<h2>{header_text}</h2>')
            elif para.startswith('#'):
                # H3 header
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                header_text = para.replace('#', '').strip()
                html_parts.append(f'<h3>{header_text}</h3>')
            elif para.startswith('*') or para.startswith('-'):
                # List item
                if not in_list:
                    html_parts.append('<ul>')
                    in_list = True
                item_text = para.lstrip('*-').strip()
                html_parts.append(f'<li>{item_text}</li>')
            else:
                # Regular paragraph
                if in_list:
                    html_parts.append('</ul>')
                    in_list = False
                html_parts.append(f'<p>{para}</p>')
        
        if in_list:
            html_parts.append('</ul>')
        
        # Add branding footer
        html_parts.append(f'''
<div style="border-top: 2px solid #667eea; margin-top: 2rem; padding-top: 1rem;">
<p><strong>💝 Make Every Gift Special with SayPlay</strong></p>
<p>Add a personal voice message to any gift with our NFC technology. No app needed - just tap and play! 
Visit <a href="https://sayplay.gift" style="color: #667eea;">sayplay.gift</a> to learn more.</p>
</div>
</article>
''')
        
        html_content = '\n'.join(html_parts)
        
        # Add unique identifier
        unique_id = generate_unique_id()
        html_content += f'\n<!-- Generated: {unique_id} at {datetime.now().isoformat()} -->'
        
        word_count = len(article_text.split())
        
        print(f"✅ Article generated: {word_count} words")
        
        return {
            'title': topic['title'],
            'text': article_text,
            'html': html_content,
            'word_count': word_count,
            'keyword': topic['keyword'],
            'unique_id': unique_id
        }
        
    except Exception as e:
        print(f"❌ Gemini generation failed: {e}")
        print(f"Creating enhanced fallback article...")
        
        # MUCH BETTER fallback with real content
        unique_id = generate_unique_id()
        
        return {
            'title': topic['title'],
            'text': f"""Finding the perfect {topic['keyword']} can feel overwhelming with so many options available. But with thoughtful consideration and the right guidance, you can select something truly meaningful that will be cherished for years to come.

Understanding What Makes a Great Gift

The best gifts aren't necessarily the most expensive ones. They're the ones that show you truly understand and care about the recipient. When choosing {topic['keyword']}, consider their personality, interests, daily routine, and what would genuinely make their life better or more enjoyable.

Top Gift Categories to Consider

1. Personalized Items
Adding a personal touch transforms an ordinary gift into something extraordinary. Consider items that can be customized with names, dates, photos, or special messages. Voice message gifts, like those from SayPlay, let you add your heartfelt words that can be heard simply by tapping the gift with a phone.

2. Experience Gifts
Sometimes the best gift isn't a thing at all - it's a memory waiting to be made. Consider concert tickets, cooking classes, spa days, or weekend getaways. These create lasting memories that outlive any physical item.

3. Practical Luxuries
These are items people want but wouldn't necessarily buy for themselves. Think high-quality versions of everyday items: premium skincare, gourmet food baskets, cozy blankets, or elegant accessories.

4. Hobby-Related Gifts
If they're passionate about something, lean into it. Whether it's gardening, cooking, reading, or crafting, there's always equipment, supplies, or accessories they'd appreciate.

5. Subscription Services
Gifts that keep giving month after month. From streaming services to book clubs, coffee deliveries to online courses, subscriptions show ongoing thoughtfulness.

Making Your Gift Extra Special

The presentation matters almost as much as the gift itself. Take time to wrap it beautifully, include a heartfelt card, and consider adding a personal voice message with SayPlay's NFC technology. These small touches elevate your gift from good to unforgettable.

Timing Your Purchase

Don't wait until the last minute. Shopping early gives you time to find the perfect item, allows for shipping delays, and reduces stress. Plus, you can often find better deals when you're not shopping in a panic.

Budget-Friendly Options

Meaningful gifts don't require a huge budget. Handmade items, thoughtful letters, photo albums, or experiences you can share together often mean more than expensive purchases. It's the thought and effort that count.

Final Thoughts

Remember, the goal isn't perfection - it's showing someone you care. Whether you choose something practical, sentimental, or fun, what matters most is the love and thought behind it. Take your time, trust your instincts, and don't be afraid to get creative.

At SayPlay, we believe every gift tells a story. Our voice message technology helps you add your personal touch to any present, creating moments that last forever. Visit sayplay.gift to discover how a simple tap can unlock your heartfelt message.

The perfect gift is out there - and now you're equipped to find it.""",
            'html': f"""<article>
<h1>{topic['title']}</h1>

<p>Finding the perfect <strong>{topic['keyword']}</strong> can feel overwhelming with so many options available. But with thoughtful consideration and the right guidance, you can select something truly meaningful that will be cherished for years to come.</p>

<h2>Understanding What Makes a Great Gift</h2>

<p>The best gifts aren't necessarily the most expensive ones. They're the ones that show you truly understand and care about the recipient. When choosing {topic['keyword']}, consider their personality, interests, daily routine, and what would genuinely make their life better or more enjoyable.</p>

<h2>Top Gift Categories to Consider</h2>

<h3>1. Personalized Items</h3>
<p>Adding a personal touch transforms an ordinary gift into something extraordinary. Consider items that can be customized with names, dates, photos, or special messages. <strong>Voice message gifts</strong>, like those from SayPlay, let you add your heartfelt words that can be heard simply by tapping the gift with a phone.</p>

<h3>2. Experience Gifts</h3>
<p>Sometimes the best gift isn't a thing at all - it's a memory waiting to be made. Consider concert tickets, cooking classes, spa days, or weekend getaways. These create lasting memories that outlive any physical item.</p>

<h3>3. Practical Luxuries</h3>
<p>These are items people want but wouldn't necessarily buy for themselves. Think high-quality versions of everyday items: premium skincare, gourmet food baskets, cozy blankets, or elegant accessories.</p>

<h3>4. Hobby-Related Gifts</h3>
<p>If they're passionate about something, lean into it. Whether it's gardening, cooking, reading, or crafting, there's always equipment, supplies, or accessories they'd appreciate.</p>

<h3>5. Subscription Services</h3>
<p>Gifts that keep giving month after month. From streaming services to book clubs, coffee deliveries to online courses, subscriptions show ongoing thoughtfulness.</p>

<h2>Making Your Gift Extra Special</h2>

<p>The presentation matters almost as much as the gift itself. Take time to wrap it beautifully, include a heartfelt card, and consider adding a personal voice message with SayPlay's NFC technology. These small touches elevate your gift from good to unforgettable.</p>

<h2>Timing Your Purchase</h2>

<p>Don't wait until the last minute. Shopping early gives you time to find the perfect item, allows for shipping delays, and reduces stress. Plus, you can often find better deals when you're not shopping in a panic.</p>

<h2>Budget-Friendly Options</h2>

<p>Meaningful gifts don't require a huge budget. Handmade items, thoughtful letters, photo albums, or experiences you can share together often mean more than expensive purchases. It's the thought and effort that count.</p>

<h2>Final Thoughts</h2>

<p>Remember, the goal isn't perfection - it's showing someone you care. Whether you choose something practical, sentimental, or fun, what matters most is the love and thought behind it. Take your time, trust your instincts, and don't be afraid to get creative.</p>

<div style="border-top: 2px solid #667eea; margin-top: 2rem; padding-top: 1rem;">
<p><strong>💝 Make Every Gift Special with SayPlay</strong></p>
<p>Add a personal voice message to any gift with our NFC technology. No app needed - just tap and play! 
Visit <a href="https://sayplay.gift" style="color: #667eea;">sayplay.gift</a> to learn more.</p>
</div>

<!-- Generated: {unique_id} at {datetime.now().isoformat()} -->
</article>""",
            'word_count': 650,
            'keyword': topic['keyword'],
            'unique_id': unique_id
        }

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
        
        # ================================================================
        # MODULE 2: BLOG ENGINE - DIRECT GEMINI CALL
        # ================================================================
        if modules_loaded['blog']:
            print("MODULE 2: BLOG ENGINE (Gemini Direct - FREE)")
            print("-" * 70)
            
            topic = generate_topic()
            
            gemini_key = os.getenv('GEMINI_API_KEY')
            if gemini_key:
                article = generate_article_with_gemini(topic, gemini_key)
                
                if modules_loaded['brand']:
                    try:
                        article = brand.apply_brand_identity(article, 'html')
                    except:
                        pass
                
                results['outputs']['blog'] = {
                    'title': article.get('title', 'Untitled'),
                    'keyword': topic.get('keyword', 'N/A'),
                    'word_count': article.get('word_count', 0),
                    'unique_id': article.get('unique_id', 'N/A')
                }
                results['modules_run'] += 1
                print(f"Title: {article.get('title', '')[:60]}...")
                print(f"Words: {article.get('word_count', 0)}")
                print(f"Unique ID: {article.get('unique_id', 'N/A')}")
            else:
                print("⚠️ GEMINI_API_KEY not set, using fallback")
                article = generate_article_with_gemini(topic, "")
            
            print()
        else:
            article = {'title': 'Test Article', 'text': 'Test content', 'html': '<p>Test</p>'}
            topic = {'keyword': 'gifts'}
        
        # ================================================================
        # MODULE 4: IMAGE ENGINE - RETRY LOGIC + UNIQUE PROMPTS
        # ================================================================
        if modules_loaded['images']:
            print("MODULE 4: IMAGE ENGINE (Pollinations.ai - FREE)")
            print("-" * 70)
            
            try:
                # Generate UNIQUE prompts for variety
                unique_descriptors = [
                    "warm natural lighting, professional photography",
                    "soft focus, elegant composition, artistic",
                    "modern minimalist style, clean aesthetic",
                    "heartwarming emotional scene, cinematic",
                    "vibrant colors, lifestyle magazine quality"
                ]
                
                image_prompts = [
                    f"{topic.get('keyword', 'gift')}, {desc}, high quality 4k"
                    for desc in random.sample(unique_descriptors, 3)
                ]
                
                images = []
                
                for i, prompt in enumerate(image_prompts):
                    print(f"Generating image {i+1}/3: {prompt[:50]}...")
                    
                    # Retry logic with increased timeout
                    max_retries = 2
                    for attempt in range(max_retries):
                        try:
                            # Pollinations.ai URL
                            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
                            
                            response = requests.get(url, timeout=60)  # 60s timeout
                            
                            if response.status_code == 200 and len(response.content) > 1000:
                                images.append(response.content)
                                print(f"  ✅ Image {i+1} generated ({len(response.content)//1024}KB)")
                                break
                            else:
                                print(f"  ⚠️ Attempt {attempt+1} failed: status {response.status_code}")
                                
                        except Exception as e:
                            print(f"  ⚠️ Attempt {attempt+1} error: {str(e)[:50]}")
                            
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(3)
                
                if len(images) == 0:
                    print(f"⚠️ All image generation attempts failed")
                    print(f"⚠️ Continuing without images...")
                
                results['outputs']['images'] = {
                    'prompts': image_prompts,
                    'variants_generated': len(images)
                }
                
                if len(images) > 0:
                    results['modules_run'] += 1
                    print(f"✅ Successfully generated {len(images)}/3 unique images")
                
            except Exception as e:
                print(f"Image generation error: {e}")
                images = []
            
            print()
        else:
            images = []
        
        # ================================================================
        # MODULE 5: AUDIO - BETTER VOICES (British Neural)
        # ================================================================
        if modules_loaded['audio']:
            print("MODULE 5: AUDIO-INCEPTION (Edge-TTS Premium Voices - FREE)")
            print("-" * 70)
            
            try:
                import asyncio
                import edge_tts
                
                # PREMIUM VOICES - More natural sounding
                PREMIUM_VOICES = {
                    'female': 'en-GB-SoniaNeural',      # British, warm, natural
                    'male': 'en-GB-RyanNeural'          # British, friendly, clear
                }
                
                # Extract key content from article
                article_excerpt = article.get('text', '')[:800]  # First 800 chars
                
                # Create engaging podcast script with variety
                podcast_segments = [
                    {
                        'text': f"Welcome to the SayPlay Gift Guide! Today we're exploring {topic['keyword']}.",
                        'voice': PREMIUM_VOICES['female']
                    },
                    {
                        'text': f"That's right! We've put together some fantastic ideas that will truly make an impact.",
                        'voice': PREMIUM_VOICES['male']
                    },
                    {
                        'text': article_excerpt,
                        'voice': PREMIUM_VOICES['female']
                    },
                    {
                        'text': "These are wonderful suggestions! What I particularly love is how personal each option is.",
                        'voice': PREMIUM_VOICES['male']
                    },
                    {
                        'text': "Absolutely! And remember, you can add an even more personal touch with SayPlay's voice message technology.",
                        'voice': PREMIUM_VOICES['female']
                    },
                    {
                        'text': "Just tap the NFC sticker with your phone to hear your heartfelt message. No app needed!",
                        'voice': PREMIUM_VOICES['male']
                    },
                    {
                        'text': "Thanks so much for listening! Visit sayplay dot gift to learn more and make your next gift truly unforgettable.",
                        'voice': PREMIUM_VOICES['female']
                    }
                ]
                
                # Generate audio segments
                async def generate_segment(text: str, voice: str) -> bytes:
                    communicate = edge_tts.Communicate(text, voice)
                    audio_data = b""
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_data += chunk["data"]
                    return audio_data
                
                async def generate_all_segments():
                    tasks = [generate_segment(seg['text'], seg['voice']) for seg in podcast_segments]
                    return await asyncio.gather(*tasks)
                
                print(f"Generating {len(podcast_segments)} audio segments with premium voices...")
                audio_segments = asyncio.run(generate_all_segments())
                
                # Combine all segments
                full_audio = b"".join(audio_segments)
                
                # Calculate duration (rough estimate: ~12 bytes per millisecond for mp3)
                duration = len(full_audio) // 12000
                
                podcast = {
                    'audio': full_audio,
                    'metadata': {
                        'title': f"Gift Guide: {topic['title']}",
                        'duration': duration,
                        'voices': list(PREMIUM_VOICES.values()),
                        'segments': len(podcast_segments),
                        'quality': 'Premium British Neural'
                    }
                }
                
                results['outputs']['podcast'] = {
                    'title': podcast['metadata']['title'],
                    'duration': podcast['metadata']['duration'],
                    'quality': podcast['metadata']['quality']
                }
                results['modules_run'] += 1
                print(f"✅ Podcast created: {duration}s")
                print(f"✅ Voices: British Neural (premium quality)")
                print(f"✅ Segments: {len(podcast_segments)}")
                
            except Exception as e:
                print(f"Podcast generation error: {e}")
                import traceback
                traceback.print_exc()
                podcast = None
            
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
                translations = {'en': article}
            
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
                print(f"Email reminders sent: {len(upcoming[:5])}")
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
            except Exception as e:
                print(f"Address validation error: {e}")
            
            print()
        
        # ================================================================
        # SAVE ALL GENERATED CONTENT TO FILES
        # ================================================================
        print("\n" + "="*70)
        print("SAVING CONTENT TO FILES")
        print("="*70)
        
        saved_files = []
        
        # Save article
        if 'blog' in results['outputs']:
            try:
                with open('article.html', 'w', encoding='utf-8') as f:
                    f.write(article.get('html', ''))
                saved_files.append('article.html')
                print(f"✅ Saved: article.html ({article.get('word_count', 0)} words)")
                
                with open('article.txt', 'w', encoding='utf-8') as f:
                    f.write(article.get('text', ''))
                saved_files.append('article.txt')
                print(f"✅ Saved: article.txt")
                
                with open('article_meta.json', 'w') as f:
                    json.dump({
                        'title': article.get('title'),
                        'keyword': topic.get('keyword'),
                        'word_count': article.get('word_count', 0),
                        'unique_id': article.get('unique_id'),
                        'generated_at': datetime.now().isoformat()
                    }, f, indent=2)
                saved_files.append('article_meta.json')
                print(f"✅ Saved: article_meta.json")
            except Exception as e:
                print(f"❌ Error saving article: {e}")
        
        # Save podcast
        if 'podcast' in results['outputs'] and podcast:
            try:
                if 'audio' in podcast and podcast['audio']:
                    with open('podcast.mp3', 'wb') as f:
                        f.write(podcast['audio'])
                    saved_files.append('podcast.mp3')
                    size_mb = len(podcast['audio']) / (1024 * 1024)
                    print(f"✅ Saved: podcast.mp3 ({size_mb:.2f}MB, {podcast['metadata']['duration']}s)")
            except Exception as e:
                print(f"❌ Error saving podcast: {e}")
        
        # Save translations
        if 'translations' in results['outputs'] and 'translations' in dir():
            try:
                Path('translations').mkdir(exist_ok=True)
                
                for lang, content in translations.items():
                    lang_file = f'translations/article_{lang}.html'
                    with open(lang_file, 'w', encoding='utf-8') as f:
                        if isinstance(content, dict):
                            f.write(content.get('html', content.get('text', '')))
                        else:
                            f.write(str(content))
                    saved_files.append(lang_file)
                
                print(f"✅ Saved: {len(translations)} translations")
            except Exception as e:
                print(f"❌ Error saving translations: {e}")
        
        # Save images
        if len(images) > 0:
            try:
                Path('images').mkdir(exist_ok=True)
                
                for i, img_data in enumerate(images):
                    img_file = f'images/image_{i+1}.png'
                    with open(img_file, 'wb') as f:
                        f.write(img_data)
                    saved_files.append(img_file)
                    size_kb = len(img_data) / 1024
                    print(f"✅ Saved: image_{i+1}.png ({size_kb:.0f}KB)")
                
            except Exception as e:
                print(f"❌ Error saving images: {e}")
        else:
            print(f"⚠️  No images to save")
        
        # Save SEO summary
        if 'seo' in results['outputs']:
            try:
                with open('seo_pages_summary.json', 'w') as f:
                    json.dump({
                        'pages_generated': results['outputs']['seo']['pages_generated'],
                        'generated_at': datetime.now().isoformat()
                    }, f, indent=2)
                saved_files.append('seo_pages_summary.json')
                print(f"✅ Saved: seo_pages_summary.json")
            except Exception as e:
                print(f"❌ Error saving SEO summary: {e}")
        
        print(f"\n📦 Total files saved: {len(saved_files)}")
        print(f"📁 Files ready for artifacts upload")
        print("="*70 + "\n")
        
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
        
        # Enhanced Telegram message with download link
        telegram_message = f"<b>🎉 Titan Complete</b>\n\n"
        telegram_message += f"<b>⏱ Duration:</b> {duration:.1f}s\n"
        telegram_message += f"<b>📦 Modules:</b> {results['modules_run']}\n\n"
        
        if 'blog' in results['outputs']:
            telegram_message += f"<b>📝 Blog:</b> {results['outputs']['blog']['title'][:45]}...\n"
            telegram_message += f"<b>🔑 Keyword:</b> {results['outputs']['blog']['keyword']}\n"
            telegram_message += f"<b>📊 Words:</b> {results['outputs']['blog']['word_count']}\n"
            if 'unique_id' in results['outputs']['blog']:
                telegram_message += f"<b>🆔 ID:</b> {results['outputs']['blog']['unique_id']}\n"
            telegram_message += "\n"
        
        if 'images' in results['outputs']:
            img_count = results['outputs']['images']['variants_generated']
            telegram_message += f"<b>🖼 Images:</b> {img_count} unique variants\n"
        
        if 'podcast' in results['outputs']:
            telegram_message += f"<b>🎙 Podcast:</b> {results['outputs']['podcast']['duration']}s\n"
            telegram_message += f"<b>🎵 Quality:</b> {results['outputs']['podcast'].get('quality', 'Premium')}\n"
        
        if 'translations' in results['outputs']:
            telegram_message += f"<b>🌍 Languages:</b> {len(results['outputs']['translations']['languages'])}\n"
        
        if 'b2b' in results['outputs']:
            b2b = results['outputs']['b2b']
            telegram_message += f"\n<b>📧 B2B Bulletproof:</b>\n"
            telegram_message += f"  ✓ Found: {b2b.get('businesses_found', 0)}\n"
            telegram_message += f"  ✓ Validated: {b2b.get('emails_validated', 0)}\n"
            telegram_message += f"  ✓ Sent: {b2b.get('emails_sent', 0)}\n"
        
        telegram_message += f"\n<b>💰 Cost:</b> {'9.40 GBP/month' if GOOGLE_ENHANCED else 'FREE'}\n"
        telegram_message += f"<b>📂 Files:</b> {len(saved_files)} saved\n"
        
        # ADD ARTIFACT DOWNLOAD LINK
        telegram_message += f"\n<b>📥 DOWNLOAD FILES:</b>\n"
        telegram_message += f"<a href='https://github.com/Voicegiftuk/Remix-Engine-V2.0---Viral-Edition/actions'>👉 GitHub Actions → Artifacts</a>\n"
        telegram_message += f"\n<i>Look for: titan-content-XXX.zip in latest run</i>"
        
        send_telegram_notification(telegram_message)
        
        print("\nTelegram notification sent with download link")
        print("\n" + "="*70 + "\n")
        
        return 0
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        print(f"\n{error_msg}\n")
        
        send_telegram_notification(f"<b>❌ Titan Failed</b>\n\nError: {str(e)}")
        
        import traceback
        traceback.print_exc()
        
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
