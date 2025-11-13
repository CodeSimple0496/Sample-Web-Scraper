from scraper import WebScraper, scrape_example_website # WebScraper: Main scraping class, # scrape_example_website: Pre-built example function
import json # For data serialization and pretty printing

def example_basic_scraping():
    """Basic example of web scraping"""
    print("=== Basic Web Scraping Example ===")
    
    # 1. Initialize scraper with target URL
    scraper = WebScraper("https://httpbin.org/html")
    
    # 2. Fetch page (with error checking)
    if scraper.fetch_page():

        # 3. Extract titles
        titles = scraper.scrape_titles()
        print("Titles:")
        for title in titles:
            print(f"  - {title['tag']}: {title['text']}")
        
        # 4. Extract links
        links = scraper.scrape_links()
        print(f"\nFound {len(links)} links")
        
        # 5. Extract data
        scraper.save_to_json('titles.json', titles)
        scraper.save_to_csv('links.csv', links)

def example_custom_scraping():    # Purpose: Shows how to target specific elements using CSS selectors
    """Example of custom scraping with specific selectors"""
    print("\n=== Custom Scraping Example ===")
    
    scraper = WebScraper("https://httpbin.org/html")
    
    if scraper.fetch_page():
        # Define custom selectors for specific elements
        selectors = {
            'main_heading': 'h1',                    # Single element
            'paragraphs': 'p',                       # Multiple elements
            'all_headers': 'h1, h2, h3, h4, h5, h6'  # Complex selector
        }
        
        results = scraper.custom_scrape(selectors)
        print("Custom scraping results:")
        print(json.dumps(results, indent=2))

def example_multiple_pages():  # Purpose: Demonstrates scraping multiple websites in one run
    """Example of scraping multiple pages"""
    print("\n=== Multiple Pages Example ===")
    
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/xml"   # Different content type
    ]
    
    all_data = {}
    
    for url in urls:
        print(f"Scraping: {url}")  # Progress indicator
        scraper = WebScraper(url)
        
        if scraper.fetch_page():
            titles = scraper.scrape_titles()
            all_data[url] = {
                'titles': titles,
                'page_title': extract_text(scraper.soup.title) if scraper.soup.title else 'No title'
            }
    
    # Save combined data
    with open('multiple_pages.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("Multiple pages scraped and saved to multiple_pages.json")

def extract_text(soup_element):
    """Helper function to extract text from soup element"""
    return soup_element.get_text(strip=True) if soup_element else "No text"

if __name__ == "__main__":
    # Run examples
    example_basic_scraping()
    example_custom_scraping()
    example_multiple_pages()
    
    # Run the built-in example
    scrape_example_website()