from bs4 import BeautifulSoup  # HTML parsing
from utils.helpers import make_request, create_soup, extract_text, extract_attribute # Custom utilities: Safe function we discussed earlier
import json  # json/csv: For data export capabilities
import csv

class WebScraper:
    def __init__(self, base_url=None):
        self.base_url = base_url  # base_url: Optional base URL for relative link resolution
        self.soup = None  # soup: Stores the parsed HTML documnet
        self.data = []  # data: Collection for storing scraped results
    
    def fetch_page(self, url=None):
        """
        Fetch webpage content
        """
        target_url = url or self.base_url   # URL resolution: Uses provided URL or base_url
        if not target_url:
            raise ValueError("No URL provided")  # Validation: Ensures URL is provided
        
        response = make_request(target_url)   # Safe request: Uses our make_request utility
        if response:
            self.soup = create_soup(response.text)  # HTML parsing: Uses create_soup utility 
            return True   # Returns: True if successful, False if failed
        return False
    
    def scrape_links(self, selector='a'):  # Flexible selector: Defaults to all <a> tags
        """
        Extract all links from the page
        """
        if not self.soup:
            raise Exception("No page loaded. Call fetch_page() first.")  # Safe extraction: Uses our utility functions
        
        links = []
        for link in self.soup.select(selector):
            href = extract_attribute(link, 'href')   # URL resolution: Converts relative URLs to absolute
            text = extract_text(link)
            if href:
                links.append({
                    'text': text,
                    'url': href,
                    'full_url': self._make_absolute_url(href)
                })
        return links   # Data structure: Returns list of dictionaries
    
    def scrape_titles(self, selector='h1, h2, h3'):  # Hierarchical titles: Gets all heading levels by default
        """
        Extract titles from the page
        """
        if not self.soup:
            raise Exception("No page loaded. Call fetch_page() first.")  # Tag identification: Knows which heading level it found
        
        titles = []
        for title in self.soup.select(selector):
            titles.append({
                'tag': title.name,
                'text': extract_text(title)
            })
        return titles      # Clean text: Stripped of whitespace
    
    def scrape_images(self, selector='img'):  # Multiple attributes: Extracts scr, alt, and title
        """
        Extract images from the page
        """
        if not self.soup:
            raise Exception("No page loaded. Call fetch_page() first.")  
        
        images = []
        for img in self.soup.select(selector):   # Descriptive defaults: Clear fallback, text
            images.append({
                'src': extract_attribute(img, 'src'),
                'alt': extract_attribute(img, 'alt', 'No alt text'),
                'title': extract_attribute(img, 'title', 'No title')
            })
        return images   # Flexible selection: Can target specific images
    
    def custom_scrape(self, selectors):  # Powerful feature: Dynamic scraping based on configuration
        """
        Custom scraping based on CSS selectors
        """
        if not self.soup:
            raise Exception("No page loaded. Call fetch_page() first.")
        
        results = {}
        for key, selector in selectors.items():
            elements = self.soup.select(selector)
            if len(elements) == 1:
                results[key] = extract_text(elements[0])
            else:
                results[key] = [extract_text(el) for el in elements]
        return results
    
    def _make_absolute_url(self, url):
        """
        Convert relative URL to absolute URL
        """
        if not self.base_url or url.startswith(('http://', 'https://')):   # /about -> https://example.com/about
            return url
        
        from urllib.parse import urljoin
        return urljoin(self.base_url, url)  # page.html -> https://example.com/page.html
    
    def save_to_json(self, filename, data):  # Human-readable: Indented formatting
        """
        Save data to JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:    # Unicode support: Handles international characters
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def save_to_csv(self, filename, data, fieldnames=None):  
        """
        Save data to CSV file
        """
        if not data:
            print("No data to save")
            return
        
        if not fieldnames and data:       # Auto-headers: Detects field names from data
            fieldnames = data[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)  # Excel compatible: Proper encoding and line endings
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")

# Example usage functions
def scrape_example_website():
    """
    Example: Scrape a sample website
    """
    scraper = WebScraper("https://httpbin.org/html")
    
    if scraper.fetch_page(): # Attempts to fetch the webpage
        # Extract different types of data
        titles = scraper.scrape_titles() # All <h1>, <h2>, <h3> elements from the pages
        links = scraper.scrape_links() # All <a> elements from the page
        
        print("Titles found:")
        for title in titles:
            print(f"  {title['tag']}: {title['text']}")

        """
        Titles found:
        h1: This is atest HTML page
        h2: Sample Section
        h3: Subsection Details
        """
        
        print("\nLinks found:")
        for link in links[:5]:  # Show first 5 links
            print(f"  {link['text']}: {link['url']}")

        """
        Links found:
        Home: /
        About: /about
        Contact: /contact
        GitHub: https://github.com
        Documentation: /docs
        """
        
        return {
            'titles': titles,
            'links': links
        }
    return None

"""
- Returns a dictionary containing both datasets
- Can be used for further processing or saving to files
- if page fetch fails: Returns None
"""