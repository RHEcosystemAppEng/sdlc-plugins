# TC-8001 Triage: Step 8 Remediation

> Simulated run. Nothing was created in Jira. Every task, link and comment below is a
> **proposal** that waits for engineer confirmation. Jira keys are placeholders
> (`<TASK-n>`).

## Decision summary

| Input | Value |
|---|---|
| CVE | CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14; CVSS 7.5, DoS) |
| Issue scope | 2.2.x (suffix `[rhtpa-2.2]`) |
| Ecosystem | Cargo, a source dependency, so 2 tasks per affected stream |
| Affected repository | rhtpa-backend |
| **Deployment context** | **customer-shipped** (from the Source Repositories table in Security Configuration) |
| Parent security level | Copy from TC-8001 `security` at creation time. It is not available in the mock data. |

Decision tree:

1. **Step 7 (concurrent triage):** skipped, because the Upstream Affected Component field is not configured.
2. **Step 7.5 (release Jira):** pending, because Jira access is needed. Linking actions appear below.
3. **Supported versions affected?** Yes: 2.1.0, 2.1.1, 2.2.0, 2.2.1 and 2.2.2.
4. **Scoped issue with other streams affected?** Yes, 2.1.x. This triggers **Case A**: a cross-stream comment, plus preemptive tasks for 2.1.x because no 2.1.x sibling CVE Jira was found (simulated; see data-extraction.md Step 4).
5. **Case B for the in-scope 2.2.x stream:** Step 2.5 shows the fix is already on `release/0.4.z` (v0.4.11 and v0.4.12 ship 0.11.14). That selects the **dependency bump + downstream propagation** variant.
   - **Note for the engineer:** 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14. Tasks 1 and 2 therefore only confirm that branch HEAD stays at 0.11.14 or higher and that the next 2.2.z build carries it. The engineer may decline them and instead record that the fix shipped in 2.2.3.
6. **Stream 2.1.x:** there is no evidence of a fix on `release/0.3.z`, so the **upstream backport + downstream propagation** variant applies (preemptive).

## Proposed tasks

| # | Stream | Type | Summary | Labels | Link to TC-8001 |
|---|---|---|---|---|---|
| 1 | 2.2.x | Dependency bump | Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 2 | 2.2.x | Downstream propagation | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| 3 | 2.1.x | Upstream backport (preemptive) | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| 4 | 2.1.x | Downstream propagation (preemptive) | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

Each task is created with `security: <TC-8001 security level>`. A description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) is posted right after creation, before any links.

---

## Task 1: Dependency bump (2.2.x)

**Summary:** Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (2.2.x)

```markdown
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 via dependency update.
The vulnerable dependency (quinn-proto < 0.11.14) is already fixed upstream —
a package manager update is sufficient. quinn-proto before 0.11.14 panics when a
remote peer sends a QUIC STREAMS frame requesting an excessive number of streams
(denial of service, CVSS 7.5).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12),
RHTPA 2.2.2 (retag of 2.2.1). RHTPA 2.2.3 and 2.2.4 already ship 0.11.14.
Source commit(s): v0.4.5, v0.4.8 (affected); v0.4.11, v0.4.12 (fixed)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: not determined during triage (likely transitive via quinn);
  confirm with `cargo tree -i quinn-proto`
- **Remediation action**: run the appropriate package manager update command:
  - **Cargo**: `cargo update -p quinn-proto` to pull in the latest compatible version
- If the update pulls a version that still falls within the affected range,
  pin explicitly: `cargo add quinn-proto@0.11.14`
- Verify Cargo.lock reflects quinn-proto >= 0.11.14 after the update (released
  tags v0.4.11/v0.4.12 already ship 0.11.14 — confirm branch HEAD has not regressed)
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] Lock file updated via package manager (not manual edit)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 2: Downstream propagation (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <TASK-1>.

The dependency bump (<TASK-1>) bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix. Note: the current pin (v0.4.12, RHTPA 2.2.4)
already ships quinn-proto 0.11.14 — verify the pin is not older than v0.4.11.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: not determined (likely transitive) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-1> (dependency bump must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 3: Upstream backport (2.1.x, preemptive)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

```markdown
## Repository

backend (rhtpa-backend)

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

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (likely transitive via quinn);
  confirm with `cargo tree -i quinn-proto`
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When quinn-proto is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When quinn-proto is a **transitive** dependency, use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (e.g., quinn / reqwest)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

---

## Task 4: Downstream propagation (2.1.x, preemptive)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

```markdown
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
CVE-2026-31812 fix from <TASK-3>.

The upstream backport (<TASK-3>) bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: not determined (likely transitive) — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE
assignment, advisory preparation, and formal disclosure. Fix must be released via a
security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <TASK-3> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Coordination guidance section

The affected repository is **rhtpa-backend**. Its Deployment Context in Security
Configuration > Source Repositories is **`customer-shipped`**. Every remediation task
above (1 to 4) therefore has this `### Coordination Guidance` subsection appended to its
Implementation Notes:

> This component is shipped to customers. Coordinate with Product Security for CVE
> assignment, advisory preparation, and formal disclosure. Fix must be released via a
> security advisory with explicit CVE-to-component mapping.

What this means in practice:
- Do not treat the fix as a routine internal merge. Product Security has to be involved for CVE assignment and the advisory.
- The fixed RHTPA build (the next 2.1.z, and the 2.2.z release that carries the fix) must ship with a security advisory that maps CVE-2026-31812 to the `org/rhtpa-server` component.
- The `internal` guidance (merge in-repo only) and the `upstream` guidance (coordinate with upstream maintainers and follow the embargo policy) do **not** apply.

---

## Jira linkage (proposed, in order)

1. Create Task 1 and post its digest. Then link: Depend (inward TC-8001, outward <TASK-1>).
2. Create Task 2 and post its digest. Then link: Depend (TC-8001 to <TASK-2>), and Blocks (inward <TASK-1>, outward <TASK-2>).
3. Create Task 3 and post its digest. Then link: Related (inward TC-8001, outward <TASK-3>).
4. Create Task 4 and post its digest. Then link: Related (TC-8001 to <TASK-4>), and Blocks (<TASK-3> to <TASK-4>).
5. Release Jira (Step 7.5, pending): link non-preemptive Tasks 1 and 2 to the `RHTPA <next 2.2.z> CVE triage` release Task with Blocks. Link TC-8001 to that release Task with Related. Preemptive tasks are not linked to release Jira.
6. Leave TC-8001 status as is if it is already Assigned from Step 0.8, which is an equivalent `indeterminate` status. Otherwise transition it to In Progress.

## Proposed comments on TC-8001

Every comment ends with the triage-security Comment Footnote.

**Affects Versions correction (Step 3):**
> Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix.

**Cross-stream impact (Case A):**
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock
> file analysis. These streams are tracked by companion issues (see Related links)
> or may require separate PSIRT triage.

**Preemptive tasks:**
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <TASK-3>, <TASK-4> (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label. When
> PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and
> remove the label.

**Task list:**
> Remediation tasks created: <TASK-1> (dependency bump), <TASK-2> (downstream
> propagation, blocked by <TASK-1>)

**Post-triage summary:**
- Add the `ai-cve-triaged` label.
- The comment contains: the version impact table, the Affects Versions correction, the outcome (remediation created, Case A + Case B), links to Tasks 1 to 4, release Jira references (pending), dedup results (none, since Step 7.5.3 was not run), and an ADF @mention of the TC-8001 reporter. The reporter's account ID is not available in the mock data.

## Pre-creation checklist

- [x] Task count per stream: 2 for 2.2.x and 2 for 2.1.x (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks (no sibling CVE Jira found, simulated)
- [x] Link types: Depend for own-CVE tasks, Related for preemptive tasks, Blocks from upstream to downstream
- [x] Preemptive labels: `security-preemptive` is on Tasks 3 and 4
- [x] Coordination guidance: the customer-shipped guidance is in every task's Implementation Notes
- [ ] Release Jira linking: pending Step 7.5, which needs Jira
- [x] Dedup consistency: no dedup'd streams

## Caveats

- The security matrices are 152 days old (Last-Updated 2026-06-28). Refresh them before acting.
- MITRE and OSV were not queried, so fix threshold confidence is reduced.
- The dependency chain (direct or transitive) and the dev/production scope are unverified.
- The sibling search, lifecycle check and release Jira steps were not run. No external calls were allowed.
