# Step 2 -- Version Impact Summary

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

The issue is scoped to the **2.2.x** stream. Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the scoped stream. Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected and will be addressed via cross-stream impact handling (Case A).

---

# Step 8 -- Remediation

## Triage Decision: Case B -- Affected versions exist, create remediation tasks

Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable version of quinn-proto (< 0.11.14). Remediation tasks are required.

### Case A: Cross-stream impact

The version impact analysis reveals that the 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). A cross-stream impact comment would be proposed:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

---

## Remediation Tasks for Stream 2.2.x (Scoped)

**Ecosystem**: Cargo (source dependency) -- creates **two** tasks per stream: upstream backport + downstream propagation.

### Task 1: Upstream Backport Task

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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
```

**Post-creation steps (proposed):**

1. After `jira.create_issue(...)` returns the upstream task key, re-fetch the task description from Jira:
   ```
   jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute a SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post a description digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. Create Depend link to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira Issue:**
- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation steps (proposed):**

1. After `jira.create_issue(...)` returns the downstream task key, re-fetch the task description from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the re-fetched description to a temp file and compute a SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post a description digest comment (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
4. Create Depend link to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
5. Create Blocks link from upstream to downstream:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

---

## Deployment Context and Coordination Guidance

The Source Repositories table in the project CLAUDE.md does **not** include a Deployment Context column. Per backward compatibility rules (remediation-templates.md), all repositories default to `upstream` and the Coordination Guidance subsection is **omitted entirely** from remediation task descriptions. No `### Coordination Guidance` subsection is appended to any task's Implementation Notes.

This ensures backward compatibility -- existing behavior is unaffected by the absence of the Deployment Context column.

---

## Post-Triage Summary (Proposed)

After all triage actions are complete:

1. **Add the `ai-cve-triaged` label** to TC-8001 to mark it as triaged.

2. **Post a summary comment** to TC-8001 documenting:
   - The version impact table
   - The Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - The triage outcome (remediation tasks created)
   - Links to upstream backport task and downstream propagation subtask
   - An @mention of the vulnerability reporter using an ADF mention node

3. **Transition** TC-8001 to In Progress (if not already).

All proposed actions require explicit engineer confirmation before execution.
