#!/usr/bin/env python3
"""
Track improvements over time by comparing monthly metrics
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import json

def track_monthly_improvements(base_path, output_file='improvement_tracker.csv'):
    """Track key metrics month over month"""
    
    base = Path(base_path) / "eGain KB Data" / "Failed searches"
    
    monthly_data = []
    
    # Process failed searches by month
    for year_dir in sorted(base.iterdir()):
        if year_dir.is_dir():
            for file in sorted(year_dir.glob("*.xlsx")):
                try:
                    # Extract month/year from filename
                    filename = file.stem
                    
                    # Read the file
                    df = pd.read_excel(file, skiprows=range(0, 9), engine='openpyxl')
                    
                    if 'Search Phrase' in df.columns and 'Failed Searches' in df.columns:
                        total_failures = df['Failed Searches'].sum()
                        unique_terms = df['Search Phrase'].nunique()
                        
                        monthly_data.append({
                            'file': filename,
                            'total_failed_searches': int(total_failures) if pd.notna(total_failures) else 0,
                            'unique_search_terms': int(unique_terms),
                            'avg_failures_per_term': round(total_failures / unique_terms, 2) if unique_terms > 0 else 0
                        })
                        print(f"✓ {filename}: {int(total_failures):,} failures")
                
                except Exception as e:
                    print(f"  ⚠️  Could not process {file.name}: {str(e)[:50]}")
    
    # Create DataFrame and save
    if monthly_data:
        df = pd.DataFrame(monthly_data)
        df.to_csv(output_file, index=False)
        print(f"\n✅ Improvement tracker saved to: {output_file}")
        print(f"\nSummary:")
        print(f"  Total months tracked: {len(monthly_data)}")
        print(f"  Average monthly failures: {df['total_failed_searches'].mean():,.0f}")
        print(f"  Trend: {'📈 Increasing' if df['total_failed_searches'].iloc[-1] > df['total_failed_searches'].iloc[0] else '📉 Decreasing'}")
        
        # Show recent trend (last 6 months)
        if len(df) >= 6:
            recent = df.tail(6)
            print(f"\n  Recent 6-Month Trend:")
            for _, row in recent.iterrows():
                print(f"    {row['file'][:20]:<20}: {row['total_failed_searches']:>6,} failures")
        
        return df
    
    return None

def generate_improvement_report():
    """Generate a report showing month-over-month improvements"""
    
    print("=" * 70)
    print("📊 KNOWLEDGE BASE IMPROVEMENT TRACKER")
    print("=" * 70)
    print("\nAnalyzing monthly trends...\n")
    
    base_path = Path(__file__).parent
    df = track_monthly_improvements(base_path)
    
    if df is not None and len(df) > 1:
        print("\n" + "=" * 70)
        print("💡 INSIGHTS")
        print("=" * 70)
        
        # Calculate trends
        first_month = df.iloc[0]
        last_month = df.iloc[-1]
        
        change = last_month['total_failed_searches'] - first_month['total_failed_searches']
        pct_change = (change / first_month['total_failed_searches'] * 100) if first_month['total_failed_searches'] > 0 else 0
        
        print(f"\n📈 Overall Trend (First vs Latest Month):")
        print(f"  First month: {first_month['total_failed_searches']:,} failures")
        print(f"  Latest month: {last_month['total_failed_searches']:,} failures")
        print(f"  Change: {change:+,} ({pct_change:+.1f}%)")
        
        # Best and worst months
        best_month = df.loc[df['total_failed_searches'].idxmin()]
        worst_month = df.loc[df['total_failed_searches'].idxmax()]
        
        print(f"\n🏆 Best Month: {best_month['file']}")
        print(f"   {best_month['total_failed_searches']:,} failures")
        
        print(f"\n⚠️  Worst Month: {worst_month['file']}")
        print(f"   {worst_month['total_failed_searches']:,} failures")
        
        # Action items
        print("\n" + "=" * 70)
        print("📋 ACTION ITEMS")
        print("=" * 70)
        
        if pct_change > 10:
            print("\n🔴 Failed searches are increasing!")
            print("   → Focus on addressing top failed search queries")
            print("   → Review search algorithm and synonyms")
            print("   → Create missing content immediately")
        elif pct_change < -10:
            print("\n✅ Great job! Failed searches are decreasing!")
            print("   → Continue current improvement efforts")
            print("   → Document what's working")
            print("   → Share best practices")
        else:
            print("\n🔶 Failed searches are relatively stable")
            print("   → Time to focus on new areas of improvement")
            print("   → Review content quality, not just quantity")
            print("   → Optimize existing high-performing content")

if __name__ == "__main__":
    generate_improvement_report()




