# Remediation Tasks for CVE-2026-31812

## Triage Decision

### Stream 2.2.x (scoped stream -- Case A with fix already present)

The fix for CVE-2026-31812 (quinn-proto >= 0.11.14) is already shipped in RHTPA 2.2.3
(build 0.4.11) and RHTPA 2.2.4 (build 0.4.12). The upstream branch release/0.4.z
already contains quinn-proto 0.11.14. No new remediation tasks are needed for the
2.2.x stream.

Affects Versions set to: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (documenting which
versions shipped the vulnerable dependency).

### Stream 2.1.x (cross-stream impact -- Case B preemptive remediation)

All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is below the fix
threshold of 0.11.14. The upstream branch release/0.3.z has NOT been updated. No
CVE Jira exists for the 2.1.x stream.

Creating preemptive remediation tasks with `security-preemptive` label and "Related"
link type to the originating CVE TC-8001.

---

## Preemptive Upstream Backport Task (2.1.x stream)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
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
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8: quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12: quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Linkage for Upstream Backport Task

**PROPOSAL** (link to originating CVE -- "Related" for preemptive tasks):
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "<upstream-task-key>",
  type: "Related"
)
```

**PROPOSAL** (description digest comment):
```
jira.add_comment("<upstream-task-key>", "[sdlc-workflow] Description digest: <sha256-md:computed-hash>")
```

---

## Preemptive Downstream Propagation Task (2.1.x stream)

**PROPOSAL: Create Jira Task**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
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

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix
from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Linkage for Downstream Propagation Task

**PROPOSAL** (link to originating CVE -- "Related" for preemptive tasks):
```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "<downstream-task-key>",
  type: "Related"
)
```

**PROPOSAL** (block by upstream task):
```
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

**PROPOSAL** (description digest comment):
```
jira.add_comment("<downstream-task-key>", "[sdlc-workflow] Description digest: <sha256-md:computed-hash>")
```

---

## Cross-Stream Impact Comment

**PROPOSAL** (comment on TC-8001):
```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x has no companion CVE Jira.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```

---

## Post-Triage Summary Comment

**PROPOSAL** (summary comment on TC-8001):
```
## CVE-2026-31812 Triage Summary

### Version Impact

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.11.14 | NO | fix version shipped |
| 2.2.x | 2.2.4 | 0.11.14 | NO | fix version shipped |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

- **2.2.x stream**: Fix already present in RHTPA 2.2.3+ (quinn-proto 0.11.14).
  No new remediation tasks needed.
- **2.1.x stream (cross-stream)**: All versions affected. Preemptive remediation
  tasks created:
  - <upstream-task-key>: bump quinn-proto to 0.11.14 on release/0.3.z
  - <downstream-task-key>: update backend ref in rhtpa-release.0.3.z

@<reporter-name> (reporter mention)
```

**PROPOSAL**: Add label `ai-cve-triaged` to TC-8001.

---

## Important: No Coordination Guidance

The Source Repositories table in CLAUDE.md does NOT have a Deployment Context column.
Per the backward compatibility rule in remediation-templates.md: "When the Deployment
Context column is absent from the Source Repositories table (backward compatibility),
omit the coordination guidance entirely -- do not add the subsection."

Accordingly, no `### Coordination Guidance` subsection has been added to any of the
remediation task descriptions above.
