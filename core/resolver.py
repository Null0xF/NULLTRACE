from sources.github import GitHubSource
from sources.reddit import RedditSource
from sources.instagram import InstagramSource
from sources.tiktok import TikTokSource
from sources.dns import DNSSource
from sources.whois import WhoisSource
from sources.email_breach import EmailBreachSource

class Resolver:
    def __init__(self):
        self.username_sources = [
            GitHubSource(), 
            RedditSource(),
            InstagramSource(),
            TikTokSource()
        ]
        self.domain_sources = [DNSSource(), WhoisSource()]
        self.email_sources = [EmailBreachSource()]

    def get_sources_for_target(self, target_type: str) -> list:
        """Return the list of source modules for a specific target type."""
        if target_type == "username":
            return self.username_sources
        elif target_type == "domain":
            return self.domain_sources
        elif target_type == "email":
            return self.email_sources
        return []
