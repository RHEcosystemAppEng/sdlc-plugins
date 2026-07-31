# Step 8 -- Remediation

## Triage Outcome

**Case B (Affected)**: Version 2.2.0 in the 2.2.x stream ships h2 0.4.5, which is below the enriched fix threshold of 0.4.8 (from Step 1.5). Remediation tasks are required.

**Case A (Cross-stream impact)**: The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship h2 0.4.5). A cross-stream impact comment would be posted on TC-8030.

**Ecosystem**: Cargo (source dependency) -- 2 tasks per stream: upstream backport + downstream propagation.

---

## Remediation Tasks for 2.2.x Stream (Issue Scope)

### Task 1: Upstream Backport Task

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.2.0
Source commit(s): v0.4.5

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

**Post-creation digest protocol (proposed procedure):**

1. After `create_issue` returns the upstream task key, re-fetch the task description from Jira:
   `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute the SHA-256 digest using `scripts/sha256-digest.py`:
   `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post the digest comment (BEFORE creating issue links or other comments):
   `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Then create the Depend link to TC-8030:
   `jira.create_link(inwardIssue: "TC-8030", outwardIssue: <upstream-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira create_issue call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-48901 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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
- Depends on: TC-8030 (parent tracking issue)

---

**Post-creation digest protocol (proposed procedure):**

1. After `create_issue` returns the downstream task key, re-fetch the task description from Jira:
   `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute the SHA-256 digest using `scripts/sha256-digest.py`:
   `python3 scripts/sha256-digest.py /tmp/task-desc.md`
4. Post the digest comment (BEFORE creating issue links or other comments):
   `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Then create links:
   - Depend link to TC-8030: `jira.create_link(inwardIssue: "TC-8030", outwardIssue: <downstream-task-key>, type: "Depend")`
   - Blocks link (upstream blocks downstream): `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Cross-Stream Impact (Case A)

The issue is scoped to stream [rhtpa-2.2], but the version impact analysis reveals that the **2.1.x** stream is also affected:

- 2.1.0 (v0.3.8): h2 0.4.5 -- affected (0.4.5 < 0.4.8)
- 2.1.1 (v0.3.12): h2 0.4.5 -- affected (0.4.5 < 0.4.8)

**Proposed cross-stream impact comment on TC-8030:**

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

A JQL search for sibling CVE Jiras with label CVE-2026-48901 in the 2.1.x stream would determine whether preemptive remediation tasks should be created for that stream (Case A proactive remediation).

---

## Post-Triage Summary

After all remediation tasks are created:

1. **Add label**: `ai-cve-triaged` to TC-8030
2. **Transition**: TC-8030 to In Progress
3. **Post summary comment** on TC-8030 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.2.0 is correct -- only 2.2.0 is affected in the 2.2.x stream)
   - Remediation tasks created (upstream backport + downstream propagation)
   - @mention of the reporter using ADF mention node
   - Comment Footnote (sdlc-workflow/triage-security v0.13.7)
