NULLTRACE 🧭

NullTrace is a lightweight OSINT (Open Source Intelligence) tool built in Python for passive digital footprint discovery and identity correlation.

It helps analyze usernames, emails, domains, and online presence using publicly available sources without performing intrusive or active scanning.

The goal of this project is to better understand how OSINT frameworks work internally by building a modular and extensible reconnaissance pipeline.

Features
Username Intelligence

Searches for usernames across multiple public platforms to identify possible digital footprints.

Supported platforms include:

GitHub
Reddit
X
Instagram (basic checks)
TikTok (basic checks)
Custom source modules
Email Intelligence

Performs passive email analysis through:

domain extraction
email format validation
breach correlation (optional API integration)
metadata enrichment
Domain Intelligence

Collects publicly available domain information such as:

DNS records (A, MX, TXT, NS)
WHOIS records
passive subdomain discovery
basic technology fingerprinting
Data Correlation Engine

Correlates collected data points to identify potential relationships between:

usernames ↔ emails
domains ↔ organizations
repeated identifiers across platforms
Export System

Exports results in structured formats:

JSON (default)
CSV
human-readable report mode
Modular Source Architecture

Each OSINT source is implemented as an independent module for easy expansion.

Examples:

sources/github.py
sources/reddit.py
sources/dns.py
sources/whois.py
sources/email_lookup.py
Project Structure
nulltrace/
├── cli.py
├── nulltrace.py
├── README.md
│
├── core/
│   ├── engine.py
│   ├── correlator.py
│   └── resolver.py
│
├── sources/
│   ├── github.py
│   ├── reddit.py
│   ├── dns.py
│   ├── whois.py
│   └── email_lookup.py
│
├── output/
│   ├── json_writer.py
│   └── csv_writer.py
│
└── utils/
    └── validators.py
Installation
Requirements
Python 3.8+

Clone the repository:

git clone https://github.com/yourusername/nulltrace.git
cd nulltrace

Install dependencies:

pip install -r requirements.txt

Check Python version:

python --version

Display help menu:

python nulltrace.py -h
Usage
Username Search
python nulltrace.py username johndoe
Email Analysis
python nulltrace.py email test@example.com
Domain Reconnaissance
python nulltrace.py domain example.com
Full Passive Profile Analysis
python nulltrace.py profile johndoe@example.com
Export Results to CSV
python nulltrace.py username johndoe --format csv
Example Output
{
  "query": "johndoe",
  "results": {
    "github": {
      "found": true,
      "url": "https://github.com/johndoe"
    },
    "reddit": {
      "found": true
    },
    "domain_info": {
      "mx_records": [
        "mail.example.com"
      ]
    },
    "email_association": {
      "possible": false
    }
  }
}
Why I Built This

I created NullTrace to better understand:

OSINT methodologies
passive intelligence gathering
identity correlation
modular reconnaissance pipelines
structured intelligence reporting

This project helped me explore workflows commonly used in cybersecurity investigations, threat intelligence, and reconnaissance operations.

Current Limitations
No real-time scraping of restricted platforms
Limited third-party API integrations
Some sources rely only on public endpoints
No reverse image OSINT
No social graph visualization
Future Improvements

Planned improvements include:

additional OSINT sources
reverse image intelligence
social graph visualization
more breach intelligence integrations
web dashboard interface
Legal Disclaimer

This project is intended strictly for educational purposes and lawful OSINT research.

It does not:

bypass authentication
access private systems
perform intrusive scanning

Users are responsible for complying with applicable laws and platform terms of service.