"""Deterministic native-eval contracts; these tests never execute an agent."""

import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tarfile

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "evals/fullsend/triage-security"
FIXTURES = ROOT / "evals/triage-security/files"


def load_script(path):
    """Import test tooling without starting the external model runtime."""
    assert path.is_file(), f"Missing native eval tooling: {path}"
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def synthetic_fixture_root(path):
    """SYNTHETIC TEST DATA — isolated unchanged retained inputs, never live data."""
    fixtures = path / "evals/triage-security/files"
    fixtures.mkdir(parents=True)
    for name in ["fullsend-gate-interactive-config.md", "fullsend-invalid-trusted-input.md",
                 "fullsend-report-only-trusted-input.json"]:
        shutil.copy2(FIXTURES / name, fixtures / name)
    return path


def synthetic_judge_summary(value=True):
    """SYNTHETIC STATIC RECORDS — summary contract only, never live eval evidence."""
    cases = {}
    for case, count in zip(["033-absent", "034-empty", "035-malformed", "036-valid", "037-release"], [4, 5, 5, 7, 7]):
        cases[case] = {}
        for index in range(1, 8):
            condition = f'annotations.get("assertion_count", 0) > {index - 1}'
            cases[case][f"assertion_{index}"] = {
                "value": value if index <= count else None,
                "rationale": "SYNTHETIC NOT A JUDGMENT" if index <= count else f"Skipped: condition '{condition}' is false",
                "judge_type": "llm",
            }
    return {"run_id": "synthetic", "per_case": cases}


def synthetic_valid_tool_records():
    """SYNTHETIC TEST DATA — native-shaped records, never real execution evidence."""
    skill = (ROOT / "plugins/sdlc-workflow/skills/triage-security/SKILL.md").read_text()
    gate = skill.split("### Step 0.6", 1)[1].split("```bash\n", 1)[1].split("\n```", 1)[0]
    validation = skill.split("### Step 0.7", 1)[1].split("```bash\n", 1)[1].split("\n```", 1)[0]
    validation = validation.replace("${CLAUDE_PLUGIN_ROOT}", "/sandbox/claude-config/plugins/sdlc-workflow")
    records = []
    for name, identity, inputs, result in [
        ("Skill", "skill", {"skill": "sdlc-workflow:triage-security", "args": "TC-8101"}, "Skill loaded"),
        ("Bash", "gate", {"command": gate}, "sandbox mode: /sandbox/workspace/output"),
        ("Bash", "input", {"command": validation}, "Trusted triage-security input available"),
    ]:
        records.append({"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "name": name, "id": identity, "input": inputs}]}})
        records.append({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": identity, "content": result, "is_error": False}]}})
    return records


def write_synthetic_valid_transcript(run_dir, records):
    """Write explicitly synthetic native-format test records inside the case layout."""
    path = run_dir / "cases/036-valid/output/native/synthetic/iteration-1/transcripts/test.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records))
    return path


def test_safe_report_observes_matched_valid_tools_without_changing_scores(tmp_path):
    """Actual paired records yield fixed observations while false judgments stay false."""
    # Given synthetic native-format tool records and an unchanged failed summary
    common = load_script(ROOT / "evals/fullsend/run.py")
    run_dir = tmp_path / "synthetic"
    transcript = write_synthetic_valid_transcript(run_dir, synthetic_valid_tool_records())
    (run_dir / "summary.yaml").write_text(yaml.safe_dump(synthetic_judge_summary(False)))
    original = {path: path.read_bytes() for path in [transcript, run_dir / "summary.yaml"]}
    source = {key: "a" * 40 for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = 299
    # When publishing the real safe artifact without executing an agent
    common.publish_report(run_dir, tmp_path / "safe", source, 7)
    report = json.loads((tmp_path / "safe/native-result.json").read_text())
    # Then only fixed Boolean observations leave the host, with scores and bytes intact
    assert report.get("valid_case_tools") == {
        "transcript_found": True, "transcript_readable": True, "skill_invoked": True,
        "presence_gate_succeeded": True, "presence_gate_failed": False,
        "input_validation_succeeded": True, "input_validation_failed": False,
    }
    assert report["source"] == source and report["exit_code"] == 7
    assert report["complete"] is True and report["passed"] == 0 and report["total"] == 28
    assert all(value is False for case in report["outcomes"].values() for value in case.values())
    assert all(path.read_bytes() == raw for path, raw in original.items())
    assert "command" not in json.dumps(report) and "tool_use_id" not in json.dumps(report)


@pytest.mark.parametrize("defect", [
    "narration", "quoted-json", "quoted-command", "wrong-tool", "wrong-id", "future-result",
    "malformed", "truncated", "empty", "missing", "symlink-file", "symlink-directory",
    "missing-role", "wrong-role", "missing-error", "error", "wrong-output",
])
def test_valid_tool_observations_do_not_infer_gate_success(tmp_path, defect):
    """Adversarial and incomplete records cannot substitute for a matching gate result."""
    # Given ADVERSARIAL TEST FIXTURES built from explicitly synthetic records
    common = load_script(ROOT / "evals/fullsend/run.py")
    records = synthetic_valid_tool_records()
    call, result = records[2], records[3]
    gate = call["message"]["content"][0]
    output = result["message"]["content"][0]
    if defect in {"narration", "quoted-json"}:
        records = [{"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "text", "text": "SECRET " + json.dumps(records)}]}}]
    elif defect == "quoted-command":
        gate["input"]["command"] = "echo " + json.dumps(gate["input"]["command"])
    elif defect == "wrong-tool":
        gate["name"] = "Read"
    elif defect == "wrong-id":
        output["tool_use_id"] = "unmatched"
    elif defect == "future-result":
        records[2:4] = [result, call]
    elif defect == "missing-role":
        call.pop("type")
        call["message"].pop("role")
    elif defect == "wrong-role":
        call["message"]["role"] = "user"
    elif defect == "missing-error":
        output.pop("is_error")
    elif defect == "error":
        output["is_error"] = True
    elif defect == "wrong-output":
        output["content"] = "sandbox mode: /wrong SECRET"
    transcript = write_synthetic_valid_transcript(tmp_path, records)
    if defect == "malformed":
        transcript.write_text(transcript.read_text() + '{"SECRET":\n')
    elif defect == "truncated":
        transcript.write_text(transcript.read_text().rstrip("\n"))
    elif defect == "empty":
        transcript.write_text("")
    elif defect == "missing":
        transcript.unlink()
    elif defect == "symlink-file":
        outside = tmp_path / "private.jsonl"
        transcript.rename(outside)
        transcript.symlink_to(outside)
    elif defect == "symlink-directory":
        outside = tmp_path / "private-transcripts"
        transcript.parent.rename(outside)
        transcript.parent.symlink_to(outside, target_is_directory=True)
    # When extracting advisory flags without any inference
    observed = common.valid_case_tool_observations(tmp_path)
    # Then no gate success is invented and malformed/missing evidence stays visible
    assert observed["presence_gate_succeeded"] is False
    assert all(type(value) is bool for value in observed.values())
    assert "SECRET" not in json.dumps(observed)
    assert observed["transcript_found"] is (defect != "missing")
    assert observed["transcript_readable"] is (defect not in {
        "malformed", "truncated", "empty", "missing", "symlink-file", "symlink-directory"})
    assert observed["presence_gate_failed"] is (defect in {"missing-error", "error", "wrong-output"})


@pytest.mark.parametrize("kind,index", [("presence_gate", 3), ("input_validation", 5)])
def test_valid_tool_observations_preserve_mixed_success_and_failure(tmp_path, kind, index):
    """Conflicting actual paired results remain visible rather than overwriting each other."""
    # Given SYNTHETIC TEST DATA with one successful call and another failed call
    common = load_script(ROOT / "evals/fullsend/run.py")
    records = synthetic_valid_tool_records()
    repeated = json.loads(json.dumps(records[index - 1:index + 1]))
    repeated[0]["message"]["content"][0]["id"] = "repeated"
    repeated[1]["message"]["content"][0].update(tool_use_id="repeated", is_error=True, content="SECRET")
    records.extend(repeated)
    records[index]["message"]["content"][0]["content"] = [
        {"type": "text", "text": records[index]["message"]["content"][0]["content"]}]
    write_synthetic_valid_transcript(tmp_path, records)
    # When observing real-format records with text-block result content
    observed = common.valid_case_tool_observations(tmp_path)
    # Then both observations survive without exporting raw diagnostic text
    assert observed[kind + "_succeeded"] is True
    assert observed[kind + "_failed"] is True
    assert "SECRET" not in json.dumps(observed)


@pytest.mark.parametrize("skill,args", [("different-skill", "TC-8101"), ("sdlc-workflow:triage-security", "TC-9999")])
def test_valid_tool_observations_require_the_actual_skill_and_task(tmp_path, skill, args):
    """Other Skill names or tasks cannot count as the tested invocation."""
    # Given SYNTHETIC TEST DATA containing the wrong invocation
    common = load_script(ROOT / "evals/fullsend/run.py")
    records = synthetic_valid_tool_records()
    records[0]["message"]["content"][0]["input"] = {"skill": skill, "args": args}
    write_synthetic_valid_transcript(tmp_path, records)
    # When observing the tested case
    observed = common.valid_case_tool_observations(tmp_path)
    # Then neither a different skill nor a different issue establishes invocation
    assert observed["skill_invoked"] is False


@pytest.mark.parametrize("record", [None, [], {"type": []}, {"type": "user", "message": []}])
def test_valid_tool_observations_handle_untrusted_record_shapes(tmp_path, record):
    """Unexpected JSON shapes cannot prevent publishing or invent a tool observation."""
    # Given ADVERSARIAL TEST FIXTURES with arbitrary valid JSON shapes
    common = load_script(ROOT / "evals/fullsend/run.py")
    write_synthetic_valid_transcript(tmp_path, [record])
    # When parsing incomplete evidence without inference
    observed = common.valid_case_tool_observations(tmp_path)
    # Then the safe fixed flags survive and no success is fabricated
    assert observed["presence_gate_succeeded"] is False
    assert observed["input_validation_succeeded"] is False
    assert observed["skill_invoked"] is False


def test_valid_tool_observations_reject_duplicate_tool_ids(tmp_path):
    """Ambiguous repeated IDs cannot bind a result to an earlier different tool."""
    # Given ADVERSARIAL TEST FIXTURE — another tool reuses a pending Bash ID
    common = load_script(ROOT / "evals/fullsend/run.py")
    records = synthetic_valid_tool_records()
    records.insert(3, {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": "Read", "id": "gate", "input": {"file_path": "SECRET"}}]}})
    write_synthetic_valid_transcript(tmp_path, records)
    # When interpreting an ambiguous transcript
    observed = common.valid_case_tool_observations(tmp_path)
    # Then partial records cannot establish genuine success
    assert observed["transcript_readable"] is False
    assert observed["presence_gate_succeeded"] is False
    assert observed["input_validation_succeeded"] is False


def test_valid_tool_observations_handle_unreadable_transcripts(tmp_path, monkeypatch):
    """Unreadable native evidence leaves explicit incompleteness without suppressing reporting."""
    # Given SYNTHETIC TEST DATA whose transcript cannot be opened
    common = load_script(ROOT / "evals/fullsend/run.py")
    transcript = write_synthetic_valid_transcript(tmp_path, synthetic_valid_tool_records())
    original_open = Path.open
    def denied(path, *args, **kwargs):
        """Simulate an actual file-open denial only for the native transcript."""
        if path == transcript:
            raise PermissionError("SECRET")
        return original_open(path, *args, **kwargs)
    monkeypatch.setattr(Path, "open", denied)
    # When observing the inaccessible transcript
    observed = common.valid_case_tool_observations(tmp_path)
    # Then raw errors stay private and success stays unproven
    assert observed["transcript_found"] is True and observed["transcript_readable"] is False
    assert observed["presence_gate_succeeded"] is False
    assert observed["input_validation_succeeded"] is False
    assert "SECRET" not in json.dumps(observed)


def test_valid_tool_observations_handle_excessive_json_nesting(tmp_path):
    """Untrusted parser-depth failures cannot abort the source-bound safe report."""
    # Given ADVERSARIAL TEST FIXTURE — deeply nested JSON, not execution evidence
    common = load_script(ROOT / "evals/fullsend/run.py")
    transcript = write_synthetic_valid_transcript(tmp_path, [])
    transcript.write_text("[" * 30000 + "0" + "]" * 30000 + "\n")
    # When the parser encounters evidence beyond its depth limit
    observed = common.valid_case_tool_observations(tmp_path)
    # Then incompleteness is visible and cannot establish success
    assert observed["transcript_found"] is True and observed["transcript_readable"] is False
    assert observed["presence_gate_succeeded"] is False
    assert observed["input_validation_succeeded"] is False


@pytest.mark.parametrize("value", [True, False])
def test_summary_integrity_accepts_complete_boolean_results_without_grading(tmp_path, value):
    """Completeness accepts actual False outcomes; upstream alone owns thresholds."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given 28 explicitly synthetic Boolean outcomes and seven legitimate skips
    path = tmp_path / "summary.yaml"
    raw = yaml.safe_dump(synthetic_judge_summary(value)).encode()
    path.write_bytes(raw)
    # When checking integrity without any scorer or runtime invocation
    common.validate_summary(tmp_path, "synthetic")
    # Then raw outcomes/rationales remain byte-for-byte intact, including False
    assert path.read_bytes() == raw


@pytest.mark.parametrize("defect", [
    "missing-case", "extra-case", "wrong-case", "missing-assertion", "extra-assertion",
    "missing-value", "null", "integer", "string", "error", "applicable-skip",
    "false-with-skip", "nonapplicable-boolean", "nonapplicable-error", "condition-error",
    "wrong-run", "not-mapping", "case-not-mapping", "result-not-mapping",
])
def test_summary_integrity_rejects_incomplete_or_ambiguous_results(tmp_path, defect):
    """Static malformed summary records must never allow aggregate-only CI success."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given adversarial synthetic metadata, never generated execution/judge evidence
    summary = synthetic_judge_summary()
    cases = summary["per_case"]
    results = cases["033-absent"]
    result = results["assertion_1"]
    if defect == "missing-case":
        del cases["036-valid"]
    elif defect == "extra-case":
        cases["unexpected"] = results
    elif defect == "wrong-case":
        cases["wrong-valid"] = cases.pop("036-valid")
    elif defect == "missing-assertion":
        del results["assertion_1"]
    elif defect == "extra-assertion":
        results["assertion_8"] = result
    elif defect == "missing-value":
        del result["value"]
    elif defect in ["null", "integer", "string"]:
        result["value"] = {"null": None, "integer": 1, "string": "true"}[defect]
    elif defect == "error":
        result["error"] = "SYNTHETIC scorer failure, even with a Boolean value"
    elif defect == "applicable-skip":
        results["assertion_1"] = dict(results["assertion_5"])
    elif defect == "false-with-skip":
        result.update(value=False, rationale="Skipped: synthetic invalid applicable skip")
    elif defect == "nonapplicable-boolean":
        results["assertion_5"]["value"] = True
    elif defect == "nonapplicable-error":
        results["assertion_5"]["error"] = "SYNTHETIC condition failure"
    elif defect == "condition-error":
        results["assertion_5"]["rationale"] = "Condition error: SYNTHETIC failure"
    elif defect == "wrong-run":
        summary["run_id"] = "different-run"
    elif defect == "not-mapping":
        summary = []
    elif defect == "case-not-mapping":
        cases["033-absent"] = []
    else:
        results["assertion_1"] = []
    path = tmp_path / "summary.yaml"
    raw = yaml.safe_dump(summary).encode()
    path.write_bytes(raw)
    # When validating the preserved upstream artifact, fail closed without rewriting
    with pytest.raises(ValueError, match="summary"):
        common.validate_summary(tmp_path, "synthetic")
    assert path.read_bytes() == raw


@pytest.mark.parametrize("raw", [None, b"[invalid", b"run_id: synthetic\nrun_id: synthetic\n",
                                b"per_case:\n  033-absent: {}\n  033-absent: {}\n"])
def test_summary_integrity_rejects_missing_invalid_or_duplicate_yaml(tmp_path, raw):
    """Missing, unparsable and duplicate-key artifacts are not unambiguous results."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given explicitly synthetic raw YAML or no summary artifact
    path = tmp_path / "summary.yaml"
    if raw is not None:
        path.write_bytes(raw)
    with pytest.raises(ValueError, match="summary"):
        common.validate_summary(tmp_path, "synthetic")
    assert path.read_bytes() == raw if raw is not None else not path.exists()


def test_ordinary_evals_preserve_baseline_and_exclude_native_cases():
    """Ordinary Claude evals must not accidentally execute native-only scenarios."""
    # Given the manifests consumed by the existing hosted run-evals
    triage = json.loads((ROOT / "evals/triage-security/evals.json").read_text())["evals"]
    verify = json.loads((ROOT / "evals/verify-pr/evals.json").read_text())["evals"]
    # Then native cases are separate and every retained object is unchanged
    assert [c["id"] for c in triage] == list(range(1, 33))
    assert sum(len(c["assertions"]) for c in triage) == 166
    assert len(verify) == 6 and sum(len(c["assertions"]) for c in verify) == 68
    # TC-6820 appends exactly two release assertions and one prompt suffix to case1.
    # Hash the retained prefix and all other cases against the original baseline.
    baseline = json.loads(json.dumps(triage))
    suffix = ' In outputs/remediation.md also explain the Step 7.5 release orchestration confirmations and dedup decision before proposing remediation; retain all existing outputs and do not claim any Jira operation was performed.'
    assert baseline[0]["prompt"].endswith(suffix)
    assert len(baseline[0]["assertions"]) == 13
    assert baseline[0]["assertions"][-2].startswith("Release orchestration preserves")
    assert baseline[0]["assertions"][-1].startswith("Release dedup is skipped")
    baseline[0]["prompt"] = baseline[0]["prompt"].removesuffix(suffix)
    baseline[0]["assertions"] = baseline[0]["assertions"][:11]
    # Bootstrap main and reviewed PR299 contain different pre-existing triage
    # assertion objects. Accept only those two immutable baselines, never edit
    # the active ordinary manifests to match the native branch's historical hash.
    # Canonical complete-object digests keep this portable to a shallow checkout:
    # main ab20bee6, native aa15d776, and PR299 d83ee90b (TC4636 prompt repair).
    for cases, digests in [
        (baseline, {"205eeca4b564c0483c919be0951e50b3d5510f981278c61fa1c47468af5fe76d",
                  "b3f9e9d4f4ab1eb92f053c0c0e4199a36eabb12ab9589e9d27e9c59509eee501"}),
        (verify, {"251863edaed38f0b133c0cf0981ddffe80692f5d0655b51f7bfe214be38f69b1",
                  "cf587edf1e94e6a1a210d5c97788f33b3336a0818a86551e364ec056bd1a3be1",
                  "501a5fd500ff19ad460e9b1c65f7c4422b743ab6db6b58ba331b50197b45aabd"}),
    ]:
        assert hashlib.sha256(json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()).hexdigest() in digests
    assert not (FIXTURES / "fullsend-gate-tools.py").exists()


@pytest.mark.parametrize("scenario, fragment, fixture", [
    ("absent", "unset FULLSEND_OUTPUT_DIR", None),
    ("empty", "export FULLSEND_OUTPUT_DIR=''", None),
    ("malformed", None, "fullsend-invalid-trusted-input.md"),
    ("valid", None, "fullsend-report-only-trusted-input.json"),
])
def test_pre_script_prepares_native_mounts_without_live_fetch(tmp_path, scenario, fragment, fixture):
    """A native pre-script must inject distinct states before runtime startup."""
    # Given only synthetic fixture paths and the native pre-script environment
    script = SUITE / "prepare-fixture.py"
    assert script.is_file(), "Native synthetic pre-script is missing"
    root = synthetic_fixture_root(tmp_path)
    environment = dict(os.environ, TC6677_SCENARIO=scenario, TC6677_REPO_ROOT=str(root))
    environment.pop("FULLSEND_RUN_DIR", None)  # Native pre-script gets no such var.
    # When preparing the host files (not running Fullsend or an agent)
    result = subprocess.run([sys.executable, str(script)], env=environment,
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    # Then exact input bytes and only the intended gate injection are mounted
    gate = (tmp_path / "pre/tc-6677-gate.env").read_text()
    assert gate.startswith("# SYNTHETIC TEST DATA")
    assert gate.splitlines()[1:] == ([fragment] if fragment else [])
    mounted = tmp_path / "pre/triage-security-input.json"
    if fixture:
        expected = (FIXTURES / fixture).read_bytes()
        if fixture.endswith(".md"):
            expected = expected.split(b"```json\n", 1)[1].split(b"\n```", 1)[0]
        assert mounted.read_bytes() == expected
    else:
        assert not mounted.exists()
    assert sorted(p.name for p in (tmp_path / "pre").iterdir()) == (
        ["tc-6677-gate.env", "triage-security-input.json"] if fixture else ["tc-6677-gate.env"])
    assert not result.stdout and not result.stderr


def test_pre_script_refuses_stale_inputs(tmp_path):
    """Fixture failure must stay visible instead of silently reusing a prior run."""
    # Given a previously populated native pre directory
    script = SUITE / "prepare-fixture.py"
    assert script.is_file(), "Native synthetic pre-script is missing"
    (tmp_path / "pre").mkdir()
    (tmp_path / "pre/triage-security-input.json").write_bytes(b"stale")
    environment = dict(os.environ, TC6677_SCENARIO="absent", TC6677_REPO_ROOT=str(tmp_path))
    environment.pop("FULLSEND_RUN_DIR", None)
    # When an absent case would otherwise inherit a stale nonempty input
    result = subprocess.run([sys.executable, str(script)], env=environment,
                            capture_output=True, text=True, check=False)
    # Then it fails without rewriting that evidence
    assert result.returncode != 0 and "stale" in result.stderr.lower()
    assert (tmp_path / "pre/triage-security-input.json").read_bytes() == b"stale"


@pytest.mark.parametrize("failure", ["blocked-pre-directory", "missing-valid-input"])
def test_pre_script_fails_before_mounts_when_required_fixture_cannot_be_prepared(tmp_path, failure):
    """Deferred optional mounts cannot convert a real preparation failure into success."""
    # Given synthetic fixture failure, no FULLSEND_RUN_DIR and no agent/runtime
    root = synthetic_fixture_root(tmp_path)
    if failure == "blocked-pre-directory":
        (root / "pre").write_text("SYNTHETIC TEST DATA — blocks required gate delivery")
    else:
        (root / "evals/triage-security/files/fullsend-report-only-trusted-input.json").unlink()
    environment = dict(os.environ, TC6677_SCENARIO="valid", TC6677_REPO_ROOT=str(root))
    environment.pop("FULLSEND_RUN_DIR", None)
    # When the actual fixture pre-script cannot produce its required files
    result = subprocess.run([sys.executable, str(SUITE / "prepare-fixture.py")], env=environment,
                            capture_output=True, text=True, check=False)
    # Then nonzero propagates to Fullsend's pre-script abort; no gate can be mounted
    assert result.returncode == 1 and "preparation failed" in result.stderr
    expected_path = root / ("pre" if failure == "blocked-pre-directory" else
                            "evals/triage-security/files/fullsend-report-only-trusted-input.json")
    assert str(expected_path) in result.stderr
    assert not (root / "pre/tc-6677-gate.env").exists()


def test_malformed_assertion_requires_raw_abort_and_host_retention_evidence():
    """Require actual rejection for both absent output and intentional host stripping."""
    # Given the real case contract, without generating runtime evidence or grading
    annotations = yaml.safe_load((SUITE / "cases/035-malformed/annotations.yaml").read_text())
    # When inspecting the malformed output assertion's evidence requirements
    assertion = annotations["assertions"][3]
    # Then both output branches require actual rejection, not merely empty output
    assert annotations["assertion_count"] == len(annotations["assertions"]) == 5
    for requirement in [
        "actual sdlc-workflow:triage-security invocation", "invalid JSON parser error",
        "tool exit1", "no result file", "no recovery write is required",
        "If an error-only file was written", "BEFORE host validation",
        '{"error":"triage-security aborted: trusted input is missing, invalid JSON, or fails '
        'triage-security-input.schema.json; no interactive fallback is available in the sandbox."}',
        "validate-output-schema.sh", "strip_extra_properties.py", "stripped: ['error']",
        "rejection of the success schema", "collected agent-result.json exactly {}",
        "native Fullsend CLI exit nonzero", "complete ordered evidence chain",
        "no successful analysis, fallback or actions", "empty output or nonzero alone",
        "infrastructure/inference failure", "nonempty unexpected output or success report",
        "narrated outcomes are FAIL",
        "Output directory absence or a failed attempted abort write AFTER proven real Skill invalid JSON rejection",
        "accepted on the no-result path", "not a disqualifying bootstrap/inference failure",
        "disqualifying only when it prevents actual Skill input validation",
        "Without genuine invalid JSON proof, FAIL",
    ]:
        assert requirement in assertion
    assert "no output files OR sole agent-result.json containing {}" in annotations["assertions"][4]


def test_separate_suite_declares_all_strict_execution_assertions():
    """Native scenarios must retain 28 distinct execution requirements."""
    # Given the native framework's dataset rather than ordinary evals.json
    assert (SUITE / "eval.yaml").is_file(), "Separate native suite is missing"
    config = yaml.safe_load((SUITE / "eval.yaml").read_text())
    # Then the opaque CLI contract supplies every independent case to the framework
    assert config["runner"]["type"] == "cli"
    assert isinstance(config["runner"]["command"], list)
    assert "{scenario}" in config["runner"]["command"]
    assert not config.get("hooks")
    assert config["outputs"] == [{"path": "output"}]
    cases = sorted((SUITE / "cases").iterdir())
    assert [p.name for p in cases] == ["033-absent", "034-empty", "035-malformed", "036-valid", "037-release"]
    assert [len(yaml.safe_load((p / "annotations.yaml").read_text())["assertions"]) for p in cases] == [4, 5, 5, 7, 7]
    assert all(j["feedback_type"] == "bool" for j in config["judges"])
    assert all(t["min_pass_rate"] == 1.0 for t in config["thresholds"].values())


@pytest.mark.parametrize("exit_code", [0, 7])
@pytest.mark.parametrize("scenario", ["absent", "empty", "malformed", "valid", "release"])
def test_native_adapter_preserves_process_exit_and_artifacts(tmp_path, monkeypatch, exit_code, scenario):
    """Only the external CLI is doubled: staging, arguments and raw retention are real."""
    # Given a synthetic CLI process, explicitly not model or Skill execution
    adapter = load_script(SUITE / "run-fullsend.py")
    workspace = tmp_path / "case with spaces"
    workspace.mkdir()
    output = workspace / "output"
    output.mkdir()
    observed = {}
    native_bytes = b'{"synthetic":"NOT AGENT EXECUTION","total_cost_usd":2}\n'
    actual_process = subprocess.run

    def fake_process(command, **kwargs):
        """Stand in for Fullsend only; create unmistakably synthetic native files."""
        if command[0] != "/isolated/fullsend":
            return actual_process(command, **kwargs)
        observed["command"] = command
        observed["cwd"] = kwargs["cwd"]
        config_dir = Path(command[command.index("--fullsend-dir") + 1])
        observed["config_dir"] = config_dir
        observed["config"] = yaml.safe_load((config_dir / "config.yaml").read_text())
        observed["harness"] = yaml.safe_load((config_dir / "harness/triage-security-gate.yaml").read_text())
        native = Path(command[command.index("--output-dir") + 1]) / "agent-triage-security-gate-synthetic"
        (native / "iteration-1/transcripts").mkdir(parents=True)
        (native / "iteration-1/transcripts/runtime.jsonl").write_bytes(b"SYNTHETIC NOT AGENT EXECUTION\n")
        (native / "metrics.json").write_bytes(native_bytes)
        return subprocess.CompletedProcess(command, exit_code)

    monkeypatch.setattr(adapter.subprocess, "run", fake_process)
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    # When the native adapter stages its resources and delegates one command
    actual = adapter.run_case(ROOT, workspace, output, scenario, "model-under-test", "high",
                              Path("/isolated/fullsend"), Path("/isolated/linux-fullsend"))
    # Then raw failure is preserved and only native metrics are copied unchanged
    assert actual == exit_code
    command = observed["command"]
    assert command[:3] == ["/isolated/fullsend", "run", "triage-security-gate"]
    assert command[command.index("--model") + 1] == "model-under-test"
    assert command[command.index("--effort") + 1] == "high"
    assert command[command.index("--runtime") + 1] == "claude"
    assert command[command.index("--fullsend-binary") + 1] == "/isolated/linux-fullsend"
    assert "--env-file" not in command and "--status-number" not in command
    assert "--no-post-script" in command
    h = observed["harness"]
    # Reviewed production contract from d83ee90b:harness/triage-security.yaml.
    # Bootstrap ports companions only, so retain this small expected-value
    # fixture rather than requiring an unpublished git object or live harness.
    production = {
        "image": "ghcr.io/fullsend-ai/fullsend-code@sha256:9743bc7b6e451e0bcea25ae4a67e0c040c296f1fee04c08988ae80c53fafcfe6",
        "policy": "plugins/sdlc-workflow/policies/triage-security.yaml",
        "providers": ["plugins/sdlc-workflow/providers/vertex-ai.yaml"],
        "openshell": {"profiles": ["plugins/sdlc-workflow/profiles/fullsend-vertex-ai.yaml"]},
        "validation_loop": {"script": "plugins/sdlc-workflow/scripts/validate-output-schema.sh",
                            "schema": "plugins/sdlc-workflow/schemas/triage-security-result.schema.json"},
    }
    assert h["image"] == production["image"] and h["readonly_repo"] is True
    for field in ["policy", "agent", "pre_script"]:
        assert Path(h[field]).is_absolute()
    staged = observed["config_dir"]
    assert h["plugins"] == [str(staged / "plugins/sdlc-workflow")]
    assert h["policy"] == str(staged / production["policy"])
    assert h["providers"] == [str(staged / p) for p in production["providers"]]
    assert h["openshell"]["profiles"] == [str(staged / p) for p in production["openshell"]["profiles"]]
    assert h["validation_loop"]["script"] == str(staged / production["validation_loop"]["script"])
    assert h["validation_loop"]["schema"] == str(staged / production["validation_loop"]["schema"])
    assert h["host_files"][0]["src"] == str(staged / "plugins/sdlc-workflow/env/gcp-vertex.env")
    assert h["env"]["runner"]["TC6677_REPO_ROOT"] == str(staged)
    assert h["env"]["runner"]["FULLSEND_OUTPUT_SCHEMA"] == h["validation_loop"]["schema"]
    # Then delivery resources are contained real copies, not links to outside code
    plugin_files = [p for p in (ROOT / "plugins/sdlc-workflow").rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    for original in plugin_files:
        copied = staged / original.relative_to(ROOT)
        assert copied.resolve().is_relative_to(staged.resolve())
        assert copied.read_bytes() == original.read_bytes()
    assert not list(staged.rglob("__pycache__"))
    for name in ["agent.md", "prepare-fixture.py"]:
        assert (staged / "evals/fullsend/triage-security" / name).read_bytes() == (SUITE / name).read_bytes()
    fixture_names = [
        "fullsend-gate-interactive-config.md", "fullsend-invalid-trusted-input.md", "fullsend-report-only-trusted-input.json"]
    if scenario == "release":
        fixture_names.append("fullsend-release-trusted-input.json")
        fixture_names.sort()
    assert sorted(p.name for p in (staged / "evals/triage-security/files").iterdir()) == fixture_names
    for name in fixture_names:
        assert (staged / "evals/triage-security/files" / name).read_bytes() == (FIXTURES / name).read_bytes()
    assert h["validation_loop"]["max_iterations"] == 1 and "post_script" not in h
    assert "sandbox" not in h["env"] and "JIRA_API_TOKEN" not in h["env"]["runner"]
    assert h["host_files"][2]["dest"] == "/sandbox/workspace/.env.d/zz-tc-6677-gate.env"
    assert h["host_files"][1]["dest"] == "/sandbox/workspace/.pre-script/triage-security-input.json"
    assert [f["src"] for f in h["host_files"][1:3]] == ["pre/triage-security-input.json", "pre/tc-6677-gate.env"]
    assert all(f["optional"] is True for f in h["host_files"][1:3])
    assert len(h["host_files"]) == 4
    assert h["host_files"][3] == {
        "src": "${GOOGLE_APPLICATION_CREDENTIALS}", "dest": "/tmp/.gcp-credentials.json"}
    target = Path(command[command.index("--target-repo") + 1])
    # Then the actual local Git fixture satisfies native copy/read-only setup,
    # without a remote, commit, outside repository or extra project content.
    assert (target / ".git").is_dir(), "Native read-only setup requires real Git metadata"
    git_root = actual_process(["git", "-C", str(target), "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, check=True)
    assert Path(git_root.stdout.strip()).resolve() == target.resolve()
    assert actual_process(["git", "-C", str(target), "remote"],
                          capture_output=True, text=True, check=True).stdout == ""
    assert actual_process(["git", "-C", str(target), "rev-parse", "--verify", "HEAD"],
                          capture_output=True, check=False).returncode != 0
    assert (target / ".git/info/exclude").is_file()
    if scenario == "absent":
        assert (target / "CLAUDE.md").read_bytes() == (FIXTURES / "fullsend-gate-interactive-config.md").read_bytes()
        assert sorted(p.name for p in target.iterdir()) == [".git", "CLAUDE.md"]
    else:
        assert [p.name for p in target.iterdir()] == [".git"], "Noninteractive cases must not preload interactive configuration"
    assert (output / "metrics.json").read_bytes() == native_bytes
    assert sorted(p.name for p in output.iterdir()) == ["metrics.json", "native"]


def test_staged_layout_with_actual_pinned_fullsend_resolver(tmp_path, monkeypatch):
    """Use native Go resolution, not a duplicate containment check or Skill execution."""
    # Given optional read-only source and cached Go deps; consumer setup needs neither
    synthetic_adc = tmp_path / "external-synthetic-not-credentials.txt"
    synthetic_adc.write_text("# SYNTHETIC TEST DATA — NOT CREDENTIALS; native path validation only\n")
    source = os.environ.get("TC6677_FULLSEND_SOURCE")
    if not source or not shutil.which("go"):
        pytest.skip("Native resolver contract needs TC6677_FULLSEND_SOURCE and Go with cached dependencies")
    pin = "d5f36921ac754705619f38c637ef692873809fbc"
    archive = subprocess.check_output(["git", "-C", source, "archive", pin])
    snapshot = tmp_path / "pinned-source"
    snapshot.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as package:
        package.extractall(snapshot, filter="data")
    probe = tmp_path / "resolver-probe"
    probe.mkdir()
    go_mod = (snapshot / "go.mod").read_text().replace(
        "module github.com/fullsend-ai/fullsend\n", "module github.com/fullsend-ai/fullsend/tc6677-resolver-probe\n", 1)
    (probe / "go.mod").write_text(go_mod + '\nrequire github.com/fullsend-ai/fullsend v0.0.0\nreplace github.com/fullsend-ai/fullsend => ' + json.dumps(str(snapshot)) + '\n')
    shutil.copy2(snapshot / "go.sum", probe / "go.sum")
    (probe / "main.go").write_text('''// SYNTHETIC TEST DATA — calls pinned native resource APIs only, no runtime
package main
import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    "path/filepath"
    "github.com/fullsend-ai/fullsend/internal/harness"
    "github.com/fullsend-ai/fullsend/internal/resolve"
)
func main() {
    root := os.Args[1]
    h, _, err := harness.LoadWithBase(context.Background(), filepath.Join(root, "harness/triage-security-gate.yaml"), harness.ComposeOpts{WorkspaceRoot: root})
    if err == nil { err = h.ResolveRelativeTo(root) }
    var result resolve.ResolveResult
    if err == nil { result, err = resolve.ResolveHarness(context.Background(), h, resolve.ResolveOpts{WorkspaceRoot: root}) }
    if err == nil && (len(result.Profiles) != 1 || len(result.Providers) != 1) { err = fmt.Errorf("expected native profile/provider records") }
    // Actual early validation: no native-generated host variable exists yet.
    if err == nil { err = h.ValidateRunnerEnvWith(os.LookupEnv) }
    if err == nil { err = h.ValidateFilesExist() }
    if err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
    if len(h.HostFiles) != 4 { fmt.Fprintln(os.Stderr, "missing native inference credential mount"); os.Exit(1) }
    json.NewEncoder(os.Stdout).Encode(map[string]string{"gate_src": h.HostFiles[2].Src, "input_src": h.HostFiles[1].Src, "credential_src": h.HostFiles[3].Src, "credential_dest": h.HostFiles[3].Dest})
}
''')
    environment = dict(os.environ, GOPROXY="off", GOSUMDB="off", GOTOOLCHAIN="local", GOWORK="off",
                       GOCACHE=str(Path(os.environ.get("TC6677_GO_CACHE", str(tmp_path / "go-cache")))),
                       GOOGLE_APPLICATION_CREDENTIALS=str(synthetic_adc))
    binary = probe / "resolver"
    built = subprocess.run(["go", "build", "-mod=mod", "-o", str(binary), "."], cwd=probe,
                           env=environment, capture_output=True, text=True, check=False)
    assert built.returncode == 0, built.stderr
    adapter = load_script(SUITE / "run-fullsend.py")
    workspace = tmp_path / "case"
    workspace.mkdir()
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    observed = {}

    def resolve_only(command, **kwargs):
        """Replace the inference CLI boundary with the actual source-pinned resolver."""
        setup = Path(command[command.index("--fullsend-dir") + 1])
        observed["setup"] = setup
        result = subprocess.run([str(binary), str(setup)], env=environment,
                                capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        mounts = json.loads(result.stdout)
        assert mounts == {"gate_src": str(setup / "pre/tc-6677-gate.env"),
                          "input_src": str(setup / "pre/triage-security-input.json"),
                          "credential_src": "${GOOGLE_APPLICATION_CREDENTIALS}",
                          "credential_dest": "/tmp/.gcp-credentials.json"}
        assert not synthetic_adc.resolve().is_relative_to(setup.resolve())
        assert not list(setup.rglob(synthetic_adc.name))
        # Actual pinned validation must reject an unset mandatory source variable.
        missing_adc = dict(environment)
        missing_adc.pop("GOOGLE_APPLICATION_CREDENTIALS")
        rejected = subprocess.run([str(binary), str(setup)], env=missing_adc,
                                  capture_output=True, text=True, check=False)
        assert rejected.returncode == 1 and "host variable GOOGLE_APPLICATION_CREDENTIALS is not set" in rejected.stderr
        # The staged pre-script must consume the staged exact fixtures successfully.
        h = yaml.safe_load((setup / "harness/triage-security-gate.yaml").read_text())
        fixture_env = dict(environment, TC6677_REPO_ROOT=str(setup), TC6677_SCENARIO="valid")
        fixture_env.pop("FULLSEND_RUN_DIR", None)
        prepared = subprocess.run([sys.executable, h["pre_script"]], env=fixture_env,
                                 capture_output=True, text=True, check=False)
        assert prepared.returncode == 0, prepared.stderr
        assert Path(mounts["gate_src"]).read_bytes() == "# SYNTHETIC TEST DATA — deliberate native gate condition injection\n".encode()
        assert Path(mounts["input_src"]).read_bytes() == (FIXTURES / "fullsend-report-only-trusted-input.json").read_bytes()
        return result

    # Only the adapter's command launch is doubled; native resolver APIs really run
    original_run = subprocess.run
    monkeypatch.setattr(adapter.subprocess, "run", lambda command, **kwargs:
                        resolve_only(command, **kwargs) if command[0] == "/not-launched/fullsend" else original_run(command, **kwargs))
    # When staging production resources inside the configuration workspace
    assert adapter.run_case(ROOT, workspace, workspace / "output", "valid", "unused", "high",
                            Path("/not-launched/fullsend"), Path("/not-launched/linux-fullsend")) == 0
    # Then the actual resolver still rejects an external profile and a symlink escape
    setup = observed["setup"]
    path = setup / "harness/triage-security-gate.yaml"
    h = yaml.safe_load(path.read_text())
    external = ROOT / "plugins/sdlc-workflow/profiles/fullsend-vertex-ai.yaml"
    for profile in [external, setup / "escaping-profile.yaml"]:
        if profile != external:
            profile.symlink_to(external)
        h["openshell"]["profiles"] = [str(profile)]
        path.write_text(yaml.safe_dump(h))
        rejected = subprocess.run([str(binary), str(setup)], env=environment,
                                  capture_output=True, text=True, check=False)
        assert rejected.returncode == 1 and "outside workspace root" in rejected.stderr


@pytest.mark.parametrize("failure", ["stale", "mint"])
def test_native_adapter_rejects_stale_or_live_mint_configuration(tmp_path, monkeypatch, failure):
    """Synthetic execution must never reuse old evidence or mint a live forge token."""
    adapter = load_script(SUITE / "run-fullsend.py")
    workspace = tmp_path / "case"
    workspace.mkdir()
    output = workspace / "output"
    output.mkdir()
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    if failure == "stale":
        (output / "native").mkdir()
    else:
        monkeypatch.setenv("FULLSEND_MINT_URL", "https://synthetic.invalid/no-access")
    # When preparing a run before any external process could start
    with pytest.raises(ValueError):
        adapter.run_case(ROOT, workspace, output, "valid", "model", "high",
                         Path("/no-such-cli"), Path("/no-such-linux-cli"))


def test_common_entrypoint_resolves_framework_contract(tmp_path):
    """The common entrypoint must resolve CLI placeholders and absolute dataset paths."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given a Python path with spaces and explicit runtime/judge choices
    config = common.resolved_config(Path("/cache with spaces/bin/python"), "skill-model", "judge-model", "high")
    # Then framework-consumed paths and invocation agree without shell splitting
    assert config["dataset"]["path"] == str(SUITE / "cases")
    assert config["runner"]["command"][:2] == ["/cache with spaces/bin/python", str(SUITE / "run-fullsend.py")]
    assert config["execution"]["skill"] == "triage-security-gate"
    assert config["models"] == {"skill": "skill-model", "judge": "judge-model"}
    assert config["runner"]["effort"] == "high"


@pytest.mark.parametrize("score_exit, summary_present", [(0, True), (0, False), (7, True)])
def test_common_pipeline_collects_failures_before_upstream_judging(tmp_path, monkeypatch, score_exit, summary_present):
    """Nonzero execution must preserve case evidence and still reach upstream scoring."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given a synthetic framework boundary; no agent/judge/inference runs here
    calls = []
    run_dir = tmp_path / "runs/triage-security-gate/synthetic"
    workspace = tmp_path / "workspace"

    def fake_process(command, **kwargs):
        """Only external framework phases are doubled; orchestration remains real."""
        phase = Path(command[1]).stem
        calls.append((phase, command, kwargs))
        if phase == "execute":
            for case in ["033-absent", "034-empty", "035-malformed", "036-valid", "037-release"]:
                p = run_dir / "cases" / case
                p.mkdir(parents=True)
                (p / "run_result.json").write_text('{"exit_code":7}')
            return subprocess.CompletedProcess(command, 7)
        if phase == "score":
            if summary_present:
                (run_dir / "summary.yaml").write_text(yaml.safe_dump(synthetic_judge_summary()))
            return subprocess.CompletedProcess(command, score_exit)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(common.subprocess, "run", fake_process)
    # When the common pipeline delegates workspace/execute/collect/score
    if not summary_present:
        with pytest.raises(ValueError, match="summary"):
            common.pipeline(Path("/venv/python"), Path("/harness"), tmp_path / "eval.yaml",
                            workspace, run_dir, "synthetic", dict(os.environ))
    else:
        result = common.pipeline(Path("/venv/python"), Path("/harness"), tmp_path / "eval.yaml",
                                 workspace, run_dir, "synthetic", dict(os.environ))
        assert result == score_exit
    # Then expected case failures are not normalized or locally graded
    assert [c[0] for c in calls] == ["workspace", "execute", "collect", "score"]
    assert all(c[1][0] == "/venv/python" for c in calls)
    assert calls[-1][1][2] == "judges"
    assert all(json.loads(p.read_text())["exit_code"] == 7 for p in run_dir.glob("cases/*/run_result.json"))


def test_common_pipeline_refuses_missing_case_results(tmp_path, monkeypatch):
    """Infrastructure failure must not become a vacuous zero-case grading success."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    called = []

    def fake_process(command, **kwargs):
        called.append(Path(command[1]).stem)
        return subprocess.CompletedProcess(command, 1 if called[-1] == "execute" else 0)

    monkeypatch.setattr(common.subprocess, "run", fake_process)
    with pytest.raises(ValueError, match="case results"):
        common.pipeline(Path("/python"), Path("/harness"), tmp_path / "eval.yaml",
                        tmp_path / "ws", tmp_path / "run", "synthetic", dict(os.environ))
    assert called == ["workspace", "execute"]


def test_binary_setup_rejects_corrupted_release_before_install(tmp_path):
    """A pinned release mismatch must fail before any executable can be installed."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given downloaded bytes that do not match the approved release digest
    (tmp_path / "fullsend-linux-amd64.tar.gz").write_bytes(b"SYNTHETIC corrupt release")
    # When an isolated installation consumes them
    with pytest.raises(ValueError, match="digest mismatch"):
        common.install_binary(tmp_path, "linux-amd64", common.pins()["fullsend"])
    # Then neither execution nor a partial CLI install occurred
    assert not (tmp_path / "bin/fullsend-linux-amd64").exists()


def test_setup_overrides_user_pip_install_location(tmp_path, monkeypatch):
    """Host pip user-install defaults must not redirect the isolated dependency install."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    source = tmp_path / "agent-eval-harness"
    source.mkdir()
    (tmp_path / "venv/bin").mkdir(parents=True)
    (tmp_path / "venv/bin/python").touch()
    commands = []
    monkeypatch.setattr(common.sys, "version_info", (3, 12))
    monkeypatch.setattr(common, "verify_source", lambda *args: None)
    monkeypatch.setattr(common, "install_binary", lambda *args: None)

    def fake_install(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(common.subprocess, "run", fake_install)
    # When setup prepares dependency installation without external processes
    common.setup(tmp_path)
    # Then explicit venv location wins over pip's host user-install configuration
    assert all("--no-user" in command for command in commands)
    assert all(command[command.index("--cache-dir") + 1] == str(tmp_path / "pip-cache") for command in commands)
    assert "--require-hashes" in commands[0]
    assert "--no-deps" in commands[1] and "--no-build-isolation" in commands[1]


def test_verified_archive_download_uses_host_transport(tmp_path, monkeypatch):
    """Native host TLS transport and pinned archive verification both precede installation."""
    import io
    import tarfile
    common = load_script(ROOT / "evals/fullsend/run.py")
    # Given an unmistakably synthetic release archive, never an agent executable
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as package:
        member = tarfile.TarInfo("release/fullsend")
        data = b"SYNTHETIC NOT A CLI\n"
        member.size = len(data)
        package.addfile(member, io.BytesIO(data))
    archive = buffer.getvalue()
    observed = []

    def fake_download(command, **kwargs):
        """Replace only curl's network transfer with synthetic bytes."""
        observed.append(command)
        Path(command[command.index("--output") + 1]).write_bytes(archive)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(common.subprocess, "run", fake_download)
    # When setup consumes a download without using model/network credentials
    dependency = {"version": "0.43.0", "archives": {"linux-amd64": hashlib.sha256(archive).hexdigest()}}
    common.install_binary(tmp_path, "linux-amd64", dependency)
    # Then curl retains TLS verification and checksum-verified payload bytes are installed
    assert observed[0][:2] == ["curl", "--fail"]
    assert "--insecure" not in observed[0] and "-k" not in observed[0]
    assert (tmp_path / "bin/fullsend-linux-amd64").read_bytes() == data


@pytest.mark.parametrize("installed", ["wrong-version", None])
def test_dependency_preflight_rejects_unlocked_or_missing_packages(tmp_path, monkeypatch, installed):
    """A dependency-only preflight must detect drift before a model can be launched."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    (tmp_path / "requirements.lock").write_text('pyyaml==6.0.3 \\\n    --hash=sha256:' + 'a' * 64 + '\n')
    assert callable(getattr(common, "verify_locked_dependencies", None)), "Dependency lock verification is missing"
    monkeypatch.setattr(importlib.metadata, "version", lambda package: installed)
    with pytest.raises(ValueError, match="Locked dependency"):
        common.verify_locked_dependencies(tmp_path / "requirements.lock")


def test_dependency_preflight_accepts_exact_locked_packages(tmp_path, monkeypatch):
    """Exact version/hash entries remain acceptable without importing inference clients."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    (tmp_path / "requirements.lock").write_text('pyyaml==6.0.3 \\\n    --hash=sha256:' + 'a' * 64 + '\n')
    assert callable(getattr(common, "verify_locked_dependencies", None)), "Dependency lock verification is missing"
    monkeypatch.setattr(importlib.metadata, "version", lambda package: "6.0.3")
    common.verify_locked_dependencies(tmp_path / "requirements.lock")


def test_upstream_collection_retains_nested_native_bytes(tmp_path):
    """Characterize the needed opaque CLI collection boundary, without execution/grading."""
    # Given installed pinned tooling and unmistakably synthetic native artifacts
    cache = Path(os.environ.get("TC6677_EVAL_CACHE", "/tmp/tc-6677-eval-deps")).resolve()
    python = cache / "venv/bin/python"
    if not python.is_file():
        pytest.skip("Optional dependency contract: run the isolated setup first")
    common = load_script(ROOT / "evals/fullsend/run.py")
    common.verify_source(cache / "agent-eval-harness", common.pins()["harness"])
    workspace = tmp_path / "workspace"
    native = workspace / "cases/036-valid/output/native/agent-synthetic/iteration-1/transcripts"
    native.mkdir(parents=True)
    raw = b'{"synthetic":"NOT AGENT EXECUTION"}\n{"partial":'
    (native / "runtime.jsonl").write_bytes(raw)
    output = tmp_path / "collected"
    config = tmp_path / "eval.yaml"
    config.write_text(yaml.safe_dump(common.resolved_config(python, "unused", "unused", "high")))
    # When the real upstream collector consumes our declared output path
    process = subprocess.run([str(python), str(cache / "agent-eval-harness/skills/eval-run/scripts/collect.py"),
                              "--config", str(config), "--workspace", str(workspace), "--output", str(output)],
                             cwd=ROOT, capture_output=True, text=True, check=False)
    # Then nested original bytes are retained, without repaired transcripts or verdicts
    assert process.returncode == 0, process.stderr
    assert (output / "cases/036-valid/output/native/agent-synthetic/iteration-1/transcripts/runtime.jsonl").read_bytes() == raw
    assert not list(output.rglob("judge*")) and not list(output.rglob("agent-result.json"))


@pytest.mark.parametrize("termination", [signal.SIGTERM, signal.SIGKILL])
def test_native_adapter_preserves_signal_termination(tmp_path, termination):
    """A native CLI signal must not be rewritten to Python's unsigned exit code."""
    # Given a synthetic failing process, never Fullsend or inference
    fake = tmp_path / "synthetic-cli"
    fake.write_text(f'#!{sys.executable}\n# SYNTHETIC TEST DATA — process signal contract only\nimport os\nos.kill(os.getpid(),{int(termination)})\n')
    fake.chmod(0o755)
    workspace = tmp_path / "case"
    workspace.mkdir()
    environment = dict(os.environ, TC6677_FULLSEND_BIN=str(fake), TC6677_SANDBOX_FULLSEND_BIN=str(fake))
    environment.pop("FULLSEND_MINT_URL", None)
    # When the real adapter delegates to that CLI double
    process = subprocess.run([sys.executable, str(SUITE / "run-fullsend.py"), "--agent", "triage-security-gate",
                              "--workspace", str(workspace), "--output-dir", str(workspace / "output"),
                              "--scenario", "valid", "--model", "unused", "--effort", "high"],
                             env=environment, capture_output=True, text=True, check=False)
    # Then the outer process reports the same actual signal to CliRunner
    assert process.returncode == -termination


@pytest.mark.parametrize("failure_phase", ["workspace", "execute", "collect", "score", "summary", None])
def test_pipeline_exports_safe_failure_phase_without_changing_execution(tmp_path, monkeypatch, failure_phase):
    """Diagnostics preserve phase exits and grading rules without exporting subprocess text."""
    # Given synthetic framework failures and expected negative case exits
    common = load_script(ROOT / "evals/fullsend/run.py")
    run_dir = tmp_path / "synthetic"
    diagnostics = {}
    calls = []

    def fake_process(command, **kwargs):
        """Double framework execution; deliberately secret-shaped stderr stays private."""
        phase = Path(command[1]).stem
        calls.append(phase)
        if phase == "execute" and failure_phase != "execute":
            for case in common.CASES:
                directory = run_dir / "cases" / case
                directory.mkdir(parents=True)
                (directory / "run_result.json").write_text('{"exit_code":7}')
        if phase == "score" and failure_phase != "summary":
            (run_dir / "summary.yaml").write_text(yaml.safe_dump(synthetic_judge_summary()))
        if phase == failure_phase:
            kwargs["stderr"].write(b"SYNTHETIC SECRET bearer /private/credentials\n")
        return subprocess.CompletedProcess(command, 7 if phase == failure_phase or phase == "execute" else 0)

    monkeypatch.setattr(common.subprocess, "run", fake_process)
    # When the real pipeline runs and exports diagnostics to the existing safe report
    if failure_phase in {"execute", "summary"}:
        with pytest.raises(ValueError):
            common.pipeline(Path("/python"), Path("/harness"), tmp_path / "config.yaml",
                            tmp_path / "ws", run_dir, "synthetic", {}, diagnostics)
        result = 1
    else:
        result = common.pipeline(Path("/python"), Path("/harness"), tmp_path / "config.yaml",
                                 tmp_path / "ws", run_dir, "synthetic", {}, diagnostics)
    source = {key: "a" * 40 for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = 299
    common.publish_report(run_dir, tmp_path / "safe", source, result, diagnostics)
    report = json.loads((tmp_path / "safe/native-result.json").read_text())
    # Then only fixed phase/category identifiers and actual numeric exits leave the host
    assert report["diagnostics"]["phase"] == (failure_phase or "complete")
    assert report["diagnostics"]["phase_exits"] == {
        phase: 7 if phase == failure_phase or phase == "execute" else 0 for phase in calls}
    expected_code = {"execute": "missing-case-results", "summary": "invalid-summary"}.get(
        failure_phase, "phase-exit" if failure_phase else "none")
    assert report["diagnostics"]["code"] == expected_code
    assert "SECRET" not in json.dumps(report)
    assert "credentials" not in json.dumps(report)
    assert result == (0 if failure_phase is None else 1 if failure_phase in {"execute", "summary"} else 7)


@pytest.mark.parametrize("stderr,expected", [
    (b"SYNTHETIC HTTP 401 Unauthorized SECRET", "authentication-error"),
    (b"SYNTHETIC PermissionDenied SECRET", "permission-error"),
    (b"SYNTHETIC RESOURCE_EXHAUSTED SECRET", "quota-error"),
    (b"SYNTHETIC deadline exceeded SECRET", "timeout"),
    (b"SYNTHETIC connection refused SECRET", "connection-error"),
    (b"SYNTHETIC arbitrary hostile text SECRET", "phase-exit"),
])
def test_phase_failure_category_is_fixed_and_contains_no_upstream_text(tmp_path, monkeypatch, stderr, expected):
    """Known error markers map to advisory categories; arbitrary bytes never enter reports."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    diagnostics = {}
    def fake_process(command, **kwargs):
        """SYNTHETIC TEST DATA — diagnostic text only, no real inference."""
        kwargs["stderr"].write(stderr)
        return subprocess.CompletedProcess(command, 1)
    monkeypatch.setattr(common.subprocess, "run", fake_process)
    assert common.pipeline(Path("/python"), Path("/harness"), tmp_path / "config.yaml",
                           tmp_path / "ws", tmp_path / "run", "synthetic", {}, diagnostics) == 1
    assert diagnostics["code"] == expected
    assert "SECRET" not in json.dumps(diagnostics)


def test_safe_diagnostics_reject_unknown_fields_and_untrusted_values(tmp_path):
    """The safe report refuses diagnostic text or invented phase/category names."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    source = {key: "a" * 40 for key in ["head_sha", "merge_sha", "base_sha", "trusted_sha", "eval_source_sha"]}
    source["pr_number"] = 299
    for diagnostic in [
        {"phase": "score", "code": "phase-exit", "phase_exits": {}, "message": "SECRET"},
        {"phase": "SECRET", "code": "phase-exit", "phase_exits": {}},
        {"phase": "score", "code": "SECRET", "phase_exits": {}},
        {"phase": "score", "code": "phase-exit", "phase_exits": {"score": "SECRET"}},
    ]:
        with pytest.raises(ValueError, match="diagnostic"):
            common.publish_report(tmp_path / "missing", tmp_path / "safe", source, 1, diagnostic)
    assert not (tmp_path / "safe/native-result.json").exists()


def test_phase_stderr_is_streamed_with_bounded_diagnostic_reads(tmp_path, monkeypatch, capsys):
    """Large private stderr never requires a whole-log allocation before safe reporting."""
    common = load_script(ROOT / "evals/fullsend/run.py")
    reads = []
    class BoundedFile(io.BytesIO):
        """SYNTHETIC TEST DATA — reject any unbounded spool read."""
        def read(self, size=-1):
            """Record and constrain diagnostic read sizes."""
            assert 0 < size <= 65536
            reads.append(size)
            return super().read(size)
    monkeypatch.setattr(common.tempfile, "TemporaryFile", BoundedFile)
    def fake_process(command, **kwargs):
        """SYNTHETIC TEST DATA — large output remains in the private stderr stream."""
        kwargs["stderr"].write(b"HTTP 401 Unauthorized\n" + b"x" * 200000)
        return subprocess.CompletedProcess(command, 1)
    monkeypatch.setattr(common.subprocess, "run", fake_process)
    diagnostics = {}
    assert common.pipeline(Path("/python"), Path("/harness"), tmp_path / "config.yaml",
                           tmp_path / "ws", tmp_path / "run", "synthetic", {}, diagnostics) == 1
    assert len(reads) >= 4
    assert diagnostics["code"] == "authentication-error"
    assert len(capsys.readouterr().err) == len(b"HTTP 401 Unauthorized\n") + 200000


def test_release_case_inventory_and_fixture_preparation(tmp_path):
    """Reviewed release coverage stages only the synthetic credential-free bundle."""
    common = load_script(ROOT / 'evals/fullsend/run.py')
    assert common.CASES == ['033-absent', '034-empty', '035-malformed', '036-valid', '037-release']
    assert common.ASSERTION_COUNTS['037-release'] == 7
    root = synthetic_fixture_root(tmp_path)
    shutil.copy2(FIXTURES / 'fullsend-release-trusted-input.json',
                 root / 'evals/triage-security/files/fullsend-release-trusted-input.json')
    load_script(SUITE / 'prepare-fixture.py').prepare(root, 'release')
    assert (root / 'pre/triage-security-input.json').read_bytes() == (
        FIXTURES / 'fullsend-release-trusted-input.json').read_bytes()
    assert 'unset FULLSEND_OUTPUT_DIR' not in (root / 'pre/tc-6677-gate.env').read_text()
