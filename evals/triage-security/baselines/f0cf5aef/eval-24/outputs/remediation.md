# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Decision

- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency) — 2 tasks per affected stream
- **Deployment context**: upstream (default; Deployment Context column absent from Source Repositories table)
- **Coordination Guidance**: Omitted (Deployment Context column absent — backward compatibility)

### Stream 2.2.x (in-scope)

The fix is already present in the latest releases of the 2.2.x stream:
- Upstream branch `release/0.4.z` already has quinn-proto 0.11.14 (since tag v0.4.11)
- Downstream releases 2.2.3 (build 0.4.11) and 2.2.4 (build 0.4.12) already ship the fix
- **No new remediation tasks needed** — the fix has already been shipped
- Affects Versions corrected to: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Stream 2.1.x (cross-stream, Case A — preemptive)

The 2.1.x stream is affected but has no stream-specific CVE Jira for CVE-2026-31812.
Upstream branch `release/0.3.z` does NOT have the fix (latest tag v0.3.12 ships quinn-proto 0.11.9).
Two preemptive remediation tasks are created below.

---

## Task 1: Upstream Backport (2.1.x — preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE Jira from stream 2.2.x)

### Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Upstream fix is NOT present on release/0.3.z — this branch still has quinn-proto 0.11.9
- The fix exists on release/0.4.z (2.2.x stream) since v0.4.11 — may be useful as a reference for the backport

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog and PR quinn-rs/quinn#2048)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE tracking issue, stream 2.2.x)

---

## Task 2: Downstream Propagation (2.1.x — preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE Jira from stream 2.2.x); Blocked by Task 1 (upstream backport)

### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task (Task 1).

The upstream backport (Task 1) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: Task 1 (upstream backport must merge first)
- Related to: TC-8001 (originating CVE tracking issue, stream 2.2.x)

---

## Jira Linkage Summary

| Task | Type | Link to TC-8001 | Link Between Tasks |
|------|------|-----------------|-------------------|
| Task 1 (upstream backport, 2.1.x) | Preemptive | Related | — |
| Task 2 (downstream propagation, 2.1.x) | Preemptive | Related | Blocked by Task 1 (Blocks) |

## Post-Triage Actions

1. **Correct Affects Versions** on TC-8001: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Add `ai-cve-triaged` label** to TC-8001
3. **Post cross-stream impact comment** to TC-8001:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
   > All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9 (vulnerable).
   > Stream 2.1.x is not tracked by a companion CVE Jira and may require separate PSIRT triage.
4. **Post preemptive task comment** to TC-8001:
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: Task 1 (upstream backport), Task 2 (downstream propagation) (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive
   > label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   > reconciliation will link them and remove the label.
5. **Post summary comment** to TC-8001 with version impact table, Affects Versions correction, and triage outcome
