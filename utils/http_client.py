import requests
import logging

class HTTPClient:
    """A simple wrapper around requests to provide consistent headers and timeouts."""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "NullTrace/1.0 (OSINT Research Tool)",
            "Accept": "application/json, text/plain, */*"
        }

    def get(self, url: str, params=None, extra_headers=None, allow_redirects=True) -> requests.Response:
        headers = self.headers.copy()
        if extra_headers:
            headers.update(extra_headers)
            
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=self.timeout,
                allow_redirects=allow_redirects
            )
            return response
        except requests.RequestException as e:
            logging.debug(f"HTTP GET failed for {url}: {e}")
            return None
