#!/usr/bin/env python3
# SYNTHETIC TEST DATA — hosted-only driver for four isolated skill gate scenarios.
"""Invoke the real skill and record raw observations; never grade or simulate it.

Used only by hosted run-evals cases. The driver, outside the skill's namespace,
prepares mounts and records the Claude tool stream. Only /sandbox/output is
writable for skill output. No local model invocation is part of the pytest suite.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


FIXTURES = Path(__file__).resolve().parent
SCENARIOS = ("absent", "empty", "malformed", "valid")
SANDBOX_SETTINGS = Path("/tmp/eval-sandbox-settings.json")


def prepare_workspace(workspace, scenario):
    """Prepare independent read-only input mounts before invoking the skill."""
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
    """Keep inference/runtime configuration, remove triage tokens and parent gate."""
    environment = {key: value for key, value in parent.items()
                   if key not in {"FULLSEND_OUTPUT_DIR", "CLAUDECODE"}
                   and not key.startswith(("JIRA_", "GITHUB_", "GH_"))}
    if scenario == "empty":
        environment["FULLSEND_OUTPUT_DIR"] = ""
    elif scenario in ("malformed", "valid"):
        environment["FULLSEND_OUTPUT_DIR"] = "/sandbox/output"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def command(workspace, output, plugin):
    """Build the isolated actual-skill invocation, preserving hosted Bash policy."""
    # Start with an independent root so creating /sandbox never modifies the
    # host root (which may not contain that path). Reuse system paths read-only.
    argv = ["bwrap", "--die-with-parent", "--tmpfs", "/"]
    for path in sorted(Path("/").iterdir()):
        if path.name not in {"tmp", "sandbox", "proc", "dev"}:
            argv.extend(["--ro-bind", str(path), str(path)])
    return argv + [
        "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp", "--tmpfs", "/sandbox",
        "--ro-bind", str(workspace), "/sandbox/workspace",
        "--bind", str(output), "/sandbox/output",
        "--ro-bind", str(SANDBOX_SETTINGS), str(SANDBOX_SETTINGS),
        "--chdir", "/sandbox/workspace",
        "claude", "--bare", "--no-session-persistence", "--no-chrome",
        "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}',
        "--plugin-dir", str(plugin), "--add-dir", "/sandbox/output",
        "--permission-mode", "dontAsk", "--tools", "Bash,Read,Skill",
        "--allowedTools", "Bash,Read,Skill",
        "--settings", str(SANDBOX_SETTINGS),
        "--output-format", "stream-json", "--verbose",
    ]


def prompt(scenario):
    """Request actual routing and validation, with no alternate implementation."""
    context = {
        "absent": "FULLSEND_OUTPUT_DIR is absent. Read the local CLAUDE.md only after the gate. It deliberately lacks Security Configuration: stop at the existing Step 0 configuration guard before credentials or external calls.",
        "empty": "FULLSEND_OUTPUT_DIR is exported empty. Stop at the Step 0.6 failure, before configuration, trusted input, credentials or any later step. Write no result file.",
        "malformed": "FULLSEND_OUTPUT_DIR is nonempty. The read-only trusted input mount contains malformed JSON. Execute Step 0.7's failure branch, writing only its exact error object to /sandbox/output/agent-result.json, then stop. No analysis or fallback.",
        "valid": "FULLSEND_OUTPUT_DIR is nonempty. Read the schema-valid authorization-withheld trusted bundle for TC-8101. Complete analysis using only its evidence, reporting unavailable evidence honestly. Include its pinned release/development lock evidence and withheld assignment, field edits, transition, comment, link and remediation task. Produce the completed report-only result with exactly one report-only action; execute the skill's actual inline final JSON/schema validator on that final file before finishing.",
    }[scenario]
    return (
        "Invoke sdlc-workflow:triage-security via the Skill tool with issue "
        + ("TC-8101" if scenario == "valid" else "TC-8001")
        + ". This is a fixture-only hosted gate evaluation. " + context
        + " Evaluation clock: 2026-09-21T12:00:00Z. Before numbered steps, use Bash to observe ONLY the presence/value of FULLSEND_OUTPUT_DIR (never print the environment or credentials), then execute the delivered Step 0.6 gate. Execute the delivered skill's instructions, not a test helper, duplicated gate, parser proxy or alternate validator. Preserve failing Bash exits in tool results; do not mask them. Never contact Jira/GitHub/CVE/lifecycle services, run Git, inspect credentials, or execute actions. After stopping, summarize in the final response only. In sandbox mode the sole permitted skill file write is /sandbox/output/agent-result.json; no logs, receipts, matrices or analysis Markdown files. The eval driver outside your namespace captures raw tool evidence; do not fabricate that evidence or write a grading verdict."
    )


def record_process(argv, environment, outputs, timeout=900):
    """Capture unmodified stdout/stderr and status on the evaluation side."""
    with (outputs / "execution.jsonl").open("w") as stdout, (outputs / "execution.stderr").open("w") as stderr:
        try:
            completed = subprocess.run(argv, env=environment, stdout=stdout, stderr=stderr,
                                       timeout=timeout, check=False)
            return {"process_exit_code": completed.returncode, "timed_out": False}
        except subprocess.TimeoutExpired:
            return {"process_exit_code": None, "timed_out": True}


def main():
    """Run one hosted scenario, failing visibly if isolation cannot be established."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    parser.add_argument("--plugin-root", type=Path, required=True)
    args = parser.parse_args()
    outputs = args.outputs.resolve()
    plugin = args.plugin_root.resolve()
    outputs.mkdir(parents=True, exist_ok=True)
    sandbox_output = outputs / "sandbox-output"
    sandbox_output.mkdir()  # Refuse reuse; an existing result cannot prove this run.
    receipt = {"scenario": args.scenario, "sandbox_output_files": [],
               "process_exit_code": None, "timed_out": False}
    try:
        if not shutil.which("bwrap") or not shutil.which("claude") or not SANDBOX_SETTINGS.is_file():
            raise RuntimeError("Hosted bwrap, Claude CLI and eval-sandbox-settings.json are required; no fallback")
        if not (plugin / "skills/triage-security/SKILL.md").is_file():
            raise RuntimeError("The evaluated plugin must contain the actual triage-security skill")
        with tempfile.TemporaryDirectory(prefix="tc-6677-gate-") as temporary:
            workspace = Path(temporary) / "workspace"
            prepare_workspace(workspace, args.scenario)
            environment = child_environment(os.environ, args.scenario)
            receipt["gate"] = {"present": "FULLSEND_OUTPUT_DIR" in environment,
                               "value": environment.get("FULLSEND_OUTPUT_DIR")}
            invocation = command(workspace, sandbox_output, plugin) + ["-p", prompt(args.scenario)]
            receipt["launch_argv"] = invocation
            receipt.update(record_process(invocation, environment, outputs))
    except (OSError, RuntimeError) as error:
        receipt["infrastructure_error"] = str(error)
    receipt["sandbox_output_files"] = sorted(
        str(path.relative_to(sandbox_output)) for path in sandbox_output.rglob("*") if path.is_file())
    (outputs / "execution-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    # A CLI zero exit is not a verdict about skill gates/validators. Graders must
    # inspect their actual Bash tool results in execution.jsonl independently.
    return 1 if receipt.get("infrastructure_error") or receipt["timed_out"] else (receipt["process_exit_code"] or 0)


if __name__ == "__main__":
    raise SystemExit(main())
