#!/usr/bin/env python3
"""Blog Article Generator - PROJECT TITAN"""
import sys
import os
from pathlib import Path
from typing import Dict, List
import random
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import google.generativeai as genai

class Logger:
    @staticmethod
    def info(msg): print(f"INFO: {msg}")
    @staticmethod
    def success(msg): print(f"SUCCESS: {msg}")
    @staticmethod
    def error(msg): print(f"ERROR: {msg}")
    @staticmethod
    def warning(msg): print(f"WARNING: {msg}")

logger = Logger()


class ArticleGenerator:
    """Human-like article generation with anti-AI detection"""
    
    def __init__(self, api_key: str):
        """Initialize article generator"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("ArticleGenerator initialized")
    
    def write_article(self, brief: Dict) -> Dict:
        """Generate complete SEO article"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        target_length = brief.get('target_length', 2000)
        brand_voice = brief.get('brand_voice', '')
        
        logger.info(f"Generating article: {keyword}")
        
        outline = self._generate_outline(brief)
        
        sections = []
        for idx, section in enumerate(outline, 1):
            logger.info(f"Writing section {idx}/{len(outline)}: {section['h2']}")
            content = self._write_section(section, brief)
            sections.append(content)
        
        logger.info("Writing introduction...")
        intro = self._write_introduction(keyword, outline, brief)
        
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
        """Generate article outline from brief"""
        
        keyword = brief.get('primary_keyword', 'personalized gifts')
        
        prompt = f"""Create an outline for a blog article about "{keyword}".

Requirements:
- 5-7 main sections (H2 headers)
- Each section should have 2-3 subsections (H3 headers)
- Focus on practical value and emotional connection

Format each section as:
## H2 Title
### H3 Subsection 1
### H3 Subsection 2

Output ONLY the outline, no additional text."""
        
        try:
            response = self.model.generate_content(prompt)
            outline_text = response.text.strip()
            outline = self._parse_outline(outline_text)
            logger.success(f"Generated outline with {len(outline)} sections")
            return outline
            
        except Exception as e:
            logger.error(f"Outline generation failed: {e}")
            return [
                {'h2': f'What Makes {keyword} Special?', 'h3s': []},
                {'h2': f'Why Choose {keyword}', 'h3s': []},
                {'h2': f'How to Select the Perfect {keyword}', 'h3s': []},
                {'h2': 'Real Customer Stories', 'h3s': []},
                {'h2': 'Frequently Asked Questions', 'h3s': []}
            ]
    
    def _write_section(self, section: Dict, brief: Dict) -> str:
        """Write one section of the article"""
        
        h2_title = section['h2']
        h3s = section.get('h3s', [])
        
        h3_text = '\n'.join('### ' + h3 for h3 in h3s) if h3s else ''
        
        prompt = f"""Write a blog section about: {h2_title}

Requirements:
- 300-400 words
- Conversational and warm tone
- Use real examples
- Natural keyword usage

Write the content (no headers)."""
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            return f"## {h2_title}\n\n{content}\n"
            
        except Exception as e:
            logger.error(f"Section writing failed: {e}")
            return f"## {h2_title}\n\nThis is where we'd discuss the importance of {h2_title.lower()}. SayPlay creates personalized voice message gifts that capture authentic moments and emotions.\n"
    
    def _write_introduction(self, keyword: str, outline: List, brief: Dict) -> str:
        """Write engaging introduction"""
        
        prompt = f"""Write an engaging 150-word introduction for a blog about "{keyword}".

Start with a question or bold statement.
Be warm and personal.
Promise value to the reader.

Write ONLY the introduction."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip() + "\n\n"
        except Exception as e:
            logger.error(f"Introduction failed: {e}")
            return f"Finding the perfect {keyword} can transform a simple celebration into an unforgettable memory. At SayPlay, we believe gifts should do more than just look good – they should capture real emotions and authentic moments.\n\n"
    
    def _write_conclusion(self, keyword: str, brief: Dict) -> str:
        """Write compelling conclusion with CTA"""
        
        prompt = f"""Write a 100-word conclusion for a blog about "{keyword}".

Summarize key points.
Mention SayPlay (voice message gifts).
End with a warm call-to-action.

Write ONLY the conclusion."""
        
        try:
            response = self.model.generate_content(prompt)
            return "\n\n## Conclusion\n\n" + response.text.strip()
        except Exception as e:
            logger.error(f"Conclusion failed: {e}")
            return "\n\n## Conclusion\n\nThe best gifts aren't found in stores – they're created from the heart. SayPlay helps you capture authentic moments in voice messages that last forever. Ready to create something truly special?\n"
    
    def _apply_human_patterns(self, text: str) -> str:
        """Apply human-like patterns"""
        interjections = [
            "You know what?",
            "Here's the thing:",
            "And honestly?",
            "But here's why:",
            "Quick tip:"
        ]
        
        for _ in range(random.randint(1, 2)):
            paragraphs = text.split('\n\n')
            if len(paragraphs) > 3:
                insert_at = random.randint(1, len(paragraphs) - 2)
                paragraphs[insert_at] = f"{random.choice(interjections)} {paragraphs[insert_at]}"
                text = '\n\n'.join(paragraphs)
        
        return text
    
    def _text_to_html(self, text: str, outline: List) -> str:
        """Convert markdown-style text to HTML"""
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
        """Generate SEO metadata"""
        first_sentences = text.split('.')[:2]
        description = '.'.join(first_sentences).strip()[:160]
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
                if current_h2:
                    sections.append({'h2': current_h2, 'h3s': current_h3s})
                current_h2 = line[3:].strip()
                current_h3s = []
            elif line.startswith('### '):
                current_h3s.append(line[4:].strip())
        
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
    
    print("\nTesting Article Generator...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\nGEMINI_API_KEY not found in .env")
        exit(1)
    
    try:
        generator = ArticleGenerator(api_key)
        
        brief = {
            'primary_keyword': 'personalized birthday gifts 2025',
            'related_keywords': [
                'unique birthday presents',
                'custom gift ideas',
                'voice message card'
            ],
            'target_length': 1500,
            'brand_voice': 'Warm, personal brand creating voice message gifts'
        }
        
        print(f"\nGenerating article: {brief['primary_keyword']}")
        
        article = generator.write_article(brief)
        
        print(f"\nArticle generated successfully!")
        print(f"Title: {article['title']}")
        print(f"Words: {article['word_count']}")
        print(f"Sections: {len(article['outline'])}")
        
        print(f"\nPreview:")
        print(article['text'][:300] + "...")
        
        output_file = Path('test_article.html')
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{article['title']}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #FF6B35; }}
        h2 {{ color: #004E89; margin-top: 2em; }}
        h3 {{ color: #1A659E; }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    {article['html']}
</body>
</html>"""
        
        output_file.write_text(full_html, encoding='utf-8')
        print(f"\nSaved to: {output_file.absolute()}")
        print("Test complete!")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
And update requirements_titan.txt:
txt# Use OLD package (still works better)
google-generativeai>=0.3.0

# Core dependencies
requests>=2.31.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
Pillow>=10.0.0
aiohttp>=3.9.0
python-slugify>=8.0.0
