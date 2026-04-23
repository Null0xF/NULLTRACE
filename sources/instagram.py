from utils.http_client import HTTPClient

class InstagramSource:
    def __init__(self):
        self.name = "instagram"
        self.base_url = "https://www.instagram.com/{}/"
        self.client = HTTPClient()

    def search_username(self, username: str) -> dict:
        url = self.base_url.format(username)
        # Instagram blocks a lot of scrapers, we do a basic GET with standard headers
        response = self.client.get(url, allow_redirects=False)
        
        result = {"found": False}
        if response:
            if response.status_code == 200:
                result["found"] = True
                result["url"] = url
            elif response.status_code == 404:
                result["found"] = False
            else:
                # 301/302 redirects usually mean they're redirecting to login because of rate limits,
                # but let's assume if it doesn't 404, there's a good chance the profile exists
                # or we got rate limited.
                result["error"] = f"HTTP {response.status_code}. Rate limit or login required."
                result["url"] = url
                
        return result
