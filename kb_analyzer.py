#!/usr/bin/env python3
"""
Knowledge Base Data Analyzer
Analyzes eGain KB usage data to surface insights, pain points, and trends
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class KBAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.data = {
            'scorecards': [],
            'article_summaries': [],
            'failed_searches': [],
            'search_effectiveness': []
        }
        self.insights = {}
        
    def find_files(self, pattern, years=None):
        """Find all files matching a pattern"""
        if years is None:
            years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025']
        
        files = []
        for year in years:
            year_path = self.base_path / year
            if year_path.exists():
                files.extend(year_path.rglob(pattern))
        return sorted(files)
    
    def read_excel_safe(self, file_path, sheet_name=0, header=0, skip_rows=None):
        """Safely read Excel files with error handling"""
        try:
            # Try reading with different engines
            try:
                if skip_rows:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=skip_rows)
                else:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', header=header)
            except:
                if skip_rows:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='xlrd', skiprows=skip_rows)
                else:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='xlrd', header=header)
            return df
        except Exception as e:
            print(f"  ⚠️  Could not read {file_path.name}: {str(e)[:100]}")
            return None
    
    def analyze_scorecards(self):
        """Analyze monthly scorecard data"""
        print("\n📊 Analyzing Scorecards...")
        scorecard_files = self.find_files("*scorecard*.xlsx")
        
        metrics = []
        for file in scorecard_files:
            df = self.read_excel_safe(file)
            if df is not None and not df.empty:
                # Extract date from filename or path
                date_str = self.extract_date_from_path(file)
                df['month'] = date_str
                df['file'] = file.name
                metrics.append(df)
        
        if metrics:
            print(f"  ✓ Found {len(metrics)} scorecard files")
            self.data['scorecards'] = metrics
        return metrics
    
    def analyze_article_summaries(self):
        """Analyze which articles are most/least used"""
        print("\n📄 Analyzing Article Usage...")
        article_files = self.find_files("*Article*Summary*.xlsx")
        article_files.extend(self.find_files("*Article*Summary*.xlsm"))
        
        all_articles = []
        for file in article_files:
            # First try without skipping rows
            df = self.read_excel_safe(file)
            
            # If columns are unnamed, try skipping header rows
            if df is not None and not df.empty and len(df.columns) > 0:
                if 'Unnamed' in str(df.columns[0]):
                    df = self.read_excel_safe(file, skip_rows=range(0, 9))
            
            if df is not None and not df.empty:
                date_str = self.extract_date_from_path(file)
                df['month'] = date_str
                all_articles.append(df)
        
        if all_articles:
            print(f"  ✓ Found {len(all_articles)} article summary files")
            self.data['article_summaries'] = all_articles
        return all_articles
    
    def analyze_failed_searches(self):
        """Analyze failed searches to identify pain points"""
        print("\n🔍 Analyzing Failed Searches (Pain Points)...")
        failed_search_path = self.base_path / "Failed searches"
        
        failed_searches = []
        if failed_search_path.exists():
            for year_dir in failed_search_path.iterdir():
                if year_dir.is_dir():
                    for file in list(year_dir.glob("*.xlsx")) + list(year_dir.glob("*.xls")) + list(year_dir.glob("*.xlsm")):
                        # Skip first 9 rows (0-8) so row 9 becomes the header
                        df = self.read_excel_safe(file, skip_rows=range(0, 9))
                        if df is not None and not df.empty:
                            date_str = self.extract_date_from_path(file)
                            df['month'] = date_str
                            failed_searches.append(df)
        
        if failed_searches:
            print(f"  ✓ Found {len(failed_searches)} failed search files")
            self.data['failed_searches'] = failed_searches
        return failed_searches
    
    def analyze_search_effectiveness(self):
        """Analyze search effectiveness data"""
        print("\n🎯 Analyzing Search Effectiveness...")
        search_files = self.find_files("*Search*Effectiveness*.xlsx")
        
        search_data = []
        for file in search_files:
            df = self.read_excel_safe(file)
            if df is not None and not df.empty:
                date_str = self.extract_date_from_path(file)
                df['month'] = date_str
                search_data.append(df)
        
        if search_data:
            print(f"  ✓ Found {len(search_data)} search effectiveness files")
            self.data['search_effectiveness'] = search_data
        return search_data
    
    def extract_date_from_path(self, file_path):
        """Extract date/month from file path or filename"""
        path_str = str(file_path)
        
        # Try to extract from path components
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        
        for part in file_path.parts:
            part_lower = part.lower()
            for i, month in enumerate(months):
                if month in part_lower:
                    # Try to find year
                    for year in ['2019', '2020', '2021', '2022', '2023', '2024', '2025']:
                        if year in part_lower or year in path_str:
                            return f"{year}-{str(i+1).zfill(2)}"
        
        return "unknown"
    
    def generate_insights(self):
        """Generate key insights from all data"""
        print("\n\n" + "="*70)
        print("🎯 GENERATING INSIGHTS")
        print("="*70)
        
        insights = {
            'summary': {},
            'top_content': {},
            'pain_points': {},
            'trends': {},
            'recommendations': []
        }
        
        # Analyze failed searches for pain points
        if self.data['failed_searches']:
            insights['pain_points'] = self.analyze_pain_points()
        
        # Analyze article usage
        if self.data['article_summaries']:
            insights['top_content'] = self.analyze_top_content()
        
        # Analyze search effectiveness
        if self.data['search_effectiveness']:
            insights['search_insights'] = self.analyze_search_patterns()
        
        # Generate recommendations
        insights['recommendations'] = self.generate_recommendations()
        
        self.insights = insights
        return insights
    
    def analyze_pain_points(self):
        """Identify key pain points from failed searches"""
        print("\n🔴 PAIN POINTS - What's NOT Working:")
        print("-" * 70)
        
        pain_points = {
            'total_failed_searches': 0,
            'top_failed_queries': {},
            'top_user_queries': {},
            'top_internal_queries': {},
            'by_portal': {},
            'patterns': []
        }
        
        all_failed = []
        user_failed = []
        internal_failed = []
        portal_breakdown = defaultdict(int)
        
        for df in self.data['failed_searches']:
            # Try to find columns with search terms
            search_cols = [col for col in df.columns if any(term in str(col).lower() 
                          for term in ['search', 'query', 'phrase', 'term'])]
            
            # Find portal column
            portal_cols = [col for col in df.columns if 'portal' in str(col).lower()]
            portal_col = portal_cols[0] if portal_cols else None
            
            if search_cols:
                search_col = search_cols[0]
                count_col = None
                
                # Find count column  
                count_cols = [col for col in df.columns if any(term in str(col).lower() 
                             for term in ['failed', 'count', 'frequency', 'number', 'total'])]
                if count_cols:
                    count_col = count_cols[0]
                
                for idx, row in df.iterrows():
                    if pd.notna(row[search_col]):
                        search_term = str(row[search_col]).strip()
                        portal = str(row[portal_col]).strip() if portal_col and pd.notna(row[portal_col]) else 'Unknown'
                        
                        try:
                            count = int(float(row[count_col])) if count_col and pd.notna(row[count_col]) else 1
                        except (ValueError, TypeError):
                            count = 1
                        
                        if search_term and count > 0:
                            # Determine if it's a pure number (likely article ID)
                            is_numeric = search_term.replace('-', '').replace('_', '').isdigit()
                            is_internal = 'internal' in portal.lower() or 'dbi' in portal.lower()
                            
                            item = {
                                'term': search_term.lower(),
                                'count': count,
                                'month': row.get('month', 'unknown'),
                                'portal': portal,
                                'is_numeric': is_numeric
                            }
                            
                            all_failed.append(item)
                            portal_breakdown[portal] += count
                            
                            # Separate user vs internal searches
                            if is_internal or is_numeric:
                                internal_failed.append(item)
                            else:
                                user_failed.append(item)
        
        if all_failed:
            # Aggregate all failed searches
            term_counts = defaultdict(int)
            for item in all_failed:
                term_counts[item['term']] += item['count']
            
            # Aggregate USER failed searches (excluding internal/numeric)
            user_term_counts = defaultdict(int)
            for item in user_failed:
                user_term_counts[item['term']] += item['count']
            
            # Sort by frequency
            sorted_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
            sorted_user_terms = sorted(user_term_counts.items(), key=lambda x: x[1], reverse=True)
            
            pain_points['total_failed_searches'] = sum(term_counts.values())
            pain_points['top_failed_queries'] = dict(sorted_terms[:100])
            pain_points['top_user_queries'] = dict(sorted_user_terms[:100])  # Real user searches!
            pain_points['unique_failed_queries'] = len(term_counts)
            pain_points['unique_user_queries'] = len(user_term_counts)
            pain_points['by_portal'] = dict(portal_breakdown)
            
            print(f"\n  Total Failed Searches: {pain_points['total_failed_searches']:,}")
            print(f"  Unique Failed Search Terms: {pain_points['unique_failed_queries']:,}")
            
            # Show portal breakdown
            print(f"\n  📊 Breakdown by Portal:")
            for portal, count in sorted(portal_breakdown.items(), key=lambda x: x[1], reverse=True):
                print(f"    {portal:<30} {count:>8,} failures")
            
            print(f"\n  🔴 Top 30 REAL USER Pain Points (excluding internal/ID searches):")
            for i, (term, count) in enumerate(sorted_user_terms[:30], 1):
                print(f"    {i:2}. {term[:60]:<60} ({count:,} times)")
            
            print(f"\n  🔧 Top 20 Internal/System Searches (for reference):")
            internal_term_counts = defaultdict(int)
            for item in internal_failed:
                internal_term_counts[item['term']] += item['count']
            sorted_internal = sorted(internal_term_counts.items(), key=lambda x: x[1], reverse=True)
            for i, (term, count) in enumerate(sorted_internal[:20], 1):
                print(f"    {i:2}. {term[:60]:<60} ({count:,} times)")
            
            # Identify patterns from user searches
            patterns = self.identify_search_patterns(sorted_user_terms)
            pain_points['patterns'] = patterns
            pain_points['user_patterns'] = patterns
            
            if patterns:
                print(f"\n  🔍 Identified Patterns in Failed Searches:")
                for pattern in patterns[:10]:
                    print(f"    • {pattern}")
        
        return pain_points
    
    def identify_search_patterns(self, sorted_terms):
        """Identify common patterns in search terms"""
        patterns = []
        
        # Common topics
        topics = {
            'password': ['password', 'pw', 'login', 'forgot password'],
            'benefits': ['benefit', 'insurance', 'health', 'dental', 'vision'],
            'payroll': ['payroll', 'pay', 'salary', 'wage', 'paycheck'],
            'time_off': ['pto', 'vacation', 'time off', 'leave', 'absence'],
            'forms': ['form', 'template', 'document'],
            'technical': ['error', 'issue', 'not working', 'how to'],
        }
        
        topic_counts = defaultdict(int)
        for term, count in sorted_terms:
            for topic, keywords in topics.items():
                if any(keyword in term.lower() for keyword in keywords):
                    topic_counts[topic] += count
        
        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                patterns.append(f"{topic.replace('_', ' ').title()}: {count:,} failed searches")
        
        return patterns
    
    def analyze_top_content(self):
        """Identify most and least used content"""
        print("\n✅ TOP PERFORMING CONTENT:")
        print("-" * 70)
        
        top_content = {
            'most_viewed': {},
            'least_viewed': {},
            'total_views': 0
        }
        
        all_articles = []
        for df in self.data['article_summaries']:
            # Look for "Article Name" column specifically (most reliable)
            if 'Article Name' in df.columns and 'Article Views' in df.columns:
                title_col = 'Article Name'
                view_col = 'Article Views'
            else:
                # Fall back to searching for similar column names
                title_cols = [col for col in df.columns if any(term in str(col).lower() 
                             for term in ['article name', 'article', 'title', 'name', 'subject'])]
                view_cols = [col for col in df.columns if any(term in str(col).lower() 
                            for term in ['article view', 'view', 'count', 'hit'])]
                
                if not (title_cols and view_cols):
                    continue
                    
                title_col = title_cols[0]
                view_col = view_cols[0]
            
            for idx, row in df.iterrows():
                if pd.notna(row[title_col]) and pd.notna(row[view_col]):
                    try:
                        views = int(float(row[view_col]))
                        title = str(row[title_col]).strip()
                        
                        # Filter out article IDs (pure numbers)
                        is_numeric_id = title.replace('-', '').replace('_', '').isdigit()
                        
                        if title and views > 0 and not is_numeric_id and len(title) > 3:
                            all_articles.append({
                                'title': title,
                                'views': views,
                                'month': row.get('month', 'unknown')
                            })
                    except (ValueError, TypeError):
                        pass
        
        if all_articles:
            # Aggregate by title
            article_views = defaultdict(int)
            for item in all_articles:
                article_views[item['title']] += item['views']
            
            sorted_articles = sorted(article_views.items(), key=lambda x: x[1], reverse=True)
            
            top_content['most_viewed'] = dict(sorted_articles[:30])
            top_content['least_viewed'] = dict(sorted_articles[-20:])
            top_content['total_views'] = sum(article_views.values())
            
            print(f"\n  Total Article Views: {top_content['total_views']:,}")
            print(f"\n  Top 20 Most Viewed Articles:")
            for i, (title, views) in enumerate(sorted_articles[:20], 1):
                print(f"    {i:2}. {title[:60]:<60} ({views:,} views)")
            
            print(f"\n  Bottom 10 Least Viewed Articles (may need review/removal):")
            for i, (title, views) in enumerate(sorted_articles[-10:], 1):
                print(f"    {i:2}. {title[:60]:<60} ({views:,} views)")
        
        return top_content
    
    def analyze_search_patterns(self):
        """Analyze successful search patterns"""
        print("\n🎯 SEARCH EFFECTIVENESS:")
        print("-" * 70)
        
        search_insights = {
            'successful_queries': {},
            'click_through_rates': []
        }
        
        for df in self.data['search_effectiveness']:
            print(f"\n  Columns found: {list(df.columns)[:5]}...")
            # This will vary by file structure, but generally look for:
            # - Search phrases
            # - Click-through rates
            # - Success rates
            
        return search_insights
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("\n\n💡 RECOMMENDATIONS:")
        print("-" * 70)
        
        recommendations = []
        
        # Based on failed searches
        if self.data['failed_searches']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Content Gaps',
                'recommendation': 'Create articles for top failed search queries',
                'action': 'Review top 20 failed searches and create missing content'
            })
        
        # Based on article usage
        if self.data['article_summaries']:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Content Cleanup',
                'recommendation': 'Archive or improve low-performing articles',
                'action': 'Review articles with <10 views and decide: update, merge, or remove'
            })
            
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Content Promotion',
                'recommendation': 'Optimize and feature top-performing content',
                'action': 'Ensure top 20 articles are easy to find and well-maintained'
            })
        
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Search Optimization',
            'recommendation': 'Improve search synonyms and related terms',
            'action': 'Add synonyms for common failed searches to existing articles'
        })
        
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'User Experience',
            'recommendation': 'Analyze user journey for pain points',
            'action': 'Track where users are getting stuck and simplify those flows'
        })
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n  {i}. [{rec['priority']}] {rec['category']}")
            print(f"     → {rec['recommendation']}")
            print(f"     Action: {rec['action']}")
        
        return recommendations
    
    def export_insights(self, output_file='kb_insights_report.json'):
        """Export insights to JSON file"""
        print(f"\n\n💾 Exporting insights to {output_file}...")
        
        # Convert to JSON-serializable format
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'insights': {}
        }
        
        # Export pain points
        if 'pain_points' in self.insights:
            export_data['insights']['pain_points'] = self.insights['pain_points']
        
        # Export top content
        if 'top_content' in self.insights:
            export_data['insights']['top_content'] = self.insights['top_content']
        
        # Export recommendations
        if 'recommendations' in self.insights:
            export_data['insights']['recommendations'] = self.insights['recommendations']
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"  ✓ Insights exported successfully!")
    
    def create_summary_report(self, output_file='kb_summary_report.txt'):
        """Create a human-readable summary report"""
        print(f"\n📝 Creating summary report: {output_file}...")
        
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("KNOWLEDGE BASE USAGE ANALYSIS - EXECUTIVE SUMMARY\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Pain Points
            if 'pain_points' in self.insights:
                pp = self.insights['pain_points']
                f.write("🔴 PAIN POINTS - What Users Can't Find:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Failed Searches: {pp.get('total_failed_searches', 0):,}\n")
                f.write(f"Unique User Search Terms: {pp.get('unique_user_queries', 0):,}\n\n")
                
                # Show portal breakdown
                if pp.get('by_portal'):
                    f.write("Breakdown by Portal:\n")
                    for portal, count in sorted(pp.get('by_portal', {}).items(), key=lambda x: x[1], reverse=True):
                        f.write(f"  {portal:<30} {count:>8,} failures\n")
                    f.write("\n")
                
                f.write("Top 50 REAL USER Failed Searches (excluding internal/IDs):\n")
                user_queries = pp.get('top_user_queries', pp.get('top_failed_queries', {}))
                for i, (term, count) in enumerate(list(user_queries.items())[:50], 1):
                    f.write(f"  {i:2}. {term:<65} {count:>6,} times\n")
                f.write("\n")
                
                if pp.get('patterns'):
                    f.write("Common Failure Patterns:\n")
                    for pattern in pp['patterns']:
                        f.write(f"  • {pattern}\n")
                f.write("\n\n")
            
            # Top Content
            if 'top_content' in self.insights:
                tc = self.insights['top_content']
                f.write("✅ TOP PERFORMING CONTENT:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total Article Views: {tc.get('total_views', 0):,}\n\n")
                
                f.write("Most Viewed Articles (Top 30):\n")
                for i, (title, views) in enumerate(list(tc.get('most_viewed', {}).items())[:30], 1):
                    f.write(f"  {i:2}. {title:<65} {views:>6,} views\n")
                f.write("\n")
                
                f.write("Least Viewed Articles (Bottom 20 - Consider Review):\n")
                for i, (title, views) in enumerate(list(tc.get('least_viewed', {}).items()), 1):
                    f.write(f"  {i:2}. {title:<65} {views:>6,} views\n")
                f.write("\n\n")
            
            # Recommendations
            if 'recommendations' in self.insights:
                f.write("💡 RECOMMENDATIONS:\n")
                f.write("-" * 80 + "\n")
                for i, rec in enumerate(self.insights['recommendations'], 1):
                    f.write(f"\n{i}. [{rec['priority']}] {rec['category']}\n")
                    f.write(f"   Recommendation: {rec['recommendation']}\n")
                    f.write(f"   Action: {rec['action']}\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"  ✓ Summary report created!")

def main():
    print("=" * 70)
    print("📚 KNOWLEDGE BASE DATA ANALYZER")
    print("=" * 70)
    print("\nAnalyzing your eGain KB data to find insights and pain points...\n")
    
    # Initialize analyzer
    base_path = Path(__file__).parent / "eGain KB Data"
    analyzer = KBAnalyzer(base_path)
    
    # Run analysis
    analyzer.analyze_scorecards()
    analyzer.analyze_article_summaries()
    analyzer.analyze_failed_searches()
    analyzer.analyze_search_effectiveness()
    
    # Generate insights
    analyzer.generate_insights()
    
    # Export results
    analyzer.export_insights()
    analyzer.create_summary_report()
    
    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nOutput files created:")
    print("  • kb_insights_report.json - Detailed JSON data")
    print("  • kb_summary_report.txt - Human-readable summary")
    print("\n")

if __name__ == "__main__":
    main()

