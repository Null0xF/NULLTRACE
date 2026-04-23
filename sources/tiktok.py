from utils.http_client import HTTPClient

class TikTokSource:
    def __init__(self):
        self.name = "tiktok"
        self.base_url = "https://www.tiktok.com/@{}"
        self.client = HTTPClient()

    def search_username(self, username: str) -> dict:
        url = self.base_url.format(username)
        # TikTok also blocks basic requests often
        response = self.client.get(url, allow_redirects=False)
        
        result = {"found": False}
        if response:
            if response.status_code == 200:
                result["found"] = True
                result["url"] = url
            elif response.status_code == 404:
                result["found"] = False
            else:
                result["error"] = f"HTTP {response.status_code}. Rate limit or captcha required."
                result["url"] = url
                
        return result
