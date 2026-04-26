import os
import re
from utils.http_client import HTTPClient

class PhoneSource:
    """
    Phone number analysis source.
    - Identity lookup via Tellows/PagineBianche
    - Account discovery via Google Dorking links
    - Social platform check (WhatsApp, Telegram)
    - Truecaller (Requires auth)
    """
    def __init__(self):
        self.name = "phone_analysis"
        self.client = HTTPClient()

    def analyze_phone(self, phone: str) -> dict:
        result = {}
        # Normalize phone (remove spaces, dashes)
        clean_phone = re.sub(r"[\s\-\(\)]", "", phone)
        
        # Ensure it has a leading + for international search if missing
        if not clean_phone.startswith("+") and len(clean_phone) > 8:
             # Heuristic: if it doesn't start with + but looks like intl, keep as is
             # but for dorks we might want both formats.
             pass

        # 1. Tellows lookup (Good for spam and sometimes identity)
        result["tellows"] = self._lookup_tellows(clean_phone)
        
        # 2. Pagine Bianche (Italy specific, but very useful for landlines/business)
        result["paginebianche"] = self._lookup_paginebianche(clean_phone)

        # 3. Account discovery (Google Dorks)
        result["accounts"] = self._get_account_dorks(clean_phone)
        
        # 4. Social Presence check
        result["social_presence"] = self._check_social_presence(clean_phone)
        
        # 5. Truecaller (Stub/Config check)
        result["truecaller"] = self._lookup_truecaller(clean_phone)

        return result

    def _lookup_tellows(self, phone: str) -> dict:
        # Tellows is global, choosing it.it as default for Italian context
        url = f"https://www.tellows.it/num/{phone}"
        response = self.client.get(url)
        name = "Unknown"
        
        if response and response.status_code == 200:
            # Extract name from <title> or <h1>
            title_match = re.search(r"<title>(.*?)</title>", response.text)
            if title_match:
                title = title_match.group(1)
                # Tellows title format: "Name con 012345678 | Punteggio..."
                if " con " in title:
                    name = title.split(" con ")[0].strip()
                elif "|" in title:
                    name = title.split("|")[0].strip()
                
                # Filter out generic titles or titles that just contain the number
                clean_name = re.sub(r"\D", "", name)
                clean_query = re.sub(r"\D", "", phone)
                
                if "Chi chiama" in name or "Punteggio" in name or "appartiene" in name or clean_query in clean_name:
                    name = "Unknown"

        return {
            "source": "Tellows",
            "url": url,
            "name": name,
            "info": f"Identified as: {name}" if name != "Unknown" else "Check link for identity/spam reports."
        }

    def _lookup_paginebianche(self, phone: str) -> dict:
        # Pagine Bianche 'Chi Chiama'
        url = f"https://www.paginebianche.it/chi-chiama?qs={phone}"
        return {
            "source": "Pagine Bianche",
            "url": url,
            "info": "Primary source for Italian landlines and verified business mobiles."
        }

    def _get_account_dorks(self, phone: str) -> dict:
        platforms = {
            "Facebook": f"site:facebook.com \"{phone}\"",
            "Instagram": f"site:instagram.com \"{phone}\"",
            "LinkedIn": f"site:linkedin.com \"{phone}\"",
            "Twitter": f"site:twitter.com \"{phone}\"",
            "Telegram": f"site:t.me \"{phone}\"",
            "WhatsApp": f"site:wa.me \"{phone}\""
        }
        dorks = {}
        for name, query in platforms.items():
            dorks[name] = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return dorks

    def _check_social_presence(self, phone: str) -> dict:
        # WhatsApp 'Click to Chat' link
        clean_num = re.sub(r"\D", "", phone)
        return {
            "whatsapp_link": f"https://wa.me/{clean_num}",
            "telegram_link": f"https://t.me/+{clean_num}" if phone.startswith("+") else f"https://t.me/{clean_num}"
        }

    def _lookup_truecaller(self, phone: str) -> dict:
        token = os.environ.get("TRUECALLER_TOKEN")
        if not token:
            return {
                "found": False,
                "message": "Truecaller requires authentication. Set TRUECALLER_TOKEN to enable."
            }
        
        return {
            "found": True,
            "message": "Truecaller authentication detected. [PRO] Integration in progress."
        }
