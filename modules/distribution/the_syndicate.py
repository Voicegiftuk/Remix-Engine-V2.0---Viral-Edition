#!/usr/bin/env python3
"""
The Syndicate - Distribution Engine
PROJECT TITAN Module 5

Purpose: Safe multi-platform content distribution
Strategy: Parasite SEO + Whisper Marketing + Human Approval

Platforms:
- Tier 1: Medium, Pinterest, LinkedIn (100% auto)
- Tier 2: Reddit, Quora, Instructables (semi-auto)
- Tier 3: Wedding/Parenting blogs (outreach)
- Tier 4: Mumsnet (monitor only, manual whisper)
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.brand_identity.brand_core import get_brand_core
from modules.distribution.publishers.medium_publisher import MediumPublisher
from modules.distribution.publishers.linkedin_publisher import LinkedInPublisher
from modules.distribution.publishers.pinterest_publisher import PinterestPublisher
from modules.distribution.monitors.reddit_monitor import RedditMonitor
from modules.distribution.monitors.quora_monitor import QuoraMonitor
from modules.distribution.monitors.mumsnet_monitor import MumsnetMonitor
from modules.distribution.outreach.email_engine import EmailOutreachEngine
from loguru import logger


class TheSyndicate:
    """
    Central distribution orchestrator for PROJECT TITAN
    
    Responsibilities:
    1. Distribute blog articles to parasite SEO platforms
    2. Monitor forums for opportunities
    3. Send outreach emails to blogs
    4. Protect brand (no spam, human approval)
    
    Safety Features:
    - Human-in-the-loop for risky platforms
    - Rate limiting (no flooding)
    - Platform-specific rules (Mumsnet = extreme care)
    - Telegram approval for all semi-auto
    """
    
    def __init__(self, config: Dict):
        """
        Initialize The Syndicate
        
        Args:
            config: {
                'medium_token': Medium API token,
                'linkedin_token': LinkedIn API token,
                'pinterest_token': Pinterest API token,
                'reddit_client_id': Reddit API client,
                'reddit_secret': Reddit API secret,
                'telegram_bot_token': For approval notifications,
                'telegram_chat_id': Where to send approvals
            }
        """
        self.config = config
        self.brand = get_brand_core()
        
        # Tier 1: Auto-safe publishers
        self.publishers = {
            'medium': MediumPublisher(config.get('medium_token')),
            'linkedin': LinkedInPublisher(config.get('linkedin_token')),
            'pinterest': PinterestPublisher(config.get('pinterest_token'))
        }
        
        # Tier 2: Semi-auto monitors
        self.monitors = {
            'reddit': RedditMonitor(
                config.get('reddit_client_id'),
                config.get('reddit_secret')
            ),
            'quora': QuoraMonitor(config.get('quora_cookies')),
            'mumsnet': MumsnetMonitor()  # Monitor only, never post
        }
        
        # Tier 3: Outreach engine
        self.outreach = EmailOutreachEngine(config)
        
        # Tracking
        self.stats = {
            'published': {},
            'monitored': {},
            'outreach_sent': {}
        }
        
        logger.info("The Syndicate initialized - Safe distribution ready")
    
    async def distribute_article(
        self,
        article: Dict,
        platforms: List[str] = None,
        auto_publish: bool = False
    ) -> Dict:
        """
        Distribute article to multiple platforms
        
        Args:
            article: Article package from Blog Module
            platforms: Which platforms to use (default: all Tier 1)
            auto_publish: True = auto-publish to safe platforms
                         False = send to Telegram for approval
        
        Returns:
            Distribution results
        """
        
        if platforms is None:
            # Default: All Tier 1 (safe auto-publish)
            platforms = ['medium', 'linkedin', 'pinterest']
        
        results = {}
        
        logger.info(f"Distributing article: {article['title']}")
        logger.info(f"Target platforms: {', '.join(platforms)}")
        
        # Tier 1: Auto-safe platforms
        for platform in platforms:
            if platform in self.publishers:
                try:
                    if auto_publish:
                        # Direct publish
                        result = await self.publishers[platform].publish(article)
                        results[platform] = result
                        logger.success(f"✓ Published to {platform}")
                    else:
                        # Send to Telegram for approval
                        await self._send_for_approval(platform, article)
                        results[platform] = {'status': 'pending_approval'}
                        logger.info(f"→ {platform}: Awaiting approval")
                
                except Exception as e:
                    logger.error(f"✗ {platform} failed: {e}")
                    results[platform] = {'status': 'error', 'error': str(e)}
        
        # Update stats
        self.stats['published'][datetime.now().isoformat()] = results
        
        return results
    
    async def monitor_opportunities(
        self,
        keywords: List[str] = None,
        platforms: List[str] = None
    ) -> List[Dict]:
        """
        Monitor forums for content opportunities
        
        Args:
            keywords: What to look for (default: gift-related)
            platforms: Which forums (default: Reddit, Quora)
        
        Returns:
            List of opportunities found
        """
        
        if keywords is None:
            keywords = [
                'gift ideas',
                'birthday gift',
                'wedding gift',
                'anniversary gift',
                'personalized gift',
                'unique gift',
                'voice message'
            ]
        
        if platforms is None:
            platforms = ['reddit', 'quora']
        
        opportunities = []
        
        logger.info(f"Monitoring platforms: {', '.join(platforms)}")
        logger.info(f"Keywords: {', '.join(keywords[:3])}...")
        
        for platform in platforms:
            if platform in self.monitors:
                try:
                    found = await self.monitors[platform].find_opportunities(keywords)
                    opportunities.extend(found)
                    logger.info(f"✓ {platform}: Found {len(found)} opportunities")
                
                except Exception as e:
                    logger.error(f"✗ {platform} monitoring failed: {e}")
        
        # Send top opportunities to Telegram
        if opportunities:
            await self._send_opportunities_for_review(opportunities[:10])
        
        # Update stats
        self.stats['monitored'][datetime.now().isoformat()] = len(opportunities)
        
        return opportunities
    
    async def run_outreach_campaign(
        self,
        campaign_type: str = 'wedding_blogs',
        count: int = 10
    ) -> Dict:
        """
        Send outreach emails to blogs
        
        Args:
            campaign_type: Type of blogs to target
                          'wedding_blogs', 'parenting_blogs', 'gift_guides'
            count: How many emails to send
        
        Returns:
            Campaign results
        """
        
        logger.info(f"Starting outreach campaign: {campaign_type}")
        logger.info(f"Target: {count} emails")
        
        # Find blogs
        target_blogs = await self.outreach.find_blogs(campaign_type, count)
        
        # Generate personalized emails
        emails = []
        for blog in target_blogs:
            email = await self.outreach.generate_email(
                blog,
                campaign_type
            )
            emails.append(email)
        
        # Send to Telegram for approval (never auto-send cold emails!)
        await self._send_emails_for_approval(emails)
        
        logger.info(f"✓ Generated {len(emails)} outreach emails")
        logger.info("→ Awaiting approval on Telegram")
        
        # Update stats
        self.stats['outreach_sent'][datetime.now().isoformat()] = {
            'campaign': campaign_type,
            'count': len(emails)
        }
        
        return {
            'campaign': campaign_type,
            'emails_generated': len(emails),
            'status': 'pending_approval'
        }
    
    async def daily_distribution_workflow(self, article: Dict) -> Dict:
        """
        Complete daily distribution workflow
        
        Takes one blog article and distributes it everywhere safely
        
        Workflow:
        1. Auto-publish to Medium + Pinterest (safe)
        2. Queue LinkedIn for approval
        3. Monitor Reddit/Quora for opportunities
        4. Send Mumsnet opportunities (manual only)
        5. Report to Telegram
        
        Args:
            article: Article from Blog Module
        
        Returns:
            Complete distribution report
        """
        
        logger.info("=" * 60)
        logger.info("STARTING DAILY DISTRIBUTION WORKFLOW")
        logger.info("=" * 60)
        
        results = {}
        
        # Step 1: Auto-publish to safe platforms
        logger.info("\n📤 STEP 1: Auto-Publishing to Safe Platforms...")
        
        auto_platforms = ['medium', 'pinterest']  # LinkedIn needs approval
        auto_results = await self.distribute_article(
            article,
            platforms=auto_platforms,
            auto_publish=True
        )
        results['auto_published'] = auto_results
        
        # Step 2: Queue LinkedIn for approval
        logger.info("\n⏳ STEP 2: Queueing LinkedIn for Approval...")
        
        linkedin_result = await self.distribute_article(
            article,
            platforms=['linkedin'],
            auto_publish=False  # Needs approval
        )
        results['pending_approval'] = linkedin_result
        
        # Step 3: Monitor forums
        logger.info("\n👀 STEP 3: Monitoring Forums for Opportunities...")
        
        opportunities = await self.monitor_opportunities(
            platforms=['reddit', 'quora', 'mumsnet']
        )
        results['opportunities_found'] = len(opportunities)
        
        # Step 4: Generate outreach (but don't send yet)
        logger.info("\n📧 STEP 4: Generating Outreach Emails...")
        
        # Only run outreach 1x/week (Friday)
        if datetime.now().weekday() == 4:  # Friday
            outreach_result = await self.run_outreach_campaign(
                campaign_type='wedding_blogs',
                count=5
            )
            results['outreach'] = outreach_result
        else:
            results['outreach'] = {'status': 'skipped', 'reason': 'not_friday'}
        
        # Step 5: Report to Telegram
        logger.info("\n📱 STEP 5: Sending Report to Telegram...")
        
        await self._send_daily_report(results)
        
        logger.info("\n" + "=" * 60)
        logger.info("DAILY DISTRIBUTION WORKFLOW COMPLETE")
        logger.info("=" * 60)
        
        return results
    
    async def _send_for_approval(self, platform: str, article: Dict):
        """Send article to Telegram for approval before publishing"""
        # TODO: Implement Telegram approval message
        pass
    
    async def _send_opportunities_for_review(self, opportunities: List[Dict]):
        """Send forum opportunities to Telegram for review"""
        # TODO: Implement opportunity review message
        pass
    
    async def _send_emails_for_approval(self, emails: List[Dict]):
        """Send outreach emails to Telegram for approval"""
        # TODO: Implement email approval message
        pass
    
    async def _send_daily_report(self, results: Dict):
        """Send daily distribution report to Telegram"""
        # TODO: Implement daily report message
        pass
    
    def get_stats(self) -> Dict:
        """Get distribution statistics"""
        return {
            'total_published': len(self.stats['published']),
            'total_monitored': sum(self.stats['monitored'].values()),
            'total_outreach': len(self.stats['outreach_sent']),
            'details': self.stats
        }


if __name__ == "__main__":
    """Test The Syndicate"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("🌐 Testing The Syndicate - Distribution Engine...")
    
    # Test config
    config = {
        'medium_token': os.getenv('MEDIUM_TOKEN'),
        'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID')
    }
    
    syndicate = TheSyndicate(config)
    
    # Test article
    article = {
        'title': 'The Ultimate Guide to Personalized Birthday Gifts 2025',
        'text': 'Full article text here...',
        'html': '<h1>Article</h1><p>Content...</p>',
        'url': 'https://sayplay.co.uk/blog/personalized-birthday-gifts-2025'
    }
    
    print("\n📤 Testing distribution...")
    
    # This would be async in real usage
    # results = asyncio.run(syndicate.distribute_article(article))
    
    print("\n✅ The Syndicate initialized successfully!")
    print("   Ready to distribute content across platforms")
