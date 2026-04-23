from utils.http_client import HTTPClient

class GitHubSource:
    def __init__(self):
        self.name = "github"
        self.base_url = "https://api.github.com/users/"
        self.client = HTTPClient()

    def search_username(self, username: str) -> dict:
        url = f"{self.base_url}{username}"
        response = self.client.get(url)
        
        result = {"found": False}
        if response and response.status_code == 200:
            data = response.json()
            result["found"] = True
            result["url"] = data.get("html_url")
            result["name"] = data.get("name")
            result["company"] = data.get("company")
            result["blog"] = data.get("blog")
            result["location"] = data.get("location")
            result["public_repos"] = data.get("public_repos")
            result["followers"] = data.get("followers")
            
        return result
