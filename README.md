# NULLTRACE 🧭

NullTrace is a lightweight OSINT (Open Source Intelligence) tool built in Python for passive digital footprint discovery and identity correlation.

It is designed to help analyze usernames, domains, emails, and online presence across publicly available sources without performing intrusive or active scanning.

The goal is to understand how OSINT frameworks work internally by building a modular, extensible reconnaissance pipeline.

## Features

### Username Intelligence
Searches for a username across multiple public platforms to identify possible associated accounts and digital footprints.
- GitHub
- Reddit
- X (Twitter)
- Instagram (basic check)
- TikTok (basic check)
- Custom source modules

### Email OSINT
Performs passive email analysis:
- domain extraction
- breach correlation (optional API integration)
- format validation
- metadata enrichment

### Domain Intelligence
Collects publicly available domain information:
- DNS records (A, MX, TXT, NS)
- WHOIS lookup
- subdomain discovery (passive sources)
- technology hints (basic fingerprinting)

### Data Correlation Engine
Correlates collected data points to build a unified identity graph:
- username ↔ email matches
- domain ↔ organization mapping
- repeated identifiers across platforms

### Export System
Results can be exported in structured formats:
- JSON (default)
- CSV
- optional report mode (human-readable summary)

### Modular Sources System
Each OSINT source is implemented as a separate module, allowing easy extension:
- `sources/github.py`
- `sources/reddit.py`
- `sources/dns.py`
- `sources/whois.py`

## Installation

Standard (Python 3.8+)
```bash
git clone https://github.com/yourusername/nulltrace.git
cd nulltrace

# Install dependencies
pip install -r requirements.txt
```

Check Python version:
```bash
python --version
```

Run help:
```bash
python nulltrace.py -h
```

## Usage

**Username search**
```bash
python nulltrace.py username johndoe
```

**Email analysis**
```bash
python nulltrace.py email test@example.com
```

**Domain reconnaissance**
```bash
python nulltrace.py domain example.com
```

**Full passive profile**
```bash
python nulltrace.py profile johndoe@example.com
```

**Export to CSV**
```bash
python nulltrace.py username johndoe --format csv
```

## Example Output
```json
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
    "email_association": {
      "possible": false
    }
  }
}
```

## Why I Built This
NullTrace was created to understand:
- OSINT methodologies
- passive data collection techniques
- identity correlation across platforms
- modular reconnaissance system design
- structured intelligence reporting

This project simulates the workflow of OSINT tools used in cybersecurity investigations and threat intelligence analysis.

## Current Limitations
- No real-time scraping of restricted platforms
- Limited API integrations
- Some sources rely on public endpoints only
- No image-based OSINT (reverse image search not implemented)
- No social graph visualization yet

## Legal Disclaimer
This tool is intended for educational and lawful OSINT research only.
It only collects publicly available information and does not:
- bypass authentication
- access private data
- perform intrusive scanning

Users are responsible for complying with applicable laws and platform terms of service.
