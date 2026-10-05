"""Trusted workflow contracts; no native suite or model execution lives here."""

import json
import os
from pathlib import Path
import subprocess

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]

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


@pytest.mark.parametrize("defect", [None, "wrong-source", "wrong-eval-source", "missing-outcome", "null", "false", "scorer-failed", "missing-report"])
def test_reporting_verifies_source_and_boolean_outcomes(defect):
    """Missing/incomplete/scorer failure cannot be published as successful native evidence."""
    source = {"pr_number": 299, "head_sha": "a" * 40, "merge_sha": "c" * 40,
              "base_sha": "b" * 40, "trusted_sha": "e" * 40, "eval_source_sha": "f" * 40}
    outcomes = {case: {f"assertion_{i}": True for i in range(1, n+1)}
                for case,n in {"033-absent": 4, "034-empty": 5, "035-malformed": 5, "036-valid": 7}.items()}
    report = {"source": source, "outcomes": outcomes, "complete": True, "total": 21, "exit_code": 0,
              "rationale": "SECRET /tmp/gha-creds-evil"}
    if defect == "wrong-source": source["head_sha"] = "d" * 40
    elif defect == "wrong-eval-source": source["eval_source_sha"] = "d" * 40
    elif defect == "missing-outcome": del outcomes["033-absent"]["assertion_1"]
    elif defect in {"null", "false"}: outcomes["033-absent"]["assertion_1"] = None if defect == "null" else False
    elif defect == "scorer-failed": report["exit_code"] = 7
    elif defect == "missing-report": report = None
    env = {"PR_NUMBER": "299", "HEAD_SHA": "a" * 40, "MERGE_SHA": "c" * 40,
           "BASE_SHA": "b" * 40, "TRUSTED_SHA": "e" * 40, "EVAL_SOURCE_SHA": "f" * 40, "NATIVE_RESULT": "success"}
    result = run_js(script_step("report-status", "Publish native result alongside ordinary review")["with"]["script"],
                    {"report": report}, env)
    assert bool(result["errors"]) == (defect is not None)
    if result["reviews"]:
        assert result["reviews"][0]["commit_id"] == "a" * 40
        assert "SECRET" not in result["reviews"][0]["body"]



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
