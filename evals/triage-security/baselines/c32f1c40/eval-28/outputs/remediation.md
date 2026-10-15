# Step 7 — Concurrent Triage Detection

The Upstream Affected Component custom field is not configured in the Security Configuration (claude-md-security-config.md does not list an Upstream Affected Component custom field). Step 7 is skipped entirely.

---

# Step 7.5 — Release Jira Orchestration

## Release Jira Confirmations

Before creating remediation tasks, Step 7.5 would find or create the release Jira structure for the 2.2.x stream:

1. **7.5.1 — Resolve stream-to-version mapping**: Parse stream `rhtpa-2.2` to the `2.2.x` release family. Search for an existing release Epic matching `"RHTPA 2.2.* Release Tasks"`. If no Epic exists, propose the next patch version (based on the latest released version 2.2.4, default to `RHTPA 2.2.5`). Present options to the engineer:
   - Accept the proposed version
   - Specify a different version
   - Skip release Jira for this stream

   **This requires engineer confirmation** — the exact release version is a high-stakes decision and cannot be automated.

2. **7.5.2 — Find or create the release Task**: Search for a release Task under the release Epic matching `"RHTPA <version> CVE triage"`. If none exists, prompt the engineer to confirm creation. **Individual confirmation required.**

3. **7.5.3 — Cross-CVE dedup check**: The Upstream Affected Component custom field is not configured in the Security Configuration. Per the prerequisite, dedup is **skipped** — proceed directly to Step 8 remediation task creation.

Since release orchestration and dedup require interactive confirmations and external Jira access (which are prohibited in this eval), these steps are documented as pending work. Remediation tasks are described below as they would be created after release Jira is resolved.

---

# Step 8 — Remediation

## Triage Decision

**Case B: Affected — create remediation tasks.**

The version impact table shows 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Versions 2.2.3 and 2.2.4 are not affected (h2 0.4.5 >= 0.4.5).

The ecosystem is **Cargo** (source dependency). Per the ecosystem classification table, this requires **two tasks** per affected stream:
- One upstream task (dependency bump, since the fix is available upstream per Step 2.5)
- One downstream propagation subtask (update source reference in Konflux release repo)

The vulnerable dependency h2 is a **transitive** dependency. The remediation approach follows the two-tier strategy documented in the dependency chain context (Step 2.3.5).

---

## Remediation Task 1: Upstream Dependency Bump (Source Repo)

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-99010: update h2 to 0.4.5 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: bump h2 to 0.4.5 via dependency update.
The vulnerable dependency (h2 < 0.4.5) is already fixed upstream —
a package manager update is sufficient.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend → reqwest → hyper → h2, 3 levels deep)
- h2 is NOT a direct dependency of backend. It is pulled in through:
  backend (workspace) → reqwest → hyper → h2

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through
intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency (reqwest)**
- Identify the direct dependency that pulls in h2: `reqwest`
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Run `cargo update -p reqwest` to pull in the latest compatible version
- Verify the lock file reflects h2 >= 0.4.5 after the update
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release
available with h2 >= 0.4.5 in its transitive closure):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding
  the transitive resolution
- Document why the reqwest bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)
```

### Description Digest Protocol

After creating this task via `jira.create_issue`:

1. **Re-fetch the description** from Jira: `jira.get_issue(<upstream-task-key>, fields=["description"])`
2. **Write the description** to a temp file (e.g., `/tmp/task-desc.md`)
3. **Compute the digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md` — the script auto-detects format and produces a tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`)
4. **Post digest comment** on the newly created task (BEFORE creating any issue links or other comments):
   ```
   [sdlc-workflow] Description digest: <tagged-digest>
   ```

The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue, since Jira normalizes content during storage.

### Post-Digest Linkage

After posting the description digest comment:

1. **Link to CVE** (Depend): `jira.create_link(inwardIssue: "TC-8060", outwardIssue: <upstream-task-key>, type: "Depend")`
2. **Link to release Task** (Blocks, if release Jira is active from Step 7.5): `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

## Remediation Task 2: Downstream Propagation Subtask (Konflux Release Repo)

### Proposed Jira Issue

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-99010"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99010 fix from <upstream-task-key>.

The upstream dependency bump (<upstream-task-key>) updates h2 to 0.4.5
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: transitive — carried forward from upstream task
  (chain: backend → reqwest → hyper → h2)
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach via cargo add),
  verify the pinning is reflected in the downstream build's lock file after
  the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream dependency bump must merge first)
- Depends on: TC-8060 (parent tracking issue)
```

### Description Digest Protocol

After creating this task via `jira.create_issue`:

1. **Re-fetch the description** from Jira: `jira.get_issue(<downstream-task-key>, fields=["description"])`
2. **Write the description** to a temp file (e.g., `/tmp/task-desc.md`)
3. **Compute the digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md` — the script auto-detects format and produces a tagged digest
4. **Post digest comment** on the newly created task (BEFORE creating any issue links or other comments):
   ```
   [sdlc-workflow] Description digest: <tagged-digest>
   ```

The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue.

### Post-Digest Linkage

After posting the description digest comment:

1. **Link to CVE** (Depend): `jira.create_link(inwardIssue: "TC-8060", outwardIssue: <downstream-task-key>, type: "Depend")`
2. **Link upstream blocks downstream** (Blocks): `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`
3. **Link to release Task** (Blocks, if release Jira is active from Step 7.5): `jira.create_link(inwardIssue: <downstream-task-key>, outwardIssue: <release-task-key>, type: "Blocks")`

---

## Post-Creation Actions

After creating both remediation tasks:

1. **Link CVE to release Task** (Related, if release Jira is active): `jira.create_link(inwardIssue: <release-task-key>, outwardIssue: "TC-8060", type: "Related")`

2. **Transition TC-8060 to In Progress** (if not already): `jira.transition_issue("TC-8060", <in-progress-transition-id>)`

3. **Add `ai-cve-triaged` label** to TC-8060: `jira.edit_issue("TC-8060", labels=[..., "ai-cve-triaged"])`

4. **Post summary comment** to TC-8060 documenting:
   - Version impact table (3 of 5 versions affected)
   - Affects Versions correction (if applicable)
   - Remediation tasks created: <upstream-task-key> (upstream dependency bump), <downstream-task-key> (downstream propagation, blocked by <upstream-task-key>)
   - Dependency chain: h2 is transitive (backend → reqwest → hyper → h2)
   - @mention of reporter (psirt-analyst, account ID: 557058:psirt-analyst-mock-id) using ADF mention node:
     ```json
     { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }
     ```
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.13.10."

---

## Pre-Creation Checklist

- [x] **Task count per stream**: 2 tasks for 2.2.x stream (source dependency ecosystem: upstream dependency bump + downstream propagation) — matches the ecosystem classification table.
- [x] **Cross-stream coverage**: Issue is scoped to [rhtpa-2.2]; cross-stream impact on 2.1.x would need to be checked for h2 versions in that stream. Case A would apply if 2.1.x is also affected.
- [x] **Link types**: "Depend" for tasks linked to TC-8060 (their own CVE Jira), "Blocks" for upstream → downstream within the stream.
- [x] **Coordination guidance**: Source Repositories table has no Deployment Context column — coordination guidance subsection is omitted entirely (backward compatibility).
- [x] **Release Jira linking**: Pending engineer confirmation of release version in Step 7.5.
- [x] **Dedup consistency**: Upstream Affected Component custom field is not configured — dedup is skipped.
