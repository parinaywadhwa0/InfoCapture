# InfoCapture 🚀

A powerful web crawler built with Selenium and Python that automatically captures company information from websites.

## Features ✨

- 📊 **CSV-Based Processing**: Read company names and IDs from CSV files
- 🔍 **Automatic Search**: Automatically searches Google and opens the most relevant website
- 📞 **Information Extraction**: Captures phone numbers, email addresses, and company descriptions
- 🎨 **Visual Sidebar**: Displays captured information in a beautiful sidebar on the right side of the browser
- ✅ **Interactive Validation**: Click on any field to verify and validate the captured data
- 💾 **Data Export**: Saves all captured information to a CSV file

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/parinaywadhwa0/InfoCapture.git
cd InfoCapture
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage 📖

1. **Prepare your CSV file**: Create or edit `companies.csv` with your company data:
```csv
id,company_name
1,Microsoft Corporation
2,Apple Inc
3,Amazon.com Inc
```

2. **Run the crawler**:
```bash
python src/crawler.py
```

3. **Review captured data**:
   - The crawler will automatically search for each company
   - Information will appear in the sidebar on the right side of the browser
   - Click on any field (phone, email, about, website) to verify it
   - Press Enter to continue to the next company

4. **Access results**: All captured data is saved to `captured_data.csv`

## How It Works 🔧

1. **CSV Reading**: Loads company names with their IDs from the CSV file
2. **Google Search**: Automatically searches for each company and opens the most relevant website
3. **Information Extraction**: 
   - Extracts phone numbers using regex patterns
   - Finds email addresses in mailto links and text content
   - Captures company descriptions from meta tags and about sections
   - Stores the website URL
4. **Sidebar Display**: Injects a beautiful sidebar into the browser showing all captured information
5. **User Validation**: Allows clicking on fields to verify and validate the data
6. **Data Export**: Saves results to a CSV file for further processing

## Project Structure 📁

```
InfoCapture/
├── src/
│   └── crawler.py          # Main crawler script
├── extension/
│   ├── sidebar.html        # Sidebar UI template
│   └── sidebar.js          # Sidebar JavaScript functionality
├── companies.csv           # Input: Company names and IDs
├── captured_data.csv       # Output: Captured information
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Requirements 📋

- Python 3.7+
- Chrome browser
- Internet connection

## Dependencies 📦

- selenium: Web automation
- pandas: CSV handling
- webdriver-manager: Automatic ChromeDriver management
- beautifulsoup4: HTML parsing
- lxml: XML/HTML parser

## Contributing 🤝

Contributions are welcome! Feel free to open issues or submit pull requests.

## License 📄

This project is open source and available under the MIT License.
