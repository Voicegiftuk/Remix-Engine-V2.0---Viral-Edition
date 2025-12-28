#!/usr/bin/env python3
"""View content generation statistics"""
import json
from pathlib import Path
from datetime import datetime


def show_stats():
    """Display content statistics"""
    
    db_file = Path('titan_modules/blog/intelligence/topics_database.json')
    
    if not db_file.exists():
        print("No statistics yet. Generate some articles first!")
        return
    
    with open(db_file, 'r') as f:
        db = json.load(f)
    
    print("\n" + "=" * 60)
    print("📊 TITAN CONTENT ENGINE - STATISTICS")
    print("=" * 60)
    
    print(f"\n📈 Total Articles Generated: {db['stats']['total_generated']}")
    
    print(f"\n📁 By Category:")
    for cat, count in sorted(db['stats']['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat.title()}: {count}")
    
    print(f"\n🕐 Last Update: {db.get('last_update', 'Never')}")
    print(f"📝 Last Category: {db.get('last_category', 'None')}")
    
    print(f"\n🎯 Unique Topics Used: {len(db['used_topics'])}")
    
    if db['used_topics']:
        print(f"\n📋 Recent Topics:")
        for topic in db['used_topics'][-5:]:
            print(f"   • {topic}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    show_stats()
