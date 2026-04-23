BANNER = r"""
███╗   ██╗██╗   ██╗██╗     ██╗     ████████╗██████╗  █████╗  ██████╗███████╗
████╗  ██║██║   ██║██║     ██║     ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
██╔██╗ ██║██║   ██║██║     ██║        ██║   ██████╔╝███████║██║     █████╗
██║╚██╗██║██║   ██║██║     ██║        ██║   ██╔══██╗██╔══██║██║     ██╔══╝
██║ ╚████║╚██████╔╝███████╗███████╗   ██║   ██║  ██║██║  ██║╚██████╗███████╗
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

        [ OSINT ENGINE :: EMAIL | USERNAME | DOMAIN | LEAKS ]

=====================================================================
  > uncover identities
  > correlate digital footprints
  > map public exposure
=====================================================================

[MODULES]

[1] EMAIL MODULE
    ├─ breach lookup
    ├─ domain extraction
    ├─ provider analysis
    └─ pattern generation

[2] USERNAME MODULE
    ├─ github enumeration
    ├─ reddit lookup
    ├─ social discovery
    └─ profile correlation

[3] DOMAIN MODULE
    ├─ whois lookup
    ├─ dns records
    ├─ subdomain enum
    └─ certificate logs

[4] LEAK MODULE
    ├─ public breach search
    ├─ paste lookup
    ├─ metadata extraction
    └─ risk scoring

[5] CORRELATION ENGINE
    ├─ identity clustering
    ├─ graph mapping
    ├─ confidence scoring
    └─ report generation

=====================================================================

USAGE:

python nulltrace.py username johndoe
python nulltrace.py email test@gmail.com
python nulltrace.py domain example.com
python nulltrace.py profile target@example.com

=====================================================================
              NULLTRACE | No User Logged Locally
=====================================================================
"""

import sys

def print_banner():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    print(BANNER)
