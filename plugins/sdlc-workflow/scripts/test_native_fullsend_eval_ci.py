"""Trusted workflow contracts; no native suite or model execution lives here."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import shutil

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]


def synthetic_execution(cases):
    """SYNTHETIC TEST DATA — fixed observations, never authentic runtime evidence."""
    return {"phases_completed": True, "cases": {case: dict.fromkeys([
        "case_result_valid", "transcript_readable", "runtime_completed", "skill_invoked", "tools_completed"], True)
        for case in cases}}


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
const outputs = {}, statuses = [], errors = [], reviews = [], updates = [];
const storedReviews = data.existingReviews || [];
let prReads = 0;
const delays = [];
const setTimeout = (fn,ms)=>{delays.push(ms);fn();};
const require = name => {if (name !== 'fs') throw Error('unexpected module');
 return {existsSync:()=>Boolean(data.report),readFileSync:()=>JSON.stringify(data.report)};};
const core = {setOutput: (k,v) => outputs[k]=v, setFailed: x => errors.push(x), info:()=>{}};
const context = {repo:{owner:'RHEcosystemAppEng',repo:'sdlc-plugins'},
 payload:{workflow_run:{head_sha:data.eventHead || 'a'.repeat(40),
 head_repository:{full_name:'mrizzi/sdlc-plugins'}}}, serverUrl:'https://github.com',runId:1,runAttempt:1};
const pr = {number:data.number || 299,state:'open',user:{login:'synthetic'},
 head:{sha:data.head || 'a'.repeat(40),ref:data.branch || 'verify-pr-fullsend',repo:{full_name:'mrizzi/sdlc-plugins'}},
 base:{sha:'b'.repeat(40),ref:data.base || 'main'},merge_commit_sha:'c'.repeat(40)};
const github = {paginate:async (fn,args)=>{const response=await fn(args);return response.data || response;},rest:{
 actions:{getWorkflowRun:async()=>{
   if(data.apiError && data.apiError !== 'list') throw Error('API unavailable');
   return {data:{id:1,run_number:1,workflow_id:10,run_attempt:data.attempt || 1,created_at:'2026-10-06T07:00:00Z'}};},
 listWorkflowRuns:async()=> {if(data.apiError === 'list') throw Error('API unavailable');
 return (data.runs || []).map(r=>({...r,
   display_title:`Eval PR Run ${r.other_head?'b'.repeat(40):process.env.HEAD_SHA}`}));}},
 pulls:{list:async()=>[pr],get:async()=>{
 const revision=(data.revisions || [])[Math.min(prReads,(data.revisions || []).length-1)] || {};
 prReads++;
 return {data:{...pr,...revision}};},
 listReviews:async()=>({data:storedReviews}),
 updateReview:async r=>{updates.push(r);storedReviews.find(s=>s.id===r.review_id).body=r.body;},
 createReview:async r=>{reviews.push(r);storedReviews.push({...r,id:storedReviews.length+1,user:{login:'github-actions[bot]'}});},
 listFiles:async()=> (data.paths||[]).map(filename=>({filename}))},
 git:{getCommit:async()=>({data:{parents:(data.parents||['b'.repeat(40),'a'.repeat(40)]).map(sha=>({sha}))}})},
 repos:{getCollaboratorPermissionLevel:async()=>({data:{permission:data.permission||'read'}}),
 getContent:async()=>({data:{}}),createCommitStatus:async s=>statuses.push(s)}}};
(async()=>{for(let i=0;i<(data.repeat || 1);i++){SCRIPT
}})().then(()=>process.stdout.write(JSON.stringify({outputs,statuses,errors,reviews,updates,prReads,delays})))
.catch(e=>{process.stdout.write(JSON.stringify({outputs,statuses,errors:[...errors,e.message],reviews,updates}));});
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
    (299, "verify-pr-fullsend", ".github/scripts/check-native-fullsend-execution.py", "true"),
    (299, "verify-pr-fullsend", "plugins/sdlc-workflow/scripts/test_native_fullsend_execution.py", "true"),
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
    assert native["permissions"] == {"contents": "read", "pull-requests": "read", "id-token": "write"}
    assert native["needs"] == ["discover", "gate"]
    assert "needs.gate.result == 'success'" in native["if"]
    assert "needs.discover.outputs.native == 'true'" in native["if"]
    assert "needs.discover.outputs.native == 'true'" in jobs["gate"]["if"]
    assert jobs["gate"]["environment"] == "eval-protected"
    checkouts = [s for s in native["steps"] if s.get("uses", "").startswith("actions/checkout@")]
    assert [s["with"]["ref"] for s in checkouts] == ["${{ github.sha }}", "${{ needs.discover.outputs.merge_sha }}",
        "${{ env.NATIVE_EVAL_SOURCE_SHA }}", "d5f36921ac754705619f38c637ef692873809fbc"]
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


@pytest.mark.parametrize("defect", [None, "wrong-source", "wrong-eval-source", "missing-outcome", "null", "false", "scorer-failed", "missing-report", "execution-failed", "missing-execution"])
def test_reporting_verifies_source_and_boolean_outcomes(defect):
    """Execution and report integrity block CI while quality outcomes remain advisory."""
    source = {"pr_number": 299, "head_sha": "a" * 40, "merge_sha": "c" * 40,
              "base_sha": "b" * 40, "trusted_sha": "e" * 40, "eval_source_sha": "f" * 40}
    outcomes = {case: {f"assertion_{i}": True for i in range(1, n+1)}
                for case,n in {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7}.items()}
    report = {"source": source, "outcomes": outcomes, "complete": True, "total": 21, "exit_code": 0,
              "rationale": "SECRET /tmp/gha-creds-evil", "execution_valid": True,
              "execution": synthetic_execution(outcomes)}
    if defect == "wrong-source": source["head_sha"] = "d" * 40
    elif defect == "wrong-eval-source": source["eval_source_sha"] = "d" * 40
    elif defect == "missing-outcome": del outcomes["033-absent"]["assertion_1"]
    elif defect in {"null", "false"}: outcomes["033-absent"]["assertion_1"] = None if defect == "null" else False
    elif defect == "scorer-failed":
        report["exit_code"] = 7
        report["execution_valid"] = False
    elif defect == "execution-failed": report["execution"]["cases"]["035-malformed"]["skill_invoked"] = False
    elif defect == "missing-execution": del report["execution"]
    elif defect == "missing-report": report = None
    env = {"PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
           "BASE_SHA": "b" * 40, "TRUSTED_SHA": "e" * 40, "EVAL_SOURCE_SHA": "f" * 40, "NATIVE_RESULT": "success"}
    result = run_js(script_step("report-status", "Publish native result alongside ordinary review")["with"]["script"],
                    {"report": report}, env)
    assert bool(result["errors"]) == (defect not in (None, "false"))
    if result["reviews"]:
        assert result["reviews"][0]["commit_id"] == "a" * 40
        assert "SECRET" not in result["reviews"][0]["body"]
        if report is not None:
            assert "quality score (advisory)" in result["reviews"][0]["body"]



def test_wrapper_rejects_different_reviewed_suite_before_credentials(tmp_path):
    """A mismatched suite checkout must stop before setup or credential access."""
    tools = tmp_path / "tools"
    tools.mkdir()
    git = tools / "git"
    git.write_text("#!/bin/sh\ncase \"$2\" in *upstream-fullsend) echo d5f36921ac754705619f38c637ef692873809fbc;; *) echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;; esac\n")
    git.chmod(0o755)
    environment = dict(os.environ, GITHUB_WORKSPACE=str(tmp_path), RUNNER_TEMP=str(tmp_path),
                       NATIVE_EVAL_SOURCE_SHA="b" * 40, PATH=str(tools) + os.pathsep + os.environ["PATH"])
    environment.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    result = subprocess.run(["bash", str(ROOT / ".github/scripts/run-native-fullsend-evals.sh"), "run"],
                            env=environment, capture_output=True, text=True)
    assert result.returncode != 0
    assert "Reviewed native eval source changed" in result.stdout
    assert "WIF host ADC" not in result.stderr


@pytest.mark.parametrize("job", ["discover", "run-evals", "report-status"])
def test_all_publication_jobs_check_latest_run(job):
    """Every status/review write requires a successful latest-run check."""
    job_data = workflow()["jobs"][job]
    guard = next(s for s in job_data["steps"] if s.get("id") == "publication")
    assert guard["env"]["HEAD_SHA"] == "${{ github.event.workflow_run.head_sha }}"
    assert workflow()["run-name"] == "Eval PR Run ${{ github.event.workflow_run.head_sha }}"
    if "permissions" in job_data:
        assert job_data["permissions"]["actions"] == "read"
    for step in job_data["steps"]:
        script = step.get("with", {}).get("script", "")
        if any(api in script for api in ["createCommitStatus(", "createReview(", "updateReview("]):
            assert any(f"steps.{name}.outputs.latest == 'true'" in step["if"]
                       for name in ["publication", "gate-publication"])


@pytest.mark.parametrize("runs,attempt,api_error,expected", [
    ([{"id": 1, "run_number": 1}], 1, False, "true"),
    ([{"id": 1, "run_number": 1}, {"id": 2, "run_number": 2}], 1, False, "false"),
    ([{"id": 1, "run_number": 1}, {"id": 2, "run_number": 2, "other_head": True}], 1, False, "true"),
    ([], 1, False, "true"),
    ([{"id": 1, "run_number": 1}], 2, False, "false"),
    ([{"id": 1, "run_number": 1}], 1, True, "false"),
])
def test_latest_run_guard_refuses_superseded_or_unidentifiable_runs(runs, attempt, api_error, expected):
    """Execute the real guard for newer runs, other heads, reruns and API failures."""
    script = script_step("discover", "Check latest run before publishing")["with"]["script"]
    result = run_js(script, {"runs": runs, "attempt": attempt, "apiError": api_error}, {"HEAD_SHA": "a" * 40})
    assert result["outputs"].get("latest") == expected
    assert bool(result["errors"]) == api_error


def test_same_pr_head_cannot_publish_concurrently():
    """The workflow lock covers both ordinary and native publication sequences."""
    concurrency = workflow().get("concurrency", {})
    assert concurrency.get("group") == "eval-pr-run-${{ github.event.workflow_run.head_sha }}"
    assert concurrency["cancel-in-progress"] is False


@pytest.mark.parametrize("native", [True, False])
@pytest.mark.parametrize("existing_kind", ["none", "matching", "wrong-head", "human", "other-suite", "later-page"])
def test_review_reruns_reuse_only_matching_bot_head_review(native, existing_kind):
    """Both publishers create once, update reruns and leave unrelated reviews alone."""
    job, name = ("report-status", "Publish native result alongside ordinary review") if native else (
        "run-evals", "Post eval results review")
    script = script_step(job, name)["with"]["script"]
    marker = "## Native Fullsend Eval Results" if native else "## Eval Results"
    existing = {"id": 888, "user": {"login": "github-actions[bot]"}, "commit_id": "a" * 40, "body": marker}
    if existing_kind == "wrong-head": existing["commit_id"] = "b" * 40
    elif existing_kind == "human": existing["user"]["login"] = "human"
    elif existing_kind == "other-suite": existing["body"] = "## Eval Results" if native else "## Native Fullsend Eval Results"
    stored = [] if existing_kind == "none" else [existing]
    if existing_kind == "later-page":
        stored = [{"id": i, "user": {"login": "human"}} for i in range(100)] + stored
        assert "github.paginate(github.rest.pulls.listReviews" in script
    source = {"pr_number": 299, "head_sha": "a" * 40, "merge_sha": "c" * 40,
              "base_sha": "b" * 40, "trusted_sha": "e" * 40, "eval_source_sha": "f" * 40}
    report = {"source": source, "complete": True, "total": 21, "exit_code": 0,
              "outcomes": {case: {f"assertion_{i}": True for i in range(1, n+1)}
                           for case,n in {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7}.items()}}
    report.update(execution_valid=True, execution=synthetic_execution(report["outcomes"]))
    result = run_js(script, {"report": report, "existingReviews": stored, "repeat": 2}, {
        "PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
        "BASE_SHA": "b" * 40, "TRUSTED_SHA": "e" * 40, "EVAL_SOURCE_SHA": "f" * 40,
        "NATIVE_RESULT": "success", "SKILLS_CSV": "triage-security"})
    reuse = existing_kind in {"matching", "later-page"}
    assert result["errors"] == []
    assert len(result["reviews"]) == (0 if reuse else 1)
    assert len(result["updates"]) == (2 if reuse else 1)
    assert all(r["body"].startswith(marker) for r in result["reviews"] + result["updates"])
    if reuse:
        assert all(r["review_id"] == 888 for r in result["updates"])
    else:
        assert all(r["review_id"] != 888 for r in result["updates"])


@pytest.mark.parametrize("revisions,parents,expected_sha,reads", [
    ([{"merge_commit_sha": None}, {"merge_commit_sha": "c" * 40}], None, "c" * 40, 2),
    ([{"merge_commit_sha": None}], None, None, 3),
    ([{"merge_commit_sha": None}, {"merge_commit_sha": "c" * 40, "head": {"sha": "d" * 40}}], None, None, 2),
    ([{"merge_commit_sha": None}, {"merge_commit_sha": "c" * 40}], ["b" * 40, "d" * 40], None, 2),
    ([{"merge_commit_sha": "invalid"}], None, None, 1),
])
def test_merge_source_poll_is_bounded_and_preserves_revision_checks(revisions, parents, expected_sha, reads):
    """Transient nulls recover; persistent nulls and changed revisions fail closed."""
    # Given API mergeability responses and exact merge-parent evidence
    data = {"revisions": revisions}
    if parents is not None:
        data["parents"] = parents
    # When resolving the event-associated PR in the real workflow script
    result = run_js(script_step("discover", "Resolve PR identity and check trust")["with"]["script"], data)
    # Then retries are bounded and only the verified merge reaches downstream jobs
    assert result["outputs"].get("merge_sha") == expected_sha
    assert bool(result["errors"]) == (expected_sha is None)
    assert result["prReads"] == reads
    assert result["delays"] == [2000] * (reads - 1)
    if revisions == [{"merge_commit_sha": None}]:
        assert result["errors"] == ["PR identity/revision changed or merge source unavailable"]


def test_native_artifact_download_failure_keeps_controlled_reporting():
    """Missing native artifacts are nonfatal downloads while evidence still fails closed."""
    # Given the reporting job's native artifact download
    step = script_step("report-status", "Download safe native result")
    # Then its existing guard is preserved and download errors can reach the reporter
    assert step.get("continue-on-error") is True
    assert step["if"] == "needs.discover.outputs.native == 'true' && needs.run-native-evals.result != 'skipped'"
    assert step["with"] == {"name": "native-fullsend-result", "path": "native-report"}
    # When no artifact is available, the real publisher emits controlled failure evidence
    result = run_js(script_step("report-status", "Publish native result alongside ordinary review")["with"]["script"], {}, {
        "PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
        "BASE_SHA": "b" * 40, "TRUSTED_SHA": "e" * 40, "EVAL_SOURCE_SHA": "f" * 40, "NATIVE_RESULT": "failure"})
    assert result["errors"] == ["Native evidence incomplete, failed, or missing"]
    assert "No safe native result was produced; native execution/approval failed." in result["reviews"][0]["body"]


def run_credential_wrapper(tmp_path, output, passed=21, broken_execution=False):
    """Run the real wrapper/checker with synthetic credentials and inference records."""
    # Given explicitly synthetic native artifacts, generated without inference
    spec = importlib.util.spec_from_file_location("execution_fixtures", ROOT / "plugins/sdlc-workflow/scripts/test_native_fullsend_execution.py")
    fixtures = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixtures)
    private, run, safe, source, status = fixtures.synthetic_run(tmp_path, passed)
    source.update(merge_sha="c" * 40, base_sha="b" * 40, trusted_sha="e" * 40, eval_source_sha="b" * 40)
    report = json.loads(safe.read_text())
    report["source"] = source
    safe.write_text(json.dumps(report))
    if broken_execution:
        next((run / "cases/035-malformed").glob("output/native/*/iteration-*/output.jsonl")).unlink()
    private.rename(tmp_path / "tc6726-private")
    safe.parent.rename(tmp_path / "tc6726-safe")
    checker_path = tmp_path / ".github/scripts/check-native-fullsend-execution.py"
    checker_path.parent.mkdir(parents=True)
    shutil.copy2(ROOT / ".github/scripts/check-native-fullsend-execution.py", checker_path)
    tools = tmp_path / "tools"
    tools.mkdir()
    scripts = tmp_path / "upstream-fullsend/internal/scaffold/fullsend-repo/scripts"
    scripts.mkdir(parents=True)
    fixture = tmp_path / "prepared-output.txt"
    fixture.write_text(output)
    (scripts / "prepare-sandbox-credentials.sh").write_text(
        '#!/bin/sh\n# SYNTHETIC TEST DATA — emit the test environment file\ncat "$TC6742_FIXTURE" >> "$GITHUB_ENV"\n')
    doubles = {
        "git": '#!/bin/sh\n# SYNTHETIC TEST DATA — immutable checkout identities\ncase "$2" in *upstream-fullsend) echo d5f36921ac754705619f38c637ef692873809fbc;; *) echo bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;; esac\n',
        "jq": '#!/bin/sh\n# SYNTHETIC TEST DATA — host ADC type\necho external_account\n',
        "python3.12": '#!/usr/bin/env python3\n# SYNTHETIC TEST DATA — double inference only; execute the actual checker\nimport json, os, sys\nfrom pathlib import Path\nif sys.argv[1].endswith("check-native-fullsend-execution.py"):\n    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])\nPath(os.environ["TC6742_CAPTURE"]).with_suffix(".argv.json").write_text(json.dumps(sys.argv[1:]))\nPath(os.environ["TC6742_CAPTURE"]).write_text(json.dumps({k: os.environ.get(k) for k in ["GOOGLE_APPLICATION_CREDENTIALS", "TC6726_SANDBOX_CREDENTIALS", "GCP_OIDC_TOKEN_FILE", "FULLSEND_GCP_OIDC_URL", "FULLSEND_GCP_OIDC_AUTH_FILE", "TC6742_UNEXPECTED"]}))\nsys.exit(int(os.environ["TC6809_RUNNER_EXIT"]))\n',
    }
    for name, content in doubles.items():
        path = tools / name
        path.write_text(content)
        path.chmod(0o755)
    capture = tmp_path / "captured.json"
    environment = dict(os.environ, GITHUB_WORKSPACE=str(tmp_path), RUNNER_TEMP=str(tmp_path),
                       GOOGLE_APPLICATION_CREDENTIALS="synthetic-host-adc", ANTHROPIC_VERTEX_PROJECT_ID="synthetic",
                       CLOUD_ML_REGION="global", TC6726_HEAD_SHA="a" * 40, NATIVE_EVAL_SOURCE_SHA="b" * 40,
                       TC6726_MERGE_SHA="c" * 40, TC6726_BASE_SHA="b" * 40, TC6726_TRUSTED_SHA="e" * 40,
                       TC6726_EVAL_SOURCE_SHA="b" * 40, TC6726_PR_NUMBER="299", TC6809_RUNNER_EXIT=str(status),
                       TC6742_FIXTURE=str(fixture), TC6742_CAPTURE=str(capture),
                       PATH=str(tools) + os.pathsep + os.environ["PATH"])
    for name in ["TC6726_SANDBOX_CREDENTIALS", "GCP_OIDC_TOKEN_FILE", "FULLSEND_GCP_OIDC_URL", "FULLSEND_GCP_OIDC_AUTH_FILE", "TC6742_UNEXPECTED"]:
        environment.pop(name, None)
    result = subprocess.run(["bash", str(ROOT / ".github/scripts/run-native-fullsend-evals.sh"), "run"],
                            env=environment, capture_output=True, text=True)
    return result, json.loads(capture.read_text()) if capture.exists() else None


@pytest.mark.parametrize("passed,broken,expected", [(20, False, 0), (16, False, 0), (0, False, 0), (21, True, 1)])
def test_wrapper_enforces_execution_integrity_instead_of_quality_score(tmp_path, passed, broken, expected):
    """The real wrapper accepts advisory scores but blocks missing native execution."""
    # Given synthetic credential preparation and native artifacts
    output = "GOOGLE_APPLICATION_CREDENTIALS=synthetic-adc\nGCP_OIDC_TOKEN_FILE=synthetic-token\nFULLSEND_GCP_OIDC_URL=https://synthetic.invalid/\nFULLSEND_GCP_OIDC_AUTH_FILE=synthetic-auth\n"
    # When running the actual shell wrapper and trusted Python checker
    result, _ = run_credential_wrapper(tmp_path, output, passed, broken)
    # Then CI exit policy follows execution evidence, not the LLM score
    assert result.returncode == expected, result.stderr
    assert "Native execution evidence:" in result.stdout


@pytest.mark.parametrize("heredoc", [False, True])
def test_credential_parser_accepts_blank_lines_and_heredoc_values(tmp_path, heredoc):
    """Valid environment syntax captures/masks required values and preserves host ADC."""
    # Given synthetic credentials, with optional multiline output
    expected = {"TC6726_SANDBOX_CREDENTIALS": "synthetic-sandbox-adc", "GCP_OIDC_TOKEN_FILE": "synthetic-token-file",
                "FULLSEND_GCP_OIDC_URL": "https://synthetic.invalid/?audience=eval", "FULLSEND_GCP_OIDC_AUTH_FILE": "synthetic-auth-file"}
    names = {"GOOGLE_APPLICATION_CREDENTIALS": "TC6726_SANDBOX_CREDENTIALS", **{k: k for k in expected if k != "TC6726_SANDBOX_CREDENTIALS"}}
    if heredoc:
        expected["FULLSEND_GCP_OIDC_AUTH_FILE"] = "synthetic-auth%file\nsynthetic-second-line"
    output = "\n".join(f"{name}<<END\n{expected[key]}\nEND" if heredoc else f"{name}={expected[key]}"
                       for name,key in names.items())
    # When the actual wrapper parses blank lines and heredoc input
    result, captured = run_credential_wrapper(tmp_path, "\n" + output + "\n\n")
    # Then the scoring process gets parsed values and the original host ADC
    assert result.returncode == 0, result.stderr
    assert captured == {"GOOGLE_APPLICATION_CREDENTIALS": "synthetic-host-adc", **expected, "TC6742_UNEXPECTED": None}
    for value in expected.values():
        escaped = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        assert f"::add-mask::{escaped}" in result.stdout


@pytest.mark.parametrize("record", [
    "TC6742_UNEXPECTED=synthetic-unknown-value\n",
    "TC6742_UNEXPECTED<<END\nGOOGLE_APPLICATION_CREDENTIALS=synthetic-unknown-value\nEND\n",
])
def test_credential_parser_rejects_unknown_names_without_exposing_values(tmp_path, record):
    """Unknown names fail before inference with a diagnostic that exposes no value."""
    # Given valid known outputs followed by an unrecognized name
    output = "GOOGLE_APPLICATION_CREDENTIALS=synthetic-adc\nGCP_OIDC_TOKEN_FILE=synthetic-token\nFULLSEND_GCP_OIDC_URL=https://synthetic.invalid/\nFULLSEND_GCP_OIDC_AUTH_FILE=synthetic-auth\n" + record
    # When parsing a single-line or complete heredoc record
    result, captured = run_credential_wrapper(tmp_path, output)
    # Then the allowlist fails closed before the native runner is invoked
    assert result.returncode != 0
    assert "::error::Unexpected upstream credential output" in result.stdout
    assert "synthetic-unknown-value" not in result.stdout + result.stderr
    assert captured is None


@pytest.mark.parametrize("output,error", [
    ("\nGOOGLE_APPLICATION_CREDENTIALS=synthetic-adc\n", "Native OIDC mount is required"),
    ("GOOGLE_APPLICATION_CREDENTIALS<<END\nsynthetic-adc\n", "Unterminated upstream credential value"),
])
def test_credential_parser_rejects_missing_or_unterminated_required_data(tmp_path, output, error):
    """Missing required fields and incomplete heredocs fail before native inference."""
    # Given incomplete synthetic credential output
    # When the actual wrapper processes it
    result, captured = run_credential_wrapper(tmp_path, output)
    # Then required guards prevent execution without complete credentials
    assert result.returncode != 0
    assert error in result.stdout + result.stderr
    assert captured is None


@pytest.mark.parametrize("api_error,newer,expected", [("get", False, "failure"), ("list", False, "failure"), (False, True, None)])
def test_guard_errors_publish_terminal_failure_but_superseded_runs_skip(api_error, newer, expected):
    """API guard errors conclude the check; observed newer runs still suppress writes."""
    # Given successful eval jobs and a guard error or an observed newer run
    runs = [{"id": 1, "run_number": 1}]
    if newer:
        runs.append({"id": 2, "run_number": 2})
    guard = run_js(script_step("report-status", "Check latest run before publishing")["with"]["script"],
                   {"apiError": api_error, "runs": runs}, {"HEAD_SHA": "a" * 40})
    # When evaluating the real final status step condition
    step = script_step("report-status", "Set final commit status")
    condition = step["if"].replace("always()", "true")
    for key in ["latest", "error"]:
        condition = condition.replace(f"steps.publication.outputs.{key}", json.dumps(guard["outputs"].get(key, "")))
    allowed = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify(Boolean({condition})));"],
                             capture_output=True, text=True, check=True)
    env = {"DISCOVER_RESULT": "success", "EVALS_RESULT": "success", "GATE_RESULT": "skipped",
           "NATIVE_REQUESTED": "false", "SKILLS_CSV": "triage-security", "PUBLICATION_GUARD_ERROR": guard["outputs"].get("error", "")}
    result = run_js(step["with"]["script"], {}, env) if json.loads(allowed.stdout) else {"statuses": []}
    # Then API errors terminate with failure, while supersession posts no status
    assert [s["state"] for s in result["statuses"]] == ([] if expected is None else [expected])
    if api_error:
        assert step["env"]["PUBLICATION_GUARD_ERROR"] == "${{ steps.publication.outputs.error }}"


@pytest.mark.parametrize("runs,expected", [
    ([], True), ([{"id": 0, "run_number": 0}], True),
    ([{"id": 1, "run_number": 1}], True), ([{"id": 2, "run_number": 2}], False),
])
def test_unindexed_current_run_posts_pending_and_approval_statuses(runs, expected):
    """Only an observed newer run suppresses current pending/approval publication."""
    # Given a lagging or newer Actions run list
    guard = run_js(script_step("discover", "Check latest run before publishing")["with"]["script"],
                   {"runs": runs}, {"HEAD_SHA": "a" * 40})
    # When evaluating each real pending-status condition and script
    states = []
    for name in ["Set pending commit status", "Update status for approval gate"]:
        step = script_step("discover", name)
        condition = step["if"]
        for key,value in {"steps.publication.outputs.latest": guard["outputs"].get("latest", ""),
                          "steps.gate-publication.outputs.latest": guard["outputs"].get("latest", ""),
                          "steps.pr.outputs.trusted": "false", "steps.pr.outputs.pr_number": "299"}.items():
            condition = condition.replace(key, json.dumps(value))
        allowed = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify(Boolean({condition})));"],
                                 capture_output=True, text=True, check=True)
        if json.loads(allowed.stdout):
            states.extend(s["state"] for s in run_js(step["with"]["script"], {})["statuses"])
    # Then both statuses publish unless strictly newer execution is observed
    assert guard["errors"] == []
    assert states == (["pending", "pending"] if expected else [])


def test_multiline_credentials_register_individual_nonempty_masks(tmp_path):
    """Each nonempty credential line receives an escaped explicit mask directive."""
    # Given multiline synthetic credentials with an empty line and command-like data
    output = "GOOGLE_APPLICATION_CREDENTIALS=synthetic-adc\nGCP_OIDC_TOKEN_FILE=synthetic-token\nFULLSEND_GCP_OIDC_URL=https://synthetic.invalid/\nFULLSEND_GCP_OIDC_AUTH_FILE<<END\nsynthetic%first\n\n::warning::synthetic-second\nEND\n"
    # When the real wrapper prepares credential masks
    result, captured = run_credential_wrapper(tmp_path, output)
    # Then each line is registered without emitting a second workflow command
    assert result.returncode == 0, result.stderr
    assert captured["FULLSEND_GCP_OIDC_AUTH_FILE"] == "synthetic%first\n\n::warning::synthetic-second"
    lines = result.stdout.splitlines()
    assert "::add-mask::synthetic%25first" in lines
    assert "::add-mask::::warning::synthetic-second" in lines
    assert "::add-mask::" not in lines
    assert "::warning::synthetic-second" not in lines


def test_native_wrapper_passes_requested_judge_model(tmp_path):
    """The trusted wrapper overrides the reviewed runner's older judge default."""
    output = ("GOOGLE_APPLICATION_CREDENTIALS=synthetic-sandbox-adc\n"
              "GCP_OIDC_TOKEN_FILE=synthetic-token\n"
              "FULLSEND_GCP_OIDC_URL=synthetic-url\n"
              "FULLSEND_GCP_OIDC_AUTH_FILE=synthetic-auth\n")
    result, _ = run_credential_wrapper(tmp_path, output)
    assert result.returncode == 0
    arguments = json.loads((tmp_path / "captured.argv.json").read_text())
    assert arguments[1] == "run"
    assert arguments[arguments.index("--judge-model") + 1] == "claude-opus-4-8"


def run_ordinary_eval_step(tmp_path, mode, skills="first"):
    """SYNTHETIC TEST DATA — execute real CI shell with a non-inference Claude stub."""
    tools = tmp_path / "tools"
    tools.mkdir()
    claude = tools / "claude"
    claude.write_text(f"#!{sys.executable}\n" + r'''
import json, os, re, sys
from pathlib import Path
args = sys.argv[1:]
workspace = Path(re.search(r"Workspace: (.+)", args[args.index("-p") + 1])[1])
with open("calls.jsonl", "a") as capture:
    capture.write(json.dumps(args) + "\n")
with open("wait-settings.jsonl", "a") as capture:
    capture.write(json.dumps({name: os.environ.get(name) for name in (
        "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS", "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB")}) + "\n")
mode = os.environ["EVAL_STUB_MODE"] if workspace.name == "first-eval-pr" else "correct"
if mode == "exit":
    sys.exit(7)
target = Path("pr-head/eval-workspace") if mode == "misplaced" else workspace
target.mkdir(parents=True, exist_ok=True)
for name in ("benchmark.json", "feedback.json", "summary.md"):
    if mode == "missing-" + name or mode == "absent":
        continue
    if mode == "directory-" + name:
        (target / name).mkdir()
        continue
    if mode == "symlink-" + name:
        outside = Path.cwd() / ("outside-" + name)
        outside.write_text("synthetic outside result\n")
        (target / name).symlink_to(outside)
        continue
    (target / name).write_text("" if mode == "empty-" + name else "synthetic result\n")
''')
    claude.chmod(0o755)
    for skill in skills.split(","):
        source = tmp_path / "pr-head/evals" / skill
        source.mkdir(parents=True)
        (source / "evals.json").write_text('{"evals": [{"id": 1}]}')
    step = script_step("run-evals", "Run PR evals")
    script = step["run"].replace(
        'workspace="/tmp/${skill}-eval-pr"', f'workspace="{tmp_path}/${{skill}}-eval-pr"')
    env = dict(os.environ, PATH=f"{tools}:{os.environ['PATH']}",
               SKILLS_CSV=skills, EVAL_STUB_MODE=mode)
    env.pop("CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS", None)
    for name in ("CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS", "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB"):
        if name in step["env"]:
            env[name] = step["env"][name]
    result = subprocess.run(["bash", "-e", "-o", "pipefail", "-c", script], cwd=tmp_path,
                            env=env,
                            capture_output=True, text=True)
    calls = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
    return result, calls


def test_ordinary_eval_passes_background_wait_setting_to_each_cli(tmp_path):
    """Both real shell invocations inherit the workflow wait policy and scrubbing."""
    result, calls = run_ordinary_eval_step(tmp_path, "correct", "first,second")
    assert result.returncode == 0, result.stdout + result.stderr
    assert len(calls) == 2
    settings = [json.loads(line) for line in (tmp_path / "wait-settings.jsonl").read_text().splitlines()]
    assert settings == [{"CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0",
                         "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1"}] * 2


def test_ordinary_eval_job_bounds_background_wait():
    """Disabling the CLI idle ceiling still leaves an explicit total CI limit."""
    assert workflow()["jobs"]["run-evals"].get("timeout-minutes") == 90


@pytest.mark.parametrize("mode", ["absent", "misplaced", "missing-benchmark.json",
                                 "missing-feedback.json", "missing-summary.md",
                                 "empty-benchmark.json", "empty-feedback.json", "empty-summary.md",
                                 "directory-benchmark.json", "directory-feedback.json", "directory-summary.md",
                                 "symlink-benchmark.json", "symlink-feedback.json", "symlink-summary.md"])
def test_ordinary_eval_rejects_missing_results_in_requested_workspace(tmp_path, mode):
    """An exit-zero CLI cannot pass CI with absent, empty, relocated or linked results."""
    result, _ = run_ordinary_eval_step(tmp_path, mode)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "::error::" in result.stdout


def test_ordinary_eval_authorizes_requested_workspace_and_keeps_results(tmp_path):
    """The invocation grants the exact output directory without dropping sandbox settings."""
    result, calls = run_ordinary_eval_step(tmp_path, "correct")
    assert result.returncode == 0, result.stdout + result.stderr
    args = calls[0]
    directories = [args[i + 1] for i, arg in enumerate(args) if arg == "--add-dir"]
    assert "pr-head" in directories
    assert str(tmp_path / "first-eval-pr") in directories
    assert args[args.index("--permission-mode") + 1] == "dontAsk"
    assert args[args.index("--settings") + 1] == "/tmp/eval-sandbox-settings.json"
    assert (tmp_path / "first-eval-pr/summary.md").read_text() == "synthetic result\n"


@pytest.mark.parametrize("mode", ["exit", "absent", "symlink-summary.md"])
def test_ordinary_eval_attempts_remaining_skills_after_failure(tmp_path, mode):
    """CLI and result-path failures must not skip subsequent requested skills."""
    result, calls = run_ordinary_eval_step(tmp_path, mode, "first,second")
    assert result.returncode == 1, result.stdout + result.stderr
    assert len(calls) == 2
    assert (tmp_path / "second-eval-pr/summary.md").is_file()
