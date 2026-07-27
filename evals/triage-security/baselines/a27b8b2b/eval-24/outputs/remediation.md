# Step 8 -- Remediation

## Triage Outcome: Case B -- Affected, Create Remediation Tasks

The version impact table shows that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected.

**Ecosystem**: Cargo (source dependency)
**Tasks per stream**: 2 (upstream backport + downstream propagation)
**Deployment Context**: upstream (default -- Deployment Context column absent from Source Repositories table)

Since the Deployment Context column is absent from the Source Repositories table, no Coordination Guidance subsection is included in the remediation task descriptions. This maintains backward compatibility with existing configurations that predate the Deployment Context feature.

---

## Task 1: Upstream Backport Task

**Proposed Jira creation** (requires confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
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

Note: The Implementation Notes section does **not** include a Coordination Guidance subsection. The Source Repositories table in the project CLAUDE.md has no Deployment Context column, so coordination guidance is omitted entirely per backward compatibility rules.

### Description Digest Protocol (Post-Creation)

After creating this task, the following digest procedure would be performed:

1. **Re-fetch the description** from Jira after `create_issue` (the API may normalize content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the SHA-256 digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`

3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then create issue links:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira creation** (requires confirmation):

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```markdown
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

Note: The Implementation Notes section does **not** include a Coordination Guidance subsection. The Source Repositories table in the project CLAUDE.md has no Deployment Context column, so coordination guidance is omitted entirely per backward compatibility rules.

### Description Digest Protocol (Post-Creation)

After creating this task, the following digest procedure would be performed:

1. **Re-fetch the description** from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Compute the SHA-256 digest**:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```

3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Then create issue links:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (Cargo = source dependency ecosystem -- matches classification table)
- [x] **Cross-stream coverage**: 2.1.x stream is also affected -- Case A cross-stream impact comment would be posted, and preemptive tasks or sibling CVE Jira check would be performed for that stream
- [x] **Link types**: "Depend" for tasks linked to TC-8001 (their own CVE Jira), "Blocks" for upstream -> downstream within the stream
- [x] **Preemptive labels**: not applicable for the 2.2.x tasks (they are linked to their own CVE Jira)
- [x] **Coordination guidance**: OMITTED -- the Source Repositories table has no Deployment Context column; backward compatibility requires omitting the subsection entirely

## Post-Triage Summary

After remediation task creation, the following post-triage actions would be proposed:

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (upstream backport + downstream propagation)
   - @mention of the vulnerability reporter using ADF mention node
3. **Transition TC-8001 to In Progress** (if not already transitioned)

The summary comment would include the Comment Footnote:
```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.13.6.
```
