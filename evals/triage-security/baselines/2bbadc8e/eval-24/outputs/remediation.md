# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Decision

### 2.2.x Stream (scoped)

The fix for CVE-2026-31812 is **already present** in the 2.2.x stream. Product versions 2.2.3 (build 0.4.11) and 2.2.4 (build 0.4.12) ship quinn-proto 0.11.14, which is the fixed version. The upstream branch `release/0.4.z` already carries the fix.

**No new remediation tasks are required for the 2.2.x stream.** The Affects Versions correction (Step 3) records the historical impact on versions 2.2.0, 2.2.1, and 2.2.2.

### 2.1.x Stream (cross-stream, preemptive)

All versions in the 2.1.x stream (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). The upstream branch `release/0.3.z` does NOT have the fix. No sibling CVE Jira exists for this stream.

**Preemptive remediation tasks are required** -- two tasks per the Cargo (source dependency) ecosystem classification: upstream backport + downstream propagation.

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x)

**PROPOSED Jira Task creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

quinn-proto before version 0.11.14 allows a remote attacker to cause a panic
by sending a QUIC transport frame that creates an excessive number of streams
(denial of service).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (quinn-proto is a direct Cargo dependency)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

### Proposed Jira Links

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

Note: "Related" link type is used (not "Depend") because this is a preemptive task linked to a different stream's CVE Jira.

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

**PROPOSED Jira Task creation** (not executed):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-backport-task-key> (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

### Proposed Jira Links

```
# Block relationship: upstream backport must complete first
jira.create_link(
  inwardIssue: <upstream-backport-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

# Related link to originating CVE (preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)
```

---

## Additional Proposed Jira Mutations (all PROPOSALS, not executed)

### 1. Assign and Transition (Step 0.8)

```
PROPOSAL: Assign TC-8001 to current user
PROPOSAL: Transition TC-8001 from New to Assigned
```

### 2. Affects Versions Correction (Step 3)

```
PROPOSAL: Remove Affects Versions "RHTPA 2.0.0"
PROPOSAL: Add Affects Versions "RHTPA 2.2.0", "RHTPA 2.2.1", "RHTPA 2.2.2"
```

Rationale: PSIRT assigned RHTPA 2.0.0, but no 2.0.x stream exists. Lock file evidence shows versions 2.2.0-2.2.2 ship vulnerable quinn-proto (0.11.9 or 0.11.12). Versions 2.2.3+ ship the fixed version (0.11.14).

### 3. Cross-Stream Impact Comment (Case A)

```
PROPOSAL: Add comment to TC-8001:
"Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All versions in 2.1.x (2.1.0, 2.1.1) ship
quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the 'Related' link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label."
```

### 4. Add ai-cve-triaged Label (Post-Triage)

```
PROPOSAL: Add label "ai-cve-triaged" to TC-8001
```

### 5. Post-Triage Summary Comment

```
PROPOSAL: Add summary comment to TC-8001:

"Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14):

Version Impact:
| Stream | Version | quinn-proto | Affected? |
|--------|---------|-------------|-----------|
| 2.1.x  | 2.1.0   | 0.11.9      | YES       |
| 2.1.x  | 2.1.1   | 0.11.9      | YES       |
| 2.2.x  | 2.2.0   | 0.11.9      | YES       |
| 2.2.x  | 2.2.1   | 0.11.12     | YES       |
| 2.2.x  | 2.2.2   | 0.11.12     | YES (retag of 2.2.1) |
| 2.2.x  | 2.2.3   | 0.11.14     | NO        |
| 2.2.x  | 2.2.4   | 0.11.14     | NO        |

Affects Versions corrected: removed RHTPA 2.0.0, added RHTPA 2.2.0,
RHTPA 2.2.1, RHTPA 2.2.2.

Triage outcome:
- 2.2.x (scoped stream): Fix already shipped in versions 2.2.3+.
  No new remediation tasks needed.
- 2.1.x (cross-stream): Preemptive remediation tasks created:
  <upstream-task-key> (upstream backport) and <downstream-task-key>
  (downstream propagation). Both carry the security-preemptive label."
```

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo ecosystem -> 2 tasks per stream (upstream backport + downstream propagation). 2.1.x: 2 preemptive tasks. 2.2.x: 0 tasks (fix already present).
- [x] **Cross-stream coverage**: 2.1.x has no sibling CVE Jira -> preemptive tasks created.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (different stream's CVE Jira). "Blocks" for upstream -> downstream within a stream.
- [x] **Preemptive labels**: 2.1.x tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Source Repositories table has NO Deployment Context column. Coordination Guidance subsection is omitted entirely from all task descriptions.
- [x] **Dedup consistency**: No dedup applicable (no prior remediation tasks exist).
