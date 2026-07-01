# Step 8 -- Remediation

## Triage Decision

Based on the version impact analysis:

- **Stream 2.1.x**: AFFECTED -- versions 2.1.0 and 2.1.1 both ship h2 0.4.5 (< 0.4.8)
- **Stream 2.2.x**: NOT AFFECTED -- all versions ship h2 >= 0.4.8

This is an **unscoped** issue (no stream suffix). The issue covers all streams by definition. Therefore:

- **Case A applies for stream 2.1.x** -- affected versions exist, remediation tasks needed
- **Case B does NOT apply** -- the issue is unscoped, so cross-stream impact notice is not generated. Cross-stream notices apply only to scoped issues where other streams outside the issue's scope are also affected. Since this issue covers all streams, there is no "outside scope."
- **Case C does NOT apply globally** -- at least some supported versions are affected

Remediation tasks are created **only for stream 2.1.x** (the affected stream). Stream 2.2.x already ships the patched version and requires no remediation.

## Remediation Tasks (Stream 2.1.x -- Cargo ecosystem)

Since h2 is a Cargo (source dependency) ecosystem package, two tasks are created per Important Rule 8: an upstream backport task and a downstream propagation subtask.

---

### Task 1: Upstream Backport Task

**Proposed Jira API call**:
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
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

**Post-creation steps (proposed)**:

1. Re-fetch the upstream task description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post description digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   Note: The digest is computed from the re-fetched description (via Jira API after create_issue), not from the description string passed to create_issue, because Jira normalizes content during storage.

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira API call**:
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

**Post-creation steps (proposed)**:

1. Re-fetch the downstream task description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post description digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```

---

## Jira Linkage (Proposed)

After creating both tasks and posting their digest comments:

1. **Link upstream task to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream subtask as blocked by upstream task**:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

3. **Link downstream task to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

4. **Propose transition** of TC-8004 to In Progress.

5. **Propose assignment** of TC-8004 to current user.

6. **Propose comment** on TC-8004:
   ```
   Remediation tasks created:
   - <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z)
   - <downstream-task-key> (downstream propagation: update rhtpa-backend ref in
     rhtpa-release.0.3.z, blocked by <upstream-task-key>)

   Remediation scoped to stream 2.1.x only. Stream 2.2.x ships h2 >= 0.4.8 and
   is not affected.
   ```

All proposed Jira mutations above require explicit engineer confirmation before execution.

---

## Post-Triage Summary

### 1. Add the `ai-cve-triaged` label

**Proposed action**: Add `ai-cve-triaged` label to TC-8004 to mark it as triaged.

### 2. Post summary comment

**Proposed comment on TC-8004** (pending engineer confirmation):

```
## CVE-2026-33501 Triage Summary

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | pinned at v0.3.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | pinned at v0.3.12 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fix version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships post-fix version |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships post-fix version |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

RHTPA 2.2.0 removed (ships h2 0.4.8 -- not affected).
RHTPA 2.1.1 added (ships h2 0.4.5 -- affected).

### Triage Outcome

Remediation tasks created for stream 2.1.x:
- <upstream-task-key>: Upstream backport -- bump h2 to 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update rhtpa-backend ref in
  rhtpa-release.0.3.z (blocked by <upstream-task-key>)

Stream 2.2.x requires no remediation (ships h2 >= 0.4.8).

@<reporter-name> (reporter @mention via ADF mention node with reporter account ID
from TC-8004 issue data)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.1.
```

Note: The reporter @mention is implemented as an ADF mention node:
```json
{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }
```
where the account ID and display name come from TC-8004's reporter field.

---

## Key Decision Points

1. **Unscoped issue**: No stream suffix means ALL streams were analyzed. This is correct per the skill protocol.
2. **Mixed impact**: 2.1.x affected, 2.2.x not affected. Remediation only for 2.1.x.
3. **No cross-stream notice**: Case B does not apply because the issue is unscoped -- it already covers all streams by definition. Cross-stream impact notices are only generated for scoped issues.
4. **Two tasks for Cargo ecosystem**: Upstream backport + downstream propagation with Blocks dependency (Important Rule 8).
5. **No Coordination Guidance**: The Source Repositories table has no Deployment Context column, so the subsection is omitted entirely per backward compatibility.
6. **All actions are proposals**: Every Jira mutation (Affects Versions correction, task creation, label addition, status transition, comments) is presented as a proposed action requiring engineer confirmation before execution (Guardrails).
