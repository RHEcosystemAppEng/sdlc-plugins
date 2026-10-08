#!/usr/bin/env python3
"""Common local/CI entrypoint for the native Fullsend gate suite."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid
import venv


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CASES = ["033-absent", "034-empty", "035-malformed", "036-valid"]
ASSERTION_COUNTS = dict(zip(CASES, [4, 5, 5, 7]))


def pins():
    """Read the repository-owned immutable dependency manifest."""
    return json.loads((HERE / "dependencies.json").read_text())


def binaries(cache):
    """Select host and Linux sandbox binaries; macOS cannot run in the sandbox."""
    arch = {"x86_64": "amd64", "arm64": "arm64", "aarch64": "arm64"}.get(platform.machine())
    system = {"Darwin": "darwin", "Linux": "linux"}.get(platform.system())
    if not arch or not system:
        raise ValueError("Supported hosts are macOS/Linux amd64/arm64")
    return cache / "bin" / f"fullsend-{system}-{arch}", cache / "bin" / f"fullsend-linux-{arch}"


def install_binary(cache, key, dependency):
    """Verify an archive's immutable digest before installing only its CLI file."""
    destination = cache / "bin" / f"fullsend-{key}"
    archive = cache / f"fullsend-{key}.tar.gz"
    if not archive.exists():
        url = f'https://github.com/fullsend-ai/fullsend/releases/download/v{dependency["version"]}/fullsend_{dependency["version"]}_{key.replace("-", "_")}.tar.gz'
        subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error",
                        "--output", str(archive), url], check=True)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != dependency["archives"][key]:
        raise ValueError(f"Fullsend archive digest mismatch for {key}")
    with tarfile.open(archive, "r:gz") as package:
        candidates = [m for m in package.getmembers() if m.isfile() and Path(m.name).name == "fullsend"]
        if len(candidates) != 1:
            raise ValueError("Fullsend archive must contain exactly one regular CLI binary")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with package.extractfile(candidates[0]) as source, destination.open("wb") as target:
            shutil.copyfileobj(source, target)
    destination.chmod(0o755)


def verify_source(source, dependency):
    """Reject changed tracked framework code or a different source revision."""
    actual = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", str(source), "status", "--porcelain", "--untracked-files=no"], text=True)
    if actual != dependency["commit"] or dirty:
        raise ValueError("Eval-harness source is not the clean approved immutable revision")


def setup(cache):
    """Install isolated locked dependencies and CLI binaries; never inference/services."""
    if sys.version_info[:2] != (3, 12):
        raise ValueError("Use Python3.12 for the locked dependency setup")
    dependency = pins()
    cache.mkdir(parents=True, exist_ok=True)
    source = cache / "agent-eval-harness"
    if not source.exists():
        subprocess.run(["git", "init", "-q", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "fetch", "--depth", "1", dependency["harness"]["repository"], dependency["harness"]["commit"]], check=True)
        subprocess.run(["git", "-C", str(source), "checkout", "--detach", "FETCH_HEAD"], check=True)
    verify_source(source, dependency["harness"])
    environment = cache / "venv"
    if not (environment / "bin/python").is_file():
        venv.EnvBuilder(with_pip=True).create(environment)
    python = environment / "bin/python"
    pip = [str(python), "-m", "pip", "--cache-dir", str(cache / "pip-cache"), "install", "--no-user"]
    subprocess.run([*pip, "--require-hashes", "-r", str(HERE / "requirements.lock")], check=True)
    subprocess.run([*pip, "--no-deps", "--no-build-isolation", str(source)], check=True)
    for binary in set(binaries(cache)):
        install_binary(cache, binary.name.removeprefix("fullsend-"), dependency["fullsend"])
    print("Isolated dependency setup complete; no inference or host-service changes")


def resolved_config(python, model, judge_model, effort, plugin_root=None):
    """Resolve repository paths before upstream workspace/execute path handling."""
    import yaml
    config = yaml.safe_load((HERE / "triage-security/eval.yaml").read_text())
    config["dataset"]["path"] = str(HERE / "triage-security/cases")
    config["runner"]["command"][0:2] = [str(python), str(HERE / "triage-security/run-fullsend.py")]
    if plugin_root is not None:
        config["runner"]["command"].extend(["--plugin-root", str(plugin_root)])
    config["runner"]["effort"] = effort
    config["models"] = {"skill": model, "judge": judge_model}
    return config


def verify_locked_dependencies(lock):
    """Reject installed version drift from the checked-in transitive hash lock."""
    import importlib.metadata
    requirements = re.findall(r"^([A-Za-z0-9_.-]+)==([^\s;\\]+)", lock.read_text(), re.MULTILINE)
    if not requirements:
        raise ValueError("Locked dependency manifest is empty")
    for package, expected in requirements:
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            actual = None
        if actual != expected:
            raise ValueError(f"Locked dependency mismatch: {package}, expected {expected}, installed {actual}")


def preflight(cache, model, judge_model, effort):
    """Validate dependencies/config/CLI contracts only; no sandbox or model launch."""
    import importlib.metadata
    import jsonschema  # Required by the trusted host output validator.
    import yaml
    from agent_eval.config import EvalConfig
    dependency = pins()
    if sys.version_info[:2] != (3, 12):
        raise ValueError("Preflight requires the Python3.12 isolated environment")
    verify_source(cache / "agent-eval-harness", dependency["harness"])
    if importlib.metadata.version("agent-eval-harness") != dependency["harness"]["version"]:
        raise ValueError("Unexpected installed eval-harness version")
    verify_locked_dependencies(HERE / "requirements.lock")
    subprocess.run([sys.executable, "-m", "pip", "--cache-dir", str(cache / "pip-cache"), "check"], check=True)
    for phase in ["workspace", "execute", "collect", "score"]:
        subprocess.run([sys.executable, str(cache / f"agent-eval-harness/skills/eval-run/scripts/{phase}.py"), "--help"],
                       cwd=ROOT, stdout=subprocess.DEVNULL, check=True)
    host, sandbox = binaries(cache)
    if not sandbox.is_file():
        raise ValueError("Missing Linux sandbox Fullsend binary; run setup")
    for executable, version in [(host, dependency["fullsend"]["version"]), ("openshell", dependency["openshell"]),
                                ("openshell-gateway", dependency["openshell"])]:
        result = subprocess.check_output([str(executable), "--version"], text=True)
        if not re.search(r"(?<![\d.])" + re.escape(version) + r"(?![\d.])", result):
            raise ValueError(f"Unexpected {Path(executable).name} version; expected {version}")
    help_text = subprocess.check_output([str(host), "run", "--help"], text=True)
    if not all(flag in help_text for flag in ["--fullsend-binary", "--fullsend-dir", "--target-repo", "--no-post-script"]):
        raise ValueError("Fullsend CLI contract mismatch")
    subprocess.run(["podman", "--version"], check=True)
    config = resolved_config(Path(sys.executable), model, judge_model, effort)
    with tempfile.TemporaryDirectory(prefix="tc6677-preflight-") as temporary:
        path = Path(temporary) / "eval.yaml"
        path.write_text(yaml.safe_dump(config, sort_keys=False))
        parsed = EvalConfig.from_yaml(path)
        if parsed.runner.type != "cli" or parsed.eval_name() != "triage-security-gate":
            raise ValueError("Opaque CLI config binding mismatch")
    cases = sorted((HERE / "triage-security/cases").iterdir())
    if [p.name for p in cases] != CASES:
        raise ValueError("Native dataset must contain exactly four gate cases")
    if [yaml.safe_load((p / "annotations.yaml").read_text())["assertion_count"] for p in cases] != [4, 5, 5, 7]:
        raise ValueError("Native assertion count mismatch")
    print("NO-INFERENCE preflight passed; propagation, services, credentials and runtime success remain unproven")


def validate_summary(run_dir, run_id):
    """Require complete upstream outcomes without judging or rewriting the artifact."""
    import yaml

    class UniqueKeyLoader(yaml.SafeLoader):
        """Reject ambiguous YAML mappings instead of silently keeping the last key."""

        def construct_mapping(self, node, deep=False):
            keys = [self.construct_object(key, deep=deep) for key, _ in node.value]
            if len(keys) != len(set(keys)):
                raise ValueError("Ambiguous upstream summary: duplicate YAML key")
            return super().construct_mapping(node, deep=deep)

    try:
        summary = yaml.load((run_dir / "summary.yaml").read_text(), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError, TypeError) as exc:
        raise ValueError(f"Invalid or missing upstream summary: {exc}") from exc
    if not isinstance(summary, dict) or summary.get("run_id") != run_id:
        raise ValueError("Invalid upstream summary: expected current run mapping")
    cases = summary.get("per_case")
    if not isinstance(cases, dict) or set(cases) != set(CASES):
        raise ValueError("Invalid upstream summary: expected exactly four gate cases")
    names = {f"assertion_{index}" for index in range(1, 8)}
    for case, count in ASSERTION_COUNTS.items():
        results = cases[case]
        # The pinned scorer emits all seven names, including conditional skips.
        if not isinstance(results, dict) or set(results) != names:
            raise ValueError(f"Invalid upstream summary: unexpected assertions for {case}")
        for index in range(1, 8):
            name = f"assertion_{index}"
            result = results[name]
            if not isinstance(result, dict) or "value" not in result or "error" in result:
                raise ValueError(f"Incomplete upstream summary: {case}/{name}")
            rationale = result.get("rationale", "")
            if index <= count:
                if (type(result["value"]) is not bool or result.get("skipped")
                        or (isinstance(rationale, str) and rationale.startswith(("Skipped:", "Condition error:")))):
                    raise ValueError(f"Incomplete upstream summary: {case}/{name} requires a Boolean outcome")
            else:
                condition = f'annotations.get("assertion_count", 0) > {index - 1}'
                if result["value"] is not None or rationale != f"Skipped: condition '{condition}' is false":
                    raise ValueError(f"Invalid upstream summary: {case}/{name} requires its nonapplicable skip")


def phase_failure_code(stderr):
    """Map observed stderr markers to fixed advisory categories, never raw messages."""
    for code, pattern in [
        ("authentication-error", r"unauthenticated|unauthorized|invalid_grant|\b401\b"),
        ("permission-error", r"permission.?denied|forbidden|\b403\b"),
        ("quota-error", r"resource_exhausted|rate.limit|\b429\b"),
        ("timeout", r"timed? ?out|deadline exceeded"),
        ("connection-error", r"connection refused|connection reset|name resolution"),
    ]:
        if re.search(pattern, stderr, re.IGNORECASE):
            return code
    return "phase-exit"


def pipeline(python, source, config, workspace, run_dir, run_id, environment, diagnostics=None):
    """Delegate case execution/collection/grading entirely to the upstream framework."""
    diagnostics = diagnostics if diagnostics is not None else {}
    diagnostics["phase_exits"] = {}
    scripts = source / "skills/eval-run/scripts"
    phases = [
        ("workspace", ["--config", str(config), "--run-id", run_id, "--symlinks", "none"]),
        ("execute", ["--workspace", str(workspace), "--config", str(config), "--output", str(run_dir), "--run-id", run_id]),
        ("collect", ["--config", str(config), "--workspace", str(workspace), "--output", str(run_dir)]),
        ("score", ["judges", "--config", str(config), "--run-id", run_id]),
    ]
    for phase, arguments in phases:
        diagnostics.update(phase=phase, code="runtime-error")
        with tempfile.TemporaryFile() as stderr:
            process = subprocess.run([str(python), str(scripts / f"{phase}.py"), *arguments],
                                     cwd=ROOT, env=environment, stderr=stderr, check=False)
            stderr.seek(0)
            text = stderr.read(65536).decode("utf-8", errors="replace")
            sys.stderr.write(text)  # The trusted wrapper keeps this stream private.
            while chunk := stderr.read(65536):
                sys.stderr.write(chunk.decode("utf-8", errors="replace"))
        diagnostics["phase_exits"][phase] = process.returncode
        diagnostics["code"] = phase_failure_code(text) if process.returncode else "none"
        if phase == "execute":
            if not all((run_dir / "cases" / case / "run_result.json").is_file() for case in CASES):
                diagnostics["code"] = "missing-case-results"
                raise ValueError("Missing native case results; infrastructure failure, refusing zero-case grading")
            if process.returncode:
                print(f"Upstream execution exit {process.returncode}; retaining actual exits for native evidence judges", file=sys.stderr)
        elif process.returncode:
            return process.returncode
    diagnostics.update(phase="summary", code="invalid-summary")
    validate_summary(run_dir, run_id)
    diagnostics.update(phase="complete", code="none")
    return 0


def valid_case_tool_observations(run_dir):
    """Observe matched native tools without exporting text or replacing judgments."""
    observations = dict.fromkeys([
        "transcript_found", "transcript_readable", "skill_invoked",
        "presence_gate_succeeded", "presence_gate_failed",
        "input_validation_succeeded", "input_validation_failed",
    ], False)
    try:
        paths = list(run_dir.glob("cases/036-valid/output/native/*/iteration-*/transcripts/*.jsonl"))
        observations["transcript_found"] = bool(paths)
        observations["transcript_readable"] = bool(paths)
        skill = (ROOT / "plugins/sdlc-workflow/skills/triage-security/SKILL.md").read_text()
        commands = {}
        for step, kind in [("0.6", "presence_gate"), ("0.7", "input_validation")]:
            command = skill.split(f"### Step {step}", 1)[1].split("```bash\n", 1)[1].split("\n```", 1)[0]
            commands[command.replace("${CLAUDE_PLUGIN_ROOT}", "/sandbox/claude-config/plugins/sdlc-workflow")] = kind
    except (OSError, UnicodeError, IndexError):
        observations["transcript_readable"] = False
        return observations
    expected = {"presence_gate": "sandbox mode: /sandbox/workspace/output",
                "input_validation": "Trusted triage-security input available"}
    for path in paths:
        pending = {}
        identities = set()
        observed = dict.fromkeys(observations, False)
        try:
            if any(parent.is_symlink() for parent in [path, *path.parents]):
                raise ValueError("Symlinked transcript")
            with path.open() as transcript:
                seen = False
                for line in transcript:
                    seen = True
                    if not line.endswith("\n"):
                        raise ValueError("Truncated transcript")
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        raise ValueError("Invalid transcript record")
                    if record.get("type") not in ("assistant", "user"):
                        continue
                    message = record.get("message", {})
                    if not isinstance(message, dict) or message.get("role") != record.get("type"):
                        continue
                    blocks = message.get("content", [])
                    if not isinstance(blocks, list):
                        continue
                    for block in blocks:
                        if not isinstance(block, dict):
                            continue
                        if record["type"] == "assistant" and block.get("type") == "tool_use":
                            identity = block.get("id")
                            if not isinstance(identity, str) or not identity or identity in identities:
                                raise ValueError("Invalid or duplicate tool ID")
                            identities.add(identity)
                            inputs = block.get("input", {})
                            if not isinstance(inputs, dict):
                                continue
                            if (block.get("name") == "Skill" and inputs.get("skill") == "sdlc-workflow:triage-security"
                                    and inputs.get("args") == "TC-8101"):
                                observed["skill_invoked"] = True
                            command = inputs.get("command")
                            if block.get("name") == "Bash" and isinstance(identity, str) and isinstance(command, str):
                                pending[identity] = commands.get(command.strip())
                        elif record["type"] == "user" and block.get("type") == "tool_result":
                            identity = block.get("tool_use_id")
                            kind = pending.pop(identity, None) if isinstance(identity, str) else None
                            if kind is None:
                                continue
                            content = block.get("content", "")
                            if isinstance(content, list):
                                content = "\n".join(item["text"] for item in content
                                                    if isinstance(item, dict) and item.get("type") == "text"
                                                    and isinstance(item.get("text"), str))
                            success = (block.get("is_error") is False and isinstance(content, str)
                                       and expected[kind] in content.splitlines())
                            observed[kind + ("_succeeded" if success else "_failed")] = True
                if not seen:
                    raise ValueError("Empty transcript")
        except (OSError, UnicodeError, ValueError, RecursionError):
            observations["transcript_readable"] = False
            continue
        for key, value in observed.items():
            observations[key] = observations[key] or value
    if not observations["transcript_readable"]:
        for key in ["skill_invoked", "presence_gate_succeeded", "input_validation_succeeded"]:
            observations[key] = False
    return observations


def publish_report(run_dir, destination, source, exit_code, diagnostics=None):
    """Export source pins, Boolean outcomes and fixed observations; raw evidence stays private."""
    import yaml
    sha_keys = {"head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"}
    if (set(source) != sha_keys | {"pr_number"} or type(source["pr_number"]) is not int
            or source["pr_number"] <= 0
            or any(not re.fullmatch(r"[0-9a-f]{40}", source[key]) for key in sha_keys)):
        raise ValueError("Invalid CI source provenance")
    outcomes = {}
    complete = False
    try:
        validate_summary(run_dir, run_dir.name)
        summary = yaml.safe_load((run_dir / "summary.yaml").read_text())
        outcomes = {case: {f"assertion_{i}": summary["per_case"][case][f"assertion_{i}"]["value"]
                          for i in range(1, count + 1)} for case, count in ASSERTION_COUNTS.items()}
        complete = True
    except ValueError:
        exit_code = exit_code or 1
    report = {"source": source, "exit_code": exit_code, "complete": complete, "outcomes": outcomes,
              "passed": sum(value is True for case in outcomes.values() for value in case.values()), "total": 21,
              "valid_case_tools": valid_case_tool_observations(run_dir)}
    if diagnostics is not None:
        phases = {"preflight", "configuration", "workspace", "execute", "collect", "score", "summary", "complete"}
        codes = {"none", "runtime-error", "phase-exit", "missing-case-results", "invalid-summary",
                 "authentication-error", "permission-error", "quota-error", "timeout", "connection-error"}
        if (set(diagnostics) != {"phase", "code", "phase_exits"}
                or diagnostics["phase"] not in phases or diagnostics["code"] not in codes
                or not isinstance(diagnostics["phase_exits"], dict)
                or any(key not in {"workspace", "execute", "collect", "score"} or type(value) is not int
                       for key, value in diagnostics["phase_exits"].items())):
            raise ValueError("Invalid safe diagnostic values")
        report["diagnostics"] = diagnostics
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "native-result.json").write_text(json.dumps(report, indent=2) + "\n")


def main():
    """Use the same setup/preflight/run command in local shells and trusted CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["setup", "preflight", "run"])
    parser.add_argument("--cache", type=Path, default=Path(tempfile.gettempdir()) / "tc-6677-eval-deps")
    parser.add_argument("--output", type=Path, default=Path(tempfile.gettempdir()) / "tc-6677-native-evals")
    parser.add_argument("--model", default="claude-opus-4-8")
    parser.add_argument("--judge-model", default="claude-opus-4-6")
    parser.add_argument("--effort", choices=["low", "medium", "high", "max"], default="high")
    parser.add_argument("--plugin-root", type=Path, help="Sandbox-tested plugin; tooling always comes from this checkout")
    parser.add_argument("--report-dir", type=Path, help="Allowlisted CI result directory; never raw credentials/transcripts")
    args = parser.parse_args()
    cache = args.cache.resolve()
    run_dir = args.output.resolve() / "missing-run"
    exit_code = 1
    diagnostics = {"phase": "preflight", "code": "runtime-error", "phase_exits": {}}
    try:
        if args.command == "setup":
            setup(cache)
            return 0
        python = cache / "venv/bin/python"
        if not python.is_file():
            raise ValueError("Missing isolated dependencies; run setup first")
        if Path(sys.prefix).resolve() != (cache / "venv").resolve():
            os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])
        preflight(cache, args.model, args.judge_model, args.effort)
        if args.command == "preflight":
            return 0
        diagnostics["phase"] = "configuration"
        import yaml
        run_id = "tc6677-" + uuid.uuid4().hex
        workspace = Path(tempfile.gettempdir()) / "agent-eval" / run_id
        run_dir = args.output.resolve() / "triage-security-gate" / run_id
        if workspace.exists() or run_dir.exists():
            raise ValueError("Refusing existing run identifier")
        run_dir.mkdir(parents=True)
        config = run_dir / "eval.yaml"
        config.write_text(yaml.safe_dump(resolved_config(python, args.model, args.judge_model, args.effort,
                                                       args.plugin_root.absolute() if args.plugin_root else None), sort_keys=False))
        host, sandbox = binaries(cache)
        environment = dict(os.environ, TC6677_FULLSEND_BIN=str(host), TC6677_SANDBOX_FULLSEND_BIN=str(sandbox),
                           AGENT_EVAL_RUNS_DIR=str(args.output.resolve()))
        print(f"Native evidence destination: {run_dir}", flush=True)
        exit_code = pipeline(python, cache / "agent-eval-harness", config, workspace, run_dir, run_id, environment, diagnostics)
        return exit_code
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Fullsend eval setup/runner failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if args.command == "run" and args.report_dir:
            source = {key: os.environ.get("TC6726_" + key.upper(), "")
                      for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
            source["pr_number"] = int(os.environ.get("TC6726_PR_NUMBER", "0"))
            publish_report(run_dir, args.report_dir.resolve(), source, exit_code, diagnostics)


if __name__ == "__main__":
    sys.exit(main())
