#!/usr/bin/env python3
# SYNTHETIC TEST DATA — hosted gate fixtures and raw observations, never inference.
"""Support the existing run-evals agent's tools, without implementing the skill.

The agent invokes Skill and supplies its delivered Bash instructions on stdin.
This helper only prepares case mounts, executes those bytes, and captures real
observations outside /sandbox/output. It never invokes a model or grades a run.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


FIXTURES = Path(__file__).resolve().parent
SCENARIOS = ("absent", "empty", "malformed", "valid")
CASE_IDS = dict(zip(SCENARIOS, (33, 34, 35, 36)))


def prepare_workspace(workspace, scenario):
    """Prepare synthetic inputs once, outside the skill's writable mount."""
    workspace.mkdir()
    mounted = workspace / ".pre-script"
    mounted.mkdir()
    if scenario == "absent":
        shutil.copyfile(FIXTURES / "fullsend-gate-interactive-config.md", workspace / "CLAUDE.md")
    elif scenario == "malformed":
        document = (FIXTURES / "fullsend-invalid-trusted-input.md").read_text()
        malformed = document.split("```json\n", 1)[1].split("\n```", 1)[0]
        (mounted / "triage-security-input.json").write_text(malformed)
    elif scenario == "valid":
        shutil.copyfile(FIXTURES / "fullsend-report-only-trusted-input.json",
                        mounted / "triage-security-input.json")


def child_environment(parent, scenario):
    """Override only the case gate; inherit the existing hosted subprocess policy."""
    environment = dict(parent)
    environment.pop("FULLSEND_OUTPUT_DIR", None)
    if scenario == "empty":
        environment["FULLSEND_OUTPUT_DIR"] = ""
    elif scenario in ("malformed", "valid"):
        environment["FULLSEND_OUTPUT_DIR"] = "/sandbox/output"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def command(workspace, output):
    """Mount the fixed skill paths for one Bash instruction, without a model CLI."""
    argv = ["bwrap", "--die-with-parent", "--unshare-net", "--tmpfs", "/"]
    for path in sorted(Path("/").iterdir()):
        if path.name not in {"tmp", "sandbox", "proc", "dev"}:
            argv.extend(["--ro-bind", str(path), str(path)])
    return argv + [
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/sandbox",
        "--ro-bind", str(workspace), "/sandbox/workspace",
        "--bind", str(output), "/sandbox/output", "--chdir", "/sandbox/workspace",
        "bash", "--noprofile", "--norc", "-s",
    ]


def record_command(argv, environment, script, capture, timeout=120):
    """Preserve exact supplied command bytes, actual streams and actual exit."""
    (capture / "command.sh").write_bytes(script)
    observation = {"argv": argv, "exit_code": None, "timed_out": False}
    with (capture / "stdout").open("wb") as stdout, (capture / "stderr").open("wb") as stderr:
        try:
            result = subprocess.run(argv, input=script, env=environment, stdout=stdout,
                                    stderr=stderr, timeout=timeout, check=False)
            observation["exit_code"] = result.returncode
        except subprocess.TimeoutExpired:
            observation["timed_out"] = True
    (capture / "observation.json").write_text(json.dumps(observation, indent=2) + "\n")
    return observation


def initial_prompt(raw):
    """Read only the initial user prompt from an existing runtime transcript."""
    for line in raw.splitlines():
        try:
            message = json.loads(line).get("message", {})
        except (ValueError, AttributeError):
            continue
        if message.get("role") != "user":
            continue
        content = message.get("content", "")
        if isinstance(content, list):
            content = "\n".join(block.get("text", "") for block in content if block.get("type") == "text")
        return content if isinstance(content, str) else ""
    return ""


def capture_transcript(outputs, case_id, projects):
    """Copy one runtime-created transcript prefix unchanged; never synthesize it.

    Claude Code persists subagents at projects/{project}/{session}/subagents/.
    The initial run-evals task and absolute assigned output path distinguish this
    eval from concurrent cases and graders. Missing/ambiguous logs fail visibly.
    """
    matches = []
    for path in projects.glob("*/*/subagents/agent-*.jsonl"):
        raw = path.read_bytes()
        prompt = initial_prompt(raw)
        if (prompt.startswith("You are executing an eval")
                and f"Task: TC-6677_GATE_CASE={case_id}\n" in prompt
                and f"Write all outputs to: {outputs}" in prompt):
            matches.append((path, raw))
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one matching runtime eval transcript; found {len(matches)}; no fallback")
    source, raw = matches[0]
    # A concurrent runtime append may leave a partial last line. Preserve the
    # complete prefix byte-for-byte; tell the grader exactly where it ends.
    end = raw.rfind(b"\n") + 1
    snapshot = raw[:end]
    (outputs / "execution.jsonl").write_bytes(snapshot)
    return {"source_path": str(source), "prefix_snapshot": True,
            "bytes": len(snapshot), "source_bytes_observed": len(raw),
            "sha256": hashlib.sha256(snapshot).hexdigest()}


def inventory(output):
    """Observe the actual skill output files, without repairing or interpreting them."""
    return sorted(str(path.relative_to(output)) for path in output.rglob("*") if path.is_file())


def main():
    """Prepare, execute one agent-supplied instruction, or snapshot real evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("init", "run", "capture"))
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    args = parser.parse_args()
    outputs = args.outputs.resolve()
    outputs.mkdir(parents=True, exist_ok=True)
    output = outputs / "sandbox-output"
    try:
        if args.operation == "init":
            if not shutil.which("bwrap"):
                raise RuntimeError("Existing hosted bwrap is required; no fallback")
            output.mkdir()  # Refuse stale result reuse.
            temporary = Path(tempfile.mkdtemp(prefix="tc-6677-gate-"))
            workspace = temporary / "workspace"
            prepare_workspace(workspace, args.scenario)
            state = {"scenario": args.scenario, "workspace": str(workspace)}
            (outputs / "fixture-state.json").write_text(json.dumps(state, indent=2) + "\n")
            return 0
        state = json.loads((outputs / "fixture-state.json").read_text())
        if state["scenario"] != args.scenario:
            raise RuntimeError("Case state does not match the requested scenario")
        if args.operation == "run":
            captures = outputs / "commands"
            captures.mkdir(exist_ok=True)
            capture = captures / f"{len(list(captures.iterdir())) + 1:04d}"
            capture.mkdir()
            environment = child_environment(os.environ, args.scenario)
            observed = record_command(command(Path(state["workspace"]), output), environment,
                                      sys.stdin.buffer.read(), capture)
            observed["gate"] = {"present": "FULLSEND_OUTPUT_DIR" in environment,
                                "value": environment.get("FULLSEND_OUTPUT_DIR")}
            observed["sandbox_output_files"] = inventory(output)
            (capture / "observation.json").write_text(json.dumps(observed, indent=2) + "\n")
            sys.stdout.buffer.write((capture / "stdout").read_bytes())
            sys.stderr.buffer.write((capture / "stderr").read_bytes())
            return 124 if observed["timed_out"] else observed["exit_code"]
        projects = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))) / "projects"
        receipt = capture_transcript(outputs, CASE_IDS[args.scenario], projects)
        receipt["sandbox_output_files"] = inventory(output)
        (outputs / "execution-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        return 0
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"ERROR: eval fixture tooling unavailable: {error}", file=sys.stderr)
        (outputs / "fixture-error.txt").write_text(str(error) + "\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
