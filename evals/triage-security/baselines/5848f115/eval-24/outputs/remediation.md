# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Decision

### Stream 2.2.x (scoped stream) -- No new tasks needed

The fix is already present in the latest releases of this stream:
- 2.2.3 (v0.4.11) ships quinn-proto 0.11.14 (fixed version)
- 2.2.4 (v0.4.12) ships quinn-proto 0.11.14 (fixed version)

No remediation tasks are required for the 2.2.x stream. Affects Versions are corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 to track which versions shipped the vulnerability.

### Stream 2.1.x (cross-stream, Case A) -- Preemptive remediation tasks

Stream 2.1.x is affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9) and no fix exists in this stream. The upstream branch release/0.3.z has not received the fix. Since no stream-specific CVE Jira exists for 2.1.x, preemptive remediation tasks are created per Case A.

Ecosystem: Cargo (source dependency) -- 2 tasks per stream.

---

## Preemptive Task 1: Upstream Backport (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Link type:** Related (to originating CVE TC-8001, because this is a preemptive task for a different stream)

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive (verify via `Cargo.lock` inspection at v0.3.12)
- The upstream fix PR (quinn-rs/quinn#2048) provides the patch for quinn-proto.
  The fix is already present on release/0.4.z (2.2.x stream) -- use that as
  a reference for the backport to release/0.3.z.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain in Cargo.lock)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira for stream 2.2.x)

---

## Preemptive Task 2: Downstream Propagation (2.1.x)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Link type:** Related (to originating CVE TC-8001, because this is a preemptive task for a different stream)
**Blocked by:** Preemptive Task 1 (upstream backport must merge first)

### Task Description

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
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira for stream 2.2.x)

---

## Jira Linkage Summary

After creating both preemptive tasks:

1. **Link** each preemptive task to TC-8001 with "Related" (not "Depend",
   because these are preemptive tasks for a different stream):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Related")
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Related")
   ```

2. **Link** the downstream task as blocked by the upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. **Post comment** on TC-8001:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
   - 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive, blocked by <upstream-task-key>)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

## Post-Triage Summary

**Version Impact:**

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= fix version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= fix version |

**Affects Versions Correction:** RHTPA 2.0.0 --> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Triage Outcome:**
- 2.2.x (scoped): Already fixed in 2.2.3+ -- no new remediation tasks
- 2.1.x (cross-stream): 2 preemptive remediation tasks created (upstream backport + downstream propagation)

**Label:** `ai-cve-triaged` added to TC-8001
