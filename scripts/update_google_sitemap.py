"""
GOOGLE SEARCH CONSOLE SITEMAP UPDATER
Automatically updates sitemap in Google Search Console
"""
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
from datetime import datetime


class GoogleSitemapUpdater:
    """
    Update sitemap in Google Search Console
    """
    
    def __init__(self):
        # Load service account credentials from environment
        credentials_json = os.getenv('GOOGLE_SEARCH_CONSOLE_KEY')
        
        if credentials_json:
            import json
            credentials_dict = json.loads(credentials_json)
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/webmasters']
            )
            self.service = build('searchconsole', 'v1', credentials=self.credentials)
        else:
            print("⚠️ GOOGLE_SEARCH_CONSOLE_KEY not set")
            self.service = None
    
    def generate_sitemap(self, output_dir: Path) -> Path:
        """Generate sitemap.xml from all articles"""
        print("\n🗺 Generating sitemap...")
        
        sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
        
        # Add blog articles
        blog_dir = output_dir / 'web' / 'blog'
        if blog_dir.exists():
            for html_file in blog_dir.glob('*.html'):
                slug = html_file.stem
                url = f"https://sayplay.co.uk/blog/{slug}"
                lastmod = datetime.now().strftime('%Y-%m-%d')
                
                sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''
        
        # Add SEO pages
        seo_dir = output_dir / 'web' / 'seo'
        if seo_dir.exists():
            for html_file in seo_dir.glob('*.html'):
                slug = html_file.stem
                url = f"https://sayplay.co.uk/seo/{slug}"
                lastmod = datetime.now().strftime('%Y-%m-%d')
                
                sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
        
        sitemap_content += '</urlset>'
        
        # Save sitemap
        sitemap_file = output_dir / 'web' / 'sitemap.xml'
        with open(sitemap_file, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"✅ Sitemap generated: {sitemap_file}")
        
        return sitemap_file
    
    def submit_sitemap(self, sitemap_url: str = "https://sayplay.co.uk/sitemap.xml"):
        """Submit sitemap to Google Search Console"""
        
        if not self.service:
            print("⚠️ Cannot submit - credentials not configured")
            return False
        
        print(f"\n📤 Submitting sitemap to Google Search Console...")
        print(f"   URL: {sitemap_url}")
        
        try:
            site_url = "https://sayplay.co.uk"
            
            # Submit sitemap
            self.service.sitemaps().submit(
                siteUrl=site_url,
                feedpath=sitemap_url
            ).execute()
            
            print(f"✅ Sitemap submitted successfully")
            print(f"   Google will crawl your new pages within 24-48 hours")
            
            return True
            
        except Exception as e:
            print(f"❌ Submission failed: {e}")
            return False


def main():
    """Main function"""
    # Find latest output directory
    output_dirs = sorted(Path('.').glob('TITAN_OUTPUT_*'), reverse=True)
    
    if not output_dirs:
        print("❌ No output directory found")
        return
    
    output_dir = output_dirs[0]
    print(f"📁 Using output: {output_dir}")
    
    updater = GoogleSitemapUpdater()
    
    # Generate sitemap
    sitemap_file = updater.generate_sitemap(output_dir)
    
    # Submit to Google
    updater.submit_sitemap()


if __name__ == '__main__':
    main()
