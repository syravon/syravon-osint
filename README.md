# SYRAVON OSINT Toolkit

**Version:** 1.0.0  
**Project:** SYRAVON Cybersecurity  
**Type:** Defensive, public-source OSINT command-line toolkit

SYRAVON OSINT is a Python-based CLI tool for collecting basic technical information from public-facing domains and IP addresses, checking domain-level email configuration, and inspecting metadata in image files supplied by the user.

> Use the toolkit only for systems, domains, IP addresses, email domains, and files that you own or have explicit permission to assess.

## Features

### 1. Domain reconnaissance
- DNS records: A, AAAA, MX, and TXT
- TLS certificate summary
- HTTPS response status and selected security-related response headers
- Security-header presence checks for:
  - HTTP Strict Transport Security (HSTS)
  - Content Security Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy

Header checks are informational. A missing header is not, by itself, proof of an exploitable vulnerability.

### 2. IP address lookup
- IP address classification
- Reverse DNS lookup
- Public RDAP registration summary

RDAP lookups are limited to globally routable public IP addresses. Private, loopback, link-local, and other non-global addresses are not sent for public RDAP lookup.

### 3. Email-domain checks
- MX record lookup
- SPF record check
- DMARC record check

These are domain-level configuration checks. The tool does not verify individual mailboxes or send email.

### 4. Image metadata inspection
- Basic image information
- Available EXIF metadata from a user-provided image

Only inspect files you own or are authorized to examine.

### 5. JSON reports
Export supported scan results to a JSON file using `--json`.

## Requirements

- Python 3.10 or newer
- pip
- Internet access for DNS, RDAP, and domain TLS/HTTPS lookups

## Installation

Clone the repository:

```bash
git clone https://github.com/syravon/syravon-osint.git
cd syravon-osint
```

Create and activate a virtual environment.

**Kali Linux / Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Show available commands:

```bash
python -m syravon_osint --help
```

Check a domain you are authorized to assess:

```bash
python -m syravon_osint domain example.com
```

Look up a public IP address:

```bash
python -m syravon_osint ip 8.8.8.8
```

Check email-domain DNS configuration:

```bash
python -m syravon_osint email-domain example.com
```

Inspect an image file:

```bash
python -m syravon_osint metadata ./image.jpg
```

Export a domain report as JSON:

```bash
python -m syravon_osint domain example.com --json domain-report.json
```

Replace the example domain, IP address, and image path with values you are authorized to assess.

## Responsible use and limitations

- Obtain permission before running domain or IP checks against systems you do not own.
- The toolkit performs basic information gathering; it is not a penetration-testing or vulnerability-exploitation framework.
- It does not exploit vulnerabilities, access private accounts, track people, locate phones, or discover passwords.
- Public RDAP data can be incomplete, inaccurate, or redacted.
- DNS, TLS, and HTTPS results can vary with network conditions, DNS configuration, and server behavior.
- Security-header checks cover only the selected response headers. They are not a complete website security audit or a vulnerability score.
- Image metadata may be absent, stripped, or incomplete.

## Project structure

```text
syravon-osint/
├── syravon_osint/
│   ├── __init__.py
│   ├── __main__.py
│   └── core.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Roadmap

Planned future work may include:
- A web interface for running authorized checks
- A separately hosted backend for Python-based scanning
- Improved report presentation and additional defensive checks

GitHub Pages can host static website content, but it cannot directly execute this Python CLI. A future web interface will therefore require a suitable backend service.

## License

See [LICENSE](LICENSE) for the terms of use.
