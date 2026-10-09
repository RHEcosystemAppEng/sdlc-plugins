#!/usr/bin/env python3
"""SYNTHETIC TEST DATA — native pre-script; no live prefetch or triage logic."""

import os
from pathlib import Path
import sys


def prepare(root, scenario):
    """Prepare only host mounts; Fullsend sources the fragment before inference."""
    if scenario not in {"absent", "empty", "malformed", "valid", "release"}:
        raise ValueError("Unknown synthetic gate scenario")
    fixtures = root / "evals/triage-security/files"
    pre = root / "pre"
    # This is the case-private native-config root, not Fullsend's output run dir.
    # Native resolution binds the generated mounts here; never reuse old mounts.
    if pre.exists() and any(pre.iterdir()):
        raise ValueError("Refusing stale pre-script fixture files")
    pre.mkdir(parents=True, exist_ok=True)
    fragment = "# SYNTHETIC TEST DATA — deliberate native gate condition injection\n"
    if scenario == "absent":
        fragment += "unset FULLSEND_OUTPUT_DIR\n"
    elif scenario == "empty":
        fragment += "export FULLSEND_OUTPUT_DIR=''\n"
    if scenario in {"malformed", "valid", "release"}:
        name = "fullsend-invalid-trusted-input.md" if scenario == "malformed" else "fullsend-report-only-trusted-input.json"
        if scenario == "release":
            name = "fullsend-release-trusted-input.json"
        data = (fixtures / name).read_bytes()
        if scenario == "malformed":
            data = data.split(b"```json\n", 1)[1].split(b"\n```", 1)[0]
        (pre / "triage-security-input.json").write_bytes(data)
    (pre / "tc-6677-gate.env").write_text(fragment)


def main():
    """Consume the native trusted pre-script environment without exposing it."""
    try:
        prepare(Path(os.environ["TC6677_REPO_ROOT"]), os.environ["TC6677_SCENARIO"])
    except (KeyError, OSError, ValueError, IndexError) as exc:
        print(f"Synthetic gate fixture preparation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
