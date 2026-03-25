"""
Configuration settings for trading tools
"""

# WafaBourse API Configuration
WAFABOURSE_API = "https://www.wafabourse.com/api/proxy/data/JNNJ"

# Default request headers
DEFAULT_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'origin': 'https://www.wafabourse.com',
    'referer': 'https://www.wafabourse.com/fr/market-tracking',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

# API timeout in seconds
REQUEST_TIMEOUT = 10
