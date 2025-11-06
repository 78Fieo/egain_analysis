#!/usr/bin/env python3
"""
Create an interactive HTML dashboard from KB insights
"""

import json
from datetime import datetime

def create_dashboard(insights_file='kb_insights_report.json', output_file='kb_dashboard.html'):
    """Create an interactive HTML dashboard"""
    
    # Load insights
    with open(insights_file, 'r') as f:
        data = json.load(f)
    
    insights = data.get('insights', {})
    pp = insights.get('pain_points', {})
    tc = insights.get('top_content', {})
    recs = insights.get('recommendations', [])
    
    # Create HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Base Insights Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f6f7fb;
            color: #0f172a;
            padding: 24px;
            line-height: 1.55;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .two-column-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        h1 {{
            color: #0f172a;
            font-size: 26px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .subtitle {{
            color: #64748b;
            font-size: 13px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 14px;
        }}
        
        .stat-card {{
            background: #fff;
            padding: 18px 20px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        
        .stat-number {{
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
        }}
        
        .stat-label {{
            color: #64748b;
            font-size: 12px;
            letter-spacing: .3px;
            text-transform: none;
        }}

        .stat-number.danger {{ color: #dc2626; }}
        .stat-number.accent {{ color: #334155; }}
        
        .section {{
            background: #fff;
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }}

        .section h2 {{
            color: #0f172a;
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .view-all {{
            color: #64748b;
            font-size: 12px;
            text-decoration: none;
        }}
        .view-all:hover {{ text-decoration: underline; }}
        
        .icon {{
            font-size: 1.1em;
        }}
        
        .list-item {{
            padding: 12px 12px;
            margin-bottom: 8px;
            background: #f8fafc;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #eef2f7;
        }}
        
        .list-item.pain-point {{
            border-left: 4px solid #ef4444;
        }}
        
        .list-item.top-content {{
            border-left: 4px solid #22c55e;
        }}
        
        .list-item.low-content {{
            border-left: 4px solid #f59e0b;
        }}
        
        .item-rank {{
            font-weight: 700;
            color: #334155;
            margin-right: 10px;
            min-width: 30px;
        }}
        
        .item-name {{
            flex: 1;
        }}
        
        .item-count {{
            font-weight: 700;
            color: #475569;
            background: #fff;
            padding: 6px 12px;
            border-radius: 999px;
            border: 1px solid #e5e7eb;
        }}
        
        .recommendation {{
            padding: 16px 16px 14px 16px;
            margin-bottom: 12px;
            border-radius: 10px;
            border-left: 5px solid #3b82f6;
            background: #f8fafc;
            border: 1px solid #eef2f7;
        }}
        
        .recommendation.high {{
            border-left-color: #ef4444;
        }}
        
        .recommendation.medium {{
            border-left-color: #f59e0b;
        }}
        
        .recommendation.low {{
            border-left-color: #22c55e;
        }}
        
        .rec-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        
        .priority-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            color: white;
        }}
        
        .priority-badge.high {{
            background: #ef4444;
        }}
        
        .priority-badge.medium {{
            background: #f59e0b;
        }}
        
        .priority-badge.low {{
            background: #22c55e;
        }}
        
        .rec-title {{
            font-weight: 700;
            font-size: 15px;
        }}
        
        .rec-action {{
            color: #64748b;
            font-size: 13px;
            padding-left: 20px;
        }}
        
        .pattern-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-top: 10px;
        }}
        
        .pattern-card {{
            padding: 12px;
            background: #fff;
            color: #0f172a;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e5e7eb;
        }}
        
        .pattern-name {{
            font-size: 12px;
            color: #64748b;
            margin-bottom: 4px;
        }}
        
        .pattern-count {{
            font-size: 20px;
            font-weight: 800;
            color: #2563eb;
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: none;
            border-radius: 25px;
            background: #e5e7eb;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 12px;
        }}
        
        .filter-btn.active {{
            background: #2563eb;
            color: white;
        }}
        
        .filter-btn:hover {{
            background: #2563eb;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 20px;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .two-column-grid {{
                grid-template-columns: 1fr;
            }}
            
            .list-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Knowledge Base Insights Dashboard</h1>
        <div class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        
        <!-- Key Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number danger">{pp.get('total_failed_searches', 0):,}</div>
                <div class="stat-label">Failed Searches</div>
            </div>
            <div class="stat-card">
                <div class="stat-number accent">{pp.get('unique_user_queries', pp.get('unique_failed_queries', 0)):,}</div>
                <div class="stat-label">Unique User Search Terms</div>
            </div>
            <div class="stat-card">
                <div class="stat-number accent">{tc.get('total_views', 0):,}</div>
                <div class="stat-label">Total Article Views</div>
            </div>
            <div class="stat-card">
                <div class="stat-number accent">{len(recs)}</div>
                <div class="stat-label">Action Items</div>
            </div>
        </div>
        
        <!-- Two Column Layout: Pain Points + Top Performing Content -->
        <div class="two-column-grid">
            <!-- Pain Points -->
            <div class="section">
            <div class="section-header">
                <h2><span class="icon">🔴</span> Top Pain Points - What Users Can't Find</h2>
                <a class="view-all" href="pain_points_detail.html">View all</a>
            </div>
                <p style="color: #666; margin-bottom: 15px;">
                    These are real user searches that failed (excluding internal support team searches and article IDs)
                </p>
                <div id="pain-points-list">
"""
    
    # Add top 5 USER failed searches
    top_queries = list(pp.get('top_user_queries', {}).items())[:5]
    if not top_queries:  # Fallback to all queries if user queries not available
        top_queries = list(pp.get('top_failed_queries', {}).items())[:5]
    
    for i, (term, count) in enumerate(top_queries, 1):
        html += f"""
                    <div class="list-item pain-point">
                        <span class="item-rank">{i}.</span>
                        <span class="item-name">{term}</span>
                        <span class="item-count">{count:,} times</span>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- Top Performing Content -->
            <div class="section">
            <div class="section-header">
                <h2><span class="icon">✅</span> Top Performing Content</h2>
                <a class="view-all" href="top_content_detail.html">View all</a>
            </div>
                <div id="top-content-list">
"""
    
    # Add top 5 articles
    top_articles = list(tc.get('most_viewed', {}).items())[:5]
    for i, (title, views) in enumerate(top_articles, 1):
        html += f"""
                    <div class="list-item top-content">
                        <span class="item-rank">{i}.</span>
                        <span class="item-name">{title}</span>
                        <span class="item-count">{views:,} views</span>
                    </div>
"""
    
    html += """
                </div>
            </div>
        </div>
        
        <!-- Two Column Layout: Patterns + Low Performing Content -->
        <div class="two-column-grid">
            <!-- Common Failure Patterns -->
            <div class="section">
                <div class="section-header">
                    <h2><span class="icon">🔍</span> Common Failure Patterns</h2>
                </div>
                <div class="pattern-grid">
"""
    
    # Add patterns
    for pattern in pp.get('patterns', []):
        # Parse pattern like "Benefits: 1,425 failed searches"
        parts = pattern.split(':')
        if len(parts) == 2:
            name = parts[0].strip()
            count = parts[1].strip().split()[0].replace(',', '')
            html += f"""
                    <div class="pattern-card">
                        <div class="pattern-name">{name}</div>
                        <div class="pattern-count">{count}</div>
                    </div>
"""
    
    html += """
                </div>
            </div>
            
            <!-- Low Performing Content -->
            <div class="section">
            <div class="section-header">
                <h2><span class="icon">⚠️</span> Low Performing Content - Consider Review</h2>
                <a class="view-all" href="low_content_detail.html">View all</a>
            </div>
                <div id="low-content-list">
"""
    
    # Add low performing articles (top 3)
    low_articles = list(tc.get('least_viewed', {}).items())[:3]
    for i, (title, views) in enumerate(low_articles, 1):
        html += f"""
                    <div class="list-item low-content">
                        <span class="item-rank">{i}.</span>
                        <span class="item-name">{title}</span>
                        <span class="item-count">{views:,} views</span>
                    </div>
"""
    
    html += """
                </div>
            </div>
        </div>
        
        <!-- Recommendations -->
        <div class="section">
            <div class="section-header">
                <h2><span class="icon">💡</span> Recommendations</h2>
            </div>
"""
    
    # Add recommendations
    for rec in recs:
        priority = rec.get('priority', 'MEDIUM').lower()
        html += f"""
            <div class="recommendation {priority}">
                <div class="rec-header">
                    <span class="priority-badge {priority}">{rec.get('priority', 'MEDIUM')}</span>
                    <span class="rec-title">{rec.get('category', 'Unknown')}</span>
                </div>
                <div>{rec.get('recommendation', '')}</div>
                <div class="rec-action">→ {rec.get('action', '')}</div>
            </div>
"""
    
    html += """
        </div>
    </div>
    
    <script>
        // Add interactive features
        console.log('KB Dashboard loaded successfully!');
        
        // You can add filtering, sorting, and other interactive features here
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard created: {output_file}")
    print(f"   Open this file in your web browser to view the interactive dashboard!")

if __name__ == "__main__":
    create_dashboard()

