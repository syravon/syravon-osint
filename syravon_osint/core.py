import ipaddress
import json
import re
import socket
import ssl
import urllib.error
import urllib.request
import warnings
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

UA = "SYRAVON-OSINT/1.0 (authorized defensive research)"
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000


def stamp():
    return datetime.now(timezone.utc).isoformat()


def clean_domain(value):
    value = value.strip()
    if not value:
        raise ValueError("Enter a fully qualified domain such as example.com.")

    if "://" in value:
        parsed = urlparse(value)
        if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
            raise ValueError("Enter a valid HTTP(S) URL or domain.")
        if parsed.username or parsed.password:
            raise ValueError("URLs containing credentials are not accepted.")
        value = parsed.hostname

    value = value.rstrip(".").lower()
    try:
        ascii_domain = value.encode("idna").decode("ascii")
    except UnicodeError:
        raise ValueError("Invalid internationalized domain name.")

    if len(ascii_domain) > 253 or "." not in ascii_domain:
        raise ValueError("Enter a fully qualified domain such as example.com.")

    labels = ascii_domain.split(".")
    label_pattern = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
    if any(not label_pattern.fullmatch(label) for label in labels):
        raise ValueError("Invalid domain name or hostname label.")

    try:
        ipaddress.ip_address(ascii_domain)
    except ValueError:
        pass
    else:
        raise ValueError("Enter a domain name, not an IP address.")

    return ascii_domain


def dns_records(name, kind):
    try:
        import dns.resolver
    except ImportError:
        return {
            "status": "not_checked",
            "reason": "Install dnspython from requirements.txt",
        }

    try:
        answers = dns.resolver.resolve(name, kind, lifetime=4)
        return {
            "status": "found",
            "records": [str(record).strip('"') for record in answers],
        }
    except Exception as exc:
        return {
            "status": "not_found_or_unavailable",
            "detail": type(exc).__name__,
        }


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Do not follow redirects during a domain header check."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def domain_report(target):
    domain = clean_domain(target)
    out = {
        "tool": "SYRAVON OSINT",
        "version": "1.0.0",
        "generated_at": stamp(),
        "module": "domain",
        "target": domain,
        "authorization_note": "Only assess domains you own or are authorized to test.",
        "dns": {
            record_type: dns_records(domain, record_type)
            for record_type in ("A", "AAAA", "MX", "TXT")
        },
    }

    try:
        addresses = sorted({
            item[4][0]
            for item in socket.getaddrinfo(
                domain, None, proto=socket.IPPROTO_TCP
            )
        })
        out["resolved_addresses"] = addresses
    except socket.gaierror as exc:
        addresses = []
        out["resolved_addresses"] = []
        out["resolution_error"] = type(exc).__name__

    # Avoid making TLS/HTTP connections to domains resolving to non-public IPs.
    public_addresses = []
    for address in addresses:
        try:
            parsed_address = ipaddress.ip_address(address)
            if parsed_address.is_global:
                public_addresses.append(str(parsed_address))
        except ValueError:
            continue

    if not public_addresses:
        out["tls"] = {
            "status": "skipped",
            "detail": "No globally routable IP address was resolved.",
        }
        out["https"] = {
            "status": "skipped",
            "detail": "No globally routable IP address was resolved.",
        }
        return out

    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=4) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=domain) as tls_socket:
                certificate = tls_socket.getpeercert()
                out["tls"] = {
                    "status": "connected",
                    "version": tls_socket.version(),
                    "subject": certificate.get("subject"),
                    "issuer": certificate.get("issuer"),
                    "not_after": certificate.get("notAfter"),
                }
    except Exception as exc:
        out["tls"] = {
            "status": "unavailable",
            "detail": type(exc).__name__,
        }

    try:
        request = urllib.request.Request(
            "https://" + domain,
            headers={
                "User-Agent": UA,
                "Accept": "*/*",
                "Accept-Encoding": "identity",
                "Connection": "close",
                # Ask for only the first byte where supported. The response
                # body is never read; the connection is closed after headers.
                "Range": "bytes=0-0",
            },
            method="GET",
        )
        opener = urllib.request.build_opener(NoRedirectHandler)
        with opener.open(request, timeout=15) as response:
            header_names = (
                "Server",
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Content-Type-Options",
                "X-Frame-Options",
                "Referrer-Policy",
            )
            out["https"] = {
                "status": response.status,
                "final_url": response.geturl(),
                "headers": {
                    name: response.headers.get(name) for name in header_names
                },
            }
    except urllib.error.HTTPError as exc:
        # A redirect is reported, not followed.
        if exc.code in (301, 302, 303, 307, 308):
            out["https"] = {
                "status": exc.code,
                "detail": "Redirect not followed by safety policy.",
                "location": exc.headers.get("Location"),
            }
        else:
            out["https"] = {
                "status": "unavailable",
                "detail": type(exc).__name__,
                "http_status": exc.code,
            }
    except Exception as exc:
        out["https"] = {
            "status": "unavailable",
            "detail": type(exc).__name__,
        }

    # Summarize common defensive security headers. A failed/skipped HTTPS
    # request is reported as not_checked, not as missing.
    header_labels = {
        "Strict-Transport-Security": "HSTS",
        "Content-Security-Policy": "CSP",
        "X-Frame-Options": "X-Frame-Options",
        "X-Content-Type-Options": "X-Content-Type-Options",
        "Referrer-Policy": "Referrer-Policy",
    }
    https_result = out.get("https", {})
    if isinstance(https_result.get("status"), int):
        response_headers = https_result.get("headers", {})
        out["security_headers"] = {
            label: {
                "status": "present" if response_headers.get(header) else "missing",
                "value": response_headers.get(header),
            }
            for header, label in header_labels.items()
        }
    else:
        out["security_headers"] = {
            label: {"status": "not_checked", "value": None}
            for label in header_labels.values()
        }

    checked_headers = [
        item for item in out["security_headers"].values()
        if item["status"] in ("present", "missing")
    ]
    if checked_headers:
        present_count = sum(
            item["status"] == "present" for item in checked_headers
        )
        total_count = len(checked_headers)
        if present_count == total_count:
            assessment = "Good header coverage"
        elif present_count >= 3:
            assessment = "Some headers need review"
        else:
            assessment = "Review recommended"

        out["security_summary"] = {
            "headers_present": present_count,
            "headers_checked": total_count,
            "score_percent": round((present_count / total_count) * 100),
            "assessment": assessment,
            "scope_note": (
                "This is a presence check for these five response headers only; "
                "it is not a complete website security score or vulnerability assessment."
            ),
        }
    else:
        out["security_summary"] = {
            "status": "not_checked",
            "assessment": "Security headers could not be assessed because no HTTP response was available.",
            "scope_note": (
                "This is a presence check for five response headers only; "
                "it is not a complete website security score or vulnerability assessment."
            ),
        }

    return out


def ip_report(target):
    try:
        ip = ipaddress.ip_address(target.strip())
    except ValueError:
        raise ValueError("Enter a valid IPv4 or IPv6 address.")

    out = {
        "tool": "SYRAVON OSINT",
        "version": "1.0.0",
        "generated_at": stamp(),
        "module": "ip",
        "target": str(ip),
        "classification": {
            "version": ip.version,
            "is_global": ip.is_global,
            "is_private": ip.is_private,
            "is_loopback": ip.is_loopback,
            "is_multicast": ip.is_multicast,
            "is_reserved": ip.is_reserved,
        },
    }

    if not ip.is_global:
        out["reverse_dns"] = None
        out["rdap"] = {
            "status": "skipped",
            "detail": "RDAP lookup is only performed for globally routable IPs.",
        }
    else:
        try:
            out["reverse_dns"] = socket.gethostbyaddr(str(ip))[0]
        except (socket.herror, socket.gaierror):
            out["reverse_dns"] = None

        try:
            request = urllib.request.Request(
                f"https://rdap.org/ip/{ip}",
                headers={"User-Agent": UA},
            )
            with urllib.request.urlopen(request, timeout=6) as response:
                data = json.loads(
                    response.read(500_000).decode("utf-8", "replace")
                )
            fields = (
                "name",
                "handle",
                "country",
                "startAddress",
                "endAddress",
                "type",
                "status",
            )
            out["rdap"] = {key: data.get(key) for key in fields}
        except Exception as exc:
            out["rdap"] = {
                "status": "unavailable",
                "detail": type(exc).__name__,
            }

    out["note"] = (
        "RDAP data can be redacted or incomplete; it does not identify an end user."
    )
    return out


def email_domain_report(target):
    value = target.strip()
    if "@" in value:
        local_part, domain = value.rsplit("@", 1)
        if (
            not local_part
            or len(local_part) > 64
            or any(character.isspace() for character in local_part)
        ):
            raise ValueError("Enter a valid email address or domain.")
    else:
        domain = value

    domain = clean_domain(domain)
    txt_result = dns_records(domain, "TXT")
    txt_records = txt_result.get("records", [])
    spf_records = [
        record for record in txt_records
        if record.lower().startswith("v=spf1")
    ]

    dmarc_result = dns_records("_dmarc." + domain, "TXT")
    dmarc_records = dmarc_result.get("records", [])
    dmarc_found = any(
        record.lower().startswith("v=dmarc1")
        for record in dmarc_records
    )

    return {
        "tool": "SYRAVON OSINT",
        "version": "1.0.0",
        "generated_at": stamp(),
        "module": "email-domain",
        "target_domain": domain,
        "mx": dns_records(domain, "MX"),
        "spf": {
            "status": "found" if spf_records else "not_found",
            "records": spf_records,
        },
        "dmarc": {
            "status": "found" if dmarc_found else "not_found",
            "records": dmarc_records,
        },
        "note": (
            "Domain-level mail configuration only; does not verify a mailbox "
            "or identify its owner."
        ),
    }


def metadata_report(target):
    path = Path(target).expanduser()
    if not path.is_file():
        raise ValueError(
            "File not found; provide a file you are authorized to inspect."
        )

    file_size = path.stat().st_size
    if file_size > MAX_IMAGE_BYTES:
        raise ValueError(
            f"Image exceeds the {MAX_IMAGE_BYTES // (1024 * 1024)} MB size limit."
        )

    out = {
        "tool": "SYRAVON OSINT",
        "version": "1.0.0",
        "generated_at": stamp(),
        "module": "metadata",
        "file_name": path.name,
        "file_size_bytes": file_size,
        "note": "Metadata may contain sensitive information; review before sharing.",
    }

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS

        # Treat Pillow's decompression-bomb warning as an error.
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(path) as image:
                width, height = image.size
                if width <= 0 or height <= 0:
                    raise ValueError("Invalid image dimensions.")
                if width * height > MAX_IMAGE_PIXELS:
                    raise ValueError("Image dimensions exceed the safety limit.")

                out["image"] = {
                    "format": image.format,
                    "size": [width, height],
                    "mode": image.mode,
                }
                out["exif"] = {
                    TAGS.get(tag_id, str(tag_id)): str(value)[:500]
                    for tag_id, value in image.getexif().items()
                }
    except ImportError:
        out["metadata_status"] = "Install Pillow from requirements.txt"
    except Exception as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("Image "):
            raise
        out["metadata_status"] = "No supported image metadata found"
        out["detail"] = type(exc).__name__

    return out
