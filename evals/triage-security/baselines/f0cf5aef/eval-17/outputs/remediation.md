# Step 8 -- Remediation

## Triage Outcome

### In-Scope Stream: 2.2.x

The 2.2.x stream is **already fixed** in versions 2.2.3 and 2.2.4, which ship quinn-proto 0.11.14. No remediation tasks are needed for this stream. The vulnerability affected versions 2.2.0, 2.2.1, and 2.2.2, but the fix was organically incorporated in build 0.4.11 (version 2.2.3).

**Action**: Correct Affects Versions (Step 3) to reflect RHTPA 2.2.0, 2.2.1, and 2.2.2. No remediation tasks are created for 2.2.x since the latest release already includes the fix.

### Cross-Stream Impact: 2.1.x (Case A)

The issue is scoped to 2.2.x, but version impact analysis reveals that the **2.1.x stream** is also affected. All versions in 2.1.x (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable.

#### Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All versions in 2.1.x ship quinn-proto 0.11.9.
This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

#### Preemptive Remediation Tasks for 2.1.x

Since the 2.1.x stream has no existing CVE Jira for CVE-2026-31812 (assumed -- no sibling found), preemptive remediation tasks are created per Case A. As quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** are created:

---

### Task 1: Upstream Backport -- quinn-proto fix to release/0.3.z

**Summary**: CVE-2026-31812: Bump quinn-proto to >= 0.11.14 on release/0.3.z [rhtpa-2.1]

**Issue Type**: Task
**Labels**: `security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001 (not "Depend" -- this is a preemptive task)

**Description**:

```
## Context

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The quinn-proto
crate does not properly validate the number of streams requested in a STREAMS
frame, allowing a remote attacker to cause a denial of service (DoS) via panic.

- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
- Fixed version: quinn-proto 0.11.14

## Preemptive Remediation

This is a preemptive remediation task created from CVE triage of TC-8001
(scoped to stream 2.2.x). Cross-stream analysis identified that all versions
in the 2.1.x stream ship quinn-proto 0.11.9 (vulnerable). This task carries
the security-preemptive label and uses a "Related" link to TC-8001.

## Task

Backport or bump quinn-proto to version >= 0.11.14 on the upstream source
repository branch `release/0.3.z`.

### Steps

1. Check the current quinn-proto version on `release/0.3.z` in the
   rhtpa-backend repository (Cargo.lock)
2. Update quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
3. Run tests to verify compatibility
4. Create PR against `release/0.3.z`

### Acceptance Criteria

- quinn-proto version in Cargo.lock on release/0.3.z is >= 0.11.14
- All existing tests pass
- PR merged to release/0.3.z

## Implementation Notes

- Repository: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)
- Branch: release/0.3.z
- Deployment context: upstream
- Ecosystem: Cargo
- Lock file: Cargo.lock
```

---

### Task 2: Downstream Propagation -- quinn-proto fix to rhtpa-release.0.3.z

**Summary**: CVE-2026-31812: Propagate quinn-proto fix to rhtpa-release.0.3.z [rhtpa-2.1]

**Issue Type**: Task
**Labels**: `security`, `CVE-2026-31812`, `security-preemptive`
**Link**: Related to TC-8001; Blocked by Task 1 (upstream backport)

**Description**:

```
## Context

CVE-2026-31812 affects quinn-proto versions before 0.11.14. This is the
downstream propagation task for the 2.1.x stream -- it updates the Konflux
release repo to reference the fixed upstream build.

- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
- Fixed version: quinn-proto 0.11.14
- Upstream backport task: [Task 1 key]

## Preemptive Remediation

This is a preemptive remediation task created from CVE triage of TC-8001
(scoped to stream 2.2.x). Cross-stream analysis identified that all versions
in the 2.1.x stream ship quinn-proto 0.11.9 (vulnerable). This task carries
the security-preemptive label and uses a "Related" link to TC-8001.

## Task

After the upstream backport (Task 1) is merged, update the Konflux release
repo rhtpa-release.0.3.z to reference the new backend build that includes
the quinn-proto fix.

### Steps

1. Wait for the upstream backport task to complete (Task 1)
2. Identify the new backend build tag from release/0.3.z that includes
   quinn-proto >= 0.11.14
3. Update `artifacts.lock.yaml` in rhtpa-release.0.3.z to reference
   the new backend tag
4. Verify the updated lock file references a build containing the fix
5. Create PR against rhtpa-release.0.3.z

### Acceptance Criteria

- artifacts.lock.yaml in rhtpa-release.0.3.z references a backend build
  that ships quinn-proto >= 0.11.14
- The resulting product version (next 2.1.x release) is no longer vulnerable
  to CVE-2026-31812

## Implementation Notes

- Repository: rhtpa-release.0.3.z (git.example.com/rhtpa/rhtpa-release.0.3.z)
- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Deployment context: upstream
- This task is blocked by the upstream backport task
```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (source dependency / Cargo -- upstream backport + downstream propagation). 0 tasks for 2.2.x (already fixed).
- [x] **Cross-stream coverage**: 2.1.x (outside scope) gets preemptive tasks since no sibling CVE Jira exists.
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (cross-stream). "Blocks" for upstream task blocking downstream task within the 2.1.x stream.
- [x] **Preemptive labels**: Both tasks carry the `security-preemptive` label.
- [x] **Coordination guidance**: Implementation Notes include deployment context (`upstream`) for both tasks.

## Post-Triage Summary

After remediation task creation, the following actions would be taken on TC-8001:

1. **Add label**: `ai-cve-triaged`
2. **Post summary comment** documenting:
   - Version impact table (2.2.x: 3 versions affected, fixed in 2.2.3+; 2.1.x: all versions affected)
   - Affects Versions correction: removed RHTPA 2.0.0, added RHTPA 2.2.0/2.2.1/2.2.2
   - Triage outcome: 2.2.x already fixed; preemptive remediation tasks created for 2.1.x
   - Links to preemptive tasks created
   - @mention of the issue reporter
