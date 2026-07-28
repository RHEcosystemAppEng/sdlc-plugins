# Step 2 — Version Impact Analysis (Summary)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | _(outside issue scope — 2.1.x stream)_ |
| 2.1.1 | 0.11.9 | YES | _(outside issue scope — 2.1.x stream)_ |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Step 3 — Affects Versions Correction (Summary)

Current Affects Versions: [RHTPA 2.0.0]
Proposed Affects Versions (scoped to 2.2.x stream): [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

The PSIRT-assigned version RHTPA 2.0.0 does not correspond to an actual supported version. Based on lock file analysis at pinned commits from the supportability matrix, the versions within the 2.2.x stream that are actually affected are 2.2.0, 2.2.1, and 2.2.2.

## Case A — Cross-Stream Impact Notice

This is a scoped issue ([rhtpa-2.2]). The version impact analysis reveals that stream **2.1.x** is also affected:
- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

Proposed cross-stream impact comment on TC-8001:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Case B — Remediation Task Creation (Step 8)

Affected versions in the 2.2.x stream: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
Ecosystem: Cargo (source dependency) -> 2 tasks required.

### Deployment Context Note

The Source Repositories table does **not** include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. Because the Deployment Context column is absent, the Coordination Guidance subsection is **omitted entirely** from all remediation task descriptions below. This maintains backward compatibility with existing behavior.

---

### Task 1: Upstream Backport Task

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
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

**Post-creation steps (description digest protocol):**

1. Re-fetch the task description from Jira after create_issue:
   `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   The script auto-detects format (ADF or markdown) and outputs a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. Post the digest comment BEFORE creating issue links or other comments:
   `jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Then create the Depend link to TC-8001:
   `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")`

---

### Task 2: Downstream Propagation Subtask

**Proposed Jira API call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

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

**Post-creation steps (description digest protocol):**

1. Re-fetch the task description from Jira after create_issue:
   `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. Write the re-fetched description to a temp file
3. Compute SHA-256 digest using: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
   The script auto-detects format and outputs a tagged digest
4. Post the digest comment BEFORE creating issue links or other comments:
   `jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`
5. Then create the links:
   - Depend link to TC-8001: `jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")`
   - Blocks link (upstream blocks downstream): `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Post-Triage Summary

### 1. Add label

Proposed: Add `ai-cve-triaged` label to TC-8001.

### 2. Transition

Proposed: Transition TC-8001 to In Progress.

### 3. Summary comment

Proposed comment on TC-8001 documenting the triage outcome:

> **Triage summary for CVE-2026-31812 (quinn-proto)**
>
> **Version impact:**
>
> | Version | quinn-proto | Affected? | Notes |
> |---------|-------------|-----------|-------|
> | 2.2.0 | 0.11.9 | YES | |
> | 2.2.1 | 0.11.12 | YES | |
> | 2.2.2 | -- | YES | retag of 2.2.1 |
> | 2.2.3 | 0.11.14 | NO | |
> | 2.2.4 | 0.11.14 | NO | |
>
> **Affects Versions corrected**: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
>
> **Triage outcome**: Remediation tasks created.
> - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
> - <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)
>
> **Cross-stream impact**: Stream 2.1.x is also affected (quinn-proto 0.11.9 in all versions).
>
> @reporter-mention (ADF mention node: `{ "type": "mention", "attrs": { "id": "<reporter-account-id>", "text": "@<reporter-name>" } }`)
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7.

## Pre-Creation Checklist

- [x] **Task count per stream**: Cargo ecosystem (source dependency) -> 2 tasks (upstream backport + downstream propagation). Correct.
- [x] **Cross-stream coverage**: Stream 2.1.x is also affected. Cross-stream impact comment will be posted. (Preemptive tasks or sibling CVE Jira handling depends on JQL search results not available in this eval.)
- [x] **Link types**: "Depend" for tasks linked to TC-8001 (their own CVE Jira). "Blocks" for upstream -> downstream within the stream.
- [x] **Preemptive labels**: Not applicable for the 2.2.x stream tasks (this is the scoped stream).
- [x] **Coordination guidance**: The Source Repositories table does NOT have a Deployment Context column. All repositories default to `upstream`. The Coordination Guidance subsection is **omitted entirely** from all remediation task descriptions. Backward compatibility maintained.
