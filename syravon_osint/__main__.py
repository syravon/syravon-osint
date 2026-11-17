import argparse, json, sys
from pathlib import Path
from .core import domain_report, ip_report, email_domain_report, metadata_report

BANNER = """
  ____  __   ____ ____   ___  _   _  ___  _   _
 / ___| \\ \\ / /  _|  _ \\ / _ \\| \\ | |/ _ \\| \\ | |
 \\___ \\  \\ V /| | | |_) | | | |  \\| | | | |  \\| |
  ___) |  | | | |_|  _ <| |_| | |\\  | |_| | |\\  |
 |____/   |_| |___|_| \\_\\\\___/|_| \\_|\\___/|_| \\_|

             SYRAVON OSINT  v1.0.0
"""

def main():
    parser = argparse.ArgumentParser(prog="syravon-osint",
        description="Public-source OSINT checks for authorized defensive use.")
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd, help_text in [
        ("domain", "DNS, HTTPS headers and TLS summary"),
        ("ip", "IP classification, reverse DNS and RDAP"),
        ("email-domain", "MX, SPF and DMARC checks"),
        ("metadata", "Inspect metadata in a user-provided image")]:
        p = sub.add_parser(cmd, help=help_text)
        p.add_argument("target")
        p.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    print(BANNER)
    try:
        fn = {"domain": domain_report, "ip": ip_report,
              "email-domain": email_domain_report, "metadata": metadata_report}[args.command]
        result = fn(args.target)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        if args.json_path:
            Path(args.json_path).write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
            print(f"\\n[+] JSON report saved: {args.json_path}")
    except (ValueError, OSError) as exc:
        print(f"[!] Error: {exc}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
