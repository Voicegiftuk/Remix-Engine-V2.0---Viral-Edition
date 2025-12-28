#!/usr/bin/env python3
"""Blog Article Generator - UNIQUE FALLBACKS"""
import sys
import os
import time
from pathlib import Path
from typing import Dict, List
import random
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from google import genai

class Logger:
    @staticmethod
    def info(msg): print(f"ℹ️  {msg}")
    @staticmethod
    def success(msg): print(f"✅ {msg}")
    @staticmethod
    def error(msg): print(f"❌ {msg}")
    @staticmethod
    def warning(msg): print(f"⚠️  {msg}")

logger = Logger()


class ArticleGenerator:
    """Article generator with unique fallback content"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-1.5-flash'
        self.section_counter = 0  # Track which section we're on
        
        logger.info(f"ArticleGenerator initialized with {self.model}")
    
    def _call_api(self, prompt: str, max_retries: int = 3) -> str:
        """Call API with retry logic"""
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                
                if response and response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response")
                    
            except Exception as e:
                error_msg = str(e)
                
                if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
                    logger.warning(f"Quota exceeded! Attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        wait_time = 60
                        logger.info(f"Waiting {wait_time}s for quota reset...")
                        time.sleep(wait_time)
                    else:
                        raise
                else:
                    logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep((attempt + 1) * 5)
                    else:
                        raise
        
        return ""
    
    def write_article(self, brief: Dict) -> Dict:
        """Generate complete article"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        self.section_counter = 0  # Reset counter
        
        logger.info(f"Generating article: {keyword}")
        
        outline = self._generate_outline(brief)
        time.sleep(5)
        
        sections = []
        for idx, section in enumerate(outline, 1):
            self.section_counter = idx  # Track section number
            logger.info(f"Writing section {idx}/{len(outline)}: {section['h2']}")
            
            content = self._write_section(section, brief)
            sections.append(content)
            
            if idx < len(outline):
                time.sleep(8)
        
        logger.info("Writing introduction...")
        intro = self._write_introduction(keyword, outline, brief)
        time.sleep(5)
        
        logger.info("Writing conclusion...")
        conclusion = self._write_conclusion(keyword, brief)
        
        full_text = self._assemble_article(intro, sections, conclusion)
        full_text = self._apply_human_patterns(full_text)
        html = self._text_to_html(full_text, outline)
        meta = self._generate_metadata(keyword, full_text)
        
        result = {
            'text': full_text,
            'html': html,
            'title': meta['title'],
            'meta_description': meta['description'],
            'word_count': len(full_text.split()),
            'outline': outline
        }
        
        logger.success(f"Article complete: {result['word_count']} words")
        return result
    
    def _generate_outline(self, brief: Dict) -> List[Dict]:
        """Generate outline"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        
        prompt = f"""Create a 5-section outline for an article about "{keyword}".

Format as:
## Section 1 Title
## Section 2 Title
## Section 3 Title
## Section 4 Title
## Section 5 Title

Make titles clear and engaging."""
        
        try:
            outline_text = self._call_api(prompt)
            outline = self._parse_outline(outline_text)
            
            if len(outline) >= 3:
                logger.success(f"Generated outline with {len(outline)} sections")
                return outline
            else:
                raise Exception("Too few sections")
                
        except Exception as e:
            logger.error(f"Outline failed: {e}")
            return [
                {'h2': f'Why Choose {keyword.title()}', 'h3s': []},
                {'h2': 'Key Features and Benefits', 'h3s': []},
                {'h2': 'How to Select the Perfect Gift', 'h3s': []},
                {'h2': 'Real Customer Experiences', 'h3s': []},
                {'h2': 'Frequently Asked Questions', 'h3s': []}
            ]
    
    def _get_unique_fallback(self, section_title: str, keyword: str) -> str:
        """Generate UNIQUE fallback content for each section"""
        
        # Different templates based on section number
        templates = {
            1: f"""## {section_title}

Voice message gifts represent a revolutionary way to celebrate life's special moments. Unlike traditional greeting cards that offer only printed words, SayPlay's NFC-enabled cards transform your heartfelt sentiments into an interactive experience that recipients can treasure forever.

The beauty of {keyword} lies in their personal touch. When you record a message in your own voice, you're not just sending words – you're sharing emotion, tone, and the genuine warmth that only your voice can convey. This creates an intimate connection that printed text simply cannot replicate.

With SayPlay's innovative technology, there's no complicated setup required. Recipients simply tap their smartphone to the card, and your voice message plays instantly. It's this perfect blend of simplicity and emotional depth that makes voice message gifts truly special for any occasion.""",

            2: f"""## {section_title}

What sets SayPlay apart is our commitment to making meaningful gifting accessible to everyone. Our voice message cards combine cutting-edge NFC technology with timeless emotional connection, creating gifts that resonate long after the celebration ends.

The personalization possibilities are endless. Record birthday wishes, anniversary messages, words of encouragement, or simply express your love – all captured in your authentic voice. Each message becomes a keepsake that recipients can replay whenever they need to feel connected to you.

Our cards work with any modern smartphone, requiring no special apps or downloads. This universal compatibility ensures that anyone can experience your heartfelt message, making SayPlay the perfect choice for tech-savvy and traditional gift-givers alike.""",

            3: f"""## {section_title}

Selecting the right gift involves understanding both the occasion and the recipient. With SayPlay voice message cards, you're choosing more than just a physical item – you're creating an emotional experience that will be remembered for years to come.

Consider the message you want to convey. Is it celebratory? Sentimental? Encouraging? Your voice naturally carries these emotions in ways that written words cannot fully express. This makes voice message gifts particularly powerful for milestone celebrations and meaningful occasions.

The versatility of our cards means they work beautifully for any event – from birthdays and weddings to graduations and thank-you gestures. Each card becomes a unique, personalized treasure that reflects the special bond you share with the recipient.""",

            4: f"""## {section_title}

Customers consistently share how SayPlay gifts have transformed their celebrations into unforgettable moments. Many tell us that recipients replay their voice messages repeatedly, finding comfort and joy in hearing their loved one's voice whenever they need it.

One grandmother shared how her grandchildren treasure their birthday cards, playing her recorded messages every night before bed. Another customer described how their anniversary message brought tears of joy to their partner, who keeps the card displayed prominently at their desk.

These stories highlight the lasting impact of personalized voice messages. Unlike traditional gifts that may be used once and forgotten, SayPlay cards become cherished keepsakes that strengthen emotional connections across any distance.""",

            5: f"""## {section_title}

Many people wonder about the technical aspects and practicality of voice message gifts. The good news is that SayPlay cards are designed with simplicity in mind, requiring minimal technical knowledge while delivering maximum emotional impact.

Recording your message is straightforward – simply use your smartphone to capture your voice, then transfer it to the card. The NFC technology embedded in each card ensures reliable playback on any compatible device, making the experience seamless for recipients of all ages.

Regarding durability, our cards are built to last, allowing recipients to enjoy your message for years to come. Whether kept as a treasured keepsake or displayed prominently, each SayPlay card represents a permanent reminder of your thoughtfulness and the special bond you share."""
        }
        
        # Use modulo to cycle through templates if we have more sections
        template_num = ((self.section_counter - 1) % 5) + 1
        
        return templates.get(template_num, templates[1])
    
    def _write_section(self, section: Dict, brief: Dict) -> str:
        """Write one section with unique fallback"""
        
        h2_title = section['h2']
        keyword = brief.get('primary_keyword', 'personalized gifts')
        
        prompt = f"""Write 250-300 words about: {h2_title}

Context: This is for an article about {keyword}.
Write in a warm, conversational tone. Include practical examples and personal insights."""
        
        try:
            content = self._call_api(prompt)
            
            if len(content) > 100:
                logger.success(f"Section complete: {len(content)} chars")
                return f"## {h2_title}\n\n{content}\n"
            else:
                raise Exception("Content too short")
                
        except Exception as e:
            logger.error(f"Section failed: {e}")
            logger.warning(f"Using unique fallback #{self.section_counter}")
            
            # Return UNIQUE fallback based on section number
            return self._get_unique_fallback(h2_title, keyword)
    
    def _write_introduction(self, keyword: str, outline: List, brief: Dict) -> str:
        """Write introduction"""
        
        prompt = f"""Write a warm, engaging 100-word introduction for an article about "{keyword}".

Start with something relatable. Be conversational and welcoming."""
        
        try:
            return self._call_api(prompt) + "\n\n"
        except Exception as e:
            logger.error(f"Intro failed: {e}")
            return f"Finding the perfect {keyword} can transform an ordinary celebration into an extraordinary memory. At SayPlay, we've revolutionized gift-giving by creating voice message cards that capture real emotions and authentic moments in a way that lasts forever.\n\n"
    
    def _write_conclusion(self, keyword: str, brief: Dict) -> str:
        """Write conclusion"""
        
        prompt = f"""Write a 100-word conclusion for an article about "{keyword}".

Mention SayPlay voice message gifts. End with encouragement and call to action."""
        
        try:
            return "\n\n## Conclusion\n\n" + self._call_api(prompt)
        except Exception as e:
            logger.error(f"Conclusion failed: {e}")
            return "\n\n## Conclusion\n\nThe most meaningful gifts come from the heart, and SayPlay's voice message cards help you express what words on paper never could. With our simple tap-to-play technology, you can create lasting memories that recipients will treasure for years to come. Ready to make your next gift truly unforgettable?\n"
    
    def _apply_human_patterns(self, text: str) -> str:
        """Add natural variations"""
        interjections = [
            "You know what?",
            "Here's the thing:",
            "And honestly?",
            "But here's why:",
            "Quick insight:"
        ]
        
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 4:
            insert_at = random.randint(2, len(paragraphs) - 2)
            paragraphs[insert_at] = f"{random.choice(interjections)} {paragraphs[insert_at]}"
            text = '\n\n'.join(paragraphs)
        
        return text
    
    def _text_to_html(self, text: str, outline: List) -> str:
        """Convert to HTML"""
        html = text
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        paragraphs = html.split('\n\n')
        paragraphs = [f'<p>{p}</p>' if not p.startswith('<h') else p for p in paragraphs]
        html = '\n'.join(paragraphs)
        
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        return html
    
    def _generate_metadata(self, keyword: str, text: str) -> Dict:
        """Generate metadata"""
        first_sentences = text.split('.')[:2]
        description = '.'.join(first_sentences).strip()[:160]
        title = f"{keyword.title()} | SayPlay Voice Message Gifts"
        
        return {
            'title': title,
            'description': description
        }
    
    def _parse_outline(self, outline_text: str) -> List[Dict]:
        """Parse outline"""
        sections = []
        
        for line in outline_text.split('\n'):
            line = line.strip()
            
            if line.startswith('## '):
                title = line[3:].strip()
                if title:
                    sections.append({'h2': title, 'h3s': []})
            elif line.startswith('### '):
                if sections:
                    sections[-1]['h3s'].append(line[4:].strip())
        
        return sections if sections else [{'h2': 'Main Content', 'h3s': []}]
    
    def _assemble_article(self, intro: str, sections: List[str], conclusion: str) -> str:
        """Assemble article"""
        article = intro
        article += '\n\n'.join(sections)
        article += conclusion
        return article


if __name__ == "__main__":
    """Test generator"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print("\n🧪 Testing with UNIQUE fallbacks...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n❌ GEMINI_API_KEY not found")
        exit(1)
    
    try:
        generator = ArticleGenerator(api_key)
        
        brief = {
            'primary_keyword': 'personalized birthday gifts 2025',
            'related_keywords': ['unique gifts', 'voice message'],
            'target_length': 1500
        }
        
        print(f"\n📝 Generating: {brief['primary_keyword']}")
        
        article = generator.write_article(brief)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Words: {article['word_count']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
