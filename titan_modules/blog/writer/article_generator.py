#!/usr/bin/env python3
"""Blog Article Generator - NEW GOOGLE GENAI SDK"""
import sys
import os
import time
from pathlib import Path
from typing import Dict, List
import random
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# NEW GOOGLE GENAI SDK
from google import genai
from google.genai import types

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
    """Article generation with NEW Google Genai SDK"""
    
    def __init__(self, api_key: str):
        """Initialize with NEW SDK"""
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-2.0-flash-exp'
        
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
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 3
                    time.sleep(wait_time)
                else:
                    raise
        
        return ""
    
    def write_article(self, brief: Dict) -> Dict:
        """Generate complete article"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        
        logger.info(f"Generating article: {keyword}")
        
        # Generate outline
        outline = self._generate_outline(brief)
        time.sleep(2)
        
        # Write sections with delays
        sections = []
        for idx, section in enumerate(outline, 1):
            logger.info(f"Writing section {idx}/{len(outline)}: {section['h2']}")
            
            content = self._write_section(section, brief)
            sections.append(content)
            
            if idx < len(outline):
                time.sleep(3)
        
        # Intro and conclusion
        logger.info("Writing introduction...")
        intro = self._write_introduction(keyword, outline, brief)
        time.sleep(2)
        
        logger.info("Writing conclusion...")
        conclusion = self._write_conclusion(keyword, brief)
        
        # Assemble
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
    
    def _write_section(self, section: Dict, brief: Dict) -> str:
        """Write one section"""
        
        h2_title = section['h2']
        
        prompt = f"""Write 250-300 words about: {h2_title}

Write in a warm, conversational tone. Include practical examples and personal insights. Make it engaging and helpful."""
        
        try:
            content = self._call_api(prompt)
            
            if len(content) > 100:
                logger.success(f"Section complete: {len(content)} chars")
                return f"## {h2_title}\n\n{content}\n"
            else:
                raise Exception("Content too short")
                
        except Exception as e:
            logger.error(f"Section failed: {e}")
            
            # Enhanced fallback
            return f"""## {h2_title}

When it comes to {h2_title.lower()}, personalized voice message gifts from SayPlay offer something truly unique. Our NFC-enabled greeting cards let you record heartfelt messages that recipients can play instantly with a simple tap - no app download required.

What makes these gifts special is their ability to capture authentic emotions in your own voice. Whether you're celebrating a birthday, anniversary, or any special moment, your words become a lasting treasure that goes far beyond a traditional card or generic present.

The technology is beautifully simple: just tap the card with any smartphone, and your voice message plays immediately. It's this combination of cutting-edge NFC technology and timeless emotional connection that makes SayPlay gifts so meaningful.

"""
    
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
    
    print("\n🧪 Testing NEW Google Genai SDK...")
    
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
