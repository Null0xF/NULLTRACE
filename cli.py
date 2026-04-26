import argparse

from core.banner import BANNER

def setup_cli():
    parser = argparse.ArgumentParser(
        description=BANNER,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nulltrace.py username johndoe
  python nulltrace.py email test@gmail.com
  python nulltrace.py email test@gmail.com --correlate
  python nulltrace.py domain google.com
  python nulltrace.py profile target@example.com

Pro flags:
  --correlate   Deep correlation: breach + username prediction + profile search + clustering
  --graph       Generate interactive HTML graph of findings
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Target type to analyze")
    
    # Add short flags for quick access (as seen in banner)
    parser.add_argument("-u", "--user",         dest="short_user",    help="Analyze a username")
    parser.add_argument("-e", "--email-addr",   dest="short_email",   help="Analyze an email")
    parser.add_argument("-d", "--domain-name",  dest="short_domain",  help="Analyze a domain")
    parser.add_argument("-p", "--profile-addr", dest="short_profile", help="Analyze a full profile (email)")
    parser.add_argument("-n", "--phone-num",    dest="short_phone",   help="Analyze a phone number")
    parser.add_argument("--correlate", action="store_true", default=False,
                        help="[PRO] Deep correlation: breach + username prediction + profile search + clustering")
    parser.add_argument("--graph",     action="store_true", default=False,
                        help="[PRO] Generate an interactive HTML OSINT graph")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    # Username command (subparser style)
    user_parser = subparsers.add_parser("username", aliases=['u'], help="Analyze a username across platforms")
    user_parser.add_argument("target", help="Username to search for")
    user_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    # Email command
    email_parser = subparsers.add_parser("email", aliases=['e'], help="Perform passive email analysis")
    email_parser.add_argument("target", help="Email address to analyze")
    email_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    email_parser.add_argument("--correlate", action="store_true", default=False,
                              help="[PRO] Full deep correlation for this email")
    email_parser.add_argument("--graph",     action="store_true", default=False,
                              help="[PRO] Generate interactive OSINT graph")
    
    # Domain command
    domain_parser = subparsers.add_parser("domain", aliases=['d'], help="Perform domain reconnaissance")
    domain_parser.add_argument("target", help="Domain to analyze")
    domain_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    # Profile command
    profile_parser = subparsers.add_parser("profile", aliases=['p'], help="Full passive profile (requires email address)")
    profile_parser.add_argument("target", help="Email address to build a profile from")
    profile_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    # Phone command
    phone_parser = subparsers.add_parser("phone", aliases=['n'], help="Analyze a phone number for identity and accounts")
    phone_parser.add_argument("target", help="Phone number to analyze (e.g. +39021234567)")
    phone_parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    return parser.parse_args()
