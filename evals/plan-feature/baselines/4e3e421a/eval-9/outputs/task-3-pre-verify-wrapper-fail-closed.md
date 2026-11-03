# Task 3 — Make the pre-verify wrapper fail closed on any gate failure

**Summary:** TC-9008: Fail pre-verify.sh on any non-zero gate exit instead of only on 401/403 stderr
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9008)
**Fix Versions:** (omitted, because TC-9008 has none)
**Epic group (by-sub-feature):** TC-9008: Verification gate

## Repository
release-verifier

## Target Branch
main

## Description
`scripts/pre-verify.sh` runs the gate before verification. It reports an authentication failure only when the client's stderr contains 401/403. An unauthenticated gateway request that returns 200 + `[]` never triggers that, so the wrapper lets the run continue (or skip) as green. After Tasks 1 and 2, the gate exits non-zero when tracker auth can't be verified. This task makes the wrapper honor that exit, so the whole pipeline fails closed.

## Files to Modify
- `scripts/pre-verify.sh`: propagate the gate's exit status (`set -euo pipefail`, or explicit `$?` checks). Report an auth failure when it sees the gate's stable `tracker auth unverified` message as well as 401/403. Never continue to verification, or exit 0, after a non-zero gate exit.

## Implementation Notes
- **Guard site:** in `scripts/pre-verify.sh`, the block that runs the gate and greps client stderr for 401/403. Right now the exit decision depends on the grep. Change it so that **any** non-zero exit from the gate aborts the wrapper with a non-zero status. The grep becomes diagnostic only: it picks the message ("tracker authentication failed" vs "gate failed") and no longer decides pass/fail.
- If the gate's output is piped through `grep`/`tee`, use `set -o pipefail` or capture `PIPESTATUS`, so the gate's exit code isn't masked by the pipeline.
- Keep the normal skip path: when the gate exits 0 and reports "no linked issue" or "not Ready for Verification", the wrapper skips verification and exits 0, as today.
- Per docs/constraints.md §2: commits must follow Conventional Commits, reference TC-9008 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3: branch named after the Jira task key. `gh pr create --base main`. Post the PR link on the Jira task.
- Per docs/constraints.md §5: limit changes to `scripts/pre-verify.sh` and its test. Inspect the script before editing.

## Files to Create
- `tests/scripts/test_pre_verify.py`: tests that run `scripts/pre-verify.sh` with a stubbed gate command (no shell-script test location exists in the provided repository structure; confirm the test layout against the real repo and adapt the path if a different convention exists).

## Acceptance Criteria
- [ ] **Fail-closed:** `pre-verify.sh` exits non-zero and does not start verification whenever the gate exits non-zero, whether or not stderr contains 401/403.
- [ ] The gate's `tracker auth unverified` failure is reported as an authentication failure.
- [ ] Existing 401/403 reporting keeps working.
- [ ] A gate exit of 0 with a skip result still skips verification and exits 0. A gate exit of 0 with a ready issue still runs verification.

## Test Requirements
- [ ] **Degraded-path test:** a stub gate exits non-zero with stderr that contains no 401/403 text, which simulates the 200 + `[]` unauthenticated case caught by Task 2. Assert that the wrapper exits non-zero and does not invoke the verification step.
- [ ] Test that stub gate stderr containing `tracker auth unverified` produces the authentication-failure message and a non-zero exit.
- [ ] Test that stub gate stderr containing 401 produces a non-zero exit (regression).
- [ ] Test that a stub gate exiting 0 with a skip result makes the wrapper exit 0 without running verification.

## Verification Commands
- `pytest tests/scripts/test_pre_verify.py`: all tests pass.
- `bash -n scripts/pre-verify.sh`: no syntax errors.

## Dependencies
- Depends on: Task 2 — Gate verification on a "Ready for Verification" linked issue, and fail closed when tracker auth is unverified
