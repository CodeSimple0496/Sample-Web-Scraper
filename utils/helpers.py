# feat: Add web scraping utility functions with error handling

# - Add HTTP request function with proper headers and timeout
# - Implement BeautifulSoup wrapper with error handling
# - Create safe text and attribute extraction utilities
# - Configure logging for debugging and monitoring


import requests                 
from bs4 import BeautifulSoup   
import time                     
import logging                  
from config import Config    

"""
# requests: For making HTTP requests to websites
# BeautifulSoup: For parsing and nvigating HTML content
# time : (Currently unused) Could be for adding dealys between requests
# logging: For recording errors and information
# Config: Custom configuration file with settings

"""
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
# Purpose: Creates a logging system to track what the script is doing

# Level INFO: Recodes important events (errors, warnings, info messages)
# logger: Object used to write log messages throughout the code
"""


# Make HTTP request with error handling
def make_request(url, headers=None, timeout=None):   # url: website address to request, headers=None - custom headers (uses defaults if not provided), timeout=None - custom timeout (uses default if not provided)
    """
    Website down - Logs error, returns [None]
    404 Not Found - Logs error, returns [None]
    Network timeout - Logs error, return [None]
    SSL certificate issues - Logs error, returns [None]
    Successful request - Returns response object
    """
    if headers is None:
        headers = Config.HEADERS  # If no headers provided -> uses Config.HEADERS (browser-like headers)
    if timeout is None:
        timeout = Config.TIMEOUT  # If no timeout provided -> uses Config.TIMEOUT (10 seconds)
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)  # requests.get(): HTTP GET request to the URL, headers=headers: sends browser-like headers to avoid being blockedm, timeout=timeout: Prevents hanging indefinitely
        response.raise_for_status()
        response.encoding = Config.ENCODING
        return response
    # Only runs if request was successful
    except requests.exceptions.RequestException as e:    
        logger.error(f"Request failed for {url}: {e}")
        return None
    # Request failed, but program continue
    
    """
    - ConnectionError: Cannot reach the server
    - timeout: Request took too long
    - HTTPError: 4xx/5xx status codes (from raise_for_status())
    - TooManyRedirects: Infinite redirect loops
    - Return None
    """

def create_soup(html_content, parser='html.parser'): # html_content: HTML string to parse. parser='html.parser': Optional - which parser to use 
    """
    Create BeautifulSoup object
    """
    try:
        return BeautifulSoup(html_content, parser)  # Creates a parse tree from HTML, 
    except Exception as e:
        logger.error(f"Failed to parse HTML: {e}")
        return None
    """
    - Malormed HTML - <div><p> closing div - Crash
    - Empty content - "" or None - Crash
    - Binary data - PDF/Image files - Crash
    - Encoding issues - Invalid UTF-8 characters - Crash
    - Very large files - Memory exhaustion - Crash
    """

def extract_text(element, default=''):
    """
    Safely extract text from BeautifulSoup element

    # element - BeautifulSoup element to extract text from
    # default='': Optional - value to return if element is None or invalid
    """
    if element:
        return element.get_text(strip=True) 
    return default

def extract_attribute(element, attribute, default=''):
    """
    Safely extract attribute from BeautifulSoup element

    # element: Required-BeautifulSoup element to extract attribute from
    # attribute: Required - name of the attribute to extract(e.g., 'herf', 'src', 'class')
    # default='': Optional - value to return if element or attribute doesn;t exist
    """
    if element and element.has_attr(attribute):
        return element[attribute]
    return default