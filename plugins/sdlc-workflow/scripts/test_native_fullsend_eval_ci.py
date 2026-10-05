"""Deterministic bootstrap contracts; never provision sandboxes or call models."""

import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]


def test_host_validator_dependency_is_in_isolated_lock():
    """Fresh CI must install the jsonschema module used by trusted host validation."""
    requirements = (ROOT / "evals/fullsend/requirements.in").read_text()
    lock = (ROOT / "evals/fullsend/requirements.lock").read_text()
    assert "jsonschema" in re.findall(r"^([a-zA-Z0-9_-]+)", requirements, re.MULTILINE)
    assert re.search(r"^jsonschema==[^\n]+", lock, re.MULTILINE)


@pytest.mark.parametrize("linked_part", ["plugin", "plugins"])
def test_native_cli_rejects_root_and_ancestor_plugin_symlinks(tmp_path, linked_part):
    """The CLI must reject PR path links before they redirect reads to the trusted host."""
    # Given a PR path pointing outside its checkout through either directory level
    checkout = tmp_path / "pr-head"
    checkout.mkdir()
    trusted_plugin = ROOT / "plugins/sdlc-workflow"
    if linked_part == "plugin":
        (checkout / "plugins").mkdir()
        (checkout / "plugins/sdlc-workflow").symlink_to(trusted_plugin, target_is_directory=True)
    else:
        (checkout / "plugins").symlink_to(trusted_plugin.parent, target_is_directory=True)
    environment = dict(os.environ, TC6677_FULLSEND_BIN="/not-launched", TC6677_SANDBOX_FULLSEND_BIN="/not-launched")
    environment.pop("FULLSEND_MINT_URL", None)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    # When invoking the actual CLI with the lexical selected plugin path
    result = subprocess.run([sys.executable, str(ROOT / "evals/fullsend/triage-security/run-fullsend.py"),
                             "--agent", "triage-security-gate", "--workspace", str(workspace),
                             "--output-dir", str(workspace / "output"), "--scenario", "valid",
                             "--model", "unused", "--effort", "high", "--plugin-root",
                             str(checkout / "plugins/sdlc-workflow")], env=environment, capture_output=True, text=True)
    # Then rejection precedes staging and any native launch
    assert result.returncode == 1
    assert "symlink" in result.stderr
    assert not (workspace / "native-config").exists()


def workflow():
    """Read the actual trusted workflow rather than a duplicate implementation."""
    return yaml.safe_load((ROOT / ".github/workflows/eval-pr-run.yml").read_text())


def script_step(job, name):
    """Select a workflow script by its human-readable step name."""
    return next(step for step in workflow()["jobs"][job]["steps"] if step["name"] == name)


def run_js(script, data, env=None):
    """SYNTHETIC TEST DATA — double only GitHub API responses, execute real JS."""
    code = r'''
const data = JSON.parse(process.argv[1]);
const outputs = {}, statuses = [], errors = [], reviews = [];
const require = name => {if (name !== 'fs') throw Error('unexpected module');
 return {existsSync:()=>Boolean(data.report),readFileSync:()=>JSON.stringify(data.report)};};
const core = {setOutput: (k,v) => outputs[k]=v, setFailed: x => errors.push(x)};
const context = {repo:{owner:'RHEcosystemAppEng',repo:'sdlc-plugins'},
 payload:{workflow_run:{head_sha:data.eventHead || 'a'.repeat(40),
 head_repository:{full_name:'mrizzi/sdlc-plugins'}}}, serverUrl:'https://github.com',runId:1};
const pr = {number:data.number || 299,state:'open',user:{login:'synthetic'},
 head:{sha:data.head || 'a'.repeat(40),ref:data.branch || 'verify-pr-fullsend',repo:{full_name:'mrizzi/sdlc-plugins'}},
 base:{sha:'b'.repeat(40),ref:data.base || 'main'},merge_commit_sha:'c'.repeat(40)};
const github = {paginate:async (fn,args)=>fn(args),rest:{
 pulls:{list:async()=>[pr],get:async()=>({data:pr}),createReview:async r=>reviews.push(r),
 listFiles:async()=> (data.paths||[]).map(filename=>({filename}))},
 git:{getCommit:async()=>({data:{parents:(data.parents||['b'.repeat(40),'a'.repeat(40)]).map(sha=>({sha}))}})},
 repos:{getCollaboratorPermissionLevel:async()=>({data:{permission:data.permission||'read'}}),
 getContent:async()=>({data:{}}),createCommitStatus:async s=>statuses.push(s)}}};
(async()=>{SCRIPT
})().then(()=>process.stdout.write(JSON.stringify({outputs,statuses,errors,reviews})))
.catch(e=>{process.stdout.write(JSON.stringify({outputs,statuses,errors:[...errors,e.message],reviews}));});
'''.replace("SCRIPT", script)
    result = subprocess.run(["node", "-e", code, json.dumps(data)],
                            env=dict(os.environ, **(env or {})), capture_output=True, text=True, check=True)
    return json.loads(result.stdout.splitlines()[-1])


@pytest.mark.parametrize("permission,trusted", [("admin", "true"), ("write", "true"), ("read", "false")])
def test_source_resolution_pins_api_associated_revision(permission, trusted):
    """The triggering head, merge parents and base revision form one immutable source."""
    result = run_js(script_step("discover", "Resolve PR identity and check trust")["with"]["script"],
                    {"permission": permission})
    assert result["errors"] == []
    assert {key: result["outputs"].get(key) for key in ["head_sha", "merge_sha", "base_sha", "trusted"]} == {
        "head_sha": "a" * 40, "merge_sha": "c" * 40, "base_sha": "b" * 40, "trusted": trusted}


@pytest.mark.parametrize("defect", [{"head": "d" * 40}, {"parents": ["b" * 40, "d" * 40]}, {"base": "other"}])
def test_source_resolution_refuses_stale_or_unrelated_revisions(defect):
    """A new head or unrelated merge cannot inherit the event's authorization."""
    result = run_js(script_step("discover", "Resolve PR identity and check trust")["with"]["script"], defect)
    assert result["errors"]
    assert not result["outputs"].get("merge_sha")


@pytest.mark.parametrize("number,branch,path,expected", [
    (299, "verify-pr-fullsend", "evals/fullsend/triage-security/cases/033-absent/input.yaml", "true"),
    (299, "verify-pr-fullsend", "plugins/sdlc-workflow/skills/triage-security/SKILL.md", "true"),
    (299, "verify-pr-fullsend", "plugins/sdlc-workflow/schemas/triage-security-input.schema.json", "true"),
    (299, "verify-pr-fullsend", "plugins/sdlc-workflow/providers/vertex-ai.yaml", "true"),
    (299, "verify-pr-fullsend", ".github/scripts/run-native-fullsend-evals.sh", "true"),
    (300, "verify-pr-fullsend", "evals/fullsend/run.py", "false"),
    (299, "wrong", "evals/fullsend/run.py", "false"),
    (299, "verify-pr-fullsend", "README.md", "false"),
])
def test_native_discovery_is_relevant_and_bootstrap_only(number, branch, path, expected):
    """Only relevant changes on exact PR299/source branch activate bootstrap native CI."""
    result = run_js(script_step("discover", "Discover changed skills")["with"]["script"], {"paths": [path]},
                    {"PR_NUMBER": str(number), "SOURCE_BRANCH": branch, "MERGE_SHA": "c" * 40})
    assert result["errors"] == []
    assert result["outputs"].get("native") == expected


def test_native_execution_uses_trusted_setup_and_readonly_github_permissions():
    """Credentialed host executes base scripts, and the tested revision is immutable data."""
    jobs = workflow()["jobs"]
    assert "run-native-evals" in jobs, "Native CI is not implemented"
    native = jobs["run-native-evals"]
    assert native["permissions"] == {"contents": "read", "id-token": "write"}
    assert native["needs"] == ["discover", "gate"]
    assert "needs.gate.result == 'success'" in native["if"]
    assert "needs.discover.outputs.native == 'true'" in native["if"]
    assert "needs.discover.outputs.native == 'true'" in jobs["gate"]["if"]
    assert jobs["gate"]["environment"] == "eval-protected"
    checkouts = [s for s in native["steps"] if s.get("uses", "").startswith("actions/checkout@")]
    assert [s["with"]["ref"] for s in checkouts] == ["${{ github.sha }}", "${{ needs.discover.outputs.merge_sha }}",
        "d5f36921ac754705619f38c637ef692873809fbc"]
    assert all(s["with"]["persist-credentials"] is False for s in checkouts)
    assert next(s for s in native["steps"] if s.get("id") == "revision")["name"] == "Recheck approved revision before WIF"
    auth = next(s for s in native["steps"] if s.get("uses", "").startswith("google-github-actions/auth@"))
    assert auth["with"] == {"workload_identity_provider": "${{ secrets.FULLSEND_GCP_WIF_PROVIDER }}",
                            "project_id": "${{ secrets.FULLSEND_GCP_PROJECT_ID }}"}
    wrapper = (ROOT / ".github/scripts/run-native-fullsend-evals.sh").read_text()
    assert "prepare-sandbox-credentials.sh" in wrapper
    assert "HOST_GOOGLE_APPLICATION_CREDENTIALS" in wrapper
    assert "TC6726_SANDBOX_CREDENTIALS" in wrapper
    assert "--plugin-root" in wrapper and "pr-head/plugins/sdlc-workflow" in wrapper
    assert "pr-head/" not in wrapper.replace("pr-head/plugins/sdlc-workflow", "")


@pytest.mark.parametrize("head", ["a" * 40, "d" * 40])
def test_revision_rechecked_after_approval_before_wif(head):
    """An approval waiting on an older revision must fail before authentication."""
    result = run_js(script_step("run-native-evals", "Recheck approved revision before WIF")["with"]["script"],
                    {"head": head}, {"PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
                                     "BASE_SHA": "b" * 40, "SOURCE_REPO": "mrizzi/sdlc-plugins",
                                     "SOURCE_BRANCH": "verify-pr-fullsend"})
    assert bool(result["errors"]) == (head != "a" * 40)


@pytest.mark.parametrize("ordinary,native,requested,expected", [
    ("success", "success", "true", "success"), ("success", "failure", "true", "failure"),
    ("success", "skipped", "true", "failure"), ("failure", "success", "true", "failure"),
    ("skipped", "success", "true", "success"), ("success", "skipped", "false", "success"),
])
def test_combined_status_fails_on_requested_native_failure(ordinary, native, requested, expected):
    """Neither a native failure nor a requested skip is masked by ordinary success."""
    result = run_js(script_step("report-status", "Set final commit status")["with"]["script"], {}, {
        "DISCOVER_RESULT": "success", "EVALS_RESULT": ordinary, "GATE_RESULT": "skipped",
        "NATIVE_RESULT": native, "NATIVE_REQUESTED": requested,
        "NATIVE_REPORT_RESULT": "success",
        "SKILLS_CSV": "triage-security" if ordinary != "skipped" else ""})
    assert result["statuses"][0]["state"] == expected


@pytest.mark.parametrize("report_result", ["failure", "skipped", "cancelled"])
def test_combined_status_requires_successful_native_reporting(report_result):
    """Source-bound publication is mandatory even when the execution job succeeded."""
    result = run_js(script_step("report-status", "Set final commit status")["with"]["script"], {}, {
        "DISCOVER_RESULT": "success", "EVALS_RESULT": "success", "GATE_RESULT": "skipped",
        "NATIVE_RESULT": "success", "NATIVE_REQUESTED": "true", "NATIVE_REPORT_RESULT": report_result,
        "SKILLS_CSV": "triage-security"})
    assert result["statuses"][0]["state"] == "failure"


@pytest.mark.parametrize("trusted,gate,expected", [("true", "skipped", True), ("false", "success", True),
                                                ("false", "failure", False), ("false", "skipped", False)])
def test_native_job_requires_collaborator_or_current_run_approval(trusted, gate, expected):
    """Evaluate the real job condition for approved/unapproved author combinations."""
    condition = workflow()["jobs"]["run-native-evals"]["if"]
    values = {"needs.discover.result": "success", "needs.discover.outputs.native": "true",
              "needs.discover.outputs.trusted": trusted, "needs.gate.result": gate}
    for key, value in values.items():
        condition = condition.replace(key, json.dumps(value))
    condition = condition.replace("!cancelled()", "true")
    result = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify(Boolean({condition})));"],
                            capture_output=True, text=True, check=True)
    assert json.loads(result.stdout) is expected


@pytest.mark.parametrize("defect", [None, "wrong-source", "missing-outcome", "null", "false", "scorer-failed", "missing-report"])
def test_reporting_verifies_source_and_boolean_outcomes(defect):
    """Missing/incomplete/scorer failure cannot be published as successful native evidence."""
    source = {"pr_number": 299, "head_sha": "a" * 40, "merge_sha": "c" * 40,
              "base_sha": "b" * 40, "trusted_sha": "e" * 40}
    outcomes = {case: {f"assertion_{i}": True for i in range(1, n+1)}
                for case,n in {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7}.items()}
    report = {"source": source, "outcomes": outcomes, "complete": True, "total": 21, "exit_code": 0,
              "rationale": "SECRET /tmp/gha-creds-evil"}
    if defect == "wrong-source": source["head_sha"] = "d" * 40
    elif defect == "missing-outcome": del outcomes["033-absent"]["assertion_1"]
    elif defect in {"null", "false"}: outcomes["033-absent"]["assertion_1"] = None if defect == "null" else False
    elif defect == "scorer-failed": report["exit_code"] = 7
    elif defect == "missing-report": report = None
    env = {"PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
           "BASE_SHA": "b" * 40, "TRUSTED_SHA": "e" * 40, "NATIVE_RESULT": "success"}
    result = run_js(script_step("report-status", "Publish native result alongside ordinary review")["with"]["script"],
                    {"report": report}, env)
    assert bool(result["errors"]) == (defect is not None)
    if result["reviews"]:
        assert result["reviews"][0]["commit_id"] == "a" * 40
        assert "SECRET" not in result["reviews"][0]["body"]


def test_ci_adapter_separates_trusted_validation_from_tested_plugin(tmp_path, monkeypatch):
    """PR validator/pre-script/policy bytes remain sandbox data and never host commands."""
    path = ROOT / "evals/fullsend/triage-security/run-fullsend.py"
    assert path.is_file(), "Native adapter is missing"
    spec = importlib.util.spec_from_file_location("native_adapter", path)
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    # Given a deliberately adversarial plugin and distinct synthetic ADC files
    plugin = tmp_path / "untrusted-plugin"
    shutil.copytree(ROOT / "plugins/sdlc-workflow", plugin)
    for relative in ["scripts/validate-output-schema.sh", "scripts/strip_extra_properties.py", "policies/triage-security.yaml"]:
        (plugin / relative).write_text("# ADVERSARIAL TEST FIXTURE — must never run on host\nUNTRUSTED\n")
    host_adc, sandbox_adc = tmp_path / "host-adc", tmp_path / "sandbox-adc"
    host_adc.write_text("SYNTHETIC HOST"); sandbox_adc.write_text("SYNTHETIC SANDBOX")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(host_adc))
    monkeypatch.setenv("TC6726_SANDBOX_CREDENTIALS", str(sandbox_adc))
    monkeypatch.setenv("FULLSEND_GCP_OIDC_AUTH_FILE", "/synthetic/auth")
    token = tmp_path / "oidc-token"; token.write_text("SYNTHETIC NOT A TOKEN")
    monkeypatch.setenv("GCP_OIDC_TOKEN_FILE", str(token))
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    workspace = tmp_path / "case"; workspace.mkdir()
    real_run = subprocess.run
    observed = {}

    def native_boundary(command, **kwargs):
        """Double only Fullsend execution; observe real staging and environment selection."""
        if command[0] != "/synthetic/fullsend":
            return real_run(command, **kwargs)
        setup = Path(command[command.index("--fullsend-dir") + 1])
        observed.update(setup=setup, env=kwargs["env"], harness=yaml.safe_load((setup / "harness/triage-security-gate.yaml").read_text()))
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(adapter.subprocess, "run", native_boundary)
    # When the trusted adapter selects independent plugin and host resource sources
    assert adapter.run_case(ROOT, workspace, workspace / "output", "valid", "unused", "high",
                            Path("/synthetic/fullsend"), Path("/synthetic/linux-fullsend"), plugin_root=plugin) == 7
    # Then trusted host scripts and policy retain reviewed bytes, host ADC is untouched
    h = observed["harness"]
    validator = Path(h["validation_loop"]["script"])
    assert validator.read_bytes() == (ROOT / "plugins/sdlc-workflow/scripts/validate-output-schema.sh").read_bytes()
    assert Path(h["policy"]).read_bytes() == (ROOT / "plugins/sdlc-workflow/policies/triage-security.yaml").read_bytes()
    assert not validator.is_relative_to(Path(h["plugins"][0]))
    assert (Path(h["plugins"][0]) / "scripts/validate-output-schema.sh").read_bytes() == (plugin / "scripts/validate-output-schema.sh").read_bytes()
    assert observed["env"]["GOOGLE_APPLICATION_CREDENTIALS"] == str(sandbox_adc)
    assert observed["env"]["FULLSEND_GCP_OIDC_AUTH_FILE"] == "/synthetic/auth"
    assert os.environ["GOOGLE_APPLICATION_CREDENTIALS"] == str(host_adc)
    assert not list(observed["setup"].rglob("*adc*"))
    assert h["host_files"][-1] == {"src": str(token), "dest": "/sandbox/workspace/.gcp-oidc-token"}
    assert not list(observed["setup"].rglob("oidc-token"))


@pytest.mark.parametrize("variable", ["TC6726_SANDBOX_CREDENTIALS", "GCP_OIDC_TOKEN_FILE"])
def test_prepared_credential_files_must_exist_before_native_cli(tmp_path, monkeypatch, variable):
    """Missing prepared credential/token files cause failure rather than native skips."""
    spec = importlib.util.spec_from_file_location("native_adapter", ROOT / "evals/fullsend/triage-security/run-fullsend.py")
    adapter = importlib.util.module_from_spec(spec); spec.loader.exec_module(adapter)
    monkeypatch.setenv(variable, str(tmp_path / "missing"))
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    workspace = tmp_path / "workspace"; workspace.mkdir()
    with pytest.raises(ValueError, match="Missing prepared"):
        adapter.run_case(ROOT, workspace, workspace / "output", "valid", "unused", "high",
                         Path("/not-launched"), Path("/not-launched"))


def load_common():
    """Import trusted entrypoint without running its CLI."""
    spec = importlib.util.spec_from_file_location("native_common", ROOT / "evals/fullsend/run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_plugin_argument_reaches_only_trusted_adapter():
    """The selected plugin is a data argument, never a PR-owned runner/config."""
    common = load_common()
    plugin = Path("/synthetic/pr-head/plugins/sdlc-workflow")
    config = common.resolved_config(Path("/trusted/python"), "skill", "judge", "high", plugin_root=plugin)
    assert config["runner"]["command"][:2] == ["/trusted/python", str(ROOT / "evals/fullsend/triage-security/run-fullsend.py")]
    assert config["runner"]["command"][-2:] == ["--plugin-root", str(plugin)]
    assert config["dataset"]["path"] == str(ROOT / "evals/fullsend/triage-security/cases")


def test_safe_report_contains_boolean_outcomes_and_revision_without_raw_credentials(tmp_path):
    """Publishing allowlists counts/Booleans, excluding arbitrary transcript/rationale bytes."""
    common = load_common()
    # Given adversarial upstream rationale content and strict synthetic case outcomes
    run = tmp_path / "runs/triage-security-gate/synthetic"
    run.mkdir(parents=True)
    per_case = {}
    for case, count in common.ASSERTION_COUNTS.items():
        per_case[case] = {}
        for index in range(1, 8):
            per_case[case][f"assertion_{index}"] = {"value": True if index <= count else None,
                "rationale": "SECRET bearer /tmp/gha-creds-evil" if index <= count else
                f'''Skipped: condition 'annotations.get("assertion_count", 0) > {index - 1}' is false'''}
    (run / "summary.yaml").write_text(yaml.safe_dump({"run_id": "synthetic", "per_case": per_case}))
    source = {"head_sha": "a" * 40, "merge_sha": "c" * 40, "base_sha": "b" * 40, "trusted_sha": "e" * 40, "pr_number": 299}
    # When exporting only the reviewed safe report contract
    common.publish_report(run, tmp_path / "safe", source, 0)
    result = json.loads((tmp_path / "safe/native-result.json").read_text())
    assert result["source"] == source
    assert result["passed"] == result["total"] == 21 and result["exit_code"] == 0
    assert result["outcomes"]["033-absent"] == {f"assertion_{i}": True for i in range(1, 5)}
    assert "SECRET" not in (tmp_path / "safe/native-result.json").read_text()
    assert sorted(p.name for p in (tmp_path / "safe").iterdir()) == ["native-result.json"]


def test_safe_report_fails_closed_on_missing_upstream_summary(tmp_path):
    """Infrastructure failure exports source-bound failure without invented outcomes."""
    common = load_common()
    source = {"head_sha": "a" * 40, "merge_sha": "c" * 40, "base_sha": "b" * 40, "trusted_sha": "e" * 40, "pr_number": 299}
    common.publish_report(tmp_path / "missing", tmp_path / "safe", source, 1)
    result = json.loads((tmp_path / "safe/native-result.json").read_text())
    assert result["exit_code"] == 1 and result["complete"] is False and result["outcomes"] == {}


def test_native_plugin_symlinks_are_rejected_before_host_launch(tmp_path, monkeypatch):
    """PR symlinks cannot make trusted staging read external host credential bytes."""
    spec = importlib.util.spec_from_file_location("native_adapter", ROOT / "evals/fullsend/triage-security/run-fullsend.py")
    adapter = importlib.util.module_from_spec(spec); spec.loader.exec_module(adapter)
    plugin = tmp_path / "plugin"; plugin.mkdir()
    (plugin / "escape").symlink_to(tmp_path / "credentials")
    monkeypatch.delenv("FULLSEND_MINT_URL", raising=False)
    workspace = tmp_path / "workspace"; workspace.mkdir()
    with pytest.raises(ValueError, match="symlinks"):
        adapter.run_case(ROOT, workspace, workspace / "output", "valid", "unused", "high",
                         Path("/not-launched"), Path("/not-launched"), plugin_root=plugin)
