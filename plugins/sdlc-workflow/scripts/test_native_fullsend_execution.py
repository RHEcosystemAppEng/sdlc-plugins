"""Deterministic execution-policy tests; no agent, credentials or inference."""

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
CASES = {"034-empty": 5, "035-malformed": 5, "036-valid": 7, "037-release": 7}


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


def synthetic_gate_input():
    """SYNTHETIC TEST DATA — fixed allowlisted categories, never live evidence."""
    return {case: {"transcript": "successful", "skill_invocation": "successful",
                   "presence_gate": "successful", "input_validation": "successful"}
            for case in ["036-valid", "037-release"]}


def synthetic_run(tmp_path, passed=20):
    """SYNTHETIC TEST DATA — separate private runtime records and safe report."""
    private = tmp_path / "private"
    run = private / "triage-security-gate/synthetic"
    for case in CASES:
        path = run / f"cases/{case}/output/native/synthetic/iteration-1/output.jsonl"
        path.parent.mkdir(parents=True)
        path.write_text("".join(json.dumps(r) + "\n" for r in synthetic_records()))
        (run / f"cases/{case}/run_result.json").write_text(json.dumps({"exit_code": 1}))
    # Benign judge summary: genuine rationales only, no unparsed-reply fallback.
    (run / "summary.yaml").write_text("per_case: {}\nrationale: SYNTHETIC genuine rationale\n")
    source = {key: "a" * 40 for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = 299
    outcomes = {}
    index = 0
    for case, count in CASES.items():
        outcomes[case] = {}
        for i in range(1, count + 1):
            outcomes[case][f"assertion_{i}"] = index < passed
            index += 1
    status = int(passed != 24)
    report = {"source": source, "complete": True, "total": 24, "passed": passed,
              "exit_code": status, "outcomes": outcomes, "gate_input": synthetic_gate_input(),
              "diagnostics": {
                  "phase": "score" if status else "complete", "code": "phase-exit" if status else "none",
                  "phase_exits": {"workspace": 0, "execute": 1, "collect": 0, "score": status}}}
    safe = tmp_path / "safe/native-result.json"
    safe.parent.mkdir()
    safe.write_text(json.dumps(report))
    return private, run, safe, source, status


@pytest.mark.parametrize("passed", [0, 16, 20, 23, 24])
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
    # Given ADVERSARIAL synthetic runtime evidence and a complete 24/24 judge report
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
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
    assert report["passed"] == 24 and report["complete"] is True


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
    """A complete 24-outcome report cannot hide missing release runtime evidence."""
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    (run / 'cases/037-release/run_result.json').unlink()
    assert checker().assess(private, safe, status, source) == 1
    report = json.loads(safe.read_text())
    assert report['execution_valid'] is False
    assert report['execution']['cases']['037-release']['case_result_valid'] is False


def test_old_native_inventory_is_not_accepted_as_release_coverage(tmp_path):
    """The trusted checker never derives its expected count from the report."""
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    report['total'] = report['passed'] = 17
    report['outcomes'].pop('037-release')
    safe.write_text(json.dumps(report))
    assert checker().assess(private, safe, status, source) == 1


@pytest.mark.parametrize("passed", [0, 23, 24])
def test_judge_api_error_alone_blocks_otherwise_valid_run(tmp_path, passed):
    """A scorer-error summary failure by itself invalidates an otherwise execution-valid run."""
    # Given a report and runner exit that are execution-valid apart from one judge API error
    private, run, safe, source, status = synthetic_run(tmp_path, passed)
    report = json.loads(safe.read_text())
    report["summary_failures"] = [
        {"case": "036-valid", "assertion": "assertion_3", "reason": "scorer-error", "category": "phase-exit"}]
    safe.write_text(json.dumps(report))
    # When the trusted checker assesses the run with the matching runner exit
    assert checker().assess(private, safe, status, source) == 1
    # Then only the judge error invalidates it: phases and execution evidence stay valid
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["judge_errors"] == 1
    assert result["execution"]["phases_completed"] is True
    assert all(all(e.values()) for e in result["execution"]["cases"].values())


def test_judge_api_error_is_counted_on_incomplete_report(tmp_path):
    """A judge API error on an incomplete report is reported as a judge error, not a failed verdict."""
    # Given genuine synthetic execution whose grading stopped on a judge API error (e.g. 400)
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    del report["outcomes"]["036-valid"]["assertion_3"]
    report.update(complete=False, exit_code=1, summary_failures=[
        {"case": "036-valid", "assertion": "assertion_3", "reason": "scorer-error", "category": "phase-exit"}])
    report["diagnostics"].update(phase="summary", code="invalid-summary")
    safe.write_text(json.dumps(report))
    # When the trusted checker assesses the run
    assert checker().assess(private, safe, 1, source) == 1
    # Then the run is invalid and the judge error is counted
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["judge_errors"] == 1


def test_unparsed_judge_reply_blocks_even_when_report_is_complete(tmp_path):
    """The harness's unparsed-reply fallback (scored False) must not pass as a failed verdict."""
    # Given a complete 23/24 report whose single False came from an unusable judge reply
    private, run, safe, source, status = synthetic_run(tmp_path, 23)
    (run / "summary.yaml").write_text(
        "per_case:\n  037-release:\n    assertion_7:\n      value: false\n"
        "      rationale: 'Could not parse judge response: (empty)'\n")
    # When the trusted checker assesses the run
    assert checker().assess(private, safe, status, source) == 1
    # Then the judge error invalidates the run although execution evidence is genuine
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["judge_errors"] == 1
    assert result["passed"] == 23 and result["complete"] is True


def test_genuine_failed_verdict_has_no_judge_errors(tmp_path):
    """A real False verdict stays advisory: zero judge errors, execution valid."""
    # Given a complete 23/24 report whose False verdict carries a genuine rationale
    private, run, safe, source, status = synthetic_run(tmp_path, 23)
    (run / "summary.yaml").write_text(
        "per_case:\n  037-release:\n    assertion_7:\n      value: false\n"
        "      rationale: SYNTHETIC genuine failing rationale\n")
    # When the trusted checker assesses the run
    assert checker().assess(private, safe, status, source) == 0
    # Then the failed verdict lowers only the advisory score
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is True
    assert result["execution"]["judge_errors"] == 0


def test_symlinked_summary_blocks(tmp_path):
    """A symlinked private summary cannot be trusted for judge-error detection."""
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    target = tmp_path / "outside.yaml"
    target.write_text("per_case: {}\n")
    (run / "summary.yaml").unlink()
    (run / "summary.yaml").symlink_to(target)
    assert checker().assess(private, safe, status, source) == 1


def test_missing_summary_blocks_complete_report(tmp_path):
    """A complete report whose private summary.yaml is missing is a judge error (fail-closed)."""
    # Given a complete, otherwise execution-valid 24/24 run without its judge summary
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    (run / "summary.yaml").unlink()
    # When the trusted checker assesses the run
    assert checker().assess(private, safe, status, source) == 1
    # Then the unverifiable judge results invalidate the run
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["judge_errors"] == 1
    assert result["execution"]["phases_completed"] is True


GATE_ASSERTIONS = {"036-valid": "assertion_2", "037-release": "assertion_1"}
DEPENDENTS = {"036-valid": ["assertion_1", "assertion_3", "assertion_4", "assertion_5",
                            "assertion_6", "assertion_7"],
              "037-release": [f"assertion_{i}" for i in range(2, 8)]}


def set_gate_verdict(report, case, verdict):
    """Keep the synthetic aggregate counts consistent with one changed gate verdict."""
    report["outcomes"][case][GATE_ASSERTIONS[case]] = verdict
    report["passed"] = sum(v is True for values in report["outcomes"].values() for v in values.values())
    status = int(report["passed"] != report["total"])
    report["exit_code"] = report["diagnostics"]["phase_exits"]["score"] = status
    report["diagnostics"].update(phase="score" if status else "complete",
                                 code="phase-exit" if status else "none")
    return status


@pytest.mark.parametrize("case,step", [("036-valid", "presence_gate"), ("037-release", "input_validation")])
@pytest.mark.parametrize("category", ["tool-error", "unexpected-output", "conflicting-results"])
def test_passing_gate_judgment_contradicting_observed_failure_invalidates(tmp_path, case, step, category):
    """A judge cannot pass a gate assertion while the same run observed that step failing."""
    # Given an observed gate/input failure and a passing judgment for that gate assertion
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    status = set_gate_verdict(report, case, True)
    report["gate_input"][case][step] = category
    safe.write_text(json.dumps(report))
    # When the trusted checker reconciles judgments with observed evidence
    assert checker().assess(private, safe, status, source) == 1
    # Then the scored run is invalid and the contradiction is published safely
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["consistency"][case] == "contradiction"
    assert result["execution"]["evaluability"][case] == {
        "evaluable": False, "not_evaluable_assertions": DEPENDENTS[case]}
    assert result["outcomes"][case][GATE_ASSERTIONS[case]] is True
    assert result["passed"] == 24 and result["execution"]["judge_errors"] == 0
    assert "SYNTHETIC" not in safe.read_text()


@pytest.mark.parametrize("case,step", [("036-valid", "presence_gate"), ("037-release", "input_validation")])
@pytest.mark.parametrize("category", ["not-observed", "invalid-transcript"])
def test_passing_gate_judgment_without_usable_evidence_is_inconclusive(tmp_path, case, step, category):
    """Missing or invalid evidence is inconclusive rather than a behavior finding."""
    # Given published evidence that the required step was never usable
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    status = set_gate_verdict(report, case, True)
    report["gate_input"][case][step] = category
    safe.write_text(json.dumps(report))
    # When the trusted checker reconciles the judgment with that evidence
    assert checker().assess(private, safe, status, source) == 1
    # Then the run is invalid and the case is not presented as evaluated
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["consistency"][case] == "inconclusive"
    assert result["execution"]["evaluability"][case]["evaluable"] is False


def test_passing_release_judgment_without_skill_invocation_is_inconclusive(tmp_path):
    """Release assertion 1 claims the Skill ran, so missing invocation evidence contradicts it."""
    # Given successful gate/input steps but no observed Skill invocation
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    report["gate_input"]["037-release"]["skill_invocation"] = "not-observed"
    status = set_gate_verdict(report, "037-release", True)
    safe.write_text(json.dumps(report))
    # When reconciling the release gate assertion with its required evidence
    assert checker().assess(private, safe, status, source) == 1
    # Then the missing invocation is inconclusive, not a passing behavior result
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["consistency"]["037-release"] == "inconclusive"
    assert result["passed"] == 24


@pytest.mark.parametrize("case,step", [("036-valid", "presence_gate"), ("037-release", "input_validation")])
def test_failed_gate_judgment_without_usable_evidence_is_inconclusive(tmp_path, case, step):
    """A failed verdict with no usable evidence is inconclusive, never a behavior finding."""
    # Given missing gate/input evidence and a failed judgment
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    report["gate_input"][case][step] = "not-observed"
    status = set_gate_verdict(report, case, False)
    safe.write_text(json.dumps(report))
    # When reconciling the failed verdict with that evidence
    assert checker().assess(private, safe, status, source) == 1
    # Then the case is not presented as an observed behavior result
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["consistency"][case] == "inconclusive"
    assert result["execution"]["evaluability"][case]["evaluable"] is False


@pytest.mark.parametrize("case", ["036-valid", "037-release"])
def test_genuine_failed_gate_judgment_remains_a_behavior_result(tmp_path, case):
    """A real failed gate verdict stays advisory while its dependent assertions are not evaluable."""
    # Given observed-successful gate/input execution and a genuine failed gate verdict
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    status = set_gate_verdict(report, case, False)
    safe.write_text(json.dumps(report))
    # When the trusted checker reconciles the judgment with observed success
    assert checker().assess(private, safe, status, source) == 0
    # Then only the advisory score changes and downstream assertions are not evaluable
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is True
    assert result["execution"]["consistency"][case] == "consistent"
    assert result["execution"]["evaluability"][case] == {
        "evaluable": False, "not_evaluable_assertions": DEPENDENTS[case]}
    assert result["outcomes"][case][GATE_ASSERTIONS[case]] is False
    assert result["passed"] == 23 and result["complete"] is True
    assert result["execution"]["judge_errors"] == 0


def test_observed_gate_failure_with_failed_judgment_is_a_behavior_result(tmp_path):
    """An observed tool error plus a failed gate verdict stays a behavior result, not a contradiction."""
    # Given an observed tool error and a judge that failed the same gate assertion
    private, run, safe, source, _ = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    report["gate_input"]["036-valid"]["presence_gate"] = "tool-error"
    status = set_gate_verdict(report, "036-valid", False)
    safe.write_text(json.dumps(report))
    # When the trusted checker reconciles the two observations
    assert checker().assess(private, safe, status, source) == 0
    # Then the failure is preserved as a behavior result with no contradiction
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is True
    assert result["execution"]["consistency"]["036-valid"] == "consistent"
    assert result["execution"]["evaluability"]["036-valid"]["evaluable"] is False
    assert result["passed"] == 23


@pytest.mark.parametrize("damage", ["missing", "unknown-category", "missing-case", "missing-key",
                                   "not-mapping", "non-string", "absent-with-success",
                                   "unreadable-with-success"])
def test_unvalidated_gate_input_blocks_even_with_complete_outcomes(tmp_path, damage):
    """Only allowlisted categories for both setup-dependent cases can establish evidence."""
    # Given a complete 24/24 report whose published categories are unusable
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    report = json.loads(safe.read_text())
    if damage == "missing":
        del report["gate_input"]
    elif damage == "unknown-category":
        report["gate_input"]["036-valid"]["presence_gate"] = "unknown-category"
    elif damage == "missing-case":
        del report["gate_input"]["037-release"]
    elif damage == "missing-key":
        del report["gate_input"]["036-valid"]["input_validation"]
    elif damage == "not-mapping":
        report["gate_input"]["036-valid"] = "unknown-category"
    elif damage == "absent-with-success":
        report["gate_input"]["036-valid"]["transcript"] = "not-observed"
    elif damage == "unreadable-with-success":
        report["gate_input"]["037-release"]["transcript"] = "invalid-transcript"
    else:
        report["gate_input"]["036-valid"]["presence_gate"] = True
    safe.write_text(json.dumps(report))
    # When the trusted checker validates the safe observations
    assert checker().assess(private, safe, status, source) == 1
    # Then execution stays invalid without inventing an evaluated case
    result = json.loads(safe.read_text())
    assert result["execution_valid"] is False
    assert result["execution"]["consistency"]["036-valid"] == "invalid-input"
    assert result["execution"]["consistency"]["037-release"] == "invalid-input"
    assert result["execution"]["evaluability"]["036-valid"]["evaluable"] is False
    assert result["passed"] == 24 and result["complete"] is True


def test_non_gated_cases_stay_evaluable_without_gate_evidence(tmp_path):
    """Former behavior of the two bootstrap cases is preserved by the new contract."""
    # Given a complete, otherwise execution-valid run
    private, run, safe, source, status = synthetic_run(tmp_path, 24)
    # When the trusted checker publishes evaluability
    assert checker().assess(private, safe, status, source) == 0
    result = json.loads(safe.read_text())
    # Then only the setup-dependent cases are reconciled against gate/input evidence
    assert result["execution"]["consistency"] == {"034-empty": "not-applicable", "035-malformed": "not-applicable",
                                                 "036-valid": "consistent", "037-release": "consistent"}
    assert result["execution"]["evaluability"]["034-empty"] == {"evaluable": True, "not_evaluable_assertions": []}
    assert result["execution"]["evaluability"]["035-malformed"] == {"evaluable": True,
                                                                   "not_evaluable_assertions": []}
    assert result["execution"]["evaluability"]["036-valid"]["evaluable"] is True
