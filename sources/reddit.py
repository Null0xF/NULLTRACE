from utils.http_client import HTTPClient

class RedditSource:
    def __init__(self):
        self.name = "reddit"
        self.base_url = "https://www.reddit.com/user/{}/about.json"
        self.client = HTTPClient()

    def search_username(self, username: str) -> dict:
        url = self.base_url.format(username)
        # Reddit requires a custom User-Agent to prevent 429/403
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NullTrace/1.0"}
        response = self.client.get(url, extra_headers=headers)
        
        result = {"found": False}
        if response and response.status_code == 200:
            data = response.json().get("data", {})
            # If the user is suspended or deleted, 'is_suspended' might be true
            if data.get("is_suspended"):
                result["found"] = True
                result["suspended"] = True
            else:
                result["found"] = True
                result["url"] = f"https://www.reddit.com/user/{username}"
                result["link_karma"] = data.get("link_karma")
                result["comment_karma"] = data.get("comment_karma")
                result["created_utc"] = data.get("created_utc")
        elif response and response.status_code == 404:
             result["found"] = False
        elif response:
            result["error"] = f"HTTP {response.status_code}"
            
        return result
