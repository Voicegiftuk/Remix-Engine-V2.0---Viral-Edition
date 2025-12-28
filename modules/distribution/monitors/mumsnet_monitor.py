#!/usr/bin/env python3
"""
Mumsnet Monitor - UK E-commerce Holy Grail
PROJECT TITAN - The Syndicate Module

⚠️ EXTREME CAUTION REQUIRED ⚠️

Why Mumsnet is CRITICAL for UK market:
- 12M monthly users (mostly UK moms)
- High purchasing power (£40k+ household income average)
- EXTREMELY influential (can make/break brands)
- "Mumsnet Effect" = viral product success
- Perfect audience for personalized gifts (grandparents, kids)

BUT ALSO EXTREMELY DANGEROUS:
- Users HATE marketing and detect it instantly
- Moderators ban aggressively
- Community will publicly shame obvious ads
- One bad post = permanent brand damage

SUCCESS STORIES:
- Trunki (kids' suitcase): Mumsnet discussion → £20M sales
- Emma's Diary: Banned for data scandal → brand destroyed
- Various products: "Mumsnet Recommended" = sales explosion

FAILURE STORIES:
- Multiple brands banned for subtle marketing
- Political campaigns ridiculed
- Corporate attempts at "authentic" posts exposed and mocked

STRATEGY: "WHISPER MARKETING" ONLY
- Monitor conversations about gifts for grandparents
- Monitor "what to buy" threads
- NEVER auto-post (instant ban)
- Send opportunities to human
- Human decides if/how to engage (if at all)
- When engaging: be 100% authentic, helpful, no sales pitch
- Mention SayPlay ONLY if directly relevant and adds value

This is NOT automated marketing. This is intelligence gathering.
"""
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from loguru import logger


class MumsnetMonitor:
    """
    Mumsnet conversation monitor - INTELLIGENCE ONLY
    
    Features:
    - Monitor gift-related discussions
    - Identify high-value opportunities
    - Score conversation quality
    - NEVER auto-post (ban risk)
    - Human review required for ANY engagement
    
    Safety Rules:
    1. Monitor only, never post automatically
    2. Flag opportunities for human review
    3. Include full context (so human can assess)
    4. Warn about community sentiment
    5. Suggest tone (helpful/authentic only)
    
    This module finds conversations. Humans decide if/how to participate.
    """
    
    # Target forums (gift-related)
    TARGET_FORUMS = [
        'am-i-being-unreasonable',  # AIBU - most active
        'chat',                      # General chat
        'relationships',             # Gift ideas for partners
        'parents',                   # Gifts for kids/grandparents
        'christmas'                  # Seasonal (when active)
    ]
    
    # Keywords (gift-focused only)
    KEYWORDS = [
        # Direct gift questions
        'gift for grandparents',
        'present for granny',
        'gift for nan',
        'what to get grandad',
        
        # Milestone gifts
        'grandparents day',
        'birthday present',
        'christmas gift',
        
        # Personalized signals
        'personalized gift',
        'meaningful present',
        'sentimental gift',
        'memory gift',
        
        # Voice-related
        'voice recording',
        'voice message',
        'hear their voice'
    ]
    
    # DANGER SIGNALS (avoid these conversations)
    DANGER_SIGNALS = [
        'fed up with ads',
        'marketing',
        'sponsored',
        'obvious shill',
        'hun',  # MLM terminology
        'PM me'  # Direct selling attempts
    ]
    
    def __init__(self):
        """
        Initialize Mumsnet monitor
        
        NO API - Mumsnet doesn't have public API
        We use web scraping (ethical, public data only)
        """
        self.base_url = 'https://www.mumsnet.com'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SayPlayMonitor/1.0; +https://sayplay.co.uk)'
        })
        
        logger.warning("⚠️  MumsnetMonitor: EXTREME CAUTION MODE")
        logger.warning("    NEVER auto-post. Human review required.")
    
    async def find_opportunities(
        self,
        keywords: List[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        Find gift-related conversations on Mumsnet
        
        Args:
            keywords: Custom keywords (default: self.KEYWORDS)
            limit: Max threads to check
        
        Returns:
            List of opportunities with DANGER WARNINGS
        """
        
        if keywords is None:
            keywords = self.KEYWORDS
        
        logger.info("Monitoring Mumsnet (UK Holy Grail)...")
        logger.warning("Remember: WHISPER MARKETING ONLY - NO AUTO-POST")
        
        opportunities = []
        
        for forum in self.TARGET_FORUMS:
            try:
                threads = self._scrape_forum(forum, limit=limit)
                
                for thread in threads:
                    # Check if matches keywords
                    if self._matches_keywords(thread, keywords):
                        # Check for danger signals
                        danger_level = self._assess_danger(thread)
                        
                        # Score opportunity
                        score = self._score_opportunity(thread)
                        
                        if score > 0.6 and danger_level < 3:  # High opportunity, low danger
                            opportunity = {
                                'platform': 'mumsnet',
                                'forum': forum,
                                'thread_id': thread['id'],
                                'title': thread['title'],
                                'url': f"{self.base_url}/Talk/{forum}/{thread['id']}",
                                'snippet': thread.get('snippet', ''),
                                'created': thread.get('created'),
                                'replies': thread.get('replies', 0),
                                'views': thread.get('views', 0),
                                'opportunity_score': score,
                                'danger_level': danger_level,
                                'danger_signals': thread.get('danger_signals', []),
                                'suggested_approach': self._suggest_approach(thread, danger_level),
                                'warning': self._generate_warning(danger_level)
                            }
                            
                            opportunities.append(opportunity)
                            logger.info(f"✓ Found in {forum} (score: {score:.2f}, danger: {danger_level}/5)")
            
            except Exception as e:
                logger.warning(f"Error scraping {forum}: {e}")
                continue
        
        # Sort by score, then by safety (lower danger first)
        opportunities.sort(key=lambda x: (x['opportunity_score'], -x['danger_level']), reverse=True)
        
        logger.info(f"✓ Found {len(opportunities)} opportunities on Mumsnet")
        if opportunities:
            logger.warning("⚠️  REVIEW EACH CAREFULLY - Mumsnet users detect marketing instantly")
        
        return opportunities
    
    def _scrape_forum(self, forum: str, limit: int = 20) -> List[Dict]:
        """Scrape forum threads (ethical, public data)"""
        
        try:
            url = f"{self.base_url}/Talk/{forum}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"Failed to access {forum}: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract threads
            threads = []
            thread_elements = soup.find_all('div', class_='thread-item')[:limit]
            
            for elem in thread_elements:
                try:
                    title_elem = elem.find('a', class_='thread-title')
                    
                    thread = {
                        'id': elem.get('data-thread-id', 'unknown'),
                        'title': title_elem.text.strip() if title_elem else '',
                        'snippet': elem.find('p', class_='thread-snippet').text.strip() if elem.find('p', class_='thread-snippet') else '',
                        'replies': int(elem.get('data-replies', 0)),
                        'views': int(elem.get('data-views', 0))
                    }
                    
                    threads.append(thread)
                
                except Exception as e:
                    continue
            
            return threads
        
        except Exception as e:
            logger.error(f"Scraping error for {forum}: {e}")
            return []
    
    def _matches_keywords(self, thread: Dict, keywords: List[str]) -> bool:
        """Check if thread matches keywords"""
        
        text = (thread['title'] + ' ' + thread.get('snippet', '')).lower()
        
        return any(keyword.lower() in text for keyword in keywords)
    
    def _assess_danger(self, thread: Dict) -> int:
        """
        Assess danger level (0-5)
        
        0 = Safe (genuine question, helpful community)
        1 = Low risk (normal conversation)
        2 = Medium risk (some marketing sensitivity)
        3 = High risk (anti-marketing sentiment)
        4 = Very high risk (active anti-spam discussion)
        5 = EXTREME risk (do NOT engage)
        """
        
        text = (thread['title'] + ' ' + thread.get('snippet', '')).lower()
        
        danger = 0
        danger_signals = []
        
        # Check for danger signals
        for signal in self.DANGER_SIGNALS:
            if signal in text:
                danger += 1
                danger_signals.append(signal)
        
        # High activity = higher scrutiny
        if thread.get('replies', 0) > 100:
            danger += 1
            danger_signals.append('high_activity')
        
        # AIBU forum = higher scrutiny
        if 'aibu' in thread.get('forum', '').lower():
            danger += 1
            danger_signals.append('aibu_forum')
        
        thread['danger_signals'] = danger_signals
        
        return min(danger, 5)
    
    def _score_opportunity(self, thread: Dict) -> float:
        """
        Score opportunity quality (0.0-1.0)
        
        Factors:
        - Relevance to SayPlay
        - Question format (asking for help)
        - Specific occasion mentioned
        - Grandparent-focused (perfect audience)
        - Low competition (few replies)
        """
        
        score = 0.0
        text = (thread['title'] + ' ' + thread.get('snippet', '')).lower()
        
        # Question format (0-0.3)
        if '?' in thread['title']:
            score += 0.3
        
        # Grandparent-focused (0-0.3)
        grandparent_terms = ['grandparent', 'granny', 'grandad', 'nan', 'nana', 'grandma', 'grandpa']
        if any(term in text for term in grandparent_terms):
            score += 0.3
        
        # Specific occasion (0-0.2)
        occasions = ['birthday', 'christmas', 'mothers day', 'fathers day']
        if any(occ in text for occ in occasions):
            score += 0.2
        
        # Personalization signals (0-0.2)
        personal_terms = ['personalized', 'meaningful', 'sentimental', 'special']
        if any(term in text for term in personal_terms):
            score += 0.2
        
        # Low competition (0-0.2)
        if thread.get('replies', 0) < 10:
            score += 0.2
        
        return min(score, 1.0)
    
    def _suggest_approach(self, thread: Dict, danger_level: int) -> str:
        """Suggest engagement approach based on danger level"""
        
        if danger_level >= 4:
            return "DO NOT ENGAGE - Too risky"
        
        elif danger_level == 3:
            return "EXTREME CAUTION - Only if genuinely helpful, no product mention"
        
        elif danger_level == 2:
            return "Careful approach - Share personal story, casual product mention if fits naturally"
        
        else:
            return "Standard whisper marketing - Be helpful first, mention SayPlay if directly relevant"
    
    def _generate_warning(self, danger_level: int) -> str:
        """Generate warning message for human reviewer"""
        
        warnings = {
            0: "✅ Relatively safe - Genuine question, helpful community",
            1: "⚠️  Low risk - Normal conversation, be authentic",
            2: "⚠️⚠️ Medium risk - Some marketing sensitivity detected",
            3: "⚠️⚠️⚠️ HIGH RISK - Anti-marketing sentiment present",
            4: "🚨 VERY HIGH RISK - Active anti-spam discussion",
            5: "🚨🚨🚨 EXTREME RISK - DO NOT ENGAGE"
        }
        
        return warnings.get(danger_level, "Unknown risk level")
    
    def generate_response_template(self, opportunity: Dict) -> str:
        """
        Generate response template for human to edit
        
        This is NOT for auto-posting.
        This is to give human a starting point.
        """
        
        title = opportunity['title']
        danger = opportunity['danger_level']
        
        if danger >= 3:
            return """
⚠️  HIGH RISK THREAD - Consider NOT engaging

If you must engage:
1. Read full thread carefully
2. Be 100% authentic (share real experience)
3. Focus on helping, not selling
4. Only mention product if directly asked
5. Never use marketing language
6. Be prepared for scrutiny
"""
        
        # Detect if asking about grandparents
        is_grandparent = any(term in title.lower() for term in ['grandparent', 'granny', 'nan'])
        
        if is_grandparent:
            template = """
Suggested response (EDIT BEFORE POSTING):

"I faced the same dilemma last year! Ended up getting my grandparents something they could use to hear messages from the grandkids. 

[SHARE YOUR REAL EXPERIENCE HERE - be specific and personal]

They absolutely loved being able to hear the kids' voices whenever they wanted. 

[ONLY IF ASKED: It was from SayPlay - basically a card with a voice message you can tap with your phone]

Hope that helps! X"

⚠️  IMPORTANT:
- Make it YOUR story (personalize it)
- Remove ANY sales language
- Only mention brand if it adds value
- Be ready to engage in genuine conversation if they reply
"""
        else:
            template = """
Suggested response (EDIT BEFORE POSTING):

"Have you thought about [GENUINE HELPFUL SUGGESTION]?

[SHARE REAL EXPERIENCE OR KNOWLEDGE]

[ONLY IF DIRECTLY RELEVANT: Mention SayPlay naturally]

Hope this helps! X"

⚠️  Remember: Be helpful FIRST, mention product ONLY if it genuinely solves their problem
"""
        
        return template


if __name__ == "__main__":
    """Test Mumsnet monitor"""
    
    print("👀 Testing Mumsnet Monitor...")
    print("\n⚠️⚠️⚠️ EXTREME CAUTION MODE ⚠️⚠️⚠️")
    print("    Mumsnet = UK Holy Grail BUT also extremely risky")
    print("    Users detect marketing instantly")
    print("    NEVER auto-post. Human review ALWAYS required.")
    
    monitor = MumsnetMonitor()
    
    print("\n📡 Monitoring Mumsnet for gift conversations...")
    
    # This would be async in real usage
    # opportunities = asyncio.run(monitor.find_opportunities())
    
    print("\n✅ Mumsnet Monitor ready!")
    print("   Use ONLY for intelligence gathering")
    print("   Engage ONLY if you can add genuine value")
    print("   When in doubt - DON'T POST")
