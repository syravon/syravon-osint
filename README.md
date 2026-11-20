# SYRAVON OSINT Toolkit

**A Python-based Open Source Intelligence toolkit with CLI and Web Interface.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Web-Flask-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

SYRAVON OSINT is a defensive OSINT toolkit designed to collect basic technical information from public-facing domains and IP addresses, inspect domain-level email security configuration, and extract metadata from user-provided files and images.

Use this toolkit only on systems, domains, IP addresses, email domains, and files that you own or are explicitly authorized to assess.

## Features

### 1. Domain Reconnaissance
- DNS records: A, AAAA, MX, and TXT
- TLS certificate summary
- HTTPS response status
- Selected security-related HTTP response headers
- Security-header presence checks:
  - HTTP Strict Transport Security (HSTS)
  - Content Security Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy

### 2. IP Intelligence
- IP address classification
- Public/private and reserved address indicators
- Reverse DNS lookup
- Basic network and allocation information when available

### 3. Email Domain Security
- MX record inspection
- SPF record lookup
- DMARC record lookup
- Domain-level email security configuration checks

*These checks inspect public DNS configuration. They do not verify mailbox existence or guarantee email deliverability.*

### 4. File Metadata Inspection
- Extract metadata from supported image and file inputs
- Inspect image properties and available EXIF information
- Generate structured JSON reports

## Interfaces

### Command-Line Interface (CLI)
Run reconnaissance modules directly from your terminal.

### Web Interface
Use the Flask-based web interface to:
- Select a scanning module
- Enter a target or upload a supported file
- View scan results
- Download JSON reports

## Installation

```bash
git clone https://github.com/syravon/syravon-osint.git
cd syravon-osint

python -m venv .venv
```

Activate the virtual environment:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / Kali**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Web Interface

```bash
python -m syravon_osint.web
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## Deployment

The web application can be deployed on compatible Python hosting platforms using:

**Build command**
```bash
pip install -r requirements.txt
```

**Start command**
```bash
gunicorn syravon_osint.web:app
```

## Project Structure

```text
syravon-osint/
├── .github/
│   └── workflows/
├── syravon_osint/
├── README.md
├── LICENSE
├── requirements.txt
└── run-web.sh
```

## Responsible Use

SYRAVON OSINT is intended for educational, defensive, and authorized security assessment purposes.

- Scan only authorized targets.
- Respect privacy, applicable laws, and service terms.
- Do not use the toolkit to access systems without permission.
- Results are informational and may be incomplete or change over time.

## Limitations

- DNS and network information depends on publicly available records and service responses.
- IP geolocation and allocation data may be incomplete or unavailable.
- Security-header checks are informational and do not constitute a full security audit.
- Metadata availability depends on the uploaded file and the metadata embedded in it.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

**SYRAVON Cybersecurity**

GitHub: [@syravon](https://github.com/syravon)

---

**SYRAVON OSINT — Open Source Intelligence Toolkit**
