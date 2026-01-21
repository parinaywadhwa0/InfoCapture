"""
Test script for InfoCapture crawler
Tests individual components without running the full browser automation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import re
from crawler import InfoCaptureCrawler


def test_csv_reading():
    """Test reading companies from CSV"""
    print("Testing CSV reading...")
    crawler = InfoCaptureCrawler('companies.csv')
    companies = crawler.read_companies_csv()
    
    assert len(companies) > 0, "No companies found in CSV"
    assert 'id' in companies[0], "Missing 'id' field"
    assert 'company_name' in companies[0], "Missing 'company_name' field"
    
    print(f"✓ Successfully loaded {len(companies)} companies")
    for company in companies:
        print(f"  - ID: {company['id']}, Name: {company['company_name']}")
    

def test_phone_extraction():
    """Test phone number extraction"""
    print("\nTesting phone extraction...")
    crawler = InfoCaptureCrawler()
    
    test_html = """
    <html>
    <body>
        <p>Contact us at +1 (555) 123-4567</p>
        <p>Phone: 555-123-4567</p>
    </body>
    </html>
    """
    
    phone = crawler.extract_phone(test_html)
    assert phone is not None, "Phone extraction failed"
    print(f"✓ Extracted phone: {phone}")


def test_email_extraction():
    """Test email extraction"""
    print("\nTesting email extraction...")
    crawler = InfoCaptureCrawler()
    
    test_html = """
    <html>
    <body>
        <a href="mailto:info@company.com">Contact Us</a>
        <p>Email: support@company.com</p>
    </body>
    </html>
    """
    
    email = crawler.extract_email(test_html)
    assert email is not None, "Email extraction failed"
    print(f"✓ Extracted email: {email}")


def test_about_extraction():
    """Test about section extraction"""
    print("\nTesting about extraction...")
    crawler = InfoCaptureCrawler()
    
    test_html = """
    <html>
    <head>
        <meta name="description" content="We are a leading technology company focused on innovation.">
    </head>
    <body>
        <h2>About Us</h2>
        <p>This is a test company that provides excellent services to customers worldwide.</p>
    </body>
    </html>
    """
    
    about = crawler.extract_about(test_html)
    assert about is not None, "About extraction failed"
    print(f"✓ Extracted about: {about[:100]}...")


if __name__ == '__main__':
    print("=" * 60)
    print("InfoCapture Test Suite")
    print("=" * 60)
    
    try:
        test_csv_reading()
        test_phone_extraction()
        test_email_extraction()
        test_about_extraction()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
