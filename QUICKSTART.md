# InfoCapture Quick Start Guide

## Installation

```bash
git clone https://github.com/parinaywadhwa0/InfoCapture.git
cd InfoCapture
pip install -r requirements.txt
```

**Requirements:**
- Python 3.7+
- Chrome browser installed
- Internet connection

## Basic Usage

### 1. Prepare Your Data

Edit `companies.csv`:
```csv
id,company_name
1,Your Company Name
2,Another Company
```

### 2. Run the Crawler

```bash
python src/crawler.py
```

### 3. Review Information

- Captured info appears in the sidebar (right side)
- Click any field to validate it
- Press **Enter** to continue to next company

### 4. Access Results

Results are saved to `captured_data.csv`:
```csv
id,company_name,website,phone,email,about
1,Company Name,https://...,+1-555-...,info@...,Description...
```

## Testing

```bash
# Run unit tests
python src/test_crawler.py

# Run feature demo
python src/demo.py

# Open sidebar preview
open sidebar_preview.html
```

## Troubleshooting

**Issue: ChromeDriver not found**
- Solution: WebDriver Manager will auto-download on first run

**Issue: Google cookie consent appears**
- Solution: Script automatically handles it, or click manually

**Issue: Information not captured**
- Solution: Website structure varies; some sites may not have phone/email visible

**Issue: Slow performance**
- Solution: Adjust sleep times in crawler.py if needed

## Customization

### Add More Fields

Edit `src/crawler.py` and add extraction method:
```python
def extract_address(self, html_content):
    # Your extraction logic
    return address
```

### Modify Search Query

Change in `search_company()` method:
```python
search_query = f"{company_name} contact information"
```

### Customize Sidebar

Edit `extension/sidebar.html` and `extension/sidebar.js`

## Advanced Features

### Batch Processing
The crawler automatically processes all companies in CSV sequentially.

### Data Validation
Click fields in sidebar to mark them as validated. Console logs track selections.

### Error Handling
Script continues to next company if errors occur. Check console output for details.

## Tips

1. **Accurate Search**: Use official company names for best results
2. **Manual Review**: Always verify captured information
3. **Rate Limiting**: Add delays between companies to avoid rate limits
4. **Data Privacy**: Respect website terms of service and robots.txt

## Support

- See `README.md` for full documentation
- See `IMPLEMENTATION_SUMMARY.md` for technical details
- Check issues on GitHub for common problems

## License

MIT License - Free to use and modify
