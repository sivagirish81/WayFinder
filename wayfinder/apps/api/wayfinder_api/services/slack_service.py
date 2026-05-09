import hashlib
import hmac
import time


def validate_slack_signature(signing_secret: str, timestamp: str, body: bytes, signature: str) -> bool:
    if not signing_secret:
        return False
    if abs(time.time() - int(timestamp or "0")) > 60 * 5:
        return False
    basestring = b"v0:" + timestamp.encode() + b":" + body
    digest = hmac.new(signing_secret.encode(), basestring, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"v0={digest}", signature)


def parse_wayfinder_command(text: str) -> str | None:
    lowered = text.lower()
    if "/wayfinder" in lowered:
        return text.split("/wayfinder", 1)[-1].strip()
    if "wayfinder" in lowered and "plan" in lowered:
        return text
    return None
