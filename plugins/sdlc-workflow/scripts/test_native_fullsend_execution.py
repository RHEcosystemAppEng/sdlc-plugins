"""Deterministic execution-policy tests; no agent, credentials or inference."""

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
CASES = {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7, "037-release": 7}


def checker():
    """Load the trusted checker without executing its command-line entry point."""
    path = ROOT / ".github/scripts/check-native-fullsend-execution.py"
    spec = importlib.util.spec_from_file_location("native_execution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_records():
    """SYNTHETIC TEST DATA — actual-shaped paired tools, never live eval evidence."""
    return [
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "skill", "name": "Skill", "input": {
                "skill": "sdlc-workflow:triage-security", "args": "TC-8101"}}]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "skill", "content": "Launching skill"}]},
         "tool_use_result": {"success": True, "commandName": "sdlc-workflow:triage-security"}},
        {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "bash", "name": "Bash", "input": {
                "command": "SYNTHETIC TEST ONLY"}}]}},
        {"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "bash", "is_error": True,
             "content": "Exit code 1\nSYNTHETIC expected input rejection"}]}},
        {"type": "result", "subtype": "success", "is_error": False},
    ]


def synthetic_run(tmp_path, passed=20):
    """SYNTHETIC TEST DATA — separate private runtime records and safe report."""
    private = tmp_path / "private"
    run = private / "triage-security-gate/synthetic"
    for case in CASES:
        path = run / f"cases/{case}/output/native/synthetic/iteration-1/output.jsonl"
        path.parent.mkdir(parents=True)
        path.write_text("".join(json.dumps(r) + "\n" for r in synthetic_records()))
        (run / f"cases/{case}/run_result.json").write_text(json.dumps({"exit_code": 1}))
    source = {key: "a" * 40 for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = 299
    outcomes = {}
    index = 0
    for case, count in CASES.items():
        outcomes[case] = {}
        for i in range(1, count + 1):
            outcomes[case][f"assertion_{i}"] = index < passed
            index += 1
    status = int(passed != 28)
    report = {"source": source, "complete": True, "total": 28, "passed": passed,
              "exit_code": status, "outcomes": outcomes, "diagnostics": {
                  "phase": "score" if status else "complete", "code": "phase-exit" if status else "none",
                  "phase_exits": {"workspace": 0, "execute": 1, "collect": 0, "score": status}}}
    safe = tmp_path / "safe/native-result.json"
    safe.parent.mkdir()
    safe.write_text(json.dumps(report))
    return private, run, safe, source, status


@pytest.mark.parametrize("passed", [0, 16, 20, 27, 28])
def test_quality_scores_are_advisory_with_genuine_execution(tmp_path, passed):
    """Completed tool execution accepts expected negative exits at every quality score."""
    # Given synthetic expected input rejection with a separate judge score
    private, run, safe, source, status = synthetic_run(tmp_path, passed)
    originals = {p: p.read_bytes() for p in run.rglob("*") if p.is_file()}
    original_report = json.loads(safe.read_text())
    # When enforcing the trusted execution policy
    assert checker().assess(private, safe, status, source) == 0
    # Then genuine execution passes, while original scores and raw records stay intact
    report = json.loads(safe.read_text())
    assert report["execution_valid"] is True
    assert all(report[k] == v for k, v in original_report.items())
    assert all(p.read_bytes() == raw for p, raw in originals.items())
    assert all(all(e.values()) for e in report["execution"]["cases"].values())
    assert "SYNTHETIC expected input rejection" not in safe.read_text()


@pytest.mark.parametrize("defect", [
    "missing", "empty", "malformed", "truncated", "symlink", "symlink-parent",
    "narration", "missing-skill-result", "wrong-skill", "failed-skill", "wrong-id",
    "wrong-role", "future-result", "duplicate-id", "missing-bash-result", "no-completion",
    "runtime-error", "unexpected-cli-exit", "duplicate-json-key",
])
def test_missing_or_invalid_execution_blocks_even_complete_judgments(tmp_path, defect):
    """A complete grading summary cannot turn bootstrap or broken tool evidence green."""
    # Given ADVERSARIAL synthetic runtime evidence and a complete 28/28 judge report
    private, run, safe, source, status = synthetic_run(tmp_path, 28)
    path = run / "cases/035-malformed/output/native/synthetic/iteration-1/output.jsonl"
    records = synthetic_records()
    if defect == "narration":
        records = [{"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "text", "text": json.dumps(records)}]}}, records[-1]]
    elif defect == "missing-skill-result": del records[1]
    elif defect == "wrong-skill": records[0]["message"]["content"][0]["input"]["skill"] = "other"
    elif defect == "failed-skill": records[1]["tool_use_result"]["success"] = False
    elif defect == "wrong-id": records[3]["message"]["content"][0]["tool_use_id"] = "unmatched"
    elif defect == "wrong-role": records[0]["message"]["role"] = "user"
    elif defect == "future-result": records[2:4] = [records[3], records[2]]
    elif defect == "duplicate-id": records.insert(3, records[2])
    elif defect == "missing-bash-result": del records[3]
    elif defect == "no-completion": records.pop()
    elif defect == "runtime-error": records[-1].update(subtype="error_during_execution", is_error=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    if defect == "missing": path.unlink()
    elif defect == "empty": path.write_text("")
    elif defect == "malformed": path.write_text(path.read_text() + '{"broken":\n')
    elif defect == "truncated": path.write_text(path.read_text().rstrip("\n"))
    elif defect == "duplicate-json-key": path.write_text('{"type":"result","type":"result"}\n')
    elif defect == "symlink":
        target = tmp_path / "outside.jsonl"
        path.rename(target)
        path.symlink_to(target)
    elif defect == "symlink-parent":
        target = tmp_path / "outside"
        path.parent.rename(target)
        path.parent.symlink_to(target, target_is_directory=True)
    elif defect == "unexpected-cli-exit":
        (run / "cases/035-malformed/run_result.json").write_text('{"exit_code": 137}')
    # When evaluating execution independently of the all-pass score
    assert checker().assess(private, safe, status, source) == 1
    # Then only allowlisted failure observations are published
    report = json.loads(safe.read_text())
    assert report["execution_valid"] is False
    assert report["passed"] == 28 and report["complete"] is True


@pytest.mark.parametrize("defect", ["source", "incomplete", "missing-outcome", "non-boolean",
                                      "workspace", "collect", "score", "runner", "execute", "ambiguous-run"])
def test_invalid_reports_or_infrastructure_phases_block(tmp_path, defect):
    """Valid tools cannot override an incomplete, unrelated or failed infrastructure run."""
    # Given genuine synthetic tool records with damaged report/phase provenance
    private, run, safe, source, status = synthetic_run(tmp_path)
    report = json.loads(safe.read_text())
    if defect == "source": report["source"]["head_sha"] = "b" * 40
    elif defect == "incomplete": report["complete"] = False
    elif defect == "missing-outcome": del report["outcomes"]["035-malformed"]["assertion_1"]
    elif defect == "non-boolean": report["outcomes"]["035-malformed"]["assertion_1"] = 1
    elif defect in {"workspace", "collect", "score", "execute"}:
        report["diagnostics"]["phase_exits"][defect] = 7
    elif defect == "runner": status = 7
    elif defect == "ambiguous-run": (run.parent / "another-run").mkdir()
    safe.write_text(json.dumps(report))
    # When the real checker evaluates the report and private evidence
    assert checker().assess(private, safe, status, source) == 1
    # Then runtime/report integrity remains blocking regardless of score
    assert json.loads(safe.read_text())["execution_valid"] is False


@pytest.mark.parametrize("invalid_error", [None, "false", 0])
def test_later_malformed_bash_result_cannot_inherit_earlier_success(tmp_path, invalid_error):
    """Every matched Bash result must be well formed, even after a valid roundtrip."""
    # Given two synthetic Bash calls after Skill launch; only the first is valid
    private, run, safe, source, status = synthetic_run(tmp_path)
    path = run / "cases/036-valid/output/native/synthetic/iteration-1/output.jsonl"
    records = synthetic_records()
    later_call, later_result = json.loads(json.dumps(records[2:4]))
    later_call["message"]["content"][0]["id"] = "later"
    later_result["message"]["content"][0]["tool_use_id"] = "later"
    if invalid_error is None:
        del later_result["message"]["content"][0]["is_error"]
    else:
        later_result["message"]["content"][0]["is_error"] = invalid_error
    records[-1:-1] = [later_call, later_result]
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    # When inspecting all actual-shaped tool result records
    assert checker().assess(private, safe, status, source) == 1
    # Then earlier valid tool evidence does not mask the malformed later result
    assert json.loads(safe.read_text())["execution_valid"] is False


@pytest.mark.parametrize("invalid_error", [None, 0, 1, "true", "false", [], {}])
def test_skill_result_rejects_non_boolean_error_when_present(tmp_path, invalid_error):
    """A present malformed Skill error flag cannot count as successful execution."""
    # Given ADVERSARIAL synthetic Skill metadata with a non-Boolean error flag
    private, run, safe, source, status = synthetic_run(tmp_path)
    path = run / "cases/036-valid/output/native/synthetic/iteration-1/output.jsonl"
    records = synthetic_records()
    records[1]["message"]["content"][0]["is_error"] = invalid_error
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    # When checking actual-shaped paired execution records
    assert checker().assess(private, safe, status, source) == 1
    # Then malformed Skill evidence fails even though launch metadata claims success
    assert json.loads(safe.read_text())["execution_valid"] is False


@pytest.mark.parametrize("is_error,expected", [(False, 0), (True, 1)])
def test_skill_result_honors_boolean_error_flag(tmp_path, is_error, expected):
    """Explicit Boolean Skill errors reject execution while false preserves launch."""
    # Given a well-formed synthetic Skill result with explicit error status
    private, run, safe, source, status = synthetic_run(tmp_path)
    path = run / "cases/036-valid/output/native/synthetic/iteration-1/output.jsonl"
    records = synthetic_records()
    records[1]["message"]["content"][0]["is_error"] = is_error
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    # When checking Skill launch and subsequent tool execution
    assert checker().assess(private, safe, status, source) == expected
    # Then the explicit error status controls validity
    assert json.loads(safe.read_text())["execution_valid"] is (not is_error)


def test_missing_release_execution_stays_blocking(tmp_path):
    """A complete 28-outcome report cannot hide missing release runtime evidence."""
    private, run, safe, source, status = synthetic_run(tmp_path, 28)
    (run / 'cases/037-release/run_result.json').unlink()
    assert checker().assess(private, safe, status, source) == 1
    report = json.loads(safe.read_text())
    assert report['execution_valid'] is False
    assert report['execution']['cases']['037-release']['case_result_valid'] is False


def test_old_native_inventory_is_not_accepted_as_release_coverage(tmp_path):
    """The trusted checker never derives its expected count from the report."""
    private, run, safe, source, status = synthetic_run(tmp_path, 28)
    report = json.loads(safe.read_text())
    report['total'] = report['passed'] = 21
    report['outcomes'].pop('037-release')
    safe.write_text(json.dumps(report))
    assert checker().assess(private, safe, status, source) == 1
