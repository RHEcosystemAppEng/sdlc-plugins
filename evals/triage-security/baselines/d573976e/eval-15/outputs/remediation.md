# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## Step 4.1-4.2 -- Sibling Search

Proposed JQL (not executed):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001
```

(Eval does not provide sibling search results; assuming no sibling issues found for this eval scenario.)

## Step 4.3 -- Cross-CVE Overlap Detection

Upstream Affected Component custom field: not configured in this CLAUDE.md.
Result: Step 4.3 **skipped entirely**.

## Step 4.4 -- Preemptive Task Reconciliation

Proposed JQL (not executed):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

(Assuming no preemptive tasks found.)

---

# Step 5 -- Version Lifecycle Check

Proposed check (not executed):
```
WebFetch(url: "https://access.example.com/product-life-cycle/rhtpa",
  prompt: "Extract the list of supported product versions and their support status")
```

(Assuming all affected versions 2.2.0, 2.2.1, 2.2.2 are within support lifecycle. Proceeding.)

---

# Step 6 -- Already Fixed Check

No resolved sibling Vulnerability issues found in Step 4. Proceeding to Step 7.

---

# Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field: not configured in this CLAUDE.md.
Result: Step 7 **skipped entirely**.

---

# Step 8 -- Remediation

## Triage Decision: Case A -- Affected

The issue is scoped to stream 2.2.x. Within this stream:
- **Affected versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected versions**: RHTPA 2.2.3, RHTPA 2.2.4

Ecosystem: **Cargo** (source dependency) -- requires **two** remediation tasks:
1. Upstream backport task (fix in source repo)
2. Downstream propagation subtask (update reference in Konflux release repo, blocked by upstream task)

## Cross-Stream Impact (Case B)

The version impact table shows stream 2.1.x is also affected (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact triggers Case B cross-stream handling.

**Proposed cross-stream impact comment on TC-8001**:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Stream 2.1.x versions 2.1.0 and 2.1.1
ship quinn-proto 0.11.9. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

(In a full execution, preemptive remediation tasks would also be created for stream 2.1.x if no sibling CVE Jira exists for that stream. See Case B protocol in SKILL.md.)

---

## Remediation Task 1: Upstream Backport Task (stream 2.2.x)

### Proposed Jira Creation

```
upstream_task = jira.create_issue(
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

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), RHTPA 2.2.1 (v0.4.8), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
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
```

### Description Digest Protocol (Upstream Task)

After creating the upstream task, the following digest steps are performed:

1. **Re-fetch the task description** from Jira API:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` (auto-detected)
3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue, because Jira normalizes content during storage.

---

## Remediation Task 2: Downstream Propagation Subtask (stream 2.2.x)

### Proposed Jira Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
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

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
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
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Protocol (Downstream Task)

After creating the downstream task, the following digest steps are performed:

1. **Re-fetch the task description** from Jira API:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. **Write the description to a temp file** and compute the digest:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Output: `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` (auto-detected)
3. **Post the digest comment** (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

The digest is computed from the **re-fetched** description (via Jira API after create_issue), not from the description string passed to create_issue.

---

## Jira Linkage (after digest comments)

After digest comments are posted on both tasks:

1. **Link upstream task to Vulnerability issue**:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
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
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

4. **Transition** TC-8001 to In Progress (proposed -- requires confirmation).

5. **Assign** TC-8001 to current user (proposed -- requires confirmation).

---

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label

Proposed:
```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Post-Triage Summary Comment

The following summary comment would be posted to TC-8001. This comment includes:
- The version impact table
- The Affects Versions correction
- The triage outcome (remediation created)
- Links to all remediation tasks created
- An @mention of the vulnerability issue's reporter (psirt-analyst)

**Reporter @mention**: The reporter field is always available on the Jira issue. The reporter is `psirt-analyst` with account ID `557058:psirt-analyst-mock-id`. This @mention is mandatory and requires no ProdSec configuration -- it uses the reporter field from the Jira issue.

### Full ADF Post-Triage Summary Comment

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        {
          "type": "text",
          "text": "Triage Summary — CVE-2026-31812 (quinn-proto)"
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):"
        }
      ]
    },
    {
      "type": "table",
      "content": [
        {
          "type": "tableRow",
          "content": [
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Version" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "quinn-proto" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Affected?" }] }] },
            { "type": "tableHeader", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Notes" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.1.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.0" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.9" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.1" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.12" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.2" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "—" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "YES" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "retag of 2.2.1" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.3" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        },
        {
          "type": "tableRow",
          "content": [
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "2.2.4" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "0.11.14" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "NO" }] }] },
            { "type": "tableCell", "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "" }] }] }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Affects Versions corrected: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits. Scoped to stream 2.2.x per issue suffix [rhtpa-2.2]."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Triage outcome: Remediation tasks created."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Remediation tasks created: <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z), <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9)."
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "mention",
          "attrs": {
            "id": "557058:psirt-analyst-mock-id",
            "text": "@psirt-analyst"
          }
        }
      ]
    },
    {
      "type": "rule"
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This comment was AI-generated by "
        },
        {
          "type": "text",
          "text": "sdlc-workflow/triage-security",
          "marks": [
            {
              "type": "link",
              "attrs": {
                "href": "https://github.com/mrizzi/sdlc-plugins"
              }
            }
          ]
        },
        {
          "type": "text",
          "text": " v0.11.1."
        }
      ]
    }
  ]
}
```

### Key @mention Details

1. **Reporter @mention (Step 8 -- mandatory, no configuration required)**:
   - Account ID: `557058:psirt-analyst-mock-id`
   - Display text: `@psirt-analyst`
   - Source: Jira issue `reporter` field (always available on the issue)
   - ADF node: `{ "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } }`
   - This @mention is present **by default** without any ProdSec configuration. It uses the reporter field from the Jira issue, which is always available.

2. **ProdSec @mention (Step 3 -- conditional, requires configuration)**:
   - Account ID: `557058:prodsec-mock-account-id`
   - Display text: `@prodsec-team`
   - Source: Security Configuration `ProdSec Jira account ID` field
   - ADF node: `{ "type": "mention", "attrs": { "id": "557058:prodsec-mock-account-id", "text": "@prodsec-team" } }`
   - This @mention appears in the **Affects Versions correction comment** (Step 3, see affects-versions.md) because the ProdSec Jira account ID is configured.
   - The ProdSec @mention appears **before** the Comment Footnote in the Affects Versions correction comment.
   - The ProdSec Jira account ID (`557058:prodsec-mock-account-id`) was extracted from the Security Configuration in Step 0 and used in the Step 3 Affects Versions correction comment.

### Comment Footnote

All comments posted by this skill include the Comment Footnote, using:
- Skill name: `triage-security`
- Plugin version: `0.11.1` (from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)
- Link: `https://github.com/mrizzi/sdlc-plugins`
