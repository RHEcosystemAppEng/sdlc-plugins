# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

**Case B (Affected)** for scoped stream 2.2.x, plus **Case A (Cross-stream impact)** for stream 2.1.x.

- Ecosystem: Cargo (source dependency) — 2 tasks per stream (upstream backport + downstream propagation)
- Scoped stream (2.2.x): versions 2.2.0, 2.2.1, 2.2.2 are affected
- Cross-stream (2.1.x): versions 2.1.0, 2.1.1 are affected — preemptive tasks created
- Coordination guidance: omitted (Deployment Context column absent from Source Repositories table)

---

## Task 1: Upstream Backport (Stream 2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812

**Link:** Depend (inward: TC-8001, outward: this task)

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or trace via `Cargo.lock` analysis)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If quinn-proto is a transitive dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation (Stream 2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812

**Link:** Depend (inward: TC-8001, outward: this task); Blocks (inward: Task 1, outward: this task)

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback approach), verify the pinning is reflected in the downstream build's lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 — upstream backport (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Task 3: Preemptive Upstream Backport (Stream 2.1.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link:** Related (inward: TC-8001, outward: this task) — preemptive, no stream-specific CVE Jira exists for 2.1.x

### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or trace via `Cargo.lock` analysis)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

If quinn-proto is a transitive dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding the transitive resolution

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira — different stream)

---

## Task 4: Preemptive Downstream Propagation (Stream 2.1.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link:** Related (inward: TC-8001, outward: this task) — preemptive; Blocks (inward: Task 3, outward: this task)

### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812 fix from the upstream backport task for stream 2.1.x.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 3 — preemptive upstream backport (must merge first)
- Related to: TC-8001 (originating CVE Jira — different stream)

---

## Post-Triage Summary

### Actions Taken

1. **Data Extraction (Step 1):** Parsed CVE-2026-31812 data from TC-8001. Identified quinn-proto < 0.11.14 as the vulnerable dependency, scoped to stream 2.2.x.

2. **Version Impact Analysis (Step 2):** Analyzed all versions across both streams using mock lock file data. Found 5 affected versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2) and 2 not-affected versions (2.2.3, 2.2.4) that already ship the fix.

3. **Affects Versions Correction (Step 3):** PSIRT assigned "RHTPA 2.0.0" which does not correspond to any configured stream. Corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x stream).

4. **Cross-Stream Impact (Case A):** Stream 2.1.x is also affected (quinn-proto 0.11.9 in 2.1.0 and 2.1.1). No existing CVE Jira for 2.1.x. Created preemptive remediation tasks (Tasks 3 and 4) with `security-preemptive` label and "Related" link to TC-8001.

5. **Remediation Tasks Created (Case B):**
   - **Stream 2.2.x (scoped):** Task 1 (upstream backport on release/0.4.z) + Task 2 (downstream propagation in rhtpa-release.0.4.z). Link type: Depend to TC-8001.
   - **Stream 2.1.x (preemptive):** Task 3 (upstream backport on release/0.3.z) + Task 4 (downstream propagation in rhtpa-release.0.3.z). Link type: Related to TC-8001. Labels include `security-preemptive`.

6. **Label:** `ai-cve-triaged` added to TC-8001.

### Task Summary

| Task | Type | Stream | Summary | Labels | Link to TC-8001 |
|------|------|--------|---------|--------|-----------------|
| Task 1 | Upstream backport | 2.2.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| Task 2 | Downstream propagation | 2.2.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| Task 3 | Preemptive upstream backport | 2.1.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| Task 4 | Preemptive downstream propagation | 2.1.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
