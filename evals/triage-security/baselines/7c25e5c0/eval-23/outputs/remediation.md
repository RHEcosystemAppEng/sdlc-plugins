# Step 8 — Remediation (Case B: Affected — create remediation tasks)

## Version Impact Summary

The issue is scoped to stream 2.2.x (suffix [rhtpa-2.2]). Version impact analysis shows:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Versions 2.2.0–2.2.2 are affected (quinn-proto < 0.11.14). Remediation tasks are needed.

Cross-stream impact: stream 2.1.x is also affected (2.1.0 ships 0.11.9, 2.1.1 ships 0.11.9), but this is a separate stream outside the current issue's scope. A cross-stream impact comment would be posted per Case A.

## Ecosystem Classification

Ecosystem: **Cargo** (source dependency) → 2 tasks per stream: upstream backport + downstream propagation.

## Remediation Task 1: Upstream Backport

**Proposed Jira Task** (not executed — eval prohibits Jira calls):

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Description Digest Protocol (planned procedure)

After creating the upstream backport task:
1. Re-fetch the task description from Jira via `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments on the task

## Remediation Task 2: Downstream Propagation

**Proposed Jira Task** (not executed — eval prohibits Jira calls):

- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

### Description Digest Protocol (planned procedure)

After creating the downstream propagation task:
1. Re-fetch the task description from Jira via `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post digest comment: `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. The digest comment is posted BEFORE creating issue links (Depend, Blocks) or other comments on the task

## Jira Linkage (planned)

1. Link upstream task → TC-8001 (Depend)
2. Link downstream task → TC-8001 (Depend)
3. Link upstream task → downstream task (Blocks — upstream must merge first)
4. Transition TC-8001 to In Progress
5. Add post-triage summary comment with version impact table, remediation task links, and `ai-cve-triaged` label
