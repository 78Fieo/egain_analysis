# KB Insights Dashboard

A modern, interactive dashboard for analyzing eGain Knowledge Base data, identifying pain points, and optimizing content performance.

## 🎯 Features

- **📊 Executive Dashboard** - High-level KPIs and key metrics at a glance
- **🔴 Pain Points Analysis** - Identify top failed searches and user pain points
- **✅ Top Content Tracking** - See which articles drive the most engagement
- **⚠️ Low-Performance Detection** - Find content that needs improvement
- **🔍 Common Failure Patterns** - Categorize issues by type (Benefits, Forms, Technical, Payroll, etc.)
- **💡 Smart Recommendations** - Get actionable insights prioritized by impact
- **📈 Drill-Down Details** - Interactive tables with search, filter, sort, and export capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Your eGain KB data files (scorecards, article summaries, failed searches)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kb-insights-dashboard.git
cd kb-insights-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Analyze Your Data
```bash
python3 kb_analyzer.py
```

This scans your eGain KB data and generates:
- `kb_insights_report.json` - Structured insights data
- `kb_summary_report.txt` - Human-readable analysis

#### 2. Generate Dashboard
```bash
python3 create_dashboard.py
```

This creates:
- `kb_dashboard.html` - Main dashboard
- `pain_points_detail.html` - Detailed pain points table
- `top_content_detail.html` - Detailed top content table
- `low_content_detail.html` - Detailed low content table

#### 3. View Dashboard
Open the dashboard in your browser:
```bash
open kb_dashboard.html
```

## 📁 File Structure

```
kb-insights-dashboard/
├── kb_analyzer.py              # Main analysis engine
├── create_dashboard.py         # Dashboard generator
├── kb_dashboard.html           # Main dashboard (generated)
├── pain_points_detail.html     # Pain points detail page (generated)
├── top_content_detail.html     # Top content detail page (generated)
├── low_content_detail.html     # Low content detail page (generated)
├── kb_insights_report.json     # Analysis output (generated)
├── kb_summary_report.txt       # Text report (generated)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 📊 Data Sources

The analyzer processes eGain KB data files including:
- **Scorecards** - Monthly KPIs and performance metrics
- **Article Summaries** - View counts and usage statistics
- **Failed Searches** - Searches that returned no results
- **Search Effectiveness** - Click-through and success rates
- **Portal Summaries** - Overall portal usage patterns

Supports file formats: `.xlsx`, `.xls`, `.xlsm`, `.csv`

## 🎨 Dashboard Components

### Main Dashboard (`kb_dashboard.html`)
- **KPI Cards** - Failed Searches, Unique Search Terms, Total Views, Action Items
- **Two-Column Layout**:
  - Top 5 Pain Points (what users can't find)
  - Top 5 Performing Content (what works well)
- **Common Failure Patterns** - Visual breakdown by category
- **Low Performing Content** - Articles needing review
- **Recommendations** - Prioritized action items (High/Medium/Low)

### Detail Pages
Each section has a full-featured detail page with:
- **Breadcrumb navigation** for context
- **Search & filter controls** to find specific items
- **Sortable columns** for customized views
- **Pagination** for large datasets
- **CSV export** for reporting and analysis

## 🔍 Key Insights

The dashboard helps you:
1. **Find Content Gaps** - See which search queries are failing
2. **Optimize Discoverability** - Understand why users can't find content
3. **Prioritize Updates** - Focus on high-impact content first
4. **Track Progress** - Monitor improvements over time
5. **Make Data-Driven Decisions** - Real user behavior data

## 💡 Common Use Cases

### Identify Missing Content
- Top pain points show you what content users need but can't find
- Create articles for the top 10-20 failed searches

### Improve Search & Navigation
- Analyze failure patterns by category
- Add synonyms and tags to existing articles
- Improve search query expansion

### Content Maintenance
- Review low-performing articles
- Decide: archive, update, merge, or delete
- Consolidate similar articles

### Performance Tracking
- Run monthly to see trends
- Validate that improvements are working
- Set targets and track progress

## 📈 Recommended Workflow

1. **Monthly Analysis**
   ```bash
   python3 kb_analyzer.py
   python3 create_dashboard.py
   ```

2. **Review & Plan**
   - Check dashboard for new pain points
   - Review high-priority recommendations
   - Prioritize content updates

3. **Execute**
   - Create missing articles
   - Update low-performing content
   - Improve search synonyms and tags

4. **Validate**
   - Run analysis again next month
   - Confirm failed searches decreased
   - Track content view growth

## 🛠️ Customization

### Modify Analysis Parameters
Edit `kb_analyzer.py` to:
- Change date ranges
- Adjust failure thresholds
- Filter specific KB sections
- Add custom metrics

### Customize Dashboard Styling
Edit `create_dashboard.py` CSS styles to:
- Change colors and branding
- Adjust layout and spacing
- Add custom fonts
- Include logos

### Extend Data Processing
Add new data sources:
- Customer feedback
- Support ticket data
- User session logs
- A/B test results

## 📝 Output Files

### JSON Report (`kb_insights_report.json`)
Structured data including:
- Pain points with frequency and categories
- Top/bottom performing articles
- Common failure patterns
- Recommendations with priority levels

### Text Report (`kb_summary_report.txt`)
Human-readable analysis with:
- Executive summary
- Key findings
- Actionable recommendations
- Quick wins

## 🐛 Troubleshooting

### No data showing in dashboard
- Verify data files are in the expected directories
- Check file formats are supported (.xlsx, .xls, .xlsm, .csv)
- Run `kb_analyzer.py` and check for errors

### Dashboard looks broken
- Clear browser cache
- Use a modern browser (Chrome, Safari, Firefox, Edge)
- Check browser console for JavaScript errors

### Export not working
- Check browser console for errors
- Verify your browser allows downloads
- Try a different browser

## 📄 License

[Add your license here]

## 👥 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing discussions
- Review the troubleshooting section

## 🎯 Roadmap

- [ ] Real-time data sync
- [ ] User feedback integration
- [ ] Advanced analytics and ML insights
- [ ] Email report scheduling
- [ ] Slack/Teams integration
- [ ] Multi-language support
- [ ] Custom metrics builder

## 📊 Sample Data

Example data is included in this repository. To use your own eGain data:
1. Export your KB data files
2. Place them in the appropriate directories
3. Run the analyzer
4. Generate the dashboard

## ⚡ Performance Notes

- Analysis typically takes 30-60 seconds for 5+ years of data
- Dashboard is optimized for modern browsers
- Export functionality works best in Chrome/Safari/Firefox
- Mobile-responsive design for tablet viewing

## 🔐 Privacy & Security

- No data is sent to external services
- All analysis runs locally
- Reports can be safely shared internally
- Consider password-protecting sensitive findings

---

**Made with ❤️ for better knowledge management**

Last updated: November 2025

