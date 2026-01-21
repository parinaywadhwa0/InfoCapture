"""
InfoCapture - Web Crawler for Company Information
Automatically searches and extracts company information from websites
"""

import pandas as pd
import re
import time
import os
import json
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class InfoCaptureCrawler:
    """Main crawler class for capturing company information"""
    
    def __init__(self, csv_file='companies.csv'):
        self.csv_file = csv_file
        self.driver = None
        self.current_data = {}
        self.results = []
        
    def setup_driver(self):
        """Initialize Chrome driver with custom options"""
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def inject_sidebar(self, data):
        """Inject the sidebar with company information
        
        Note: sidebar_html and sidebar_js are from trusted local files,
        not user input, so there's no XSS risk from template injection.
        """
        sidebar_html_path = os.path.join(os.path.dirname(__file__), '..', 'extension', 'sidebar.html')
        sidebar_js_path = os.path.join(os.path.dirname(__file__), '..', 'extension', 'sidebar.js')
        
        # Read sidebar HTML (trusted source - local file)
        with open(sidebar_html_path, 'r') as f:
            sidebar_html = f.read()
        
        # Read sidebar JS (trusted source - local file)
        with open(sidebar_js_path, 'r') as f:
            sidebar_js = f.read()
        
        # Inject sidebar into page
        # Note: sidebar_html is from a trusted local file, not user input
        inject_script = f"""
        // Remove existing sidebar if present
        const existingSidebar = document.querySelector('#infocapture-sidebar');
        if (existingSidebar) {{
            existingSidebar.remove();
        }}
        
        // Inject sidebar HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(`{sidebar_html}`, 'text/html');
        document.body.appendChild(doc.body.firstChild);
        
        // Inject sidebar JS
        {sidebar_js}
        
        // Update with data
        updateSidebar({data});
        """
        
        self.driver.execute_script(inject_script)
        
    def read_companies_csv(self):
        """Read company names from CSV file"""
        df = pd.read_csv(self.csv_file)
        return df.to_dict('records')
    
    def search_company(self, company_name):
        """Search for company on Google and open the most relevant website"""
        search_query = f"{company_name} official website"
        
        # Go to Google
        self.driver.get('https://www.google.com')
        time.sleep(2)
        
        try:
            # Accept cookies if present
            try:
                accept_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree')]"))
                )
                accept_button.click()
            except TimeoutException:
                pass
            
            # Find search box and search
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            search_box.clear()
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            # Click on first search result
            first_result = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#search a[href]:not([href^="#"])'))
            )
            
            result_url = first_result.get_attribute('href')
            print(f"Opening: {result_url}")
            self.driver.get(result_url)
            time.sleep(5)
            
            return result_url
            
        except Exception as e:
            print(f"Error during search: {e}")
            return None
    
    def extract_phone(self, html_content):
        """Extract phone numbers from HTML content"""
        # Common phone number patterns
        patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
        ]
        
        soup = BeautifulSoup(html_content, 'lxml')
        text = soup.get_text()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Return the first valid-looking phone number
                for match in matches:
                    # Filter out numbers that are too generic
                    if len(re.sub(r'\D', '', match)) >= 10:
                        return match
        
        return None
    
    def extract_email(self, html_content):
        """Extract email addresses from HTML content"""
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Look for email in mailto links first
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
        if mailto_links:
            email = mailto_links[0]['href'].replace('mailto:', '').split('?')[0]
            return email
        
        # Look for email patterns in text
        text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        
        if matches:
            # Filter out common false positives
            for email in matches:
                if not any(x in email.lower() for x in ['example.com', 'domain.com', 'yoursite.com']):
                    return email
        
        return None
    
    def extract_about(self, html_content):
        """Extract 'about company' information"""
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Look for meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'][:300]
        
        # Look for common about sections
        about_keywords = ['about', 'overview', 'company', 'who we are', 'our story']
        
        for keyword in about_keywords:
            # Look for headings with these keywords
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(keyword, re.I))
            for heading in headings:
                # Get text from next sibling or parent
                parent = heading.find_parent(['div', 'section', 'article'])
                if parent:
                    text = parent.get_text(strip=True)
                    if len(text) > 50:
                        return text[:300]
        
        # Fallback: Get first substantial paragraph
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 100:
                return text[:300]
        
        return None
    
    def capture_information(self):
        """Capture phone, email, and about information from current page"""
        html_content = self.driver.page_source
        current_url = self.driver.current_url
        
        print("Extracting information...")
        
        phone = self.extract_phone(html_content)
        email = self.extract_email(html_content)
        about = self.extract_about(html_content)
        
        return {
            'website': current_url,
            'phone': phone,
            'email': email,
            'about': about
        }
    
    def process_company(self, company):
        """Process a single company: search, extract, and display"""
        print(f"\n{'='*60}")
        print(f"Processing: {company['company_name']} (ID: {company['id']})")
        print(f"{'='*60}")
        
        # Search and open website
        website_url = self.search_company(company['company_name'])
        
        if website_url:
            # Capture information
            info = self.capture_information()
            
            # Combine all data
            self.current_data = {
                'id': company['id'],
                'company_name': company['company_name'],
                **info
            }
            
            # Display in sidebar
            data_json = json.dumps(self.current_data).replace('`', '\\`')
            self.inject_sidebar(data_json)
            
            # Print captured information
            print(f"\n📊 Captured Information:")
            print(f"  🔗 Website: {info['website']}")
            print(f"  📞 Phone: {info['phone'] or 'Not found'}")
            print(f"  📧 Email: {info['email'] or 'Not found'}")
            print(f"  ℹ️  About: {info['about'][:100] if info['about'] else 'Not found'}...")
            
            # Store result
            self.results.append(self.current_data)
            
            # Wait for user to review
            print("\n⏸️  Review the information in the sidebar (right side of browser)")
            print("   Click on fields to verify them")
            print("   Press Enter to continue to next company...")
            input()
        else:
            print(f"Could not find website for {company['company_name']}")
    
    def save_results(self, output_file='captured_data.csv'):
        """Save captured results to CSV"""
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(output_file, index=False)
            print(f"\n✅ Results saved to {output_file}")
    
    def run(self):
        """Main execution method"""
        print("🚀 Starting InfoCapture Crawler...")
        
        try:
            # Setup browser
            self.setup_driver()
            
            # Read companies
            companies = self.read_companies_csv()
            print(f"\n📋 Loaded {len(companies)} companies from {self.csv_file}")
            
            # Process each company
            for company in companies:
                self.process_company(company)
            
            # Save results
            self.save_results()
            
            print("\n🎉 All companies processed successfully!")
            print("Browser will close in 5 seconds...")
            time.sleep(5)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            traceback.print_exc()
        
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == '__main__':
    crawler = InfoCaptureCrawler()
    crawler.run()
