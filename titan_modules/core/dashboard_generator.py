"""
INTERACTIVE DASHBOARD GENERATOR
Creates beautiful, interactive dashboard with all content links
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import json


class DashboardGenerator:
    """
    Generate interactive HTML dashboard
    Shows all generated content with live links
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.dashboard_dir = output_dir / 'web' / 'dashboard'
        self.dashboard_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, results: Dict, topics: List[Dict]) -> Path:
        """
        Generate complete dashboard
        """
        print("\n📊 Generating interactive dashboard...")
        
        dashboard_html = self._create_dashboard_html(results, topics)
        
        # Save dashboard
        dashboard_file = self.dashboard_dir / 'index.html'
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        print(f"✅ Dashboard created: {dashboard_file}")
        print(f"   Will be live at: https://dashboard.sayplay.co.uk")
        
        return dashboard_file
    
    def _create_dashboard_html(self, results: Dict, topics: List[Dict]) -> str:
        """Create dashboard HTML"""
        
        now = datetime.now()
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SayPlay Content Dashboard - {now.strftime("%Y-%m-%d")}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #e0e0e0;
        }}
        
        .logo {{
            font-size: 42px;
            font-weight: 800;
            color: #667eea;
        }}
        
        .logo span {{ color: #FFD700; }}
        
        .date-badge {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 24px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 16px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }}
        
        .stat-number {{
            font-size: 56px;
            font-weight: 800;
            margin: 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .stat-label {{
            font-size: 14px;
            opacity: 0.95;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .section-title {{
            font-size: 28px;
            color: #333;
            font-weight: 700;
        }}
        
        .section-count {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        
        .content-card {{
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s;
            background: white;
        }}
        
        .content-card:hover {{
            border-color: #667eea;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
            transform: translateY(-3px);
        }}
        
        .episode-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
            margin-left: 10px;
        }}
        
        .status-live {{
            background: #10b981;
            color: white;
        }}
        
        .status-published {{
            background: #3b82f6;
            color: white;
        }}
        
        .content-card h3 {{
            color: #667eea;
            margin-bottom: 12px;
            font-size: 19px;
            line-height: 1.4;
        }}
        
        .content-meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 18px;
            line-height: 1.6;
        }}
        
        .content-meta span {{
            display: inline-block;
            margin-right: 15px;
        }}
        
        .content-meta span::before {{
            content: "•";
            margin-right: 8px;
            color: #667eea;
            font-weight: bold;
        }}
        
        .action-buttons {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }}
        
        .btn-primary {{
            background: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-secondary {{
            background: #f3f4f6;
            color: #333;
        }}
        
        .btn-secondary:hover {{
            background: #e5e7eb;
        }}
        
        .btn-success {{
            background: #10b981;
            color: white;
        }}
        
        .btn-success:hover {{
            background: #059669;
        }}
        
        .image-preview {{
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .performance-section {{
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            padding: 30px;
            border-radius: 15px;
            margin-top: 40px;
        }}
        
        .performance-title {{
            font-size: 24px;
            color: #333;
            font-weight: 700;
            margin-bottom: 20px;
        }}
        
        .perf-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .perf-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .perf-value {{
            font-size: 36px;
            font-weight: 800;
            color: #667eea;
            margin: 10px 0;
        }}
        
        .perf-label {{
            font-size: 14px;
            color: #666;
            font-weight: 600;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}
        
        .refresh-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .refresh-btn:hover {{
            transform: scale(1.1) rotate(180deg);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            .logo {{
                font-size: 28px;
            }}
            
            .content-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">Say<span>Play</span> Content Dashboard</div>
            <div class="date-badge">
                📅 {now.strftime("%B %d, %Y")}
            </div>
        </div>

        <!-- Stats Overview -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Articles Published</div>
                <div class="stat-number">{results.get('articles_count', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Podcasts Live</div>
                <div class="stat-number">{results.get('podcasts_count', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Images Generated</div>
                <div class="stat-number">{results.get('images_count', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">SEO Pages</div>
                <div class="stat-number">{results.get('seo_pages', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Time Saved</div>
                <div class="stat-number">{results.get('time_saved_hours', 0)}h</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Cost Saved</div>
                <div class="stat-number">£{results.get('cost_saved', 0):,.0f}</div>
            </div>
        </div>

        <!-- Articles Section -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">📝 Articles</h2>
                <span class="section-count">{len(topics)} Published</span>
            </div>
            <div class="content-grid">
'''
        
        # Add article cards
        for i, topic in enumerate(topics, 1):
            slug = topic['title'].lower().replace(' ', '-').replace("'", '')
            html += f'''
                <div class="content-card">
                    <span class="episode-badge">Episode {i}</span>
                    <span class="status-badge status-live">LIVE</span>
                    <h3>{topic['title']}</h3>
                    <div class="content-meta">
                        <span>{topic.get('word_count', 1200)} words</span>
                        <span>{topic.get('reading_time', 6)} min read</span>
                        <span>Quality: {topic.get('quality_score', 89)}%</span>
                    </div>
                    <div class="action-buttons">
                        <a href="https://sayplay.co.uk/blog/{slug}" class="btn btn-primary" target="_blank">View Live</a>
                        <a href="../01_ARTICLE/{slug}.html" class="btn btn-secondary" download>Download HTML</a>
                        <a href="../01_ARTICLE/{slug}.txt" class="btn btn-secondary" download>Download TXT</a>
                    </div>
                </div>
'''
        
        html += '''
            </div>
        </div>

        <!-- Podcasts Section -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🎙 Podcasts</h2>
                <span class="section-count">'''
        
        html += f'''{len(topics)} Episodes</span>
            </div>
            <div class="content-grid">
'''
        
        # Add podcast cards
        for i, topic in enumerate(topics, 1):
            slug = topic['title'].lower().replace(' ', '-').replace("'", '')
            html += f'''
                <div class="content-card">
                    <span class="episode-badge">Episode {i}</span>
                    <span class="status-badge status-published">ON SPOTIFY</span>
                    <h3>{topic['title']}</h3>
                    <div class="content-meta">
                        <span>5-7 minutes</span>
                        <span>Premium Voices</span>
                        <span>British Neural</span>
                    </div>
                    <div class="action-buttons">
                        <a href="https://open.spotify.com/show/YOUR_SHOW_ID" class="btn btn-success" target="_blank">Listen on Spotify</a>
                        <a href="../02_PODCAST/{slug}.mp3" class="btn btn-secondary" download>Download MP3</a>
                    </div>
                </div>
'''
        
        html += f'''
            </div>
        </div>

        <!-- Performance Section -->
        <div class="performance-section">
            <h2 class="performance-title">📈 Today's Performance</h2>
            <div class="perf-grid">
                <div class="perf-item">
                    <div class="perf-label">Generation Time</div>
                    <div class="perf-value">{results.get('duration_minutes', 0)}m</div>
                </div>
                <div class="perf-item">
                    <div class="perf-label">Modules Run</div>
                    <div class="perf-value">{results.get('modules_run', 0)}</div>
                </div>
                <div class="perf-item">
                    <div class="perf-label">Total Files</div>
                    <div class="perf-value">{results.get('total_files', 0)}</div>
                </div>
                <div class="perf-item">
                    <div class="perf-label">ROI</div>
                    <div class="perf-value">£{results.get('roi', 0):,.0f}</div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p style="font-size: 18px; font-weight: 600; margin-bottom: 10px;">
                <span style="color: #667eea;">Say</span><span style="color: #FFD700;">Play</span> Content Dashboard
            </p>
            <p>Generated by Titan Master Orchestrator V2</p>
            <p style="margin-top: 10px; font-size: 14px; opacity: 0.7;">
                Last updated: {now.strftime("%Y-%m-%d %H:%M:%S UTC")}
            </p>
        </div>
    </div>

    <div class="refresh-btn" onclick="location.reload()" title="Refresh Dashboard">
        ↻
    </div>

    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => location.reload(), 300000);
        
        // Add smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>
'''
        
        return html
