# Knowledge Base Data Analysis

## 📊 Quick Overview

This analysis tool processes your eGain KB data from 2019-2025 to surface insights, pain points, and usage patterns.

### Key Findings

- **173,938** total failed searches
- **51,417** unique search terms that failed
- **1.2+ million** total article views
- Multiple pain point categories identified

---

## 🚀 How to Use

### 1. Run the Analysis

```bash
python3 kb_analyzer.py
```

This will:
- Scan all your KB data files (scorecards, article summaries, failed searches)
- Aggregate and analyze the data
- Generate two output files:
  - `kb_summary_report.txt` - Human-readable text report
  - `kb_insights_report.json` - Structured data for further analysis

### 2. View the Dashboard

```bash
python3 create_dashboard.py
open kb_dashboard.html
```

The dashboard provides an interactive view of:
- Top failed searches (pain points)
- Most/least viewed articles
- Common failure patterns
- Actionable recommendations

---

## 📈 What the Data Tells Us

### 🔴 Major Pain Points

Top failed searches indicate content gaps:

1. **"fsa"** (351 times) - FSA information is hard to find
2. **"hsa"** (274 times) - HSA content needs improvement
3. **"lifestyle"** (303 times) - Lifestyle spending account searches failing
4. **"uber"** (246 times) - Transportation benefits unclear
5. **"w9"** (200 times) - Tax form not easily accessible

**Patterns:**
- **Benefits** (1,425 failures) - Benefits information is a major pain point
- **Payroll** (1,184 failures) - Payroll-related content gaps
- **Forms** (978 failures) - Forms are hard to find
- **Technical** (913 failures) - Technical issues/errors

### ✅ What's Working Well

Top performing articles show what users actually need:

1. **Online account login assistance** (51,969 views) 
2. **Getting started with WEX benefits mobile app** (21,308 views)
3. **How to reset your username** (11,915 views)
4. **How to reset your password** (10,348 views)
5. **What documentation is needed for my claim?** (10,185 views)

**Key insight:** Users primarily need help with account access and basic how-to guides.

### ⚠️ Content to Review

**Low-performing articles** (1 view each):
- Many technical/internal articles
- Spanish language COBRA forms
- Partner-specific guides (PNC, TELUS Health, Mercer)

**Action:** Consider archiving, consolidating, or improving discoverability.

---

## 💡 Recommendations

### Priority 1: HIGH - Fill Content Gaps

**Action:** Create or improve articles for top failed searches
- FSA/HSA overview and guides
- Lifestyle spending account details
- Transportation benefits (Uber, commuter)
- W9 and tax forms
- Common benefit questions

### Priority 2: HIGH - Fix Search/Discoverability

**Action:** Improve search functionality
- Add synonyms (FSA = "flexible spending account", HSA = "health savings account")
- Add common misspellings
- Improve tagging and categorization
- Consider search query expansion

### Priority 3: HIGH - Promote Top Content

**Action:** Make successful content even more accessible
- Feature login/password reset prominently
- Improve mobile app onboarding
- Highlight claim documentation requirements
- Consider creating a "Getting Started" hub

### Priority 4: MEDIUM - Content Cleanup

**Action:** Review and improve low-performing content
- Archive outdated partner-specific content
- Consolidate similar articles
- Translate more content to Spanish (if needed)
- Update technical documentation

### Priority 5: MEDIUM - User Journey Optimization

**Action:** Analyze complete user paths
- Where do users get stuck?
- Which articles lead to more searches vs. resolution?
- What's the ideal content flow?

---

## 📁 Files Generated

| File | Description |
|------|-------------|
| `kb_analyzer.py` | Main analysis script |
| `create_dashboard.py` | Dashboard generation script |
| `kb_summary_report.txt` | Text report with all insights |
| `kb_insights_report.json` | Structured JSON data |
| `kb_dashboard.html` | Interactive visual dashboard |
| `requirements.txt` | Python dependencies |

---

## 🔄 Regular Updates

**Recommended:** Run this analysis monthly to:
- Track if failed searches are decreasing
- Monitor new pain points
- Measure content performance changes
- Validate improvements are working

---

## 📊 Data Sources

The analyzer processes:
- **Scorecards** - Monthly KPIs and metrics
- **Article Summaries** - View counts and usage stats
- **Failed Searches** - Searches that returned no results
- **Search Effectiveness** - Click-through and success rates
- **Portal Summaries** - Overall portal usage patterns

Data spans from **2019 to 2025** across multiple folders and file formats (xlsx, xls, xlsm).

---

## 🎯 Quick Wins

Based on the analysis, here are some quick actions you can take today:

1. **Add FSA/HSA articles** to address 625+ failed searches
2. **Create W9/tax form repository** - 200+ searches failing
3. **Improve "lifestyle" content** - 303 failed searches
4. **Add transportation benefits guide** - 246 failed searches
5. **Review forms discoverability** - 978 form-related failures

---

## 🤔 Questions?

The analysis is comprehensive, but if you need:
- More specific data points
- Different date ranges
- Additional metrics
- Custom reports

Simply modify `kb_analyzer.py` or let me know what you need!

---

**Generated:** November 6, 2025




