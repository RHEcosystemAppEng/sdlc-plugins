#!/usr/bin/env python3
"""Compute SHA-256 digest for the description-digest protocol.

Accepts both ADF JSON and plain text (markdown). Outputs a format-tagged
digest so the consumer knows which representation was hashed.

  ADF JSON input  → sha256-adf:<64-char-hex>
  Plain text input → sha256-md:<64-char-hex>
"""

import hashlib
import json
import sys


def compute_adf_digest(raw: str) -> str:
    """Parse JSON input, re-serialize with compact separators, and return the SHA-256 hex digest."""
    parsed = json.loads(raw)
    normalized = json.dumps(parsed, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def compute_text_digest(raw: str) -> str:
    """Strip leading/trailing whitespace and return the SHA-256 hex digest."""
    return hashlib.sha256(raw.strip().encode("utf-8")).hexdigest()


def main() -> int:
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                raw = f.read()
        else:
            raw = sys.stdin.read()

        if not raw.strip():
            print("error: empty input", file=sys.stderr)
            return 1

        try:
            digest = compute_adf_digest(raw)
            print(f"sha256-adf:{digest}")
        except json.JSONDecodeError:
            digest = compute_text_digest(raw)
            print(f"sha256-md:{digest}")

        return 0

    except FileNotFoundError:
        print(f"error: file not found: {sys.argv[1]}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
