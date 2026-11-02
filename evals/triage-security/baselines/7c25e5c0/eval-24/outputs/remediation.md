# Step 8 — Remediation (Case B: Affected versions exist)

## Version Impact Summary

The 2.2.x stream version impact analysis shows:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 |

Versions 2.2.0 through 2.2.2 are affected. Proceeding with Case B remediation.

## Ecosystem Classification

Ecosystem: **Cargo** (source dependency) → 2 tasks per stream: upstream backport + downstream propagation.

## Remediation Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto - Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.8 retag (2.2.2)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml/Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

**Note on Coordination Guidance**: The Source Repositories table does **not** include a Deployment Context column. Per backward compatibility rules, the Coordination Guidance subsection is omitted entirely from this task's Implementation Notes. No Coordination Guidance is generated.

### Post-creation Steps (proposed, not executed)

1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Create Depend link: TC-8001 → upstream-task-key

---

## Remediation Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

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

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream-task-key (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

**Note on Coordination Guidance**: The Source Repositories table does **not** include a Deployment Context column. Per backward compatibility rules, the Coordination Guidance subsection is omitted entirely from this task's Implementation Notes. No Coordination Guidance is generated.

### Post-creation Steps (proposed, not executed)

1. Re-fetch description from Jira after create_issue
2. Compute SHA-256 digest using `scripts/sha256-digest.py`
3. Post digest comment: `[sdlc-workflow] Description digest: sha256-md:<hex>`
4. Create Depend link: TC-8001 → downstream-task-key
5. Create Blocks link: upstream-task-key → downstream-task-key

---

## Backward Compatibility Verification

The Source Repositories table in the project CLAUDE.md has the following structure:

```
| Repository | URL | Local Path |
```

There is **no Deployment Context column**. Per the skill's backward compatibility rules:
- All repositories default to deployment context `upstream`
- The `### Coordination Guidance` subsection is **omitted entirely** from both remediation task descriptions
- The triage proceeds normally through all steps without errors
- Existing eval behavior is unaffected by the absence of the Deployment Context column
