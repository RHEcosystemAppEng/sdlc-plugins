# Step 8 — Remediation

## Triage Decision

The version impact table shows mixed results:
- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

**Case B applies**: Supported versions are affected — create remediation tasks for the affected stream(s) only.

## Cross-Stream Impact Notice

**Not applicable.** This issue is **unscoped** (no stream suffix in the summary), meaning it covers all streams by definition. Cross-stream impact (Case A) applies only to stream-scoped issues. For unscoped issues, remediation tasks are created only for actually affected streams — no cross-stream notice is needed because the issue already spans all streams.

## Remediation Tasks (2.1.x stream only)

Since the ecosystem is **Cargo** (source dependency), two tasks are created per affected stream:

### Task 1: Upstream backport task

**Proposed Jira creation (pending engineer confirmation):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- The fix adds a configurable maximum header list size (defaults to 16 KiB)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Task 2: Downstream propagation subtask

**Proposed Jira creation (pending engineer confirmation):**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Description Digest Protocol

For each created remediation task, the following digest steps would be performed:

1. Re-fetch the task description from Jira after `create_issue`
2. Compute SHA-256 digest using `scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments

## Jira Linkage (proposed)

After creating both tasks:

1. Link upstream task → TC-8004 (Depend)
2. Link downstream task → TC-8004 (Depend)
3. Link upstream task → downstream task (Blocks — downstream is blocked by upstream)
4. Transition TC-8004 to In Progress
5. Add `ai-cve-triaged` label to TC-8004

## Post-Triage Summary

No remediation tasks are created for the 2.2.x stream — all 2.2.x versions ship h2 >= 0.4.8 (the fix threshold). Remediation is scoped to the 2.1.x stream only, consistent with the unscoped nature of the issue which checks all streams but acts only on affected ones.
