#!/usr/bin/env python3
"""Trusted execution gate; native LLM quality outcomes remain advisory."""

import argparse
import json
import os
from pathlib import Path


CASES = {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7}
FIELDS = ("case_result_valid", "transcript_readable", "runtime_completed", "skill_invoked", "tools_completed")


def unique_object(pairs):
    """Reject ambiguous JSON instead of trusting its last duplicate value."""
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON key")
    return result


def regular_text(path):
    """Private records must be regular files reached without following symlinks."""
    if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError("Missing or symlinked record")
    return path.read_text()


def observe_case(case_dir):
    """Require genuine paired tools and runtime completion, not narrated behavior."""
    observed = dict.fromkeys(FIELDS, False)
    try:
        result = json.loads(regular_text(case_dir / "run_result.json"), object_pairs_hook=unique_object)
        # Native exit 1 can be the expected host rejection of a negative case.
        observed["case_result_valid"] = type(result.get("exit_code")) is int and result["exit_code"] in (0, 1)
        paths = list(case_dir.glob("output/native/*/iteration-*/output.jsonl"))
        if not paths:
            return observed
        for path in paths:
            identities, pending = set(), {}
            launched = completed = False
            for line in regular_text(path).splitlines(keepends=True):
                if not line.endswith("\n") or completed:
                    raise ValueError("Truncated or trailing runtime record")
                record = json.loads(line, object_pairs_hook=unique_object)
                if not isinstance(record, dict):
                    raise ValueError("Invalid runtime record")
                if record.get("type") == "result":
                    if record.get("subtype") != "success" or record.get("is_error") is not False or pending:
                        raise ValueError("Runtime failed or tools incomplete")
                    completed = True
                    continue
                role = record.get("type")
                message = record.get("message", {})
                if role not in ("assistant", "user"):
                    continue
                if not isinstance(message, dict) or message.get("role") != role:
                    raise ValueError("Invalid tool record role")
                for block in message.get("content", []):
                    if not isinstance(block, dict):
                        continue
                    if role == "assistant" and block.get("type") == "tool_use":
                        identity = block.get("id")
                        if not isinstance(identity, str) or not identity or identity in identities:
                            raise ValueError("Invalid or duplicate tool ID")
                        identities.add(identity)
                        inputs = block.get("input", {})
                        if not isinstance(inputs, dict):
                            raise ValueError("Invalid tool input")
                        if (block.get("name") == "Skill" and inputs.get("skill") == "sdlc-workflow:triage-security"
                                and inputs.get("args") == "TC-8101"):
                            pending[identity] = "skill"
                        elif block.get("name") == "Bash" and launched and isinstance(inputs.get("command"), str):
                            pending[identity] = "bash"
                    elif role == "user" and block.get("type") == "tool_result":
                        identity = block.get("tool_use_id")
                        kind = pending.get(identity) if isinstance(identity, str) else None
                        if kind == "bash" and type(block.get("is_error")) is not bool:
                            raise ValueError("Invalid Bash tool result")
                        if kind is not None:
                            del pending[identity]
                        if kind == "skill":
                            launch = record.get("tool_use_result", {})
                            launched = (isinstance(launch, dict) and launch.get("success") is True
                                        and launch.get("commandName") == "sdlc-workflow:triage-security"
                                        and block.get("is_error") is not True)
                            observed["skill_invoked"] |= launched
                        elif kind == "bash":
                            # A real error result is valid execution evidence; quality is judged separately.
                            observed["tools_completed"] = True
            if not completed:
                raise ValueError("Missing native runtime completion")
        observed["transcript_readable"] = observed["runtime_completed"] = True
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError):
        observed["transcript_readable"] = observed["runtime_completed"] = False
    return observed


def assess(private_root, report_path, runner_exit, expected_source):
    """Add fixed observations to the safe report; never rewrite scores or raw records."""
    try:
        report = json.loads(regular_text(report_path), object_pairs_hook=unique_object)
        if not isinstance(report, dict):
            return 1
        outcomes = report.get("outcomes", {})
        complete = (report.get("complete") is True and report.get("total") == 21
                    and isinstance(outcomes, dict) and set(outcomes) == set(CASES)
                    and all(isinstance(outcomes[c], dict)
                            and set(outcomes[c]) == {f"assertion_{i}" for i in range(1, n + 1)}
                            and all(type(v) is bool for v in outcomes[c].values()) for c, n in CASES.items()))
        score = sum(v is True for case in outcomes.values() if isinstance(case, dict) for v in case.values())
        diagnostics = report.get("diagnostics", {})
        phases = diagnostics.get("phase_exits", {})
        phases_completed = (complete and report.get("source") == expected_source
                            and type(report.get("passed")) is int and report["passed"] == score
                            and type(report.get("exit_code")) is int and report["exit_code"] == runner_exit
                            and set(phases) == {"workspace", "execute", "collect", "score"}
                            and all(type(v) is int for v in phases.values())
                            and phases["workspace"] == phases["collect"] == 0 and phases["execute"] in (0, 1)
                            and runner_exit == phases["score"] == int(score < 21)
                            and (diagnostics.get("phase"), diagnostics.get("code")) ==
                            (("score", "phase-exit") if runner_exit else ("complete", "none")))
        runs = list(private_root.glob("triage-security-gate/*"))
        observations = {case: dict.fromkeys(FIELDS, False) for case in CASES}
        if len(runs) == 1:
            observations = {case: observe_case(runs[0] / "cases" / case) for case in CASES}
        report["execution"] = {"phases_completed": bool(phases_completed), "cases": observations}
        report["execution_valid"] = bool(phases_completed and all(all(e.values()) for e in observations.values()))
        report_path.write_text(json.dumps(report, indent=2) + "\n")
        return int(not report["execution_valid"])
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, RecursionError):
        return 1


def main():
    """Run only on trusted main; expose no private runtime text in CI logs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--runner-exit", type=int, required=True)
    args = parser.parse_args()
    source = {key: os.environ[f"TC6726_{key.upper()}"] for key in
              ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = int(os.environ["TC6726_PR_NUMBER"])
    status = assess(args.private_root, args.report, args.runner_exit, source)
    print("Native execution evidence: " + ("valid; quality score is advisory" if status == 0 else "invalid; blocking"))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
