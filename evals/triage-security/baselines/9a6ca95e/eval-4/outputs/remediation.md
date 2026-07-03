# Step 8 -- Remediation

## Triage Outcome: Case A (Affected) -- 2.1.x stream only

The version impact analysis shows mixed impact across streams:
- **2.1.x stream**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed)

Remediation tasks are created only for the affected 2.1.x stream. No remediation is needed for the 2.2.x stream.

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are required for the affected stream: an upstream backport task and a downstream propagation subtask.

## Sibling / Duplicate Check (Step 4)

No sibling Vulnerability issues found for CVE-2026-33501 (JQL returned empty). No duplicates, no cross-stream companions.

## Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Description

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

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size defaulting to 16 KiB

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

---

## Jira Linkage

1. Link upstream backport task to TC-8004 with type "Depend"
2. Link downstream propagation task to TC-8004 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"

## Why No 2.2.x Remediation

The 2.2.x stream does not require remediation because all versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. The patched h2 version was adopted in the 2.2.x stream before its first release (2.2.0 at build tag v0.4.5 already ships h2 0.4.8).

## Post-Triage Summary

- **CVE**: CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames)
- **Impact**: 2.1.x stream affected (h2 0.4.5), 2.2.x stream not affected (h2 >= 0.4.8)
- **Affects Versions corrected**: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- **Remediation**: 2 tasks created for 2.1.x stream (upstream backport + downstream propagation)
- **Label**: `ai-cve-triaged` added to TC-8004
