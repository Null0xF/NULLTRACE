import os
from utils.http_client import HTTPClient


class EmailBreachSource:
    """
    Email analysis source.
    - Domain extraction and classification (disposable/free)
    - Breach lookup via XposedOrNot (free, no key required)
    - Optional breach lookup via HaveIBeenPwned (requires HIBP_API_KEY env var)
    """
    def __init__(self):
        self.name = "email_analysis"
        self.client = HTTPClient()
        self.xon_url = "https://api.xposedornot.com/v1/check-email/{}"
        self.hibp_url = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

    def analyze_email(self, email: str) -> dict:
        result = {}

        # --- Domain analysis ---
        if "@" in email:
            domain = email.split("@")[-1].lower()
            result["domain"] = domain

            disposable_domains = [
                "mailinator.com", "10minutemail.com", "tempmail.com",
                "guerrillamail.com", "trashmail.com", "yopmail.com"
            ]
            free_providers = [
                "gmail.com", "yahoo.com", "hotmail.com",
                "outlook.com", "live.com", "icloud.com"
            ]
            result["is_disposable_provider"] = domain in disposable_domains
            result["is_free_provider"] = domain in free_providers

        # --- Breach check via XposedOrNot (free, no key) ---
        result["breaches"] = self._check_xposedornot(email)

        # --- Optional: HaveIBeenPwned (requires HIBP_API_KEY env var) ---
        hibp_key = os.environ.get("HIBP_API_KEY")
        if hibp_key:
            result["hibp"] = self._check_hibp(email, hibp_key)
        else:
            result["hibp"] = {
                "checked": False,
                "message": "Set HIBP_API_KEY env var to enable HaveIBeenPwned lookup."
            }

        return result

    def _check_xposedornot(self, email: str) -> dict:
        """Check email against XposedOrNot public API (free)."""
        url = self.xon_url.format(email)
        response = self.client.get(url)

        if response is None:
            return {"error": "Request failed (no response)."}

        if response.status_code == 404:
            return {
                "found": False,
                "message": "No breaches found for this email."
            }

        if response.status_code == 200:
            try:
                data = response.json()
                # The API returns {"breaches": [["Name1", "Name2", ...]], ...}
                breaches_nested = data.get("breaches", [])
                names = []
                if breaches_nested and isinstance(breaches_nested, list):
                    if isinstance(breaches_nested[0], list):
                        names = breaches_nested[0]
                    else:
                        names = breaches_nested
                
                found = len(names) > 0
                return {
                    "found": found,
                    "breach_count": len(names),
                    "breaches": names
                }
            except Exception as e:
                return {"error": f"Failed to parse response: {str(e)}"}

        return {"error": f"Unexpected HTTP {response.status_code}"}

    def _check_hibp(self, email: str, api_key: str) -> dict:
        """Check email against HaveIBeenPwned API v3 (requires paid key)."""
        url = self.hibp_url.format(email)
        headers = {
            "hibp-api-key": api_key,
            "User-Agent": "NullTrace/1.0"
        }
        response = self.client.get(url, extra_headers=headers)

        if response is None:
            return {"error": "Request failed (no response)."}

        if response.status_code == 404:
            return {"found": False, "message": "No breaches found."}

        if response.status_code == 401:
            return {"error": "Invalid HIBP API key."}

        if response.status_code == 429:
            return {"error": "HIBP rate limit reached. Try again later."}

        if response.status_code == 200:
            try:
                data = response.json()
                names = [b.get("Name", "Unknown") for b in data]
                return {
                    "found": True,
                    "breach_count": len(names),
                    "breaches": names
                }
            except Exception as e:
                return {"error": f"Failed to parse response: {str(e)}"}

        return {"error": f"Unexpected HTTP {response.status_code}"}
