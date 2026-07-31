# Step 8 -- Remediation

## Triage Decision: Case B -- Affected versions exist within scope

The 2.2.x stream (this issue's scope) has affected versions: 2.2.0, 2.2.1, 2.2.2. Remediation tasks are required.

**Ecosystem**: Cargo (source dependency) -- creates **2 tasks** per stream: upstream backport + downstream propagation subtask with Blocks dependency (Important Rule 8).

---

## Task 1: Upstream Backport Task (2.2.x stream)

### Proposed Jira Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8 (from supportability matrix)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z (from Ecosystem Mappings Upstream Branch column)
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

### Proposed Jira Task

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-backport-task-key] (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Linkage

The following Jira links would be proposed after task creation:

1. **Depend**: TC-8001 (Vulnerability issue) -> upstream backport task (remediation)
2. **Depend**: TC-8001 (Vulnerability issue) -> downstream propagation task (remediation)
3. **Blocks**: upstream backport task -> downstream propagation task (upstream must merge before downstream can proceed)

## Post-Creation Actions (Proposed)

The following actions are proposed pending engineer confirmation:

- **Propose** adding `ai-cve-triaged` label to TC-8001
- **Propose** transitioning TC-8001 to In Progress
- **Propose** posting a summary comment to TC-8001 with the version impact table, Affects Versions correction, and links to created remediation tasks

All of the above are proposed actions. No Jira mutations have been executed -- every mutation requires explicit engineer confirmation per the skill guardrails.
