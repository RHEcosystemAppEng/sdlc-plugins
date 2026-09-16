"""Intentional CI failure for the TC-6257 E2E acceptance run.

This test is designed to FAIL in CI so the CI-dispatched verify-pr run must
source the failure from the trusted-runner-prefetched check-run data
(`github.check_runs`) and read the concatenated `--log-failed` output that the
pre_script wrote to `check-run-logs.txt` (verify-pr Correctness Check 1b).

The failing assertion's actual value is a runtime-computed digest. Its 16-hex
value is NOT written anywhere in this source file, so it can only be observed in
the pytest traceback captured in the CI failure log. If the verify-pr FAIL
report (or the auto-created CI-failure sub-task) quotes that exact value, it
proves Check 1b read the prefetched log rather than inferring the failure from
the PR diff.

This file is part of the throwaway TC-6257 E2E vehicle and is deleted after the
acceptance evidence is recorded in fullsend.md — it never lands on the TC-6257
deliverable branch (PR #302).
"""

import hashlib


def test_tc6257_ci_failure_log_canary():
    canary = hashlib.sha256(b"tc-6257-verify-pr-ci-failure-canary").hexdigest()[:16]
    assert canary == "0000000000000000", f"TC-6257 log-only canary = {canary}"
