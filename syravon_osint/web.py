from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
from tempfile import NamedTemporaryFile
import hmac
import json
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .core import (
    domain_report,
    ip_report,
    email_domain_report,
    metadata_report,
)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)

MAX_UPLOAD_SIZE = 20 * 1024 * 1024
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE


@app.before_request
def require_basic_auth():
    expected_user = os.environ.get("SYRAVON_USERNAME")
    expected_password = os.environ.get("SYRAVON_PASSWORD")

    if not expected_user or not expected_password:
        app.logger.error("Authentication environment variables are missing.")
        return jsonify({"error": "Service authentication is not configured."}), 503

    supplied = request.authorization
    if (
        supplied is None
        or supplied.type.lower() != "basic"
        or not hmac.compare_digest(supplied.username or "", expected_user)
        or not hmac.compare_digest(supplied.password or "", expected_password)
    ):
        return Response(
            "Authentication required.",
            401,
            {"WWW-Authenticate": 'Basic realm="SYRAVON OSINT", charset="UTF-8"'},
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
@limiter.limit("10 per minute")
def scan():
    try:
        module = request.form.get("module", "").strip()
        target = request.form.get("target", "").strip()

        if module == "metadata":
            uploaded = request.files.get("file") or request.files.get("image")

            if not uploaded or not uploaded.filename:
                return jsonify({"error": "Please select an image."}), 400

            suffix = Path(uploaded.filename).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}:
                return jsonify({"error": "Unsupported image type."}), 400

            temp_path = None
            try:
                data = uploaded.read(MAX_UPLOAD_SIZE + 1)

                if len(data) > MAX_UPLOAD_SIZE:
                    return jsonify({"error": "Image exceeds 20 MB limit."}), 413

                with NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                    temp_file.write(data)
                    temp_path = temp_file.name

                result = metadata_report(temp_path)
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

        else:
            if not target:
                return jsonify({"error": "Target is required."}), 400

            functions = {
                "domain": domain_report,
                "ip": ip_report,
                "email-domain": email_domain_report,
            }

            if module not in functions:
                return jsonify({"error": "Invalid scan module."}), 400

            result = functions[module](target)

        return jsonify({"result": result})

    except (ValueError, OSError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Unexpected scan error")
        return jsonify({"error": "Scan failed. Check server logs."}), 500


@app.route("/api/report", methods=["POST"])
def download_report():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "result" not in data:
        return jsonify({"error": "Invalid report data."}), 400

    report = json.dumps(
        data["result"],
        indent=2,
        ensure_ascii=False,
        default=str
    ).encode("utf-8")

    return send_file(
        __import__("io").BytesIO(report),
        mimetype="application/json",
        as_attachment=True,
        download_name="syravon-osint-report.json"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
