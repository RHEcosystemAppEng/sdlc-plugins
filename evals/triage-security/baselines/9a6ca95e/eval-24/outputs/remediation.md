# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

All version data extracted from pinned commit tags in the supportability matrix, not from branch HEAD.

## Cross-Stream Impact

Stream 2.1.x (outside this issue's scope) is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers **Case B** (cross-stream impact) in addition to Case A.

---

# Step 3 -- Affects Versions Correction (Scoped to 2.2.x)

**Proposed correction** (requires engineer confirmation):

The PSIRT-assigned Affects Versions is incorrect. The issue currently lists `RHTPA 2.0.0`, which does not correspond to any version in the supportability matrix.

Based on lock file evidence, the affected versions within the 2.2.x stream scope are:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version). Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` -- not hardcoded.

---

# Step 8 -- Remediation

## Triage Decision: Case A + Case B

**Case A**: Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected. Create remediation tasks for this stream.

**Case B**: Stream 2.1.x is also affected (versions 2.1.0, 2.1.1) but is outside this issue's scope. A cross-stream impact comment would be posted, and companion sibling issues checked. Preemptive remediation tasks would be created for 2.1.x if no CVE Jira exists for that stream.

## Remediation Tasks for 2.2.x Stream (Case A)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task

**Proposed Jira creation** (requires engineer confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
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

**Post-creation steps (proposed):**
1. Re-fetch the created task's description from Jira
2. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post description digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. The digest comment is posted BEFORE creating any issue links or other comments

### Task 2: Downstream Propagation Subtask

**Proposed Jira creation** (requires engineer confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

**Post-creation steps (proposed):**
1. Re-fetch the created task's description from Jira
2. Compute SHA-256 digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post description digest comment: `[sdlc-workflow] Description digest: <tagged-digest>`
4. The digest comment is posted BEFORE creating any issue links or other comments

## Jira Linkage (Proposed)

After creating both tasks (and posting their description digest comments first):

1. Link upstream backport task to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```
2. Link downstream propagation subtask to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
3. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

## Coordination Guidance

The Deployment Context column is **absent** from the Source Repositories table in CLAUDE.md. Per backward compatibility rules, all repositories default to `upstream` deployment context. However, since the column does not exist at all, the Coordination Guidance subsection is **omitted entirely** from the remediation task descriptions above. This maintains backward compatibility -- existing workflows that predate the Deployment Context feature are unaffected.

## Post-Triage Summary (Proposed)

After all triage actions complete:

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Triage outcome: remediation tasks created
   - Links to upstream and downstream tasks
   - @mention of the vulnerability issue's reporter (account ID from Jira issue data)
   - Cross-stream impact notice for 2.1.x
   - Comment Footnote

All proposed actions above are presented for engineer confirmation before execution. No Jira mutations are performed without explicit approval.
