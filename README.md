# 🧭 NULLTRACE
> **Professional-grade OSINT framework for passive reconnaissance and identity correlation.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/nulltrace)

**NullTrace** is a modular OSINT tool designed for cybersecurity researchers and threat analysts. It automates the discovery of digital footprints across multiple public vectors, including usernames, emails, domains, and phone numbers.

---

## 📑 Table of Contents
- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Roadmap](#-roadmap)
- [Legal Disclaimer](#-legal-disclaimer)

---

## ✨ Features

### 👤 Username Intelligence
Scans high-authority platforms to identify linked digital identities.
- **Platforms**: GitHub, Reddit, X (Twitter), Instagram, TikTok.
- **Modular**: Easily add new platform scanners in `sources/`.

### 📧 Email Intelligence
Passive analysis of email addresses for risk assessment and breach history.
- **Analysis**: Domain classification (disposable/free), format validation.
- **Breaches**: Integration with XposedOrNot and HIBP.

### 🌐 Domain Intelligence
Comprehensive reconnaissance of domain infrastructure.
- **DNS**: Automated lookup of `A`, `MX`, `TXT`, and `NS` records.
- **WHOIS**: Passive registration data extraction.
- **Footprinting**: Passive subdomain discovery.

### 📞 Phone Intelligence (NEW)
Identifies owners and social presence from phone numbers.
- **Identity**: Extraction via Tellows and Pagine Bianche (Italy).
- **Socials**: Link discovery for WhatsApp, Telegram, and Facebook.
- **Pro**: Authenticated Truecaller integration.

### 🧠 Correlation Engine
Clusters disparate data points into a unified identity profile.
- **Mapping**: Username ↔ Email ↔ Domain ↔ Phone.

---

## 🏗 Project Architecture
```text
nulltrace/
├── core/               # Main logic engine
│   ├── engine.py       # Orchestration
│   ├── correlator.py   # Identity clustering
│   └── resolver.py     # Source management
├── sources/            # Individual OSINT modules
│   ├── github.py
│   ├── phone.py
│   └── email_lookup.py
├── output/             # Export handlers (JSON, CSV)
└── utils/              # Validators and HTTP client
```

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nulltrace.git
cd nulltrace
```

### 2. Setup Environment
```bash
# Install required dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration
Create a `.env` file in the root directory to enable advanced features:

```bash
# HaveIBeenPwned API Key (Optional)
HIBP_API_KEY=your_key_here

# Truecaller Session Token (Optional)
TRUECALLER_TOKEN=your_token_here
```

---

## 🛠 Usage

### 🔍 Quick Scan
Use short flags for fast lookups:
```bash
python nulltrace.py -u johndoe          # Username
python nulltrace.py -e test@gmail.com   # Email
python nulltrace.py -n +390230302400    # Phone
```

### 📊 Full Analysis
```bash
# Full email-to-profile correlation
python nulltrace.py profile target@example.com --correlate --graph
```

---

## 📝 Example Output
```json
{
  "query": "johndoe",
  "results": {
    "github": { "found": true, "url": "https://github.com/johndoe" },
    "phone": { "tellows": { "name": "Apple Store Milano", "score": 2 } }
  }
}
```

---

## 🗺 Roadmap
- [ ] Interactive Web Dashboard
- [ ] Reverse Image Search Integration
- [ ] OSINT Graph Visualization (Force-directed)
- [ ] Dark Web/Pastebin Monitoring

---

## ⚖️ Legal Disclaimer
This tool is for **educational and ethical OSINT research only**. The authors are not responsible for any misuse. Always respect platform Terms of Service and local privacy laws.