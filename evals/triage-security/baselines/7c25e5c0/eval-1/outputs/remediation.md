# Step 7.5 — Release Jira Orchestration

## 7.5.1 — Resolve Stream-to-Version Mapping

The affected stream is **2.2.x** (release family `rhtpa-2.2`). The latest released version in the 2.2.x supportability matrix is **2.2.4**.

Proposed: search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"`.

```
jira.search_jql(
  "project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC",
  fields: ["summary", "status"],
  maxResults: 5
)
```

If no release Epic exists, the default next patch bump is **RHTPA 2.2.5** (from latest 2.2.4). The engineer would be prompted to confirm:

> No release Epic found for stream 2.2.x.
>
> Proposed version: RHTPA 2.2.5 Release Tasks
> (based on latest released version 2.2.4 in supportability matrix)
>
> Options:
> 1. Accept — create Epic with version 2.2.5
> 2. Specify different version
> 3. Skip — do not create release Jira for this stream

## 7.5.2 — Find or Create the Release Task

After the release Epic is confirmed/created, search for or create a release Task:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND parent = <release-epic-key> AND summary ~ 'RHTPA <version> CVE triage' ORDER BY created DESC",
  fields: ["summary", "status", "issuelinks"],
  maxResults: 5
)
```

## 7.5.3 — Cross-CVE Dedup Check

Before creating remediation tasks, check whether an existing remediation Task already covers quinn-proto for the same release version. The Upstream Affected Component custom field is not configured in this Security Configuration, so dedup is skipped (§7.5.3 prerequisite).

Dedup decision: **Skipped** — Upstream Affected Component custom field not configured. Proceeding to Step 8 for standard remediation task creation.

---

# Step 8 — Remediation

## Triage Outcome Decision

Version impact summary for the 2.2.x stream (issue scope):

| Version | Affected? |
|---------|-----------|
| 2.2.0 | YES |
| 2.2.1 | YES |
| 2.2.2 | YES (retag) |
| 2.2.3 | NO |
| 2.2.4 | NO |

**Result**: Some supported versions are affected → **Case B: Create remediation tasks**.

### Cross-stream Impact (Case A check)

This issue is **scoped** to stream 2.2.x (suffix `[rhtpa-2.2]`). Cross-stream analysis shows the **2.1.x** stream is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

A cross-stream impact comment would be posted to TC-8001. A JQL search for sibling CVE Jiras with label CVE-2026-31812 and stream suffix [rhtpa-2.1] determines whether preemptive tasks are needed for the 2.1.x stream.

## Remediation Task Descriptions

Ecosystem: **Cargo** (source dependency) → **2 tasks per stream**: upstream backport + downstream propagation (Important Rule 8).

### Task 1: Upstream Backport Task

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description** (follows task-description-template.md format — Important Rule 9):

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z (from Ecosystem Mappings Upstream Branch)
- **Dependency type**: direct
- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation digest protocol** (§1.66):

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Compute SHA-256 digest using `scripts/sha256-digest.py` on the re-fetched description (not the input string passed to create_issue):
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment with marker **before** creating issue links or other comments:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex-digest>")
   ```

### Task 2: Downstream Propagation Subtask

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description** (follows task-description-template.md format — Important Rule 9):

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
- **Dependency type**: direct — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Post-creation digest protocol** (§1.66):

1. Re-fetch the task description from Jira after `create_issue`:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Compute SHA-256 digest using `scripts/sha256-digest.py` on the re-fetched description:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
3. Post digest comment with marker **before** creating issue links or other comments:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<hex-digest>")
   ```

## Jira Linkage

After creating both tasks and posting digest comments:

1. **Depend link** — upstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: TC-8001, outwardIssue: <upstream-task-key>, type: "Depend")
   ```
2. **Depend link** — downstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: TC-8001, outwardIssue: <downstream-task-key>, type: "Depend")
   ```
3. **Blocks link** — upstream blocks downstream:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```
4. **Release Jira linking** (if Step 7.5 produced a release Task):
   - Blocks: `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`
   - Blocks: `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`
   - Related: `jira.create_link(inwardIssue: <release-task-key>, outwardIssue: TC-8001, type: "Related")`

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8001.
2. **Transition** TC-8001 to In Progress.
3. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created: <upstream-task-key> (upstream backport), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - Release Jira references (if created in Step 7.5)
   - Comment Footnote

All triage recommendations are presented as **proposed actions** pending engineer confirmation — no Jira mutations are performed without explicit approval (Guardrails).
