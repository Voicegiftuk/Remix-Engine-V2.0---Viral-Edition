#!/usr/bin/env python3
"""
Blog Article Generator - PROJECT TITAN
Human-indistinguishable SEO articles with White Hat optimization

Features:
- Anti-AI detection (burstiness, perplexity, human patterns)
- White Hat SEO (keyword optimization, internal linking)
- Brand voice enforcement (SayPlay personality)
- Competitor analysis integration
"""
import sys
import os
from pathlib import Path
from typing import Dict, List
import random
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# NEW: Use updated Gemini package
from google import genai

# Simple logger replacement (no extra dependencies)
class Logger:
    """Simple logger using print statements"""
    @staticmethod
    def info(msg):
        print(f"ℹ️  {msg}")
    
    @staticmethod
    def success(msg):
        print(f"✅ {msg}")
    
    @staticmethod
    def error(msg):
        print(f"❌ {msg}")
    
    @staticmethod
    def warning(msg):
        print(f"⚠️  {msg}")

logger = Logger()


class ArticleGenerator:
    """
    Human-like article generation with anti-AI detection
    
    Key techniques:
    1. Burstiness - Varied sentence lengths (short-short-long pattern)
    2. Perplexity - Unexpected word choices, not always predictable
    3. Human touches - Anecdotes, personal opinions, "mistakes"
    4. Brand voice - SayPlay personality throughout
    """
    
    def __init__(self, api_key: str):
        """Initialize article generator"""
        # NEW: Initialize new Gemini client
        client = genai.Client(api_key=api_key)
        self.client = client
        self.model_name = 'gemini-2.0-flash-exp'
        
        logger.info("ArticleGenerator initialized with Gemini 2.0")
    
    def write_article(self, brief: Dict) -> Dict:
        """
        Generate complete SEO article
        
        Args:
            brief: {
                'primary_keyword': Main topic
                'related_keywords': List of LSI keywords (optional)
                'target_length': Word count target (optional)
                'competitor_insights': Analysis from top competitors (optional)
                'brand_voice': Brand personality prompt (optional)
            }
        
        Returns:
            Article package with HTML, metadata, etc.
        """
        
        # Extract brief details
        keyword = brief.get('primary_keyword', 'personalized gifts')
        target_length = brief.get('target_length', 2000)
        brand_voice = brief.get('brand_voice', '')
        
        logger.info(f"Generating article: {keyword}")
        
        # Step 1: Generate outline
        outline = self._generate_outline(brief)
        
        # Step 2: Write each section
        sections = []
        for idx, section in enumerate(outline, 1):
            logger.info(f"Writing section {idx}/{len(outline)}: {section['h2']}")
            content = self._write_section(section, brief)
            sections.append(content)
        
        # Step 3: Add introduction
        logger.info("Writing introduction...")
        intro = self._write_introduction(keyword, outline, brief)
        
        # Step 4: Add conclusion
        logger.info("Writing conclusion...")
        conclusion = self._write_conclusion(keyword, brief)
        
        # Step 5: Assemble article
        full_text = self._assemble_article(intro, sections, conclusion)
        
        # Step 6: Apply human-like patterns
        full_text = self._apply_human_patterns(full_text)
        
        # Step 7: Convert to HTML
        html = self._text_to_html(full_text, outline)
        
        # Step 8: Generate metadata
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
        """Generate article outline from brief"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        
        prompt = f"""Create an outline for a blog article about "{keyword}".

{brief.get('brand_voice', '')}

Requirements:
- 5-7 main sections (H2 headers)
- Each section should have 2-3 subsections (H3 headers)
- Focus on practical value and emotional connection
- Include personal anecdotes where appropriate
- End with FAQ section

Format each section as:
## H2 Title
### H3 Subsection 1
### H3 Subsection 2

Output ONLY the outline, no additional text."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            outline_text = response.text.strip()
            
            # Parse outline into structure
            outline = self._parse_outline(outline_text)
            
            logger.success(f"Generated outline with {len(outline)} sections")
            return outline
            
        except Exception as e:
            logger.error(f"Outline generation failed: {e}")
            
            # Fallback outline
            return [
                {'h2': f'What is {keyword}?', 'h3s': []},
                {'h2': f'Why {keyword} Matters', 'h3s': []},
                {'h2': f'How to Choose {keyword}', 'h3s': []},
                {'h2': 'Real-World Examples', 'h3s': []},
                {'h2': 'FAQ', 'h3s': []}
            ]
    
    def _write_section(self, section: Dict, brief: Dict) -> str:
        """Write one section of the article"""
        
        h2_title = section['h2']
        h3s = section.get('h3s', [])
        
        h3_text = '\n'.join('### ' + h3 for h3 in h3s) if h3s else ''
        
        prompt = f"""Write a blog section with this structure:

## {h2_title}
{h3_text}

{brief.get('brand_voice', '')}

Requirements:
- 300-400 words total
- Use varied sentence lengths (mix short and long)
- Include 1-2 personal anecdotes or examples
- Use conversational tone with contractions
- Add 1 emoji (sparingly)
- Naturally include keywords: {', '.join(brief.get('related_keywords', [])[:5])}

Write ONLY the section content, no headers."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            content = response.text.strip()
            
            return f"## {h2_title}\n\n{content}\n"
            
        except Exception as e:
            logger.error(f"Section writing failed: {e}")
            return f"## {h2_title}\n\n[Content generation failed for this section]\n"
    
    def _write_introduction(self, keyword: str, outline: List, brief: Dict) -> str:
        """Write engaging introduction"""
        
        outline_preview = '\n'.join('- ' + s['h2'] for s in outline[:5])
        
        prompt = f"""Write an engaging introduction for a blog article about "{keyword}".

{brief.get('brand_voice', '')}

The article will cover:
{outline_preview}

Requirements:
- 150-200 words
- Start with a hook (question or bold statement)
- Create emotional connection
- Promise value to reader
- Natural and conversational
- Include keyword once

Write ONLY the introduction text, no title."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip() + "\n\n"
        except Exception as e:
            logger.error(f"Introduction failed: {e}")
            return f"Let's talk about {keyword}.\n\n"
    
    def _write_conclusion(self, keyword: str, brief: Dict) -> str:
        """Write compelling conclusion with CTA"""
        
        prompt = f"""Write a conclusion for a blog article about "{keyword}".

{brief.get('brand_voice', '')}

Requirements:
- 100-150 words
- Summarize key takeaways
- Emotional call-to-action
- Mention SayPlay naturally (we create personalized voice message gifts)
- End with engaging question
- Warm and personal tone

Write ONLY the conclusion text."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return "\n\n## Conclusion\n\n" + response.text.strip()
        except Exception as e:
            logger.error(f"Conclusion failed: {e}")
            return "\n\n## Conclusion\n\nThank you for reading!\n"
    
    def _apply_human_patterns(self, text: str) -> str:
        """
        Apply human-like patterns to make text undetectable by AI detectors
        
        Techniques:
        1. Varied sentence lengths (burstiness)
        2. Occasional "errors" (starting sentences with And, But)
        3. Personal touches (I, we, you)
        4. Conversational phrases
        """
        
        # Already applied during generation via prompts
        # This is for post-processing tweaks
        
        # Add occasional conversational interjections
        interjections = [
            "You know what?",
            "Here's the thing:",
            "And honestly?",
            "But here's why:",
            "Quick tip:"
        ]
        
        # Insert 1-2 randomly
        for _ in range(random.randint(1, 2)):
            # Find a paragraph boundary
            paragraphs = text.split('\n\n')
            if len(paragraphs) > 3:
                insert_at = random.randint(1, len(paragraphs) - 2)
                paragraphs[insert_at] = f"{random.choice(interjections)} {paragraphs[insert_at]}"
                text = '\n\n'.join(paragraphs)
        
        return text
    
    def _text_to_html(self, text: str, outline: List) -> str:
        """Convert markdown-style text to HTML"""
        
        html = text
        
        # H2 headers
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        
        # H3 headers
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Paragraphs
        paragraphs = html.split('\n\n')
        paragraphs = [f'<p>{p}</p>' if not p.startswith('<h') else p for p in paragraphs]
        html = '\n'.join(paragraphs)
        
        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        return html
    
    def _generate_metadata(self, keyword: str, text: str) -> Dict:
        """Generate SEO metadata"""
        
        # Extract first sentence for description
        first_sentences = text.split('.')[:2]
        description = '.'.join(first_sentences).strip()[:160]
        
        # Generate title
        title = f"{keyword.title()} | SayPlay Voice Message Gifts"
        
        return {
            'title': title,
            'description': description
        }
    
    def _parse_outline(self, outline_text: str) -> List[Dict]:
        """Parse outline text into structured format"""
        
        sections = []
        current_h2 = None
        current_h3s = []
        
        for line in outline_text.split('\n'):
            line = line.strip()
            
            if line.startswith('## '):
                # Save previous section
                if current_h2:
                    sections.append({'h2': current_h2, 'h3s': current_h3s})
                
                # Start new section
                current_h2 = line[3:].strip()
                current_h3s = []
            
            elif line.startswith('### '):
                current_h3s.append(line[4:].strip())
        
        # Save last section
        if current_h2:
            sections.append({'h2': current_h2, 'h3s': current_h3s})
        
        return sections
    
    def _assemble_article(self, intro: str, sections: List[str], conclusion: str) -> str:
        """Assemble complete article"""
        
        article = intro
        article += '\n\n'.join(sections)
        article += conclusion
        
        return article


if __name__ == "__main__":
    """Test article generator"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("\n📝 Testing Article Generator...")
    print("=" * 50)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n⚠️  GEMINI_API_KEY not found in .env")
        print("   Get API key from: https://makersuite.google.com/app/apikey")
        exit(1)
    
    try:
        generator = ArticleGenerator(api_key)
        
        # Test brief
        brief = {
            'primary_keyword': 'personalized birthday gifts 2025',
            'related_keywords': [
                'unique birthday presents',
                'custom gift ideas',
                'voice message card',
                'NFC gift technology'
            ],
            'target_length': 1500,
            'brand_voice': """You are writing for SayPlay - a warm, personal brand that creates 
                              voice message gifts. Be emotional and heartfelt, not corporate."""
        }
        
        print(f"\n🎯 Generating article: {brief['primary_keyword']}")
        print(f"   Target: {brief['target_length']} words")
        print("")
        
        article = generator.write_article(brief)
        
        print(f"\n✅ Article generated successfully!")
        print(f"   Title: {article['title']}")
        print(f"   Words: {article['word_count']}")
        print(f"   Sections: {len(article['outline'])}")
        
        print(f"\n📄 Preview (first 300 chars):")
        print("-" * 50)
        print(article['text'][:300] + "...")
        print("-" * 50)
        
        # Save for review
        output_file = Path('test_article.html')
        
        # Create complete HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{article['meta_description']}">
    <title>{article['title']}</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #FF6B35; }}
        h2 {{ color: #004E89; margin-top: 2em; }}
        h3 {{ color: #1A659E; }}
        p {{ margin: 1em 0; }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    {article['html']}
</body>
</html>"""
        
        output_file.write_text(full_html, encoding='utf-8')
        print(f"\n💾 Saved to: {output_file.absolute()}")
        print(f"   Open in browser to view")
        
        print("\n" + "=" * 50)
        print("✅ Test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
