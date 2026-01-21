"""
Demo script for InfoCapture Crawler
This demonstrates the crawler functionality without requiring a full browser setup
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawler import InfoCaptureCrawler


def demo_extraction():
    """Demonstrate information extraction capabilities"""
    
    print("=" * 70)
    print("InfoCapture Crawler - Feature Demo")
    print("=" * 70)
    
    crawler = InfoCaptureCrawler()
    
    # Demo 1: CSV Reading
    print("\n📋 Demo 1: Reading Companies from CSV")
    print("-" * 70)
    companies = crawler.read_companies_csv()
    print(f"Loaded {len(companies)} companies:")
    for i, company in enumerate(companies, 1):
        print(f"  {i}. ID: {company['id']:2d} - {company['company_name']}")
    
    # Demo 2: Phone Extraction
    print("\n📞 Demo 2: Phone Number Extraction")
    print("-" * 70)
    sample_html_phone = """
    <html><body>
        <div class="contact">
            <p>Call us at: +1-800-555-1234</p>
            <p>Support: (555) 987-6543</p>
        </div>
    </body></html>
    """
    phone = crawler.extract_phone(sample_html_phone)
    print(f"Sample HTML contains phone numbers")
    print(f"Extracted: {phone}")
    
    # Demo 3: Email Extraction
    print("\n📧 Demo 3: Email Address Extraction")
    print("-" * 70)
    sample_html_email = """
    <html><body>
        <a href="mailto:contact@example.com">Email Us</a>
        <p>Support email: support@company.com</p>
    </body></html>
    """
    email = crawler.extract_email(sample_html_email)
    print(f"Sample HTML contains email addresses")
    print(f"Extracted: {email}")
    
    # Demo 4: About Section Extraction
    print("\nℹ️  Demo 4: Company Description Extraction")
    print("-" * 70)
    sample_html_about = """
    <html>
    <head>
        <meta name="description" content="Leading provider of innovative technology solutions for businesses worldwide.">
    </head>
    <body>
        <h2>About Our Company</h2>
        <p>We are a technology company dedicated to creating innovative solutions 
        that help businesses transform digitally. Our products serve millions of 
        users across the globe.</p>
    </body>
    </html>
    """
    about = crawler.extract_about(sample_html_about)
    print(f"Sample HTML contains company information")
    print(f"Extracted: {about}")
    
    # Demo 5: Sidebar Features
    print("\n🎨 Demo 5: Interactive Sidebar Features")
    print("-" * 70)
    print("The sidebar provides:")
    print("  ✓ Beautiful gradient design")
    print("  ✓ Displays all captured information")
    print("  ✓ Clickable fields for validation")
    print("  ✓ Visual feedback on selection")
    print("  ✓ Sticky positioning on the right side")
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print("\nTo run the full crawler with browser automation:")
    print("  python src/crawler.py")
    print("\nMake sure you have Chrome browser installed!")


if __name__ == '__main__':
    demo_extraction()
