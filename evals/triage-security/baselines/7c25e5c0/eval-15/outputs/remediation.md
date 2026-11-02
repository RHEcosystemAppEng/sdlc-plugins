# Step 8 — Remediation

## Case A: Cross-Stream Impact

Issue is scoped to 2.2.x stream. Cross-stream analysis shows 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). A cross-stream impact comment would be posted noting this.

## Case B: Remediation Tasks for 2.2.x Stream (Scoped)

Ecosystem: **Cargo** (source dependency) → **2 tasks** per the ecosystem classification table.

### Task 1: Upstream Backport Task

**Summary**: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

#### Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
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

### Task 2: Downstream Propagation Subtask

**Summary**: `Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
**Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`

#### Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
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

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Jira Linkage

For each remediation task created:

1. **Depend** link: `jira.create_link(inwardIssue: TC-8001, outwardIssue: <task-key>, type: "Depend")`
2. **Blocks** link (upstream → downstream): `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

### Description Digest Protocol (Step by Step)

For each remediation task (both upstream and downstream):

1. **Create the task** via `jira.create_issue(...)`
2. **Re-fetch the description** from Jira after creation: `jira.get_issue(<task-key>, fields=["description"])`
3. **Compute SHA-256 digest** from the re-fetched description (not from the description string passed to create_issue): `python3 scripts/sha256-digest.py /tmp/task-desc.md` → produces `sha256-md:<hex>` or `sha256-adf:<hex>`
4. **Post digest comment** with marker `[sdlc-workflow] Description digest: <tagged-digest>` via `jira.add_comment(<task-key>, ...)`
5. **Only then** create issue links (Depend, Blocks) or other comments on the task

This sequence is followed for both the upstream backport task and the downstream propagation subtask.

## Step 7.5 — Release Orchestration

Release Jira orchestration requires interactive confirmation of the exact release Epic version and separate child Task creation. Since this eval prohibits actual Jira calls, the following describes the planned procedure:

1. **7.5.1** — Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`. If found, reuse it. If not found, propose creating one with the next patch version (e.g., RHTPA 2.2.5 based on latest released version 2.2.4). Engineer must confirm the version before creation.
2. **7.5.2** — Search for existing release Task under the release Epic matching `"RHTPA <version> CVE triage"`. If found, reuse it. If not found, propose creation and await confirmation.
3. **7.5.3** — Release dedup check: Since the Upstream Affected Component custom field configuration is absent from this CLAUDE.md's Security Configuration, the dedup step is skipped entirely.

Since no actual Jira calls can be made and release evidence is unavailable, this step reports **pending work** — the release Epic and Task must be confirmed interactively before remediation tasks can be linked.

## Post-Triage Summary Comment

After all triage actions are complete, a summary comment is posted on TC-8001. This comment includes:

1. Version impact table
2. Affects Versions correction diff
3. Triage outcome (remediation created)
4. Links to all remediation tasks created
5. **@mention of the vulnerability issue's reporter** using an ADF mention node:

```json
{
  "type": "mention",
  "attrs": {
    "id": "557058:psirt-analyst-mock-id",
    "text": "@psirt-analyst"
  }
}
```

The reporter @mention is **mandatory** and requires no configuration — the reporter field (`psirt-analyst`, account ID `557058:psirt-analyst-mock-id`) is always available from the Jira issue data extracted in Step 1. This @mention notifies the PSIRT analyst who created the Vulnerability issue about the triage outcome.

6. The `ai-cve-triaged` label is added to TC-8001.
7. The comment includes the Comment Footnote:

> _This comment was generated by the `triage-security` skill of the sdlc-workflow plugin._
