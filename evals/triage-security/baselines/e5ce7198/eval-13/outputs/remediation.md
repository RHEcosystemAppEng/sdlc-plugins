# Steps 3-7 -- Jira Triage Operations and Remediation

## Step 3 -- Affects Versions Correction

### 3.1 -- Discover Available Jira Versions

Proposed API call:
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "TC",
  issueTypeId: "10024"
)
```

Filter by prefix "RHTPA". Expected versions (simulated):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (id-1) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (id-2) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (id-3) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (id-4) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (id-5) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (id-6) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (id-7) | RHTPA 2.2.4 | yes | 2026-05-04 |

### 3.2 -- Compare and Correct Affects Versions

This issue is **scoped** to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

Version impact for stream 2.2.x only:
- RHTPA 2.2.0: YES (affected)
- RHTPA 2.2.1: YES (affected)
- RHTPA 2.2.2: YES (affected, retag of 2.2.1)
- RHTPA 2.2.3: NO (not affected, ships 0.11.14)
- RHTPA 2.2.4: NO (not affected, ships 0.11.14)

**PSIRT Affects Versions are wrong.** PSIRT assigned `RHTPA 2.0.0`, but there is no 2.0.x stream configured. The correct stream-scoped Affects Versions are the affected 2.2.x versions.

**Proposed correction:**
```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

After engineer confirmation, the proposed Jira mutation:
```
jira.edit_issue("TC-8001", fields={
  "versions": [{"id": "<id-3>"}, {"id": "<id-4>"}, {"id": "<id-5>"}]
})
```

Proposed comment on TC-8001:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (>= fix threshold) and are not affected.
```

(ProdSec @mention omitted -- no ProdSec Jira account ID configured.)

---

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### 4.1/4.2 -- Sibling Search

Proposed JQL:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

(Simulated) No sibling issues found. No duplicates or cross-stream companions detected.

### 4.3 -- Cross-CVE Overlap Detection

Upstream Affected Component custom field is **not configured** in Security Configuration. Step 4.3 is skipped entirely.

### 4.4 -- Preemptive Task Reconciliation

Proposed JQL:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

(Simulated) No preemptive tasks found for CVE-2026-31812. Proceeding to Step 5.

---

## Step 5 -- Version Lifecycle Check

Proposed action:
```
WebFetch(url: "https://access.example.com/product-life-cycle/rhtpa",
  prompt: "Extract the list of supported product versions and their support status")
```

(Simulated) Assumed result: All affected versions (2.1.x and 2.2.x) are within active support lifecycle. Proceeding to Step 6.

---

## Step 6 -- Already Fixed Check

Reusing Step 4 sibling search results. No resolved sibling Vulnerability issues found for CVE-2026-31812. Cannot determine already-fixed status from siblings. Proceeding to Step 7.

---

## Step 7 -- Remediation

### Triage Outcome: Case A + Case B

**Case A -- Stream 2.2.x (in-scope)**: The issue is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2 are affected. The upstream fix is already present on the `release/0.4.z` branch (versions 2.2.3+ ship quinn-proto 0.11.14). Remediation tasks are needed for the affected versions within this stream.

However, since versions 2.2.3 and 2.2.4 already ship the fix, the upstream backport for the 2.2.x stream is already done. The remediation for stream 2.2.x involves a downstream propagation to update the Konflux release repo references for the affected versions -- but since these are already-released versions that cannot be re-shipped, the practical remediation is that the fix is already present in later releases within this stream.

Given that the fix is present in 2.2.3+ within the same stream, the remediation tasks for 2.2.x focus on ensuring the Affects Versions are correct (done in Step 3) and that the issue tracks which versions were affected.

**Case B -- Stream 2.1.x (cross-stream impact)**: The version impact analysis reveals that stream 2.1.x (versions 2.1.0, 2.1.1) is ALSO affected. This stream is outside the issue's scope (the issue is scoped to 2.2.x). No sibling CVE Jiras were found for stream 2.1.x.

Per Case B, proactive remediation tasks should be created for stream 2.1.x.

### Cross-Stream Impact Comment

Proposed comment on TC-8001:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
Versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 which is within the affected range.
Stream 2.1.x is not tracked by any companion CVE Jira and may require separate PSIRT triage or preemptive remediation.
```

---

## Remediation Task Descriptions

Since quinn-proto is a **Cargo** (source dependency) ecosystem, each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport for Stream 2.2.x

Since the upstream fix is already present on `release/0.4.z` (versions 2.2.3+ ship 0.11.14), no new upstream backport is needed for stream 2.2.x. The vulnerable versions (2.2.0-2.2.2) are already-released and the fix shipped in subsequent versions within the same stream. The Affects Versions correction (Step 3) documents which versions were affected.

**Assessment**: No new remediation task needed for stream 2.2.x. The fix is already present in versions 2.2.3 and later. The Vulnerability issue TC-8001 should be updated with corrected Affects Versions and documented.

### Task 2: Upstream Backport for Stream 2.1.x (Preemptive -- Case B)

No CVE Jira exists for stream 2.1.x, so this is a **preemptive** remediation task.

**Proposed Jira creation:**
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Upstream backport task description:**

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto Panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- quinn-proto is a transitive dependency via reqwest -> h3 -> quinn -> quinn-proto
- May require bumping the direct dependency (quinn or h3) to pull in the fix
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

#### Description Digest Protocol for Upstream Backport Task (Stream 2.1.x)

After creating the upstream task (e.g., assigned key TC-XXXX), the following description digest steps would be performed **before** creating issue links or other comments:

1. **Re-fetch the task description from Jira** (do not hash the input string -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue("TC-XXXX", fields=["description"])
   ```

2. **Write the fetched description to a temp file**:
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   The script auto-detects the format:
   - If the description is returned as ADF JSON (REST API): outputs `sha256-adf:<64-char-hex>`
   - If the description is returned as markdown (MCP): outputs `sha256-md:<64-char-hex>`

4. **Post the digest comment** on the newly created task, using the marker `[sdlc-workflow] Description digest:`:
   ```
   jira.add_comment("TC-XXXX", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   The comment is posted as a standalone comment, not embedded in other comments. The full tagged digest from the script output is used (e.g., `sha256-md:a3f2b7c9...` -- the full 64-character hex string, not truncated).

5. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-XXXX",
     type: "Related"
   )
   ```
   (Note: "Related" link type, not "Depend", because this is a preemptive task linked to a CVE from a different stream.)

---

### Task 3: Downstream Propagation Subtask for Stream 2.1.x (Preemptive -- Case B)

**Proposed Jira creation:**
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Downstream propagation subtask description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from TC-XXXX (upstream backport task).

The upstream backport (TC-XXXX) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: TC-XXXX (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Downstream Propagation Subtask (Stream 2.1.x)

After creating the downstream task (e.g., assigned key TC-YYYY), the following description digest steps would be performed **before** creating issue links or other comments:

1. **Re-fetch the task description from Jira**:
   ```
   downstream_desc = jira.get_issue("TC-YYYY", fields=["description"])
   ```

2. **Write the fetched description to a temp file**:
   ```
   Write the description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on format.

4. **Post the digest comment** on the newly created task:
   ```
   jira.add_comment("TC-YYYY", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   This is a standalone comment with exactly one line, posted before any other comments or links.

5. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   # Link downstream to originating CVE (Related, because preemptive)
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-YYYY",
     type: "Related"
   )

   # Link downstream as blocked by upstream
   jira.create_link(
     inwardIssue: "TC-XXXX",
     outwardIssue: "TC-YYYY",
     type: "Blocks"
   )
   ```

---

## Post-Remediation Linkage and Comments

### Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, the following comment would be posted on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-XXXX (upstream backport, security-preemptive), TC-YYYY (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label

Proposed mutation:
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post summary comment

Proposed comment on TC-8001 (includes @mention of the reporter and Comment Footnote):

```
## CVE-2026-31812 Triage Summary

### Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Affects Versions Correction

Corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
RHTPA 2.0.0 does not correspond to any configured version stream.

### Triage Outcome

- **Stream 2.2.x (in-scope)**: Affected versions 2.2.0, 2.2.1, 2.2.2. Fix already present in 2.2.3+ (quinn-proto 0.11.14). No new remediation tasks needed for this stream.
- **Stream 2.1.x (cross-stream, preemptive)**: All versions affected (2.1.0, 2.1.1). No companion CVE Jira exists. Preemptive remediation tasks created:
  - TC-XXXX: Upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (security-preemptive)
  - TC-YYYY: Downstream propagation -- update rhtpa-backend ref in rhtpa-release.0.3.z (security-preemptive, blocked by TC-XXXX)

@<reporter-name> (ADF mention with reporter account ID from issue data)

---
_This comment was generated by the triage-security skill of sdlc-workflow._
```

(The Comment Footnote is included at the end of the comment per `shared/comment-footnote.md`, using skill name `triage-security`.)
