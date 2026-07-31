# Remediation — TC-8004

## Step 8: Remediation Decision

### Case A: Cross-stream impact check

**Skipped.** Per Step 8 Case A guard: "Case A applies exclusively to stream-scoped issues (those whose summary contains a stream suffix like `[myproduct-2.2]`). Unscoped issues cover all streams by definition — there are no 'other streams outside this issue's scope,' so the cross-stream impact check is not applicable. For unscoped issues, skip Case A entirely and proceed directly to Case B task creation for all affected streams."

TC-8004 is unscoped (no stream suffix in summary). Cross-stream impact notice is NOT generated.

### Case B: Create remediation tasks for affected streams

The issue is unscoped, so Case B creates remediation tasks for all affected streams.

**Affected streams (from version impact table):**
- 2.1.x: **YES** — all versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable)
- 2.2.x: **NO** — all versions ship h2 >= 0.4.8 (patched)

Remediation tasks are created **only for the 2.1.x stream**, because 2.2.x already ships the patched version and is not affected.

**Ecosystem**: Cargo (source dependency) -> 2 tasks per affected stream

### Task 1: Upstream Backport (2.1.x stream)

```
Summary: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- h2 is a direct dependency of the backend workspace

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

Labels: `["ai-generated-jira", "Security", "CVE-2026-33501"]`

### Task 2: Downstream Propagation (2.1.x stream)

```
Summary: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: [upstream-task-key] (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

Labels: `["ai-generated-jira", "Security", "CVE-2026-33501"]`

### Linkage

1. Link upstream task -> TC-8004 with type "Depend"
2. Link downstream task -> TC-8004 with type "Depend"
3. Link upstream task -> downstream task with type "Blocks" (downstream blocked by upstream)

### Why no tasks for 2.2.x

The 2.2.x stream is NOT affected — all 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. No remediation is needed for the 2.2.x stream.

### Pre-creation checklist

- [x] **Task count per stream**: 2 tasks for 2.1.x (source dependency: upstream backport + downstream propagation). 0 tasks for 2.2.x (not affected).
- [x] **Cross-stream coverage**: N/A — issue is unscoped, Case A is skipped. All streams checked; only 2.1.x requires remediation.
- [x] **Link types**: "Depend" for tasks linked to TC-8004, "Blocks" for upstream -> downstream within 2.1.x stream.
- [x] **Preemptive labels**: N/A — no preemptive tasks created (issue is unscoped).
- [x] **Coordination guidance**: omitted — Deployment Context column absent from Source Repositories table (backward compatibility).
