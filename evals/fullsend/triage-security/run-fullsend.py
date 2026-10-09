#!/usr/bin/env python3
"""Opaque CLI adapter: delegate one synthetic case to native Fullsend unchanged."""

import argparse
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

import yaml


def run_case(root, workspace, output, scenario, model, effort, host_binary, sandbox_binary, plugin_root=None):
    """Stage test-only resources, call native CLI once, preserve its actual exit."""
    if scenario not in {"absent", "empty", "malformed", "valid", "release"}:
        raise ValueError("Unknown synthetic gate scenario")
    if os.environ.get("FULLSEND_MINT_URL"):
        raise ValueError("Synthetic suite requires FULLSEND_MINT_URL unset; live forge minting is forbidden")
    setup = workspace / "native-config"
    target = workspace / "synthetic-target"
    native = output / "native"
    if any(p.exists() for p in [setup, target, native, output / "metrics.json"]):
        raise ValueError("Refusing stale native configuration or output")
    suite = root / "evals/fullsend/triage-security"
    h = yaml.safe_load((suite / "harness.yaml").read_text())
    # PR content is only uploaded as a sandbox plugin. Trusted host executables,
    # policy, providers and schema remain independent even if the PR replaces them.
    plugin_root = plugin_root or root / "plugins/sdlc-workflow"
    plugin_root = plugin_root.absolute()
    if (any(p.is_symlink() for p in [plugin_root, *plugin_root.parents])
            or any(p.is_symlink() for p in plugin_root.rglob("*"))):
        raise ValueError("Tested plugin must contain regular files, not symlinks")
    plugin_destination = setup / ("tested-plugin" if plugin_root != root / "plugins/sdlc-workflow" else "plugins/sdlc-workflow")
    shutil.copytree(plugin_root, plugin_destination,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if plugin_destination == setup / "tested-plugin":
        for name in ["policies/triage-security.yaml", "providers/vertex-ai.yaml", "profiles/fullsend-vertex-ai.yaml",
                     "env/gcp-vertex.env", "schemas/triage-security-result.schema.json",
                     "scripts/validate-output-schema.sh", "scripts/strip_extra_properties.py"]:
            destination = setup / "plugins/sdlc-workflow" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / "plugins/sdlc-workflow" / name, destination)
    staged_suite = setup / "evals/fullsend/triage-security"
    staged_suite.mkdir(parents=True)
    for name in ["agent.md", "prepare-fixture.py"]:
        shutil.copy2(suite / name, staged_suite / name)
    staged_fixtures = setup / "evals/triage-security/files"
    staged_fixtures.mkdir(parents=True)
    for name in ["fullsend-gate-interactive-config.md", "fullsend-invalid-trusted-input.md",
                 "fullsend-report-only-trusted-input.json"]:
        shutil.copy2(root / "evals/triage-security/files" / name, staged_fixtures / name)
    if scenario == "release":
        name = "fullsend-release-trusted-input.json"
        shutil.copy2(root / "evals/triage-security/files" / name, staged_fixtures / name)
    for field in ["agent", "policy", "pre_script"]:
        h[field] = str(setup / h[field])
    h["plugins"] = [str(plugin_destination)]
    for field in ["providers"]:
        h[field] = [str(setup / p) for p in h[field]]
    h["openshell"]["profiles"] = [str(setup / p) for p in h["openshell"]["profiles"]]
    for field in ["script", "schema"]:
        h["validation_loop"][field] = str(setup / h["validation_loop"][field])
    h["host_files"][0]["src"] = str(setup / h["host_files"][0]["src"])
    if os.environ.get("GCP_OIDC_TOKEN_FILE"):
        token = Path(os.environ["GCP_OIDC_TOKEN_FILE"])
        if not token.is_file():
            raise ValueError("Missing prepared sandbox OIDC token")
        h["host_files"].append({"src": str(token), "dest": "/sandbox/workspace/.gcp-oidc-token"})
    h["env"]["runner"]["TC6677_SCENARIO"] = scenario
    h["env"]["runner"]["TC6677_REPO_ROOT"] = str(setup)
    h["env"]["runner"]["FULLSEND_OUTPUT_SCHEMA"] = str(setup / "plugins/sdlc-workflow/schemas/triage-security-result.schema.json")
    (setup / "harness").mkdir(parents=True)
    (setup / "harness/triage-security-gate.yaml").write_text(yaml.safe_dump(h, sort_keys=False))
    (setup / "config.yaml").write_text(yaml.safe_dump({
        "version": "1", "runtime": "claude",
        "agents": [{"source": "harness/triage-security-gate.yaml"}],
    }, sort_keys=False))
    target.mkdir()
    # Native UploadDir retains .git; read-only setup requires it, not a commit.
    subprocess.run(["git", "init", "--quiet", str(target)], check=True)
    if scenario == "absent":
        shutil.copy2(root / "evals/triage-security/files/fullsend-gate-interactive-config.md", target / "CLAUDE.md")
    output.mkdir(parents=True, exist_ok=True)
    native.mkdir()
    command = [str(host_binary), "run", "triage-security-gate", "--fullsend-dir", str(setup),
               "--target-repo", str(target), "--output-dir", str(native),
               "--fullsend-binary", str(sandbox_binary), "--runtime", "claude",
               "--model", model, "--effort", effort, "--no-post-script"]
    # Stdout/stderr go directly to CliRunner; no nested inference or env rewriting.
    environment = dict(os.environ)
    if os.environ.get("TC6726_SANDBOX_CREDENTIALS"):
        credential = Path(os.environ["TC6726_SANDBOX_CREDENTIALS"])
        if not credential.is_file():
            raise ValueError("Missing prepared sandbox credential")
        environment["GOOGLE_APPLICATION_CREDENTIALS"] = str(credential)
    # Judge processes keep original host ADC; only native Fullsend gets prepared
    # sandbox ADC. Its reserved OIDC refresh variables remain host-only upstream.
    process = subprocess.run(command, cwd=workspace, env=environment, check=False)
    metrics = list(native.glob("agent-*/metrics.json"))
    if len(metrics) == 1:
        shutil.copy2(metrics[0], output / "metrics.json")
    elif len(metrics) > 1:
        print("Ambiguous native metrics; originals retained, no root copy selected", file=sys.stderr)
    return process.returncode


def main():
    """Accept the upstream opaque CLI placeholders, not fixture-generated code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["triage-security-gate"], required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scenario", choices=["absent", "empty", "malformed", "valid", "release"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--plugin-root", type=Path)
    args = parser.parse_args()
    try:
        return run_case(Path(__file__).resolve().parents[3], args.workspace.resolve(),
                        args.output_dir.resolve(), args.scenario, args.model, args.effort,
                        Path(os.environ["TC6677_FULLSEND_BIN"]),
                        Path(os.environ["TC6677_SANDBOX_FULLSEND_BIN"]),
                        args.plugin_root.absolute() if args.plugin_root else None)
    except (KeyError, OSError, ValueError) as exc:
        print(f"Native gate eval fixture/CLI failure: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    status = main()
    if status < 0:
        # Python sys.exit(-signal) wraps it modulo256; preserve the native signal.
        if -status not in {signal.SIGKILL, signal.SIGSTOP}:
            signal.signal(-status, signal.SIG_DFL)
        os.kill(os.getpid(), -status)
    sys.exit(status)
