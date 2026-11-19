#!/usr/bin/env python3
"""Trusted execution gate; native LLM quality outcomes remain advisory."""

import argparse
import json
import os
from pathlib import Path


CASES = {"034-empty": 5, "035-malformed": 5, "036-valid": 7, "037-release": 7}
FIELDS = ("case_result_valid", "transcript_readable", "runtime_completed", "skill_invoked", "tools_completed")
# Only these cases must establish the Step 0.6/0.7 setup before their analysis is meaningful.
GATE_CASES = ("036-valid", "037-release")
GATE_ASSERTIONS = {"036-valid": "assertion_2", "037-release": "assertion_1"}
# Evidence each gate assertion is allowed to claim as its own. Assertion 1 for the
# release case also requires the actual Skill invocation, not just the two Bash steps.
GATE_ASSERTION_STEPS = {"036-valid": ("presence_gate", "input_validation"),
                        "037-release": ("skill_invocation", "presence_gate", "input_validation")}
# Assertions that carry no evidence unless the case's required setup was established.
DEPENDENT_ASSERTIONS = {"036-valid": tuple(f"assertion_{i}" for i in (1, 3, 4, 5, 6, 7)),
                        "037-release": tuple(f"assertion_{i}" for i in (2, 3, 4, 5, 6, 7))}
GATE_OBSERVATIONS = ("transcript", "skill_invocation", "presence_gate", "input_validation")
# Fixed allowlist reproduced from evals/fullsend/run.py; raw transcript text never arrives here.
EVIDENCE_CATEGORIES = frozenset(["successful", "not-observed", "tool-error", "unexpected-output",
                                 "invalid-transcript", "conflicting-results"])
OBSERVED_FAILURES = frozenset(["tool-error", "unexpected-output", "conflicting-results"])
# Pinned agent-eval-harness score.py text fallback: an unusable judge reply is
# recorded as passed=false with this rationale prefix instead of an error.
JUDGE_UNPARSED = "Could not parse judge response:"


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
                        if kind == "skill" and "is_error" in block and type(block["is_error"]) is not bool:
                            raise ValueError("Invalid Skill tool result")
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


def judge_errors(report, run):
    """Count judge failures (API errors, unusable replies) that must never pass as verdicts."""
    failures = report.get("summary_failures", [])
    if not isinstance(failures, list) or not all(isinstance(f, dict) for f in failures):
        raise ValueError("Invalid summary failures")
    # run.py records a judge exception (e.g. a 400 on forced tool_choice) as scorer-error.
    count = sum(f.get("reason") == "scorer-error" for f in failures)
    summary = run / "summary.yaml" if run is not None else None
    if summary is not None and (summary.exists() or summary.is_symlink()):
        count += regular_text(summary).count(JUDGE_UNPARSED)
    elif summary is not None and report.get("complete") is True:
        # A complete report without its summary cannot be checked for unparsed replies.
        count += 1
    return count


def gate_input(report):
    """Validate the published per-case gate/input categories; None when unusable."""
    published = report.get("gate_input")
    if not isinstance(published, dict) or set(published) != set(GATE_CASES):
        return None
    for case in GATE_CASES:
        categories = published[case]
        if not isinstance(categories, dict) or set(categories) != set(GATE_OBSERVATIONS):
            return None
        if any(value not in EVIDENCE_CATEGORIES for value in categories.values()):
            return None
        # Missing or unreadable transcripts cannot carry step-level evidence; a
        # producer that pairs them with successes is not a trustworthy report.
        transcript = categories["transcript"]
        if transcript != "successful":
            steps = [categories[step] for step in GATE_OBSERVATIONS if step != "transcript"]
            if any(value != transcript for value in steps):
                return None
    return published


def reconcile(outcomes, case, categories, observations):
    """Cross-check a case's gate verdict against observed gate/input evidence.

    Returns the fixed consistency category and whether the required setup was
    established, so dependent assertions are not published as behavior findings.
    """
    verdict = outcomes.get(case, {}).get(GATE_ASSERTIONS[case])
    verdict = verdict if type(verdict) is bool else None
    required = [categories[step] for step in GATE_ASSERTION_STEPS[case]]
    observed = all(value == "successful" for value in required)
    if not observed:
        failed = any(value in OBSERVED_FAILURES for value in required)
        if verdict is True:
            # A passing judgment cannot outrank a genuine error or wrong output;
            # missing, malformed or unreadable evidence is inconclusive instead.
            return ("contradiction" if failed else "inconclusive"), False
        if verdict is False and failed:
            # A real observed failure keeps the failed verdict a behavior result.
            return "consistent", False
        # Without usable evidence, even a failed verdict is not a behavior result.
        return ("inconclusive" if verdict is False else "not-evaluable"), False
    # Gate evidence alone is not enough: the runtime and paired Skill launch must
    # also have completed, or the dependent scores are uninterpretable.
    established = bool(categories["skill_invocation"] == "successful"
                       and observations["runtime_completed"] is True
                       and observations["skill_invoked"] is True
                       and verdict is True)
    return "consistent", established


def assess(private_root, report_path, runner_exit, expected_source):
    """Add fixed observations to the safe report; never rewrite scores or raw records."""
    try:
        report = json.loads(regular_text(report_path), object_pairs_hook=unique_object)
        if not isinstance(report, dict):
            return 1
        outcomes = report.get("outcomes", {})
        complete = (report.get("complete") is True and report.get("total") == sum(CASES.values())
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
                            and runner_exit == phases["score"] == int(score < sum(CASES.values()))
                            and (diagnostics.get("phase"), diagnostics.get("code")) ==
                            (("score", "phase-exit") if runner_exit else ("complete", "none")))
        runs = list(private_root.glob("triage-security-gate/*"))
        observations = {case: dict.fromkeys(FIELDS, False) for case in CASES}
        if len(runs) == 1:
            observations = {case: observe_case(runs[0] / "cases" / case) for case in CASES}
        # Judge errors are not failed verdicts: they invalidate the run (fail-closed).
        errors = judge_errors(report, runs[0] if len(runs) == 1 else None)
        published = gate_input(report)
        consistency, evaluability = {}, {}
        for case in CASES:
            if case not in GATE_CASES:
                state, established = "not-applicable", True
            elif published is None:
                # Unvalidated or absent safe categories cannot establish the setup.
                state, established = "invalid-input", False
            else:
                state, established = reconcile(outcomes, case, published[case], observations[case])
            consistency[case] = state
            evaluability[case] = {
                "evaluable": bool(established),
                "not_evaluable_assertions": [] if established else list(DEPENDENT_ASSERTIONS.get(case, ())),
            }
        reconciled = all(state in ("consistent", "not-applicable") for state in consistency.values())
        report["execution"] = {"phases_completed": bool(phases_completed), "judge_errors": errors,
                               "cases": observations, "consistency": consistency,
                               "evaluability": evaluability}
        report["execution_valid"] = bool(phases_completed and errors == 0 and reconciled
                                         and all(all(e.values()) for e in observations.values()))
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
    detail = ""
    try:
        execution = json.loads(args.report.read_text())["execution"]
        if not isinstance(execution, dict):
            raise ValueError("Invalid execution record")
        parts = []
        if execution.get("judge_errors"):
            parts.append(f"{execution['judge_errors']} judge errors")
        consistency = execution.get("consistency", {})
        flagged = sorted({state for state in consistency.values()
                          if state not in ("consistent", "not-applicable")}) if isinstance(consistency, dict) else []
        if flagged:
            parts.append("gate/assertion " + ", ".join(flagged))
        detail = f" ({'; '.join(parts)})" if parts else ""
    except (OSError, ValueError, KeyError, TypeError):
        pass
    print("Native execution evidence: " + ("valid; quality score is advisory" if status == 0
                                           else "invalid; blocking" + detail))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
