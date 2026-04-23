"""
Deep Correlator — NullTrace Pro Engine
Given an email, runs a full correlation pipeline:
  1. Breach lookup
  2. Username prediction
  3. Public profile search (GitHub, Reddit, Instagram, TikTok)
  4. Domain analysis
  5. Identity clustering
  6. Confidence scoring
  7. Rich terminal output
"""
import sys
from sources.email_breach import EmailBreachSource
from sources.github import GitHubSource
from sources.reddit import RedditSource
from sources.instagram import InstagramSource
from sources.tiktok import TikTokSource
from sources.dns import DNSSource
from sources.whois import WhoisSource
from core.username_predictor import UsernamePredictor
from core.identity_cluster import IdentityCluster

# Terminal colors (ANSI)
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

FREE_PROVIDERS = {"gmail.com","yahoo.com","hotmail.com","outlook.com","live.com","icloud.com","protonmail.com"}


class DeepCorrelator:
    def __init__(self):
        self.email_src   = EmailBreachSource()
        self.github_src  = GitHubSource()
        self.reddit_src  = RedditSource()
        self.ig_src      = InstagramSource()
        self.tt_src      = TikTokSource()
        self.dns_src     = DNSSource()
        self.whois_src   = WhoisSource()
        self.predictor   = UsernamePredictor()
        self.clusterer   = IdentityCluster()

    # ------------------------------------------------------------------
    # MAIN ENTRY POINT
    # ------------------------------------------------------------------
    def run(self, email: str) -> dict:
        _h("DEEP CORRELATION ENGINE", CYAN)
        print(f"  {DIM}Target:{RESET} {BOLD}{email}{RESET}\n")

        report = {
            "target": email,
            "breaches":          {},
            "predicted_usernames": [],
            "profiles":          {},
            "domain_intel":      {},
            "clusters":          [],
            "confidence_score":  0,
        }

        # ── STEP 1: Email + breach ────────────────────────────────────
        _section("1", "EMAIL & BREACH ANALYSIS")
        email_data = self.email_src.analyze_email(email)
        report["email_meta"] = email_data
        self._print_email(email_data)

        breach_data = email_data.get("breaches", {})
        report["breaches"] = breach_data

        # ── STEP 2: Username prediction ───────────────────────────────
        _section("2", "USERNAME PREDICTION")
        predictions = self.predictor.predict(email)
        report["predicted_usernames"] = predictions
        if predictions:
            print(f"  {GREEN}[+]{RESET} Generated {len(predictions)} username candidates:\n")
            for u in predictions:
                print(f"      {DIM}>{RESET} {u}")
        else:
            print(f"  {DIM}[-] No patterns extracted.{RESET}")
        print()

        # ── STEP 3: Profile search ────────────────────────────────────
        _section("3", "PUBLIC PROFILE DISCOVERY")
        profiles = {}
        for username in predictions:
            found_any = False

            gh  = self.github_src.search_username(username)
            rd  = self.reddit_src.search_username(username)
            ig  = self.ig_src.search_username(username)
            tt  = self.tt_src.search_username(username)

            hits = {k: v for k, v in
                    {"github": gh, "reddit": rd, "instagram": ig, "tiktok": tt}.items()
                    if v.get("found")}

            if hits:
                profiles[username] = hits
                found_any = True
                print(f"  {GREEN}[+]{RESET} {BOLD}{username}{RESET}")
                for platform, pdata in hits.items():
                    url = pdata.get("url", "")
                    print(f"      {GREEN}✓{RESET} {platform:<12} {url}")

            if not found_any:
                print(f"  {DIM}[-] {username} — no hits{RESET}")

        report["profiles"] = profiles
        print()

        # ── STEP 4: Domain intelligence ───────────────────────────────
        _section("4", "DOMAIN INTELLIGENCE")
        domain = email.split("@")[-1].lower()
        if domain not in FREE_PROVIDERS:
            print(f"  {CYAN}[*]{RESET} Non-free domain detected: {BOLD}{domain}{RESET} — running recon...\n")
            dns_data   = self.dns_src.analyze_domain(domain)
            whois_data = self.whois_src.analyze_domain(domain)
            report["domain_intel"] = {"dns": dns_data, "whois": whois_data}
            self._print_domain(dns_data, whois_data)
        else:
            print(f"  {DIM}[i] Domain {domain} is a public provider — skipping deep DNS recon.{RESET}\n")
            report["domain_intel"] = {"skipped": True, "reason": "free provider"}

        # ── STEP 5: Identity clustering ───────────────────────────────
        _section("5", "IDENTITY CLUSTERING")
        # Feed all found profiles into the clusterer
        flat_results = {}
        for uname, plat_dict in profiles.items():
            for platform, pdata in plat_dict.items():
                flat_results[f"{platform}:{uname}"] = pdata

        clusters = self.clusterer.build(flat_results)
        report["clusters"] = clusters

        if clusters:
            for i, c in enumerate(clusters):
                members = ", ".join(c["members"])
                conf    = c["confidence"]
                shared  = c.get("shared_attributes", {})
                shared_str = ", ".join(f"{k}={v}" for k, v in shared.items())
                print(f"  {CYAN}[Cluster {i+1}]{RESET} {BOLD}{members}{RESET}")
                print(f"    Shared attrs: {shared_str or 'username pattern'}")
                print(f"    Confidence  : {_conf_bar(conf)}\n")
        else:
            print(f"  {DIM}[-] No identity clusters detected across found profiles.{RESET}\n")

        # ── STEP 6: Confidence score ──────────────────────────────────
        _section("6", "CONFIDENCE SCORE")
        score = self._compute_score(breach_data, profiles, clusters)
        report["confidence_score"] = score
        print(f"  {BOLD}Overall confidence score: {_conf_bar(score)} ({score}/100){RESET}\n")
        self._print_risk(score)

        # ── Final summary ─────────────────────────────────────────────
        _h("CORRELATION COMPLETE", GREEN)
        b_count = breach_data.get("breach_count", 0) if isinstance(breach_data, dict) else 0
        p_count = sum(len(v) for v in profiles.values())
        print(f"  Breaches found        : {RED if b_count else GREEN}{b_count}{RESET}")
        print(f"  Usernames predicted   : {len(predictions)}")
        print(f"  Profiles discovered   : {p_count}")
        print(f"  Identity clusters     : {len(clusters)}")
        print(f"  Confidence score      : {score}/100\n")

        return report

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------
    def _print_email(self, data: dict):
        breaches = data.get("breaches", {})
        if isinstance(breaches, dict):
            if breaches.get("found"):
                count = breaches.get("breach_count", 0)
                names = ", ".join(breaches.get("breaches", []))
                print(f"  {RED}[!]{RESET} {count} breach(es) found: {BOLD}{names}{RESET}")
            else:
                print(f"  {GREEN}[+]{RESET} No breaches found in XposedOrNot database")

        domain = data.get("domain")
        if domain:
            ptype = "disposable" if data.get("is_disposable_provider") else \
                    "free provider" if data.get("is_free_provider") else "custom/corporate"
            print(f"  {CYAN}[i]{RESET} Domain: {domain}  ({ptype})")
        print()

    def _print_domain(self, dns: dict, whois: dict):
        if dns.get("A"):
            print(f"  {CYAN}[DNS]{RESET}  A records : {', '.join(dns['A'])}")
        if dns.get("MX"):
            print(f"  {CYAN}[DNS]{RESET}  MX records: {', '.join(dns['MX'])}")
        if whois:
            org = whois.get("org") or whois.get("registrar") or whois.get("name")
            if org:
                print(f"  {CYAN}[WHOIS]{RESET} Registrant: {org}")
            created = whois.get("creation_date")
            if created:
                print(f"  {CYAN}[WHOIS]{RESET} Created   : {str(created)[:10]}")
        print()

    def _compute_score(self, breaches, profiles, clusters) -> int:
        score = 0
        # Breach data = high-value intel
        if isinstance(breaches, dict) and breaches.get("found"):
            score += min(30, breaches.get("breach_count", 0) * 8)
        # Each platform hit = +8 pts (max 40)
        hits = sum(len(v) for v in profiles.values())
        score += min(40, hits * 8)
        # Clusters = corroborating evidence
        score += min(20, len(clusters) * 10)
        # Cap at 95 — never 100 without manual verification
        return min(95, score)

    def _print_risk(self, score: int):
        if score >= 70:
            label = f"{RED}HIGH EXPOSURE{RESET}"
            tip   = "Multiple public profiles + breaches detected. Strong digital footprint."
        elif score >= 40:
            label = f"{YELLOW}MODERATE EXPOSURE{RESET}"
            tip   = "Partial footprint. Some profiles or breach data present."
        else:
            label = f"{GREEN}LOW EXPOSURE{RESET}"
            tip   = "Limited public information found for this identity."
        print(f"  Risk level: {label}")
        print(f"  {DIM}{tip}{RESET}\n")


# ── Terminal formatting helpers ─────────────────────────────────────────────
def _h(title: str, color: str = BOLD):
    w = 67
    bar = "=" * w
    pad = (w - len(title) - 2) // 2
    print(f"\n{color}{bar}")
    print(f"{' ' * pad} {title} {' ' * pad}")
    print(f"{bar}{RESET}\n")

def _section(num: str, title: str):
    print(f"{BOLD}{CYAN}[STEP {num}]{RESET} {BOLD}{title}{RESET}")
    print(f"  {'─' * 55}")

def _conf_bar(score: int) -> str:
    filled = int(score / 10)
    bar = "█" * filled + "░" * (10 - filled)
    color = RED if score >= 70 else YELLOW if score >= 40 else GREEN
    return f"{color}[{bar}]{RESET} {score}%"
