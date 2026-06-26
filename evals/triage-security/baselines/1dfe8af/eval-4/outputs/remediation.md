# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (2.1.x stream only)

The version impact analysis shows that only the **2.1.x stream** is affected. The 2.2.x stream ships h2 >= 0.4.8 (the fixed version) and requires no remediation.

Since TC-8004 is **unscoped**, remediation tasks are created only for the actually affected stream (2.1.x). No cross-stream impact notice is generated because the issue is unscoped and already covers all streams in its scope -- there are no "other streams outside this issue's scope" to notify about.

## Remediation Tasks for 2.1.x Stream

The ecosystem is **Cargo** (source dependency), so two tasks are required: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage

1. Link upstream backport task to TC-8004 with "Depend"
2. Link downstream propagation task as blocked by upstream backport task with "Blocks"
3. Transition TC-8004 to In Progress
4. Assign TC-8004 to current user
5. Add ai-cve-triaged label to TC-8004

## Why No 2.2.x Remediation

The 2.2.x stream ships h2 >= 0.4.8 in all versions:
- 2.2.0 (v0.4.5): h2 0.4.8 -- fixed
- 2.2.1 (v0.4.8): h2 0.4.8 -- fixed
- 2.2.2 (v0.4.9): retag of 2.2.1 -- fixed
- 2.2.3 (v0.4.11): h2 0.4.9 -- fixed
- 2.2.4 (v0.4.12): h2 0.4.9 -- fixed

No remediation is needed for the 2.2.x stream. The PSIRT-assigned RHTPA 2.2.0 in Affects Versions was removed in Step 3 since it is not actually affected.

## Why No Cross-Stream Impact Notice

TC-8004 is **unscoped** -- it has no stream suffix in the summary. Cross-stream impact notices (Case B) are only generated for **scoped** issues when streams outside the issue's scope are also affected. Since an unscoped issue already covers all streams, there are no "other streams outside scope" to notify about. The remediation is simply scoped to the actually affected stream (2.1.x).

## Sibling Issues

JQL search for sibling Vulnerability issues with the same CVE label returned empty results. No duplicates or companions exist. Step 4 proceeds without action.
