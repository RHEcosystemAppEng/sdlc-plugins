# Step 8 -- Remediation: CVE-2026-31812

## Triage Decision Summary

### Stream 2.2.x (Issue Scope)

The issue is scoped to stream 2.2.x. Version impact analysis shows:

- Affected: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4 (already ship quinn-proto 0.11.14)

The latest releases in the 2.2.x stream (2.2.3+) already ship the fixed version of quinn-proto (0.11.14). The upstream branch `release/0.4.z` has the fix at HEAD. **No new remediation task is needed for the 2.2.x stream** -- the vulnerability has already been resolved in the latest releases.

Affects Versions should be corrected to list 2.2.0, 2.2.1, and 2.2.2 as affected (removing the incorrect RHTPA 2.0.0).

### Stream 2.1.x (Cross-Stream Impact -- Case A)

All versions in the 2.1.x stream are affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). The upstream branch `release/0.3.z` does NOT have the fix at HEAD. Since no stream-specific CVE Jira exists for the 2.1.x stream, **preemptive remediation tasks** should be created.

Ecosystem: Cargo (source dependency, fix NOT available upstream for this stream)
Task count: 2 per stream (upstream backport + downstream propagation)

---

## PROPOSED Remediation Tasks

All tasks below are PROPOSALS -- they would require engineer confirmation before Jira creation.

### Task 1: Upstream Backport (Stream 2.1.x -- Preemptive)

**PROPOSAL: Create Jira Task**

```
Summary: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
Link: Related to TC-8001 (originating CVE from stream 2.2.x)
```

#### Task Description

```markdown
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
by sending a QUIC transport frame that creates an excessive number of streams.
This is classified as a denial of service (DoS) vulnerability. CVSS: 7.5 (High).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- The upstream branch release/0.3.z currently ships quinn-proto 0.11.9
- The fix (quinn-proto 0.11.14) must be backported to this branch

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update the lock file
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog at quinn-rs/quinn#2048)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE, stream 2.2.x)
```

---

### Task 2: Downstream Propagation (Stream 2.1.x -- Preemptive)

**PROPOSAL: Create Jira Task**

```
Summary: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
Issue Type: Task
Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
Link: Related to TC-8001 (originating CVE from stream 2.2.x)
Blocked by: Task 1 (upstream backport must merge first)
```

#### Task Description

```markdown
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

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully
- After updating, confirm that the rebuilt container image includes
  quinn-proto >= 0.11.14 in its dependency tree

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (must merge first)
- Related to: TC-8001 (originating CVE, stream 2.2.x)
```

---

## PROPOSED Jira Mutations Summary

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Affects Versions Correction (TC-8001)

- **Remove**: RHTPA 2.0.0 (does not correspond to any configured stream)
- **Add**: Versions corresponding to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (discovered dynamically via Jira version metadata)
- **Rationale**: Lock file evidence confirms these versions ship quinn-proto < 0.11.14

### 2. Cross-Stream Impact Comment (TC-8001)

Post comment to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. This stream may require separate PSIRT triage.

### 3. Preemptive Remediation Task Creation (Stream 2.1.x)

- Create Task 1: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z
- Create Task 2: Downstream propagation -- update backend ref in rhtpa-release.0.3.z
- Both tasks carry the `security-preemptive` label
- Both tasks linked to TC-8001 with "Related" link type (not "Depend", since TC-8001 belongs to a different stream)
- Task 2 blocked by Task 1 ("Blocks" link)

### 4. Preemptive Task Comment (TC-8001)

Post comment to TC-8001:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
> - 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive, blocked by upstream)
>
> These tasks use the "Related" link type and carry the security-preemptive label.
> When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
> them and remove the label.

### 5. Post-Triage Label (TC-8001)

Add label `ai-cve-triaged` to TC-8001.

### 6. Post-Triage Summary Comment (TC-8001)

Post summary comment to TC-8001 documenting:
1. Version impact table (all streams)
2. Affects Versions correction (RHTPA 2.0.0 removed, correct versions added)
3. Triage outcome: 2.2.x stream already fixed in 2.2.3+; preemptive remediation created for 2.1.x
4. Links to preemptive remediation tasks
5. @mention of the issue reporter (account ID from Jira issue data)

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2.1.x gets 2 tasks (upstream backport + downstream propagation) -- matches Cargo ecosystem classification for source dependency with fix NOT available upstream
- [x] **Cross-stream coverage**: 2.1.x (the only other affected stream outside issue scope) has preemptive tasks created
- [x] **Link types**: "Related" for preemptive tasks linked to TC-8001 (different stream's CVE); "Blocks" for upstream -> downstream within 2.1.x
- [x] **Preemptive labels**: Both tasks for 2.1.x carry the `security-preemptive` label
- [x] **Coordination guidance**: Each task includes upstream coordination guidance (deployment context = upstream)
- [x] **2.2.x stream**: No remediation tasks needed -- latest versions (2.2.3, 2.2.4) already ship quinn-proto 0.11.14
