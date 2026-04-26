from core.resolver import Resolver
from core.correlator import Correlator
from utils.validators import is_valid_email, is_valid_domain, is_valid_username, is_valid_phone
import sys

class OSINTEngine:
    def __init__(self):
        self.resolver = Resolver()
        self.correlator = Correlator()

    def run(self, target_type: str, target: str) -> dict:
        self._validate_target(target_type, target)
        
        print(f"[*] Starting {target_type} analysis for: {target}")
        
        results = {}
        sources = self.resolver.get_sources_for_target(target_type)
        
        if not sources:
            print(f"[-] No sources configured for target type: {target_type}")
            return {"query": target, "results": {}}
            
        for source in sources:
            print(f"[*] Running module: {source.name}...")
            try:
                # Dispatch to appropriate method based on target type
                if target_type == "username":
                    results[source.name] = source.search_username(target)
                elif target_type == "domain":
                    results[source.name] = source.analyze_domain(target)
                elif target_type == "email":
                    results[source.name] = source.analyze_email(target)
                elif target_type == "phone":
                    results[source.name] = source.analyze_phone(target)
            except Exception as e:
                print(f"[-] Module {source.name} failed: {str(e)}")
                results[source.name] = {"error": str(e)}
                
            # Print inline summary for this module
            self._print_module_summary(results.get(source.name, {}))
                
        # Basic correlation
        correlation = self.correlator.correlate(target_type, target, results)
        if correlation and correlation.get("cross_references"):
            results["correlation_engine"] = correlation
            
        print("[+] Analysis complete.\n")
        return {
            "query": target,
            "results": results
        }
        
    def run_profile(self, target: str) -> dict:
        """Run a full profile (email + username extraction + domain)."""
        print(f"[*] Starting full profile analysis for: {target}")
        
        results = {}
        
        # Determine target types included
        if "@" in target:
            username, domain = target.split("@", 1)
            
            print(f"[*] Identified as email. Breaking down into Username: {username}, Domain: {domain}")
            
            # Run email
            email_res = self.run("email", target)
            results["email"] = email_res["results"]
            
            # Run username
            user_res = self.run("username", username)
            results["username_intel"] = user_res["results"]
            
            # Run domain
            domain_res = self.run("domain", domain)
            results["domain_intel"] = domain_res["results"]
            
        else:
            print("[-] Profile target must be an email address to extract username and domain.")
            sys.exit(1)
            
        return {
            "query": target,
            "results": results
        }

    def _validate_target(self, target_type: str, target: str):
        if target_type == "email" and not is_valid_email(target):
            print(f"[-] Invalid email format: {target}")
            sys.exit(1)
        elif target_type == "domain" and not is_valid_domain(target):
             print(f"[-] Invalid domain format: {target}")
             sys.exit(1)
        elif target_type == "username" and not is_valid_username(target):
            print(f"[-] Invalid username format: {target}")
            sys.exit(1)
        elif target_type == "phone":
            if not is_valid_phone(target):
                print(f"[-] Invalid phone number format: {target}")
                sys.exit(1)

    def _print_module_summary(self, module_result: dict):
        """Print relevant findings from a module result to the terminal."""
        if not isinstance(module_result, dict):
            return

        # Print URL if present
        if "url" in module_result:
            print(f"    [+] Link found  : {module_result['url']}")

        # Print breach summary if present
        breaches = module_result.get("breaches")
        if isinstance(breaches, dict):
            if breaches.get("found") and breaches.get("breach_count", 0) > 0:
                count = breaches["breach_count"]
                names = ", ".join(breaches.get("breaches", []))
                print(f"    [!] Breaches    : {count} found -> {names}")
            elif breaches.get("found") is False or breaches.get("breach_count", 0) == 0:
                print(f"    [+] Breaches    : No breaches found (XposedOrNot)")
            if "error" in breaches:
                print(f"    [-] Breach check error: {breaches['error']}")

        # Print HIBP summary if present
        hibp = module_result.get("hibp")
        if isinstance(hibp, dict):
            if hibp.get("found") and hibp.get("breach_count", 0) > 0:
                count = hibp["breach_count"]
                names = ", ".join(hibp.get("breaches", []))
                print(f"    [!] HIBP        : {count} breaches -> {names}")
            elif hibp.get("found") is False:
                print(f"    [+] HIBP        : No breaches found")
            elif not hibp.get("checked", True):
                print(f"    [i] HIBP        : {hibp.get('message', 'Not checked')}")
            if "error" in hibp:
                print(f"    [-] HIBP error  : {hibp['error']}")

        # Print domain info if present
        if "domain" in module_result:
            print(f"    [i] Domain      : {module_result['domain']}")
        if module_result.get("is_disposable_provider"):
            print(f"    [!] Warning     : Disposable email provider!")
        if module_result.get("is_free_provider"):
            print(f"    [i] Provider    : Free email provider")

        # --- Phone Specific Summaries ---
        if "tellows" in module_result:
            t = module_result["tellows"]
            name_str = f" [{t['name']}]" if t.get("name") and t["name"] != "Unknown" else ""
            print(f"    [i] Tellows{name_str}: {t['url']}")
        if "paginebianche" in module_result:
            print(f"    [i] PagineBianche: {module_result['paginebianche']['url']}")
        if "accounts" in module_result:
            print(f"    [*] Search for accounts on:")
            for platform, url in module_result["accounts"].items():
                print(f"        - {platform:10}: {url}")
        if "social_presence" in module_result:
             presence = module_result["social_presence"]
             print(f"    [+] Social Presence:")
             print(f"        - WhatsApp  : {presence['whatsapp_link']}")
             print(f"        - Telegram  : {presence['telegram_link']}")
        if "truecaller" in module_result:
             tc = module_result["truecaller"]
             status = "[!]" if tc.get("found") else "[-]"
             print(f"    {status} Truecaller   : {tc['message']}")
