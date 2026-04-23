import whois

class WhoisSource:
    def __init__(self):
        self.name = "whois"

    def analyze_domain(self, domain: str) -> dict:
        result = {}
        try:
            w = whois.whois(domain)
            result["registrar"] = w.registrar
            
            # Formatting lists and dates
            result["creation_date"] = str(w.creation_date) if w.creation_date else None
            result["expiration_date"] = str(w.expiration_date) if w.expiration_date else None
            
            # Sometimes name_servers is a list, sometimes a string
            if isinstance(w.name_servers, list):
                result["name_servers"] = w.name_servers
            elif w.name_servers:
                result["name_servers"] = [w.name_servers]
            else:
                result["name_servers"] = []
                
            result["emails"] = w.emails if isinstance(w.emails, list) else ([w.emails] if w.emails else [])
            result["org"] = w.org
            result["country"] = w.country
            
        except Exception as e:
            result["error"] = str(e)
            
        return result
