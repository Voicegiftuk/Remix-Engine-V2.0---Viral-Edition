#!/usr/bin/env python3
"""
TITAN MASTER ORCHESTRATOR V2 - TEST VERSION
"""
import sys
import os
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent))

from titan_modules.core.multi_topic_generator import MultiTopicGenerator

def main():
    print("\n" + "="*70)
    print("TITAN V2 - TEST RUN")
    print("="*70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    output_dir = Path(f'TITAN_OUTPUT_{timestamp}')
    output_dir.mkdir(exist_ok=True)
    
    # Create web directory
    web_dir = output_dir / 'web'
    web_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate topics
    topic_gen = MultiTopicGenerator()
    topics = topic_gen.generate_daily_topics(count=10)
    
    # Create simple index.html
    html = f'''<!DOCTYPE html>
<html>
<head>
    <title>SayPlay - Test Deployment</title>
</head>
<body style="font-family: Arial; padding: 50px; text-align: center;">
    <h1 style="color: #667eea;">Say<span style="color: #FFD700;">Play</span></h1>
    <h2>Titan V2 Test Deployment</h2>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p>Topics generated: {len(topics)}</p>
</body>
</html>'''
    
    with open(web_dir / 'index.html', 'w') as f:
        f.write(html)
    
    print(f"\n✅ Test output created: {output_dir}")
    print(f"✅ Web content ready for deployment")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
