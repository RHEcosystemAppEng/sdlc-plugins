# Step 8 — Remediation

## Triage Decision

**Issue**: TC-8030 — CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2]
**Scoped stream**: 2.2.x
**Enriched fix threshold**: h2 < 0.4.8 (from Step 1.5)

### Decision Path

1. **Any supported versions affected?** YES — 2.1.x stream ships h2 0.4.5 (< 0.4.8)
2. **Issue scoped to a single stream?** YES — scoped to 2.2.x
3. **Other streams also affected?** YES — 2.1.x is affected
4. **Result**: Case B (cross-stream impact) followed by Case A (in-scope remediation)

### In-Scope Stream (2.2.x)

No versions in the 2.2.x stream are affected. All builds ship h2 >= 0.4.8.

**Recommendation**: Close TC-8030 as **Not a Bug**.
- Resolution: Not a Bug
- VEX Justification: **Component not Present** (the vulnerable version of h2 is not present in any 2.2.x build)
- Close comment: "No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis shows all 2.2.x builds include h2 >= 0.4.8, which is at or above the fix threshold. The vulnerable range (h2 < 0.4.8) is not present in any 2.2.x release."

### Cross-Stream Impact (2.1.x) — Case B

The 2.1.x stream is affected (h2 0.4.5 < 0.4.8 in all versions) but is outside the scope of TC-8030.

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
> Stream 2.1.x ships h2 0.4.5 in all versions (2.1.0, 2.1.1).
> This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

**Preemptive remediation tasks** for 2.1.x (no CVE Jira exists for this stream):

---

## Preemptive Remediation Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (build v0.3.8, h2 0.4.5), 2.1.1 (build v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- h2 is a direct dependency of the backend workspace

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog and fix PR hyperium/h2#800)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira — cross-stream)

### Link Type

```
jira.create_link(
  inwardIssue: "TC-8030",
  outwardIssue: <upstream-task-key>,
  type: "Related"
)
```

---

## Preemptive Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: <upstream-task-key> (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira — cross-stream)

### Link Types

```
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)

jira.create_link(
  inwardIssue: "TC-8030",
  outwardIssue: <downstream-task-key>,
  type: "Related"
)
```

---

## Preemptive Tasks Comment (to be posted on TC-8030)

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <upstream-task-key> (upstream backport, security-preemptive), <downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

---

## Post-Triage Summary

### Label Addition

Add `ai-cve-triaged` label to TC-8030.

### Summary Comment (to be posted on TC-8030)

Version impact analysis for CVE-2026-48901 (h2 < 0.4.8):

**Stream 2.2.x (scoped)**:
| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.2.0 | 0.4.8 | NO | >= fix threshold |
| 2.2.1 | 0.4.8 | NO | >= fix threshold |
| 2.2.2 | — | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | >= fix threshold |
| 2.2.4 | 0.4.9 | NO | >= fix threshold |

**Stream 2.1.x (cross-stream)**:
| Version | h2 | Affected? | Notes |
|---------|-----|-----------|-------|
| 2.1.0 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 0.4.5 | YES | < 0.4.8 |

**Affects Versions correction**: No correction needed (scoped to 2.2.x, which is not affected).

**Triage outcome**: Closed as Not a Bug — no 2.2.x versions ship a vulnerable version of h2. All 2.2.x builds include h2 >= 0.4.8.

**Cross-stream impact**: 2.1.x is affected (h2 0.4.5). Preemptive remediation tasks created:
- <upstream-task-key> — bump h2 to >= 0.4.8 on release/0.3.z (security-preemptive)
- <downstream-task-key> — propagate fix to rhtpa-release.0.3.z (security-preemptive)

VEX Justification: Component not Present (vulnerable h2 version not present in 2.2.x builds).
