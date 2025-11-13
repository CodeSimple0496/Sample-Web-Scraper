# Configuration settings
import os

class Config:
    # Request headers to mimic a real browser
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Timeout in seconds
    TIMEOUT = 10
    
    # Default encoding
    ENCODING = 'utf-8'