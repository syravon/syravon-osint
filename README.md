# SYRAVON OSINT Toolkit
Version 1.0.0 — defensive public-source OSINT CLI.

## Modules
- `domain`: DNS A/AAAA/MX/TXT, HTTPS response headers, TLS certificate summary.
- `ip`: IP classification, reverse DNS, public RDAP registration summary.
- `email-domain`: MX, SPF and DMARC checks (domain-level only).
- `metadata`: inspect metadata in a user-provided image file.
- JSON report export with `--json report.json`.

## Responsible use
Use only on domains, IPs, email domains, and files you own or are authorized to assess. This tool does not exploit vulnerabilities, access private accounts, track people, locate phones, or discover passwords. Public registration data may be incomplete or redacted. HTTP/TLS checks connect to the supplied domain; obtain authorization first.

## Install
Python 3.10+
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Usage
```bash
python -m syravon_osint --help
python -m syravon_osint domain example.com
python -m syravon_osint ip 8.8.8.8
python -m syravon_osint email-domain example.com
python -m syravon_osint metadata ./image.jpg
python -m syravon_osint domain example.com --json domain-report.json
```

GitHub Pages cannot run Python scans. The future web UI will need a separately hosted backend.
