# 🛡️ SYRAVON OSINT Toolkit

### A Python-Based Open Source Intelligence Toolkit with CLI & Web Interface

<p align="center">
  <img src="syravon-logo.png" alt="SYRAVON OSINT Logo" width="180">
</p>

<p align="center">
  <a href="https://syravon-osint.onrender.com/"><strong>🚀 Launch Live Web App</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Web-Flask-black" alt="Flask">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/Version-1.0.0-blueviolet" alt="Version">
</p>

---

## 🌐 Live Web Application

Try SYRAVON OSINT directly from your browser:

### 👉 https://syravon-osint.onrender.com/

The web interface allows users to:
- Select an OSINT scanning module.
- Enter a target or upload a supported file.
- Run scans through the web interface.
- View structured scan results.
- Download JSON reports.

*Note: The free hosting service may take a short time to wake up after inactivity.*

---

## 📖 About

**SYRAVON OSINT** is a Python-based defensive Open Source Intelligence (OSINT) toolkit developed by **SYRAVON Cybersecurity**.

It collects basic technical information from public-facing domains and IP addresses, checks domain-level email security configuration, and extracts metadata from user-provided files and images.

The project provides both a Command-Line Interface (CLI) and a Flask-based Web Interface.

Use this toolkit only on systems, domains, IP addresses, email domains, and files that you own or are explicitly authorized to assess.

---

## ✨ Features

### 1. 🌍 Domain Reconnaissance
- DNS record lookup: A, AAAA, MX, and TXT
- TLS certificate information
- HTTPS response status
- Selected HTTP security headers
- Security-header presence checks:
  - HTTP Strict Transport Security (HSTS)
  - Content Security Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy

### 2. 🌐 IP Intelligence
- IP address classification
- Public, private, and reserved address indicators
- Reverse DNS lookup
- Basic network and allocation information when available

### 3. 📧 Email Domain Security
- MX record inspection
- SPF record lookup
- DMARC record lookup
- Domain-level email security configuration checks

*These checks inspect public DNS configuration. They do not verify mailbox existence or guarantee email deliverability.*

### 4. 🖼️ File Metadata Inspection
- Extract metadata from supported image and file inputs
- Inspect image properties and available EXIF information
- Generate structured JSON reports

---

## 🖥️ Interfaces

### Command-Line Interface (CLI)

Run reconnaissance modules directly from your terminal.

### Web Interface

Use the online or locally hosted Flask web interface to:
- Select a scanning module
- Enter a target or upload a supported file
- View scan results
- Download JSON reports

---

## ⚙️ Installation

### Requirements
- Python 3.11 or newer
- Git
- Internet connection for network-based scans

### 1. Clone the Repository

```bash
git clone https://github.com/syravon/syravon-osint.git
cd syravon-osint
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / Kali Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 Run the Web Interface Locally

**Linux / Kali Linux:**

```bash
chmod +x run-web.sh
./run-web.sh
```

The local web interface runs at:

```text
http://127.0.0.1:5000
```

For deployment with Gunicorn:

```bash
gunicorn syravon_osint.web:app
```

---

## 📦 Project Structure

```text
syravon-osint/
│
├── .github/
│   └── workflows/
│
├── syravon_osint/
│   └── web.py
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run-web.sh
└── syravon-logo.png
```

---

## 📊 Reports

SYRAVON OSINT provides structured JSON scan reports.

Reports include available scan results, target information, module details, and generation timestamps.

The Web Interface provides a JSON report download option.

---

## ☁️ Deployment

The Web Interface is deployed using **Render**.

- Hosting: Render
- Framework: Flask
- Production server: Gunicorn
- Source repository: GitHub

**Live URL:** https://syravon-osint.onrender.com/

---

## 🔐 Responsible Use & Disclaimer

SYRAVON OSINT is intended for educational, defensive cybersecurity, and authorized security assessment purposes.

- Only scan targets you own or have explicit permission to assess.
- Do not use this tool for unauthorized reconnaissance.
- Public DNS and network information may be incomplete or outdated.
- Results are informational and should be independently verified.
- The developer is not responsible for misuse or damage resulting from unauthorized use.

---

## 🧪 Testing

The project has been tested on:
- Kali Linux
- Windows

Cross-platform checks are also configured through GitHub Actions.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**SYRAVON Cybersecurity**

GitHub: https://github.com/syravon

Project: https://github.com/syravon/syravon-osint

Live Web App: https://syravon-osint.onrender.com/

---

<p align="center">
  <strong>SYRAVON OSINT — Intelligence. Security. Awareness.</strong>
</p>

<p align="center">
  Made with ❤️ by SYRAVON Cybersecurity
</p>
